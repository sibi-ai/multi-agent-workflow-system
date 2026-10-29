"""Tests for workflow state and routing logic."""
import pytest
from src.graph.state import WorkflowState


def make_state(**kw) -> WorkflowState:
    base: WorkflowState = {
        "task_id": "t-001", "raw_input": "test",
        "ingested_data": None, "processed_result": None,
        "needs_human_approval": False, "human_approved": None,
        "error": None, "messages": [], "audit_log": [],
    }
    return {**base, **kw}


def test_default_state():
    s = make_state()
    assert s["needs_human_approval"] is False
    assert s["error"] is None


def test_approval_pending():
    s = make_state(needs_human_approval=True)
    assert s["human_approved"] is None


def test_error_propagation():
    s = make_state(error="upstream failure")
    assert s["error"] == "upstream failure"


def test_message_accumulation():
    s = make_state(messages=[{"role": "agent", "content": "done"}])
    assert len(s["messages"]) == 1
