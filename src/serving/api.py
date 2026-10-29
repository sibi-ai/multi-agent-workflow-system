"""FastAPI service exposing the multi-agent workflow as async endpoints."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graph.workflow import build_workflow
import structlog, uuid

app = FastAPI(title="Multi-Agent Workflow API")
log = structlog.get_logger()
_workflows: dict = {}


class TaskRequest(BaseModel):
    raw_input: str
    require_approval: bool = False


class ApprovalRequest(BaseModel):
    approved: bool


@app.post("/tasks")
async def submit_task(req: TaskRequest):
    task_id = str(uuid.uuid4())
    wf = build_workflow({})
    _workflows[task_id] = wf
    state = {
        "task_id": task_id, "raw_input": req.raw_input,
        "needs_human_approval": req.require_approval,
        "human_approved": None, "ingested_data": None,
        "processed_result": None, "error": None,
        "messages": [], "audit_log": [],
    }
    result = wf.invoke(state, {"configurable": {"thread_id": task_id}})
    status = "pending_approval" if result.get("needs_human_approval") else "complete"
    log.info("task_created", task_id=task_id, status=status)
    return {"task_id": task_id, "status": status}


@app.post("/tasks/{task_id}/approve")
async def approve_task(task_id: str, req: ApprovalRequest):
    if task_id not in _workflows:
        raise HTTPException(404, "Task not found")
    wf = _workflows[task_id]
    wf.invoke({"human_approved": req.approved}, {"configurable": {"thread_id": task_id}})
    return {"task_id": task_id, "approved": req.approved}
