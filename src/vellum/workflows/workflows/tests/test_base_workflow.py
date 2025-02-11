from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.nodes.core.inline_subworkflow_node.node import InlineSubworkflowNode
from vellum.workflows.outputs.base import BaseOutputs
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


def test_base_workflow__inherit_base_outputs():
    class MyNode(BaseNode):
        class Outputs(BaseNode.Outputs):
            foo: str

        def run(self):
            return self.Outputs(foo="bar")

    class MyWorkflow(BaseWorkflow[BaseInputs, BaseState]):
        graph = MyNode

        class Outputs:
            output = MyNode.Outputs.foo

    # TEST that the Outputs class is a subclass of BaseOutputs
    assert issubclass(MyWorkflow.Outputs, BaseOutputs)

    # TEST that the Outputs class does not inherit from object
    assert object not in MyWorkflow.Outputs.__bases__

    workflow = MyWorkflow()
    terminal_event = workflow.run()

    # TEST that the Outputs class has the correct attributes
    assert hasattr(MyWorkflow.Outputs, "output")

    # TEST that the outputs should be correct
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"output": "bar"}


def test_subworkflow__inherit_base_outputs():
    class StartNode(BaseNode):
        class Outputs(BaseNode.Outputs):
            foo: str

        def run(self):
            return self.Outputs(foo="bar")

    class SubWorkflow(BaseWorkflow[BaseInputs, BaseState]):
        graph = StartNode

        class Outputs:
            output = StartNode.Outputs.foo

    class SubworkflowNode(InlineSubworkflowNode):
        subworkflow = SubWorkflow

    class MainWorkflow(BaseWorkflow[BaseInputs, BaseState]):
        graph = SubworkflowNode

        class Outputs:
            output = SubworkflowNode.Outputs.output

    # TEST that the Outputs classes are subclasses of BaseOutputs
    assert issubclass(MainWorkflow.Outputs, BaseOutputs)
    assert issubclass(SubWorkflow.Outputs, BaseOutputs)

    # TEST that the Outputs classes do not inherit from object
    assert object not in MainWorkflow.Outputs.__bases__
    assert object not in SubWorkflow.Outputs.__bases__

    # TEST execution
    workflow = MainWorkflow()
    terminal_event = workflow.run()

    # TEST that the Outputs class has the correct attributes
    assert hasattr(MainWorkflow.Outputs, "output")

    # TEST that the outputs are correct
    assert terminal_event.name == "workflow.execution.fulfilled", terminal_event
    assert terminal_event.outputs == {"output": "bar"}
