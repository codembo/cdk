from dataclasses import dataclass

from aws_cdk import Stack


@dataclass
class Builder:
    construct_id: str
    stack: Stack
