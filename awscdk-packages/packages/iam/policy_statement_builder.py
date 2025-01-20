from dataclasses import dataclass
from typing import Optional, Sequence

from aws_cdk import aws_iam as iam


@dataclass
class PolicyStatementBuilder:
    sid: Optional[str]
    principals = None
    actions = None
    effect = None
    resources: Optional[Sequence[str]] = None
    conditions = None

    def build(self) -> iam.PolicyStatement:
        return iam.PolicyStatement(
            sid=self.sid,
            principals=self.principals,
            actions=self.actions,
            effect=self.effect,
            resources=self.resources,
            conditions=self.conditions)
