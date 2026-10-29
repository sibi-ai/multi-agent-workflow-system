"""Shared state schema for the multi-agent LangGraph workflow."""
from typing import Annotated, TypedDict
import operator


class WorkflowState(TypedDict):
    task_id: str
    raw_input: str
    ingested_data: dict | None
    processed_result: dict | None
    needs_human_approval: bool
    human_approved: bool | None
    error: str | None
    messages: Annotated[list[dict], operator.add]
    audit_log: Annotated[list[dict], operator.add]
