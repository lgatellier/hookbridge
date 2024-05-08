from jsonpath_ng import parse
import logging
import re
from typing import Any, Optional, Union
from os import environ as env


from hookbridge.exceptions import UnResolvableInjectionException

logger = logging.getLogger(__name__)

INJECTION_PATTERN = re.compile(r"#([a-z]+)(\[([a-zA-Z][a-zA-Z0-9_]*)\])?(\..+)?")


class ExecutionContext:
    """
    Stores the context variables read from input, or from output responses.
    Resolves the #context[var_name] and #env[var_name] tokens.
    """

    def __init__(self, input: object = {}) -> None:
        self.__variables = {}
        self.__input = input
        self.__output = {}

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
        Replaces all `#context`, #input` and `#env` tokens in given obj.

        If obj is a `str`, `apply()` replaces all found tokens with matching value.
        If obj is a `dict`, `apply()` replaces all its values with `apply(value)` result.

        This function always returns the replacement result, without modifying given `obj`.
        """
        if isinstance(obj, str):
            return INJECTION_PATTERN.sub(self.resolve_match, obj)
        elif isinstance(obj, dict):
            return {k: self.apply(v) for k, v in obj.items()}

    def resolve_match(self, match: re.Match) -> str | int | bool:
        """
        Resolves the value corresponding to given `Pattern` `Match`.

        Input `Match` must look like `#env[var_name]` or `#context[var_name]`.
        """
        source, unused_brackets, var_name, jsonpath = match.groups()
        logger.debug(f"Resolving variable {var_name} from {source}")

        if jsonpath:
            jsonpath_expr = parse(f"${jsonpath}")

        var_value = None
        if source in ["context", "env"]:
            var_value = self.resolve_variable(source, var_name)
        elif source == "input":
            var_value = self.resolve_input(jsonpath_expr)
        elif source == "output":
            var_value = self.resolve_output(
                rule_name=var_name, jsonpath_expr=jsonpath_expr
            )
        if var_value:
            logger.debug(f"Resolved to {var_value}")
            return str(var_value)
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

    def add_output(self, rule_name: str, response_body: object = {}):
        logger.debug("Adding rule %s output to context : %s", rule_name, response_body)
        self.__output[rule_name] = response_body

    def __str__(self) -> str:
        return f"ExecutionContext[input: {self.__input}, output: {self.__output}]"

    def resolve_input(self, json_path_expr: any) -> any:
        return self.__resolve_jsonpath(json_path_expr, self.__input)

    def resolve_output(self, rule_name: str, jsonpath_expr: any) -> any:
        return self.__resolve_jsonpath(jsonpath_expr, self.__output[rule_name])

    def __resolve_jsonpath(self, jsonpath_expr, source) -> any:
        results = jsonpath_expr.find(source)
        if len(results) == 0:
            raise UnResolvableInjectionException(jsonpath_expr)
        return results[0].value
