# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
import datetime as dt
from .workflow_node_result_data import WorkflowNodeResultData
from .workflow_event_error import WorkflowEventError
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class RejectedWorkflowNodeResultEvent(UniversalBaseModel):
    """
    An event that indicates that the node has rejected its execution.
    """

    id: str
    node_id: str
    node_result_id: str
    state: typing.Literal["REJECTED"] = "REJECTED"
    ts: typing.Optional[dt.datetime] = None
    data: typing.Optional[WorkflowNodeResultData] = None
    source_execution_id: typing.Optional[str] = None
    error: WorkflowEventError

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
