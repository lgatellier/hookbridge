from os import environ as env
from typing import Union

from webhook_gateway.exceptions import ConfigurationException
from webhook_gateway.routes.route import Route
from webhook_gateway.routes.rules import OutputRule
from webhook_gateway.context import INJECTION_PATTERN


def validate_route(route: Route) -> None:
    """
    Validates a route's configuration.

    Checks the coherence of context/environment variables declaration & usage.
    """
    var_names = [
        v.variable_name for v in route.input_rules if v.variable_name is not None
    ]

    for r in route.output_rules:
        validate_rule(route.name, r, var_names)


def validate_rule(route_name: str, rule: OutputRule, var_names: list[str]) -> None:
    if rule.headers:
        for header_value in rule.headers.values():
            validate_config(route_name, header_value, var_names)

    validate_config(route_name, rule.body, var_names)

    for var_name in rule.variables.values():
        var_names.append(var_name)


def validate_config(
    route_name: str, config: Union[str, dict], var_names: list[str]
) -> None:
    if isinstance(config, dict):
        for v in config.values():
            validate_config(route_name, v, var_names)
        return
    elif not isinstance(config, str):
        raise Exception(f"Invalid type {type(config)} for config object")

    for source, var_name in INJECTION_PATTERN.findall(config):
        if source == "context" and var_name not in var_names:
            raise ConfigurationException(
                f"Route {route_name} : variable {var_name} is used but never declared"
            )
        elif source == "env" and var_name not in env:
            raise ConfigurationException(
                f"Route {route_name} : environment variable {var_name} does not exist"
            )
        elif source not in ["context", "env"]:
            raise ConfigurationException(
                f"Route {route_name} : variable source {source} does not exist"
            )
