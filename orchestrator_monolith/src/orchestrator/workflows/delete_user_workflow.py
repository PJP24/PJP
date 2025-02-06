from __future__ import annotations
import asyncio
import dataclasses
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Dict, List, Optional, Union

from temporalio import workflow


@dataclass
class DSLInput:
    root: Statement
    variables: Dict[str, Any] = dataclasses.field(default_factory=dict)


@dataclass
class ActivityStatement:
    activity: ActivityInvocation


@dataclass
class ActivityInvocation:
    name: str
    arguments: List[str] = dataclasses.field(default_factory=list)
    result: Optional[str] = None


@dataclass
class SequenceStatement:
    sequence: Sequence


@dataclass
class Sequence:
    elements: List[Statement]


Statement = Union[ActivityStatement, SequenceStatement]

@workflow.defn
class DeleteUserWorkflow:
    @workflow.run
    async def run(self, input: DSLInput) -> Dict[str, Any]:
        self.variables = dict(input.variables)
        await self.execute_statement(input.root)
        return self.variables

    async def execute_statement(self, stmt: Statement) -> None:
        if "user_id" in self.variables and self.variables["user_id"].isdigit():
            self.variables["user_id"] = int(self.variables["user_id"])
        if isinstance(stmt, ActivityStatement):
            result = await workflow.execute_activity(
                stmt.activity.name,
                args=[self.variables.get(arg, "") for arg in stmt.activity.arguments],
                start_to_close_timeout=timedelta(minutes=1),
            )
            if stmt.activity.result:
                self.variables[stmt.activity.result] = result
        elif isinstance(stmt, SequenceStatement):

            for elem in stmt.sequence.elements:
                await self.execute_statement(elem)
