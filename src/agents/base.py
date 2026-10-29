"""Base agent class with shared tooling and memory access."""
from abc import ABC, abstractmethod
from typing import Any
import structlog

logger = structlog.get_logger()


class BaseAgent(ABC):
    def __init__(self, agent_id: str, tools: list, memory_client=None):
        self.agent_id = agent_id
        self.tools = {t.name: t for t in tools}
        self.memory = memory_client
        self.log = logger.bind(agent=agent_id)

    @abstractmethod
    def run(self, state: dict) -> dict: ...

    def call_tool(self, name: str, **kwargs) -> Any:
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not registered for agent '{self.agent_id}'")
        self.log.info("tool_call", tool=name)
        result = self.tools[name].invoke(kwargs)
        self.log.info("tool_result", tool=name, type=type(result).__name__)
        return result

    def recall(self, query: str, k: int = 5) -> list[str]:
        if self.memory is None:
            return []
        return self.memory.similarity_search(query, k=k)

    def remember(self, text: str, metadata: dict | None = None) -> None:
        if self.memory is not None:
            self.memory.add_texts([text], metadatas=[metadata or {}])
