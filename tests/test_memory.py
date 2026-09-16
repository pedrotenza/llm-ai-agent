# tests/test_memory.py
"""
Tests for the conversation memory.
"""

import pytest
from src.agent.memory import ConversationMemory


def test_memory_starts_empty():
    """A new memory has no history."""
    mem = ConversationMemory()
    assert len(mem) == 0
    assert mem.get_last_user_message() is None
    assert mem.get_last_agent_response() is None


def test_memory_add_exchange():
    """Adding an exchange stores it."""
    mem = ConversationMemory()
    mem.add_exchange("¿estado de M-102?", "Mantenimiento.")
    assert len(mem) == 1
    assert mem.get_last_user_message() == "¿estado de M-102?"
    assert mem.get_last_agent_response() == "Mantenimiento."


def test_memory_sliding_window():
    """Old exchanges are dropped when max_history is exceeded."""
    mem = ConversationMemory(max_history=3)
    for i in range(5):
        mem.add_exchange(f"Q{i}", f"A{i}")
    assert len(mem) == 3
    # Only the last 3 should remain: Q2, Q3, Q4
    assert mem.history[0]["user"] == "Q2"
    assert mem.history[-1]["user"] == "Q4"


def test_memory_context_for_question():
    """get_context_for_question includes recent exchanges."""
    mem = ConversationMemory()
    mem.add_exchange("¿estado de M-102?", "Mantenimiento.")
    mem.add_exchange("¿y su temperatura?", "42°C.")
    context = mem.get_context_for_question("¿y su nombre?")
    assert "M-102" in context
    assert "42°C" in context
    assert "¿y su nombre?" in context


def test_memory_context_empty():
    """Empty memory returns empty context."""
    mem = ConversationMemory()
    assert mem.get_context_for_question("cualquier cosa") == ""


def test_memory_clear():
    """clear() removes all history."""
    mem = ConversationMemory()
    mem.add_exchange("Q", "A")
    mem.clear()
    assert len(mem) == 0


def test_memory_summary():
    """get_conversation_summary returns formatted history."""
    mem = ConversationMemory()
    mem.add_exchange("Q1", "A1")
    mem.add_exchange("Q2", "A2")
    summary = mem.get_conversation_summary()
    assert "Q1" in summary
    assert "A1" in summary
    assert "Q2" in summary
    assert "A2" in summary