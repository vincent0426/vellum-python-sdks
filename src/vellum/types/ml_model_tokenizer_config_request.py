# This file was auto-generated by Fern from our API Definition.

import typing
from .hugging_face_tokenizer_config_request import HuggingFaceTokenizerConfigRequest
from .tik_token_tokenizer_config_request import TikTokenTokenizerConfigRequest

MlModelTokenizerConfigRequest = typing.Union[HuggingFaceTokenizerConfigRequest, TikTokenTokenizerConfigRequest]
