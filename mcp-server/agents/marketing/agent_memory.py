"""
Shared per-run memory for the marketing multi-agent workflow.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional


class AgentMemory:
    """
    Lightweight in-memory store scoped to one orchestration run.

    The orchestrator creates a fresh instance for every plan generation so
    research, strategy drafts, reviews, and trace entries never leak between
    requests.
    """

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}
        self._trace: List[Dict[str, Any]] = []

    def write(self, key: str, value: Any, agent: Optional[str] = None) -> None:
        """Store a value and optionally trace which agent produced it."""
        self._data[key] = value
        if agent:
            self.add_trace(agent, f"Wrote shared memory key '{key}'", {"memory_key": key})

    def read(self, key: str, default: Any = None) -> Any:
        """Read a value from shared memory."""
        return self._data.get(key, default)

    def add_trace(self, agent: str, action: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Append a timestamped trace entry."""
        self._trace.append(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "agent": agent,
                "action": action,
                "details": details or {},
            }
        )

    def snapshot(self) -> Dict[str, Any]:
        """Return a shallow copy of stored data for debugging or inspection."""
        return dict(self._data)

    @property
    def trace(self) -> List[Dict[str, Any]]:
        """Return a copy of the trace log."""
        return list(self._trace)
