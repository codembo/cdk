import unittest

from aws_cdk import Stack, aws_dynamodb as dynamodb

from packages.databases.dynamodb.dynamodb_builder import DynamodbBuilder


class DynamoDBTestCase(unittest.TestCase):

    def test_dynamodb_builder(self):
        stack = Stack()
        dynamodb_builder = DynamodbBuilder("Table1", stack)
        dynamodb_builder.partition_key(dynamodb.Attribute(name="pk", type=dynamodb.AttributeType.STRING))
        dynamodb_builder.table_name("test-table")
        dynamodb_table = dynamodb_builder.build()

        self.assertIsNotNone(dynamodb_table)


if __name__ == '__main__':
    unittest.main()
