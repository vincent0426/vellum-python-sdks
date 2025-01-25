from vellum.workflows.inputs.base import BaseInputs
from vellum.workflows.nodes.bases.base import BaseNode
from vellum.workflows.nodes.core import ErrorNode
from vellum.workflows.ports.port import Port
from vellum.workflows.state.base import BaseState
from vellum.workflows.workflows.base import BaseWorkflow


class Inputs(BaseInputs):
    input_string: str
    pattern: str


class RegexMatchNode(BaseNode):
    class Ports(BaseNode.Ports):
        match = Port.on_if(Inputs.input_string.matches_regex(Inputs.pattern))
        no_match = Port.on_else()


class MatchNode(BaseNode):
    class Outputs(BaseNode.Outputs):
        result = True


class FailNode(ErrorNode):
    error = "Input does not match the pattern"


class RegexMatchWorkflow(BaseWorkflow[Inputs, BaseState]):
    """
    Workflow to test the matches_regex functionality.
    """

    graph = {
        RegexMatchNode.Ports.match >> MatchNode,
        RegexMatchNode.Ports.no_match >> FailNode,
    }

    class Outputs(BaseWorkflow.Outputs):
        final_value = MatchNode.Outputs.result
