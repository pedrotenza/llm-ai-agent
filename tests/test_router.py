# tests/test_router.py
"""
Tests for the semantic router logic.
These tests use the internal functions directly.
"""

import pytest
from src.agent.agent import (
    _semantic_decisions,
    extract_machine_id,
    _MANUAL_KEYWORDS,
)


def test_extract_machine_id_found():
    """extract_machine_id finds M-102 in a question."""
    assert extract_machine_id("¿estado de M-102?") == "M-102"
    assert extract_machine_id("what about m-101") == "M-101"


def test_extract_machine_id_not_found():
    """extract_machine_id returns None when no machine ID is present."""
    assert extract_machine_id("¿cuánto es 2+2?") is None
    assert extract_machine_id("¿qué dice el manual?") is None


def test_router_api():
    """A machine question selects API."""
    decisions = _semantic_decisions("¿Cuál es el estado de M-102?")
    assert "API" in decisions


def test_router_rag():
    """A manual question selects RAG."""
    decisions = _semantic_decisions("¿Qué dice el manual sobre evaluación de riesgos?")
    assert "RAG" in decisions


def test_router_none():
    """A trivial question selects NONE."""
    decisions = _semantic_decisions("¿Cuánto es 2+2?")
    assert "NONE" in decisions


def test_manual_keywords_present():
    """_MANUAL_KEYWORDS contains essential keywords."""
    assert "manual" in _MANUAL_KEYWORDS
    assert "handbuch" in _MANUAL_KEYWORDS
    assert "procedure" in _MANUAL_KEYWORDS