from aws_cdk import aws_ecr as ecr, aws_iam as iam, Stack

from packages.builder import Builder


class EcrBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__repository_name = None
        self.__image_scan_on_push = False
        self.__encryption = ecr.RepositoryEncryption.KMS
        self.__image_tag_mutability = ecr.TagMutability.IMMUTABLE
        self.__account_ids = None

    def repository_name(self, repository_name):
        self.__repository_name = repository_name

    def image_scan_on_push(self, image_scan_on_push):
        self.__image_scan_on_push = image_scan_on_push

    def encryption(self, encryption: ecr.RepositoryEncryption):
        self.__encryption = encryption

    def image_tag_mutability(self, image_tag_mutability: ecr.TagMutability):
        self.__image_tag_mutability = image_tag_mutability

    def grant_cross_account_access(self, account_ids: list[str]):
        self.__account_ids = account_ids

    def build(self) -> ecr.Repository:
        ecr_repository = ecr.Repository(self.stack,
                                        self.construct_id,
                                        repository_name=self.__repository_name,
                                        image_scan_on_push=self.__image_scan_on_push,
                                        encryption=self.__encryption,
                                        image_tag_mutability=self.__image_tag_mutability)

        if self.__account_ids:
            self.__grant_pull_push(ecr_repository)

        return ecr_repository

    def __grant_pull_push(self, ecr_repository):
        ecr_repository.add_to_resource_policy(iam.PolicyStatement(
            actions=[
                "ecr:BatchCheckLayerAvailability",
                "ecr:BatchGetImage",
                "ecr:CompleteLayerUpload",
                "ecr:GetDownloadUrlForLayer",
                "ecr:InitiateLayerUpload",
                "ecr:PutImage",
                "ecr:UploadLayerPart"
            ],
            principals=[iam.AccountPrincipal(account_id) for account_id in self.__account_ids]
        ))
