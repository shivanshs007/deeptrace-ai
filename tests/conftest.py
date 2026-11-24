import os

# Set test API key before agent modules are imported during collection.
# Tests mock all LLM calls, so this key is never used for real requests.
os.environ.setdefault("GOOGLE_API_KEY", "test-placeholder")

import pytest
from unittest.mock import AsyncMock, MagicMock

from agents.state import AgentState


@pytest.fixture
def sample_agent_state() -> AgentState:
    return AgentState(
        task_id="test-task-123",
        input_task="Compare top 3 cloud providers",
        manager_plan="",
        research_results="",
        analysis_results="",
        final_output="",
        current_agent="",
        agent_statuses={
            "manager": "waiting",
            "research": "waiting",
            "analyst": "waiting",
            "writer": "waiting",
        },
        error=None,
        metadata={},
    )


@pytest.fixture
def mock_llm_response():
    response = MagicMock()
    response.content = "Mock LLM output for testing"
    response.usage_metadata = {"total_tokens": 100}
    return response


@pytest.fixture
def mock_chromadb():
    collection = MagicMock()
    collection.query.return_value = {
        "documents": [[]],
        "metadatas": [[]],
        "distances": [[]],
    }
    collection.upsert.return_value = None

    client = MagicMock()
    client.get_or_create_collection.return_value = collection
    return client
