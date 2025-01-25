from vellum.workflows.errors.types import WorkflowErrorCode

from tests.workflows.basic_match_regex.workflow import Inputs, RegexMatchWorkflow


def test_regex_match_workflow():
    workflow = RegexMatchWorkflow()

    input_string = "Hello, World!"
    pattern = r"Hello, \w+!"
    terminal_event = workflow.run(inputs=Inputs(input_string=input_string, pattern=pattern))

    assert terminal_event.name == "workflow.execution.fulfilled"
    assert terminal_event.outputs.final_value is True


def test_regex_no_match_workflow():
    workflow = RegexMatchWorkflow()

    input_string = "Goodbye, World!"
    pattern = r"Hello, \w+!"
    terminal_event = workflow.run(inputs=Inputs(input_string=input_string, pattern=pattern))

    # THEN the workflow will reject
    assert terminal_event.name == "workflow.execution.rejected"

    assert terminal_event.error.message == "Input does not match the pattern"
    assert terminal_event.error.code == WorkflowErrorCode.USER_DEFINED_ERROR
