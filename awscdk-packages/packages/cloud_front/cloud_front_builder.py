from typing import Sequence

from aws_cdk import Stack, aws_cloudfront as cf

from packages.builder import Builder


class CloudFrontBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__certificate = None
        self.__domain_names = None
        self.__default_root_object = "index.html"
        self.__error_responses = None
        self.__default_behavior = None
        self.__web_acl_arn = None
        self.__create_origin_access_control = None

    def certificate(self, certificate):
        self.__certificate = certificate
        return self

    def domain_names(self, domain_names: Sequence[str]):
        self.__domain_names = domain_names
        return self

    def default_root_object(self, default_root_object):
        self.__default_root_object = default_root_object
        return self

    def error_responses(self, error_responses: Sequence[cf.ErrorResponse]):
        self.__error_responses = error_responses
        return self

    def default_behavior(self, default_behavior: cf.BehaviorOptions):
        self.__default_behavior = default_behavior
        return self

    def web_acl_arn(self, web_acl_arn: str):
        self.__web_acl_arn = web_acl_arn
        return self

    def create_origin_access_control(self, create_origin_access_control: bool):
        self.__create_origin_access_control = create_origin_access_control
        return self

    def __origin_access_control(self):
        return cf.CfnOriginAccessControl(self.stack, "OAC",
                                         origin_access_control_config=cf.CfnOriginAccessControl
                                         .OriginAccessControlConfigProperty(
                                             name="AOC",
                                             origin_access_control_origin_type="s3",
                                             signing_behavior="always",
                                             signing_protocol="sigv4"))

    def build(self) -> cf.Distribution:
        distribution = cf.Distribution(self.stack, self.construct_id,
                                       certificate=self.__certificate,
                                       domain_names=self.__domain_names,
                                       default_root_object=self.__default_root_object,
                                       error_responses=self.__error_responses,
                                       default_behavior=self.__default_behavior,
                                       web_acl_id=self.__web_acl_arn)

        if self.__create_origin_access_control:
            oac = self.__origin_access_control()
            cfn: cf.CfnDistribution = distribution.node.default_child
            cfn.add_property_override("DistributionConfig.Origins.0.OriginAccessControlId", oac.get_att("Id"))
            cfn.add_property_override("DistributionConfig.Origins.0.S3OriginConfig.OriginAccessIdentity", "")

        return distribution
