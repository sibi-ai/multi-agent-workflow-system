"""LangGraph workflow — agent routing and human-in-the-loop."""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.graph.state import WorkflowState


def route_after_processing(state: WorkflowState) -> str:
    if state.get("error"):
        return "error"
    return "human_review" if state.get("needs_human_approval") else "reporting"


def route_after_review(state: WorkflowState) -> str:
    return "reporting" if state.get("human_approved") else "rejected"


def build_workflow(agents: dict, checkpointer=None):
    graph = StateGraph(WorkflowState)

    graph.add_node("ingestion",   agents.get("ingestion",  lambda s: s))
    graph.add_node("processing",  agents.get("processing", lambda s: s))
    graph.add_node("reporting",   agents.get("reporting",  lambda s: s))
    graph.add_node("human_review", lambda s: s)
    graph.add_node("rejected",    lambda s: {**s, "error": "Rejected by reviewer"})
    graph.add_node("error",       lambda s: s)

    graph.set_entry_point("ingestion")
    graph.add_edge("ingestion", "processing")
    graph.add_conditional_edges("processing", route_after_processing,
        {"human_review": "human_review", "reporting": "reporting", "error": "error"})
    graph.add_conditional_edges("human_review", route_after_review,
        {"reporting": "reporting", "rejected": "rejected"})
    graph.add_edge("reporting", END)
    graph.add_edge("rejected",  END)
    graph.add_edge("error",     END)

    return graph.compile(
        checkpointer=checkpointer or MemorySaver(),
        interrupt_before=["human_review"],
    )
