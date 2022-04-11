from os import environ as env
import unittest
from webhook_gateway.routes.route import Route

from webhook_gateway.routes.validator import validate_config, validate_route
from webhook_gateway.exceptions import ConfigurationException


class ConfigurationValidatorTest(unittest.TestCase):
    def test_validate_config_str_novariable(self):
        validate_config("testroute", "teststring", ["my_var_1", "my_var_2"])

    def test_validate_config_str_withvariable_env_known(self):
        env["knownvariable"] = "varvalue"
        validate_config(
            "testroute",
            "blablabla #env[knownvariable] blablabla",
            ["my_var_1", "my_var_2"],
        )
        env.pop("knownvariable")

    def test_validate_config_str_withvariable_env_unknown(self):
        with self.assertRaises(ConfigurationException):
            validate_config(
                "testroute",
                "blablabla #env[unknownvariable] blablabla",
                ["my_var_1", "my_var_2"],
            )

    def test_validate_config_str_withvariable_context_known(self):
        validate_config(
            "testroute",
            "blablabla #context[knownvariable] blablabla",
            ["knownvariable", "my_var_2"],
        )

    def test_validate_config_str_nospace_withvariable_context_known(self):
        validate_config(
            "testroute",
            "blablabla#context[knownvariable]blablabla",
            ["knownvariable", "my_var_2"],
        )

    def test_validate_config_str_withvariable_context_unknown(self):
        with self.assertRaises(ConfigurationException):
            validate_config(
                "testroute",
                "blablabla #context[unknownvariable] blablabla",
                ["knownvariable", "my_var_2"],
            )

    def test_validate_config_dict_knownvars(self):
        env["knownvariable"] = "varvalue"
        obj = {
            "key": "value",
            "key2": {"key21": "blablabla#env[knownvariable]blablabla"},
            "key3": "blablabla#context[knownvariable]blablabla",
        }
        validate_config("testrule", obj, ["knownvariable", "my_var_2"])
        env.pop("knownvariable")

    def test_validate_config_dict_unknown_envvar(self):
        obj = {
            "key": "value",
            "key2": {"key21": "blablabla#env[unknownvariable]blablabla"},
            "key3": "blablabla#context[knownvariable]blablabla",
        }
        with self.assertRaises(ConfigurationException):
            validate_config("testrule", obj, ["knownvariable", "my_var_2"])

    def test_validate_config_dict_unknown_contextvar(self):
        env["knownvariable"] = "varvalue"
        obj = {
            "key": "value",
            "key2": {"key21": "blablabla#env[knownvariable]blablabla"},
            "key3": "blablabla#context[unknownvariable]blablabla",
        }
        with self.assertRaises(ConfigurationException):
            validate_config("testrule", obj, ["knownvariable", "my_var_2"])
        env.pop("knownvariable")


class ConfigurationRouteValidatorTest(unittest.TestCase):
    def create_route(
        self, auth_headers: dict = None, input_body: dict = None, output: dict = None
    ):
        route = {
            "auth_headers": {"X-Api-Token": "MySuperToken"},
            "input": {
                "body": {
                    "$.num": {"equalsTo": "12345", "context_variable": "TICKET_NUM"}
                }
            },
            "output": {
                "gitlab": {
                    "url": "https://gitlab.com/api/v4/projects/lgatellier%2Ftest/issues",
                    "headers": {"Private-Token": "#env[GITLAB_API_TOKEN]"},
                    "body": {"title": "Océane #context[TICKET_NUM]"},
                    "context_variables": {"$.id": "GITLAB_ISSUE_ID"},
                }
            },
        }
        if auth_headers:
            route["auth_headers"].update(auth_headers)
        if input_body:
            route["input"]["body"].update(input_body)
        if output:
            route["output"]["gitlab"].update(output)

        return Route("testroute", route)

    def test_validate_route_passing(self):
        env["GITLAB_API_TOKEN"] = "thisisasupertoken"
        validate_route(self.create_route())
        env.pop("GITLAB_API_TOKEN")

    def test_validate_route_call_unknown_context_variable(self):
        env["GITLAB_API_TOKEN"] = "thisisasupertoken"
        with self.assertRaises(ConfigurationException):
            validate_route(
                self.create_route(
                    output={"body": {"title": "Océane #context[UNKNOWN_VAR]"}}
                )
            )
        env.pop("GITLAB_API_TOKEN")

    def test_validate_route_call_unknown_env_variable(self):
        if "GITLAB_API_TOKEN" in env:
            env.pop("GITLAB_API_TOKEN")
        with self.assertRaises(ConfigurationException):
            validate_route(self.create_route())
