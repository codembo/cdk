from aws_cdk import aws_sns as sns, aws_sns_subscriptions as subs, Stack

from packages.builder import Builder


class SnsBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__display_name = None
        self.__fifo = None
        self.__sqs_subscription = None

    def display_name(self, display_name):
        self.__display_name = display_name
        return self

    def fifo(self, fifo):
        self.__fifo = fifo
        return self

    def sqs_subscription(self, queue):
        self.__sqs_subscription = subs.SqsSubscription(queue)

    def build(self) -> sns.Topic:
        topic = sns.Topic(self.stack, self.construct_id,
                          display_name=self.__display_name,
                          fifo=self.__fifo)
        # Add SQS subscription if not none
        if self.__sqs_subscription:
            topic.add_subscription(self.__sqs_subscription)
        return topic
