import json
import unittest

from fastapi import Request
from starlette.types import Scope

from webhook_router.routes.exceptions import RequestDoNotMatchRouteException
from webhook_router.routes.rules import BodyPropertyEqualsToInputRule, BodyPropertyPresentInputRule

def make_request(json_body: dict):
    req = Request(scope={
        'type': 'http'
    })
    req.json_body = json_body
    return req

class InputRulesTest(unittest.TestCase):
    def test_BodyPropertyPresentInputRule_absent(self):
        rule = BodyPropertyPresentInputRule('$.num', {})
        with self.assertRaises(RequestDoNotMatchRouteException):
            rule.apply(make_request({
                'number': '123456'
            }))

    def test_BodyPropertyPresentInputRule_present(self):
        rule = BodyPropertyPresentInputRule('$.num', {})
        rule.apply(make_request({
            'num': '123456'
        }))

    def test_BodyPropertyEqualsToInputRule_valid(self):
        rule = BodyPropertyEqualsToInputRule('$.num', { 'equalsTo': '123456' })
        rule.apply(make_request({
            'num': '123456'
        }))

    def test_BodyPropertyEqualsToInputRule_invalid(self):
        rule = BodyPropertyEqualsToInputRule('$.num', { 'equalsTo': '123456' })
        with self.assertRaises(RequestDoNotMatchRouteException):
            rule.apply(make_request({
                'num': 'wrongvalue'
            }))

    def test_BodyPropertyEqualsToInputRule_absent(self):
        rule = BodyPropertyEqualsToInputRule('$.num', { 'equalsTo': '123456' })
        with self.assertRaises(RequestDoNotMatchRouteException):
            rule.apply(make_request({
                'number': '123456'
            }))
