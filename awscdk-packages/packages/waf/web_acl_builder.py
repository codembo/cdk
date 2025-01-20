from enum import StrEnum

from aws_cdk import aws_wafv2 as wafv2, Stack

from packages.builder import Builder


class WebAclScope(StrEnum):
    CLOUDFRONT = "CLOUDFRONT"
    REGIONAL = "REGIONAL"


class CustomRules:

    @staticmethod
    def __rate_limit_custom_header(name, priority, limit, evaluation_window_sec, header_name):
        block_action_property = wafv2.CfnWebACL.BlockActionProperty(
            custom_response=wafv2.CfnWebACL.CustomResponseProperty(
                response_code=429,
                custom_response_body_key="TooManyRequestsBody"
            )
        )

        return wafv2.CfnWebACL.RuleProperty(
            name=name,
            priority=priority,
            action=wafv2.CfnWebACL.RuleActionProperty(block=block_action_property),
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="test",
                sampled_requests_enabled=True
            ),
            statement=wafv2.CfnWebACL.StatementProperty(
                rate_based_statement=wafv2.CfnWebACL.RateBasedStatementProperty(
                    limit=limit,
                    evaluation_window_sec=evaluation_window_sec,
                    aggregate_key_type="CUSTOM_KEYS",
                    custom_keys=[wafv2.CfnWebACL.RateBasedStatementCustomKeyProperty(
                        header=wafv2.CfnWebACL.RateLimitHeaderProperty(name=header_name, text_transformations=[
                            wafv2.CfnWebACL.TextTransformationProperty(priority=0, type="NONE")]))]
                )
            )
        )

    LOW_RATE_LIMIT_CUSTOM_HEADER = __rate_limit_custom_header(name="low-rate-limit",
                                                              priority=2,
                                                              limit=10,
                                                              evaluation_window_sec=60,
                                                              header_name="x-low-rate-limit")

    MEDIUM_RATE_LIMIT_CUSTOM_HEADER = __rate_limit_custom_header(name="medium-rate-limit",
                                                                 priority=1,
                                                                 limit=30,
                                                                 evaluation_window_sec=60,
                                                                 header_name="x-medium-rate-limit")

    HIGH_RATE_LIMIT_CUSTOM_HEADER = __rate_limit_custom_header(name="high-rate-limit",
                                                               priority=0,
                                                               limit=50,
                                                               evaluation_window_sec=60,
                                                               header_name="x-high-rate-limit")


class WebAclBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__scope = None
        self.__description = None
        self.__cloud_watch_metrics_enabled = True
        self.__sampled_requests_enabled = True
        self.__visibility_config_metric_name = None
        self.__rules = []
        self.__web_acl_association_resource_arn = None

    def scope(self, scope: WebAclScope):
        self.__scope = scope

    def description(self, description):
        self.__description = description

    def cloud_watch_metrics_enabled(self, cloud_watch_metrics_enabled):
        self.__cloud_watch_metrics_enabled = cloud_watch_metrics_enabled

    def sampled_requests_enabled(self, sampled_requests_enabled):
        self.__sampled_requests_enabled = sampled_requests_enabled

    def visibility_config_metric_name(self, visibility_config_metric_name):
        self.__visibility_config_metric_name = visibility_config_metric_name

    def rules(self, rules: list[wafv2.CfnWebACL.RuleProperty]):
        self.__rules = rules

    def web_acl_association_resource_arn(self, web_acl_association_resource_arn):
        self.__web_acl_association_resource_arn = web_acl_association_resource_arn

    def build(self) -> wafv2.CfnWebACL:
        custom_response_body = wafv2.CfnWebACL.CustomResponseBodyProperty(
            content="<html><body><h1>Too Many Requests</h1><p>Please try again later.</p></body></html>",
            content_type="TEXT_HTML"
        )

        web_acl = wafv2.CfnWebACL(self.stack, self.construct_id,
                                  default_action=wafv2.CfnWebACL.DefaultActionProperty(
                                      allow=wafv2.CfnWebACL.AllowActionProperty()),
                                  description=self.__description,
                                  scope=self.__scope,
                                  visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                                      cloud_watch_metrics_enabled=self.__cloud_watch_metrics_enabled,
                                      metric_name=self.__visibility_config_metric_name,
                                      sampled_requests_enabled=self.__sampled_requests_enabled
                                  ),
                                  custom_response_bodies={
                                      "TooManyRequestsBody": custom_response_body
                                  },
                                  rules=self.__rules,
                                  association_config=wafv2.CfnWebACL.AssociationConfigProperty())

        if self.__web_acl_association_resource_arn:
            wafv2.CfnWebACLAssociation(self.stack, f"{self.construct_id}WebAclAssociation",
                                       resource_arn=self.__web_acl_association_resource_arn,
                                       web_acl_arn=web_acl.attr_arn)

        return web_acl
