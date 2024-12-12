# This file was auto-generated by Fern from our API Definition.

import typing

from .test_suite_run_deployment_release_tag_exec_config_request import TestSuiteRunDeploymentReleaseTagExecConfigRequest
from .test_suite_run_external_exec_config_request import TestSuiteRunExternalExecConfigRequest
from .test_suite_run_prompt_sandbox_history_item_exec_config_request import (
    TestSuiteRunPromptSandboxHistoryItemExecConfigRequest,
)
from .test_suite_run_workflow_release_tag_exec_config_request import TestSuiteRunWorkflowReleaseTagExecConfigRequest
from .test_suite_run_workflow_sandbox_history_item_exec_config_request import (
    TestSuiteRunWorkflowSandboxHistoryItemExecConfigRequest,
)

TestSuiteRunExecConfigRequest = typing.Union[
    TestSuiteRunDeploymentReleaseTagExecConfigRequest,
    TestSuiteRunPromptSandboxHistoryItemExecConfigRequest,
    TestSuiteRunWorkflowReleaseTagExecConfigRequest,
    TestSuiteRunWorkflowSandboxHistoryItemExecConfigRequest,
    TestSuiteRunExternalExecConfigRequest,
]
