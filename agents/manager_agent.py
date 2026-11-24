import os
import time
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI

from agents.state import AgentState

SYSTEM_PROMPT = """You are a Manager Agent responsible for decomposing complex research tasks.

Given a research task, break it down into exactly 3-4 focused sub-questions that, when answered together,
will provide comprehensive coverage of the topic.

Format your response as:
RESEARCH PLAN:
1. [First sub-question]
2. [Second sub-question]
3. [Third sub-question]
4. [Optional fourth sub-question]

APPROACH: [Brief strategy for how to research this topic]

Be specific and ensure each sub-question covers a distinct aspect of the topic."""

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
    convert_system_message_to_human=True,
)


async def manager_node(state: AgentState) -> dict[str, Any]:
    """Decompose the task into a structured research plan."""
    start_time = time.time()

    statuses = dict(state.get("agent_statuses", {}))
    statuses["manager"] = "running"
    metadata = dict(state.get("metadata", {}))

    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Research task: {state['input_task']}"},
        ]

        response = await llm.ainvoke(messages)
        plan = response.content

        tokens = response.usage_metadata or {}
        metadata["manager_tokens"] = tokens.get("total_tokens", 0)
        metadata["manager_duration_ms"] = int((time.time() - start_time) * 1000)
        metadata.setdefault("total_tokens", 0)
        metadata["total_tokens"] += metadata["manager_tokens"]

        statuses["manager"] = "done"

        return {
            "manager_plan": plan,
            "current_agent": "manager",
            "agent_statuses": statuses,
            "metadata": metadata,
            "error": None,
        }

    except Exception as e:
        statuses["manager"] = "error"
        return {
            "current_agent": "manager",
            "agent_statuses": statuses,
            "metadata": metadata,
            "error": str(e),
        }
