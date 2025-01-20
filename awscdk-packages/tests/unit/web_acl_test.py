import unittest

from aws_cdk import Stack

from packages.waf.web_acl_builder import WebAclBuilder, WebAclScope, CustomRules


class WebAclTestCase(unittest.TestCase):

    def test_web_acl_builder(self):
        stack = Stack()
        web_acl_builder = WebAclBuilder("WebAclExample", stack)
        web_acl_builder.scope(WebAclScope.CLOUDFRONT)
        web_acl_builder.description("WebAcl Example")
        web_acl_builder.visibility_config_metric_name("metric-name")
        web_acl_builder.rules([CustomRules.LOW_RATE_LIMIT_CUSTOM_HEADER,
                               CustomRules.MEDIUM_RATE_LIMIT_CUSTOM_HEADER,
                               CustomRules.HIGH_RATE_LIMIT_CUSTOM_HEADER])

        web_acl = web_acl_builder.build()

        self.assertIsNotNone(web_acl)
