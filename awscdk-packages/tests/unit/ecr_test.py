import unittest

from aws_cdk import Stack

from packages.ecr.ecr_builder import EcrBuilder


class EcrTestCase(unittest.TestCase):

    def test_ecr_builder(self):
        stack = Stack()
        ecr_builder = EcrBuilder("EcrExample", stack)
        ecr_builder.repository_name("ecr-example")
        ecr_builder.grant_cross_account_access(["240761904883, 240761904882, 240761904881"])

        ecr_repository = ecr_builder.build()

        self.assertIsNotNone(ecr_repository)


if __name__ == '__main__':
    unittest.main()
