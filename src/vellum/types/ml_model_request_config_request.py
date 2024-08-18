# This file was auto-generated by Fern from our API Definition.

from ..core.pydantic_utilities import UniversalBaseModel
import typing
from .ml_model_request_authorization_config_request import MlModelRequestAuthorizationConfigRequest
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class MlModelRequestConfigRequest(UniversalBaseModel):
    headers: typing.Optional[typing.Dict[str, typing.Optional[str]]] = None
    authorization: typing.Optional[MlModelRequestAuthorizationConfigRequest] = None
    body_template: typing.Optional[str] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
