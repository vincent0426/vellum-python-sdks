# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...types.test_suite_run_exec_config_request import TestSuiteRunExecConfigRequest
from ...core.request_options import RequestOptions
from ...types.test_suite_run_read import TestSuiteRunRead
from ...core.serialization import convert_and_respect_annotation_metadata
from ...core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...core.jsonable_encoder import jsonable_encoder
from ...types.paginated_test_suite_run_execution_list import PaginatedTestSuiteRunExecutionList
from ...core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class TestSuiteRunsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def create(
        self,
        *,
        test_suite_id: str,
        exec_config: TestSuiteRunExecConfigRequest,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSuiteRunRead:
        """
        Trigger a Test Suite and create a new Test Suite Run

        Parameters
        ----------
        test_suite_id : str
            The ID of the Test Suite to run

        exec_config : TestSuiteRunExecConfigRequest
            Configuration that defines how the Test Suite should be run

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSuiteRunRead


        Examples
        --------
        from vellum import (
            TestSuiteRunDeploymentReleaseTagExecConfigDataRequest,
            TestSuiteRunDeploymentReleaseTagExecConfigRequest,
            Vellum,
        )

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.test_suite_runs.create(
            test_suite_id="test_suite_id",
            exec_config=TestSuiteRunDeploymentReleaseTagExecConfigRequest(
                data=TestSuiteRunDeploymentReleaseTagExecConfigDataRequest(
                    deployment_id="deployment_id",
                ),
            ),
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "v1/test-suite-runs",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json={
                "test_suite_id": test_suite_id,
                "exec_config": convert_and_respect_annotation_metadata(
                    object_=exec_config, annotation=TestSuiteRunExecConfigRequest, direction="write"
                ),
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSuiteRunRead,
                    parse_obj_as(
                        type_=TestSuiteRunRead,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def retrieve(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> TestSuiteRunRead:
        """
        Retrieve a specific Test Suite Run by ID

        Parameters
        ----------
        id : str
            A UUID string identifying this test suite run.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSuiteRunRead


        Examples
        --------
        from vellum import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.test_suite_runs.retrieve(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/test-suite-runs/{jsonable_encoder(id)}",
            base_url=self._client_wrapper.get_environment().default,
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSuiteRunRead,
                    parse_obj_as(
                        type_=TestSuiteRunRead,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list_executions(
        self,
        id: str,
        *,
        expand: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PaginatedTestSuiteRunExecutionList:
        """
        Parameters
        ----------
        id : str
            A UUID string identifying this test suite run.

        expand : typing.Optional[typing.Union[str, typing.Sequence[str]]]
            The response fields to expand for more information.

            - 'results.metric_results.metric_label' expands the metric label for each metric result.
            - 'results.metric_results.metric_definition' expands the metric definition for each metric result.
            - 'results.metric_results.metric_definition.name' expands the metric definition name for each metric result.

        limit : typing.Optional[int]
            Number of results to return per page.

        offset : typing.Optional[int]
            The initial index from which to return the results.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        PaginatedTestSuiteRunExecutionList


        Examples
        --------
        from vellum import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.test_suite_runs.list_executions(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/test-suite-runs/{jsonable_encoder(id)}/executions",
            base_url=self._client_wrapper.get_environment().default,
            method="GET",
            params={
                "expand": expand,
                "limit": limit,
                "offset": offset,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    PaginatedTestSuiteRunExecutionList,
                    parse_obj_as(
                        type_=PaginatedTestSuiteRunExecutionList,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncTestSuiteRunsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def create(
        self,
        *,
        test_suite_id: str,
        exec_config: TestSuiteRunExecConfigRequest,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSuiteRunRead:
        """
        Trigger a Test Suite and create a new Test Suite Run

        Parameters
        ----------
        test_suite_id : str
            The ID of the Test Suite to run

        exec_config : TestSuiteRunExecConfigRequest
            Configuration that defines how the Test Suite should be run

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSuiteRunRead


        Examples
        --------
        import asyncio

        from vellum import (
            AsyncVellum,
            TestSuiteRunDeploymentReleaseTagExecConfigDataRequest,
            TestSuiteRunDeploymentReleaseTagExecConfigRequest,
        )

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.test_suite_runs.create(
                test_suite_id="test_suite_id",
                exec_config=TestSuiteRunDeploymentReleaseTagExecConfigRequest(
                    data=TestSuiteRunDeploymentReleaseTagExecConfigDataRequest(
                        deployment_id="deployment_id",
                    ),
                ),
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "v1/test-suite-runs",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json={
                "test_suite_id": test_suite_id,
                "exec_config": convert_and_respect_annotation_metadata(
                    object_=exec_config, annotation=TestSuiteRunExecConfigRequest, direction="write"
                ),
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSuiteRunRead,
                    parse_obj_as(
                        type_=TestSuiteRunRead,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def retrieve(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> TestSuiteRunRead:
        """
        Retrieve a specific Test Suite Run by ID

        Parameters
        ----------
        id : str
            A UUID string identifying this test suite run.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSuiteRunRead


        Examples
        --------
        import asyncio

        from vellum import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.test_suite_runs.retrieve(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/test-suite-runs/{jsonable_encoder(id)}",
            base_url=self._client_wrapper.get_environment().default,
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSuiteRunRead,
                    parse_obj_as(
                        type_=TestSuiteRunRead,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def list_executions(
        self,
        id: str,
        *,
        expand: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PaginatedTestSuiteRunExecutionList:
        """
        Parameters
        ----------
        id : str
            A UUID string identifying this test suite run.

        expand : typing.Optional[typing.Union[str, typing.Sequence[str]]]
            The response fields to expand for more information.

            - 'results.metric_results.metric_label' expands the metric label for each metric result.
            - 'results.metric_results.metric_definition' expands the metric definition for each metric result.
            - 'results.metric_results.metric_definition.name' expands the metric definition name for each metric result.

        limit : typing.Optional[int]
            Number of results to return per page.

        offset : typing.Optional[int]
            The initial index from which to return the results.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        PaginatedTestSuiteRunExecutionList


        Examples
        --------
        import asyncio

        from vellum import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.test_suite_runs.list_executions(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/test-suite-runs/{jsonable_encoder(id)}/executions",
            base_url=self._client_wrapper.get_environment().default,
            method="GET",
            params={
                "expand": expand,
                "limit": limit,
                "offset": offset,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    PaginatedTestSuiteRunExecutionList,
                    parse_obj_as(
                        type_=PaginatedTestSuiteRunExecutionList,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
