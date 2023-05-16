# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx
import pydantic
from backports.cached_property import cached_property

from .core.api_error import ApiError
from .core.jsonable_encoder import jsonable_encoder
from .core.remove_none_from_headers import remove_none_from_headers
from .environment import VellumEnvironment
from .resources.documents.client import AsyncDocumentsClient, DocumentsClient
from .resources.model_versions.client import AsyncModelVersionsClient, ModelVersionsClient
from .resources.sandboxes.client import AsyncSandboxesClient, SandboxesClient
from .resources.test_suites.client import AsyncTestSuitesClient, TestSuitesClient
from .types.generate_options_request import GenerateOptionsRequest
from .types.generate_request import GenerateRequest
from .types.generate_response import GenerateResponse
from .types.search_request_options_request import SearchRequestOptionsRequest
from .types.search_response import SearchResponse
from .types.submit_completion_actual_request import SubmitCompletionActualRequest

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class Vellum:
    def __init__(self, *, environment: VellumEnvironment = VellumEnvironment.PRODUCTION, api_key: str):
        self._environment = environment
        self.api_key = api_key

    def generate(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> GenerateResponse:
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        _response = httpx.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.predict}/", "v1/generate"),
            json=jsonable_encoder(_request),
            headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(GenerateResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def search(
        self,
        *,
        index_id: typing.Optional[str] = OMIT,
        index_name: typing.Optional[str] = OMIT,
        query: str,
        options: typing.Optional[SearchRequestOptionsRequest] = OMIT,
    ) -> SearchResponse:
        _request: typing.Dict[str, typing.Any] = {"query": query}
        if index_id is not OMIT:
            _request["index_id"] = index_id
        if index_name is not OMIT:
            _request["index_name"] = index_name
        if options is not OMIT:
            _request["options"] = options
        _response = httpx.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.predict}/", "v1/search"),
            json=jsonable_encoder(_request),
            headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(SearchResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def submit_completion_actuals(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        actuals: typing.List[SubmitCompletionActualRequest],
    ) -> None:
        _request: typing.Dict[str, typing.Any] = {"actuals": actuals}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        _response = httpx.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.predict}/", "v1/submit-completion-actuals"),
            json=jsonable_encoder(_request),
            headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    @cached_property
    def documents(self) -> DocumentsClient:
        return DocumentsClient(environment=self._environment, api_key=self.api_key)

    @cached_property
    def model_versions(self) -> ModelVersionsClient:
        return ModelVersionsClient(environment=self._environment, api_key=self.api_key)

    @cached_property
    def sandboxes(self) -> SandboxesClient:
        return SandboxesClient(environment=self._environment, api_key=self.api_key)

    @cached_property
    def test_suites(self) -> TestSuitesClient:
        return TestSuitesClient(environment=self._environment, api_key=self.api_key)


class AsyncVellum:
    def __init__(self, *, environment: VellumEnvironment = VellumEnvironment.PRODUCTION, api_key: str):
        self._environment = environment
        self.api_key = api_key

    async def generate(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> GenerateResponse:
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "POST",
                urllib.parse.urljoin(f"{self._environment.predict}/", "v1/generate"),
                json=jsonable_encoder(_request),
                headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
                timeout=None,
            )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(GenerateResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def search(
        self,
        *,
        index_id: typing.Optional[str] = OMIT,
        index_name: typing.Optional[str] = OMIT,
        query: str,
        options: typing.Optional[SearchRequestOptionsRequest] = OMIT,
    ) -> SearchResponse:
        _request: typing.Dict[str, typing.Any] = {"query": query}
        if index_id is not OMIT:
            _request["index_id"] = index_id
        if index_name is not OMIT:
            _request["index_name"] = index_name
        if options is not OMIT:
            _request["options"] = options
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "POST",
                urllib.parse.urljoin(f"{self._environment.predict}/", "v1/search"),
                json=jsonable_encoder(_request),
                headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
                timeout=None,
            )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(SearchResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def submit_completion_actuals(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        actuals: typing.List[SubmitCompletionActualRequest],
    ) -> None:
        _request: typing.Dict[str, typing.Any] = {"actuals": actuals}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "POST",
                urllib.parse.urljoin(f"{self._environment.predict}/", "v1/submit-completion-actuals"),
                json=jsonable_encoder(_request),
                headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
                timeout=None,
            )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    @cached_property
    def documents(self) -> AsyncDocumentsClient:
        return AsyncDocumentsClient(environment=self._environment, api_key=self.api_key)

    @cached_property
    def model_versions(self) -> AsyncModelVersionsClient:
        return AsyncModelVersionsClient(environment=self._environment, api_key=self.api_key)

    @cached_property
    def sandboxes(self) -> AsyncSandboxesClient:
        return AsyncSandboxesClient(environment=self._environment, api_key=self.api_key)

    @cached_property
    def test_suites(self) -> AsyncTestSuitesClient:
        return AsyncTestSuitesClient(environment=self._environment, api_key=self.api_key)
