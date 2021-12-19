import logging
import re
from typing import Any, Optional, Union
from os import environ as env

logger = logging.getLogger(__name__)

INJECTION_PATTERN = re.compile(r"#([a-z]+)\[([a-zA-Z][a-zA-Z0-9_]*)\]")


class ExecutionContext:
    """
    Stores the context variables read from input, or from output responses.
    Resolves the #context[var_name] and #env[var_name] tokens.
    """

    def __init__(self) -> None:
        self.__variables = {}

    def has(self, variable_name) -> bool:
        return variable_name in self.__variables

    def get(self, variable_name) -> Any:
        """
        Retrieves a context variable value, or None if the variable is not defined.
        """
        return (
            self.__variables[variable_name]
            if variable_name in self.__variables
            else None
        )

    def set(self, variable_name, variable_value) -> None:
        """
        Sets a context variable value.
        """
        logger.debug(f"Setting variable {variable_name} to {variable_value}")
        if variable_name in self.__variables:
            logger.warning(
                f"Overriding request context variable {variable_name} ! Possible misconfiguration"
            )
        self.__variables[variable_name] = variable_value

    def apply(self, obj: Union[str, dict]):
        """
        Replaces all `#context` and `#env` tokens in given obj.

        If obj is a `str`, `apply()` replaces all found tokens with matching value.
        If obj is a `dict`, `apply()` replaces all its values with `apply(value)` result.

        This function always returns the replacement result, without modifying given `obj`.
        """
        if isinstance(obj, str):
            return INJECTION_PATTERN.sub(self.resolve_match, obj)
        elif isinstance(obj, dict):
            return {k: self.apply(v) for k, v in obj.items()}

    def resolve_match(self, match: re.Match) -> str:
        """
        Resolves the value corresponding to given `Pattern` `Match`.

        Input `Match` must look like `#env[var_name]` or `#context[var_name]`.
        """
        source, var_name = match.groups()
        logger.debug(f"Resolving variable {var_name} from {source}")

        var_value = self.resolve_variable(source, var_name)
        if var_value:
            logger.debug(f"Resolved to {var_value}")
            return var_value
        else:
            logger.warning(
                f"Unable to resolve {var_name} from {source}. Possible misconfiguration"
            )
            return f"#{source}[{var_name}]"

    def resolve_variable(self, source: str, var_name: str) -> Optional[str]:
        if source == "context" and self.has(var_name):
            return self.get(var_name)
        elif source == "env" and var_name in env:
            return env[var_name]
        return None
