from typing import TYPE_CHECKING, Any, Dict, Generator, Generic, Iterable, Literal, Type, Union

from pydantic import field_serializer

from vellum.core.pydantic_utilities import UniversalBaseModel
from vellum.workflows.errors import VellumError
from vellum.workflows.outputs.base import BaseOutput
from vellum.workflows.references import ExternalInputReference
from vellum.workflows.types.generics import OutputsType, StateType, WorkflowInputsType

from .node import (
    NodeExecutionFulfilledEvent,
    NodeExecutionInitiatedEvent,
    NodeExecutionPausedEvent,
    NodeExecutionRejectedEvent,
    NodeExecutionResumedEvent,
    NodeExecutionStreamingEvent,
)
from .types import BaseEvent, default_serializer, serialize_type_encoder

if TYPE_CHECKING:
    from vellum.workflows.workflows.base import BaseWorkflow


class _BaseWorkflowExecutionBody(UniversalBaseModel):
    workflow_definition: Type["BaseWorkflow"]

    @field_serializer("workflow_definition")
    def serialize_workflow_definition(self, workflow_definition: Type, _info: Any) -> Dict[str, Any]:
        return serialize_type_encoder(workflow_definition)


class _BaseWorkflowEvent(BaseEvent):
    body: _BaseWorkflowExecutionBody

    @property
    def workflow_definition(self) -> Type["BaseWorkflow"]:
        return self.body.workflow_definition


class WorkflowExecutionInitiatedBody(_BaseWorkflowExecutionBody, Generic[WorkflowInputsType]):
    inputs: WorkflowInputsType

    @field_serializer("inputs")
    def serialize_inputs(self, inputs: WorkflowInputsType, _info: Any) -> Dict[str, Any]:
        return default_serializer(inputs)


class WorkflowExecutionInitiatedEvent(_BaseWorkflowEvent, Generic[WorkflowInputsType]):
    name: Literal["workflow.execution.initiated"] = "workflow.execution.initiated"
    body: WorkflowExecutionInitiatedBody[WorkflowInputsType]

    @property
    def inputs(self) -> WorkflowInputsType:
        return self.body.inputs


class WorkflowExecutionStreamingBody(_BaseWorkflowExecutionBody):
    output: BaseOutput

    @field_serializer("output")
    def serialize_output(self, output: BaseOutput, _info: Any) -> Dict[str, Any]:
        return default_serializer(output)


class WorkflowExecutionStreamingEvent(_BaseWorkflowEvent):
    name: Literal["workflow.execution.streaming"] = "workflow.execution.streaming"
    body: WorkflowExecutionStreamingBody

    @property
    def output(self) -> BaseOutput:
        return self.body.output


class WorkflowExecutionFulfilledBody(_BaseWorkflowExecutionBody, Generic[OutputsType]):
    outputs: OutputsType

    @field_serializer("outputs")
    def serialize_outputs(self, outputs: OutputsType, _info: Any) -> Dict[str, Any]:
        return default_serializer(outputs)


class WorkflowExecutionFulfilledEvent(_BaseWorkflowEvent, Generic[OutputsType]):
    name: Literal["workflow.execution.fulfilled"] = "workflow.execution.fulfilled"
    body: WorkflowExecutionFulfilledBody[OutputsType]

    @property
    def outputs(self) -> OutputsType:
        return self.body.outputs


class WorkflowExecutionRejectedBody(_BaseWorkflowExecutionBody):
    error: VellumError


class WorkflowExecutionRejectedEvent(_BaseWorkflowEvent):
    name: Literal["workflow.execution.rejected"] = "workflow.execution.rejected"
    body: WorkflowExecutionRejectedBody

    @property
    def error(self) -> VellumError:
        return self.body.error


class WorkflowExecutionPausedBody(_BaseWorkflowExecutionBody):
    external_inputs: Iterable[ExternalInputReference]


class WorkflowExecutionPausedEvent(_BaseWorkflowEvent):
    name: Literal["workflow.execution.paused"] = "workflow.execution.paused"
    body: WorkflowExecutionPausedBody

    @property
    def external_inputs(self) -> Iterable[ExternalInputReference]:
        return self.body.external_inputs


class WorkflowExecutionResumedBody(_BaseWorkflowExecutionBody):
    pass


class WorkflowExecutionResumedEvent(_BaseWorkflowEvent):
    name: Literal["workflow.execution.resumed"] = "workflow.execution.resumed"
    body: WorkflowExecutionResumedBody


class WorkflowExecutionSnapshottedBody(_BaseWorkflowExecutionBody, Generic[StateType]):
    state: StateType

    @field_serializer("state")
    def serialize_state(self, state: StateType, _info: Any) -> Dict[str, Any]:
        return default_serializer(state)


class WorkflowExecutionSnapshottedEvent(_BaseWorkflowEvent, Generic[StateType]):
    name: Literal["workflow.execution.snapshotted"] = "workflow.execution.snapshotted"
    body: WorkflowExecutionSnapshottedBody[StateType]

    @property
    def state(self) -> StateType:
        return self.body.state


GenericWorkflowEvent = Union[
    WorkflowExecutionStreamingEvent,
    WorkflowExecutionRejectedEvent,
    WorkflowExecutionPausedEvent,
    WorkflowExecutionResumedEvent,
    NodeExecutionInitiatedEvent,
    NodeExecutionStreamingEvent,
    NodeExecutionFulfilledEvent,
    NodeExecutionRejectedEvent,
    NodeExecutionPausedEvent,
    NodeExecutionResumedEvent,
]

WorkflowEvent = Union[
    GenericWorkflowEvent,
    WorkflowExecutionInitiatedEvent,
    WorkflowExecutionFulfilledEvent,
    WorkflowExecutionSnapshottedEvent,
]

WorkflowEventStream = Generator[WorkflowEvent, None, None]
