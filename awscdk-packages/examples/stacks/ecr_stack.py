from aws_cdk import Stack
from constructs import Construct

from packages.ecr.ecr_builder import EcrBuilder


class EcrStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ecr_repository = self.__ecr_repository()

    def __ecr_repository(self):
        ecr_builder = EcrBuilder("ECR", self)
        ecr_builder.repository_name("ecr-repo-test")
        ecr_builder.grant_cross_account_access(["123456789", "987654321"])

        return ecr_builder.build()
