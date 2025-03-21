import pytest
from uuid import uuid4

from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.nodes.core.inline_subworkflow_node.node import InlineSubworkflowNode
from vellum.workflows.nodes.core.retry_node.node import RetryNode
from vellum.workflows.nodes.core.templating_node.node import TemplatingNode
from vellum.workflows.workflows.base import BaseWorkflow
from vellum_ee.workflows.display.nodes import BaseNodeDisplay
from vellum_ee.workflows.display.nodes.vellum.retry_node import BaseRetryNodeDisplay
from vellum_ee.workflows.display.vellum import NodeDisplayData, NodeDisplayPosition
from vellum_ee.workflows.display.workflows import VellumWorkflowDisplay
from vellum_ee.workflows.display.workflows.get_vellum_workflow_display_class import get_workflow_display


def test_serialize_workflow__node_referenced_in_workflow_outputs_not_in_graph():
    # GIVEN a couple of nodes
    class InNode(BaseNode):
        pass

    class OutNode(BaseNode):
        class Outputs(BaseNode.Outputs):
            foo: str

    # AND A workflow that references the OutNode in its outputs but only has the InNode in its graph
    class Workflow(BaseWorkflow):
        graph = InNode

        class Outputs(BaseWorkflow.Outputs):
            final = OutNode.Outputs.foo

    # WHEN we serialize it
    workflow_display = get_workflow_display(
        base_display_class=VellumWorkflowDisplay,
        workflow_class=Workflow,
    )

    # THEN it should raise an error
    with pytest.raises(ValueError) as exc_info:
        workflow_display.serialize()

    # AND the error message should be user friendly
    assert str(exc_info.value) == "Failed to serialize output 'final': Reference to node 'OutNode' not found in graph."


def test_serialize_workflow__workflow_outputs_reference_non_node_outputs():
    # GIVEN one Workflow
    class FirstWorkflow(BaseWorkflow):
        class Outputs(BaseWorkflow.Outputs):
            foo = "bar"

    # AND A workflow that references the Outputs of that Workflow
    class Workflow(BaseWorkflow):
        class Outputs(BaseWorkflow.Outputs):
            final = FirstWorkflow.Outputs.foo

    # WHEN we serialize it
    workflow_display = get_workflow_display(
        base_display_class=VellumWorkflowDisplay,
        workflow_class=Workflow,
    )

    # THEN it should raise an error
    with pytest.raises(ValueError) as exc_info:
        workflow_display.serialize()

    # AND the error message should be user friendly
    assert (
        str(exc_info.value)
        == """Failed to serialize output 'final': Reference to outputs \
'test_serialize_workflow__workflow_outputs_reference_non_node_outputs.<locals>.FirstWorkflow.Outputs' is invalid."""
    )


def test_serialize_workflow__node_display_class_not_registered():
    # GIVEN a workflow with a node that has a display class referencing display data
    class StartNode(BaseNode):
        class Outputs(BaseNode.Outputs):
            result: str

    class StartNodeDisplay(BaseNodeDisplay[StartNode]):
        node_input_ids_by_name = {}
        display_data = NodeDisplayData(position=NodeDisplayPosition(x=0, y=0), width=None, height=None)

    class MyWorkflow(BaseWorkflow):
        graph = StartNode

        class Outputs(BaseWorkflow.Outputs):
            answer = StartNode.Outputs.result

    # WHEN we serialize it
    workflow_display = get_workflow_display(
        base_display_class=VellumWorkflowDisplay,
        workflow_class=MyWorkflow,
    )
    data = workflow_display.serialize()

    # THEN it should should succeed
    assert data is not None


def test_get_event_display_context__node_display_filled_without_base_display():
    # GIVEN a simple workflow
    class StartNode(BaseNode):
        class Outputs(BaseNode.Outputs):
            foo: str

    class MyWorkflow(BaseWorkflow):
        graph = StartNode

    # WHEN we gather the event display context
    display_context = VellumWorkflowDisplay(MyWorkflow).get_event_display_context()

    # THEN the node display should be included
    assert str(StartNode.__id__) in display_context.node_displays
    node_event_display = display_context.node_displays[str(StartNode.__id__)]

    # AND so should their output ids
    assert StartNode.__output_ids__ == node_event_display.output_display


def test_get_event_display_context__node_display_to_include_subworkflow_display():
    # GIVEN a simple workflow
    class InnerNode(BaseNode):
        pass

    class Subworkflow(BaseWorkflow):
        graph = InnerNode

    # AND a workflow that includes the subworkflow
    class SubworkflowNode(InlineSubworkflowNode):
        subworkflow = Subworkflow

    class MyWorkflow(BaseWorkflow):
        graph = SubworkflowNode

    # WHEN we gather the event display context
    display_context = VellumWorkflowDisplay(MyWorkflow).get_event_display_context()

    # THEN the subworkflow display should be included
    assert str(SubworkflowNode.__id__) in display_context.node_displays
    node_event_display = display_context.node_displays[str(SubworkflowNode.__id__)]

    assert node_event_display.subworkflow_display is not None
    assert str(InnerNode.__id__) in node_event_display.subworkflow_display.node_displays


def test_get_event_display_context__node_display_for_adornment_nodes():
    # GIVEN a simple workflow with a retry node adornment
    @RetryNode.wrap(max_attempts=4)
    class MyNode(BaseNode):
        pass

    class MyWorkflow(BaseWorkflow):
        graph = MyNode

    # AND a display class for the node
    inner_node_id = uuid4()

    @BaseRetryNodeDisplay.wrap()
    class MyNodeDisplay(BaseNodeDisplay[MyNode]):
        node_id = inner_node_id

    # WHEN we gather the event display context
    display_context = VellumWorkflowDisplay(MyWorkflow).get_event_display_context()

    # THEN the subworkflow display should be included
    assert str(MyNode.__id__) in display_context.node_displays
    node_event_display = display_context.node_displays[str(MyNode.__id__)]
    assert node_event_display.subworkflow_display is not None
    assert str(inner_node_id) in node_event_display.subworkflow_display.node_displays


def test_get_event_display_context__templating_node_input_display():
    # GIVEN a simple workflow with a templating node referencing another node output
    class DataNode(BaseNode):
        class Outputs:
            bar: str

    class MyNode(TemplatingNode):
        inputs = {"foo": DataNode.Outputs.bar}

    class MyWorkflow(BaseWorkflow):
        graph = DataNode >> MyNode

    # WHEN we gather the event display context
    display_context = VellumWorkflowDisplay(MyWorkflow).get_event_display_context()

    # THEN the subworkflow display should be included
    assert str(MyNode.__id__) in display_context.node_displays
    node_event_display = display_context.node_displays[str(MyNode.__id__)]

    assert node_event_display.input_display.keys() == {"inputs.foo"}
