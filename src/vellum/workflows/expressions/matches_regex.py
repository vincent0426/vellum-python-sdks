import re
from typing import Generic, TypeVar, Union

from vellum.workflows.descriptors.base import BaseDescriptor
from vellum.workflows.descriptors.utils import resolve_value
from vellum.workflows.state.base import BaseState

_T = TypeVar("_T")


class MatchesRegexExpression(BaseDescriptor[bool], Generic[_T]):
    def __init__(
        self,
        *,
        expression: Union[BaseDescriptor[_T], _T],
        regex: Union[BaseDescriptor[str], str],
    ) -> None:
        super().__init__(name=f"{expression} matches regex {regex}", types=(bool,))
        self._expression = expression
        self._regex = regex

    def resolve(self, state: "BaseState") -> bool:
        expression = resolve_value(self._expression, state)
        if not isinstance(expression, str):
            raise ValueError(f"Expected a string expression, got: {expression.__class__.__name__}")

        regex = resolve_value(self._regex, state)
        if not isinstance(regex, str):
            raise ValueError(f"Expected a string pattern, got: {regex.__class__.__name__}")

        return re.match(regex, expression) is not None
