import unittest

from ..mocks import MockedHTTPRequest

from hookbridge.routes.exceptions import RequestDoNotMatchRouteException
from hookbridge.routes.rules import (
    BodyPropertyEqualsToInputRule,
    BodyPropertyPresentInputRule,
)


class InputRulesTest(unittest.TestCase):
    def do_test(self, cls: type, rule: str, request_body: dict, rule_params={}):
        cls(rule, rule_params).apply(MockedHTTPRequest(request_body))

    def test_BodyPropertyPresentInputRule_absent(self):
        with self.assertRaises(RequestDoNotMatchRouteException):
            self.do_test(
                cls=BodyPropertyPresentInputRule,
                rule="$.num",
                request_body={"number": "123456"},
            )

    def test_BodyPropertyPresentInputRule_present(self):
        self.do_test(
            cls=BodyPropertyPresentInputRule,
            rule="$.num",
            request_body={"num": "123456"},
        )

    def test_BodyPropertyEqualsToInputRule_valid(self):
        self.do_test(
            cls=BodyPropertyEqualsToInputRule,
            rule="$.num",
            rule_params={"equalsTo": "123456"},
            request_body={"num": "123456"},
        )

    def test_BodyPropertyEqualsToInputRule_invalid(self):
        with self.assertRaises(RequestDoNotMatchRouteException):
            self.do_test(
                cls=BodyPropertyEqualsToInputRule,
                rule="$.num",
                rule_params={"equalsTo": "123456"},
                request_body={"num": "wrongvalue"},
            )

    def test_BodyPropertyEqualsToInputRule_absent(self):
        with self.assertRaises(RequestDoNotMatchRouteException):
            self.do_test(
                cls=BodyPropertyEqualsToInputRule,
                rule="$.num",
                rule_params={"equalsTo": "123456"},
                request_body={"number": "123456"},
            )
