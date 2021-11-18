import logging
import re
from typing import Any, Optional, Union
from os import environ as env

logger = logging.getLogger(__name__)

INJECTION_PATTERN = re.compile(r"#([a-z]+)\[([a-zA-Z][a-zA-Z0-9_]*)\]")


class ExecutionContext:
    def __init__(self) -> None:
        self.__variables = {}

    def has(self, key) -> bool:
        return key in self.__variables

    def get(self, key) -> Any:
        return self.__variables[key] if key in self.__variables else None

    def set(self, key, value) -> None:
        if key in self.__variables:
            logger.warn(
                f"Overriding request context variable {key} ! Possible misconfiguration"
            )
        self.__variables[key] = value

    def apply(self, obj: Union[str, dict]):
        if isinstance(obj, str):
            return INJECTION_PATTERN.sub(self.resolve_match, obj)
        elif isinstance(obj, dict):
            return {k: self.apply(v) for k, v in obj.items()}

    def resolve_match(self, match: re.Match) -> str:
        source, var_name = match.groups()
        logger.debug(f"Resolving variable {var_name} from {source}")

        var_value = self.resolve_variable(source, var_name)
        if var_value:
            logger.debug(f"Resolved to {var_value}")
            return var_value
        else:
            logger.warn(
                f"Unable to resolve {var_name} from {source}. Possible misconfiguration"
            )
            return f"#{source}[{var_name}]"

    def resolve_variable(self, source: str, var_name: str) -> Optional[str]:
        if source == "context" and self.has(var_name):
            return self.get(var_name)
        elif source == "env" and var_name in env:
            return env[var_name]
        return None
