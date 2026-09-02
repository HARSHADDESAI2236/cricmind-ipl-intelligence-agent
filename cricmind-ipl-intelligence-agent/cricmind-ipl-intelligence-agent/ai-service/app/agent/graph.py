"""
Agent orchestration using LangGraph.

Flow (mirrors the "Overall Working Flow" in the project plan):
  1. `call_model`  - Claude reads the conversation + tool schemas and decides
                      whether to answer directly or call one or more tools.
  2. `execute_tools` - any requested tools run against the cricket data layer
                      (stats, schedule, standings, RAG, ML prediction).
  3. Loop back to `call_model` with tool results until Claude produces a
     final text answer (no more tool calls requested).

This is a small, explicit state machine rather than a deep chain, which
keeps tool-selection auditable -- every tool call and its result is kept in
`tools_used` / `sources` and returned to the frontend for transparency.
"""
from typing import TypedDict, Annotated, Any
import operator

from langgraph.graph import StateGraph, END
from anthropic import Anthropic

from app.core.config import settings
from app.tools.schemas import TOOL_SCHEMAS
from app.tools.cricket_tools import execute_tool

SYSTEM_PROMPT = """You are CricMind, an expert IPL cricket analyst agent.
You have access to tools that retrieve live statistics, schedules, standings,
head-to-head records, venue data, and a machine-learning match predictor, plus
a knowledge-base search tool for rules/terminology questions.

Guidelines:
- Use tools whenever the answer depends on specific data (stats, standings,
  predictions, historical facts) rather than guessing.
- For "why will X beat Y" style questions, prefer the analyze_match tool,
  which combines form, head-to-head, venue and the ML model in one call.
- Always present ML predictions as probabilistic estimates, not certainties.
- Keep answers concise, cite which data you used, and mention key factors."""


class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    tools_used: Annotated[list, operator.add]
    sources: Annotated[list, operator.add]
    final_answer: str


_client = Anthropic(api_key=settings.anthropic_api_key) if settings.anthropic_api_key else None


def call_model(state: AgentState) -> AgentState:
    if _client is None:
        # No API key configured (e.g. local dev without secrets) -- fail
        # gracefully with a clear message instead of crashing the graph.
        return {
            "messages": [{"role": "assistant", "content": "AI model is not configured (missing ANTHROPIC_API_KEY)."}],
            "tools_used": [],
            "sources": [],
            "final_answer": "AI model is not configured on this server yet. Set ANTHROPIC_API_KEY in ai-service/.env.",
        }

    response = _client.messages.create(
        model=settings.model_name,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=TOOL_SCHEMAS,
        messages=state["messages"],
    )

    new_messages = [{"role": "assistant", "content": response.content}]

    if response.stop_reason == "tool_use":
        return {"messages": new_messages, "tools_used": [], "sources": [], "final_answer": ""}

    text = "".join(block.text for block in response.content if block.type == "text")
    return {"messages": new_messages, "tools_used": [], "sources": [], "final_answer": text}


def execute_tools(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    tool_use_blocks = [b for b in last_message["content"] if getattr(b, "type", None) == "tool_use"]

    tool_result_content = []
    tools_used = []
    sources = []

    for block in tool_use_blocks:
        result = execute_tool(block.name, block.input)
        tools_used.append(block.name)
        sources.append({"tool": block.name, "input": block.input, "result": result})
        tool_result_content.append({
            "type": "tool_result",
            "tool_use_id": block.id,
            "content": str(result),
        })

    return {
        "messages": [{"role": "user", "content": tool_result_content}],
        "tools_used": tools_used,
        "sources": sources,
        "final_answer": "",
    }


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message["role"] == "assistant":
        has_tool_use = any(getattr(b, "type", None) == "tool_use" for b in last_message["content"])
        return "execute_tools" if has_tool_use else END
    return "call_model"


def build_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("call_model", call_model)
    graph.add_node("execute_tools", execute_tools)
    graph.set_entry_point("call_model")
    graph.add_conditional_edges("call_model", should_continue, {"execute_tools": "execute_tools", END: END})
    graph.add_edge("execute_tools", "call_model")
    return graph.compile()


_agent_graph = None


def get_agent_graph():
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = build_agent_graph()
    return _agent_graph


def run_agent(user_message: str) -> dict[str, Any]:
    graph = get_agent_graph()
    initial_state: AgentState = {
        "messages": [{"role": "user", "content": user_message}],
        "tools_used": [],
        "sources": [],
        "final_answer": "",
    }
    result = graph.invoke(initial_state)
    return {
        "answer": result["final_answer"] or "I couldn't produce an answer for that.",
        "tools_used": result["tools_used"],
        "sources": result["sources"],
        "confidence": 0.85 if result["tools_used"] else 0.6,
    }
