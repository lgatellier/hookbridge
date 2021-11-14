import unittest

from ..mocks import MockedHTTPRequest

from webhook_gateway.routes.exceptions import RequestDoNotMatchRouteException
from webhook_gateway.routes.rules import (
    BodyPropertyEqualsToInputRule,
    BodyPropertyPresentInputRule,
)


class InputRulesTest(unittest.TestCase):
    def test_BodyPropertyPresentInputRule_absent(self):
        rule = BodyPropertyPresentInputRule("$.num", {})
        with self.assertRaises(RequestDoNotMatchRouteException):
            rule.apply(MockedHTTPRequest({"number": "123456"}))

    def test_BodyPropertyPresentInputRule_present(self):
        rule = BodyPropertyPresentInputRule("$.num", {})
        rule.apply(MockedHTTPRequest({"num": "123456"}))

    def test_BodyPropertyEqualsToInputRule_valid(self):
        rule = BodyPropertyEqualsToInputRule("$.num", {"equalsTo": "123456"})
        rule.apply(MockedHTTPRequest({"num": "123456"}))

    def test_BodyPropertyEqualsToInputRule_invalid(self):
        rule = BodyPropertyEqualsToInputRule("$.num", {"equalsTo": "123456"})
        with self.assertRaises(RequestDoNotMatchRouteException):
            rule.apply(MockedHTTPRequest({"num": "wrongvalue"}))

    def test_BodyPropertyEqualsToInputRule_absent(self):
        rule = BodyPropertyEqualsToInputRule("$.num", {"equalsTo": "123456"})
        with self.assertRaises(RequestDoNotMatchRouteException):
            rule.apply(MockedHTTPRequest({"number": "123456"}))
