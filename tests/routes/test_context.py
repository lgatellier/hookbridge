import unittest
from os import environ as env

from hookbridge.context import ExecutionContext


class ExecutionContextTest(unittest.TestCase):
    def test_set_get_variable_nominal(self):
        ctx = ExecutionContext()
        ctx.set("varname", "value")
        assert "value" == ctx.get("varname")

    def test_set_get_variable_wrongname(self):
        ctx = ExecutionContext()
        ctx.set("varname", "value")
        assert ctx.get("wrongvarname") is None

    def test_has_variable(self):
        ctx = ExecutionContext()
        assert not ctx.has("varname")
        ctx.set("varname", "value")
        assert ctx.has("varname")

    def test_apply_env_variable(self):
        env["MYTESTVARIABLE"] = "VARVALUE"
        ctx = ExecutionContext()
        injection_str = "#env[MYTESTVARIABLE]"
        assert "VARVALUE" == ctx.apply(injection_str)

    def test_apply_ctx_variable(self):
        ctx = ExecutionContext()
        ctx.set("MYTESTVARIABLE", "myvalue")
        injection_str = "#context[MYTESTVARIABLE]"
        assert "myvalue" == ctx.apply(injection_str)

    def test_apply_partial_match(self):
        ctx = ExecutionContext()
        ctx.set("MYTESTVARIABLE", "myvalue")
        injection_str = "beforestr#context[MYTESTVARIABLE]afterstr"
        assert "beforestrmyvalueafterstr" == ctx.apply(injection_str)

    def test_apply_unknown_variable(self):
        ctx = ExecutionContext()
        ctx.set("MYTESTVARIABLE", "myvalue")
        injection_str = "#context[OTHERTESTVARIABLE]"
        assert "#context[OTHERTESTVARIABLE]" == ctx.apply(injection_str)

    def test_apply_unknown_variable_source(self):
        ctx = ExecutionContext()
        ctx.set("MYTESTVARIABLE", "myvalue")
        injection_str = "#unknownsource[MYTESTVARIABLE]"
        assert "#unknownsource[MYTESTVARIABLE]" == ctx.apply(injection_str)
