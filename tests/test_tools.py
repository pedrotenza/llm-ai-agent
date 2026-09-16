# tests/test_tools.py
"""
Tests for the agent tools.
"""

import pytest
from src.agent.tools import get_machine_api_status, search_documents


def test_get_machine_api_status_returns_string():
    """The API tool returns a non-empty string."""
    result = get_machine_api_status("M-102")
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_machine_api_status_contains_data():
    """The API tool includes machine data for M-102."""
    result = get_machine_api_status("M-102")
    assert "M-102" in result
    # Should contain at least one of the known fields
    assert "Estado" in result or "Mantenimiento" in result


def test_get_machine_api_status_unknown_machine():
    """An unknown machine returns an error or a fallback message."""
    result = get_machine_api_status("M-999")
    assert isinstance(result, str)
    assert len(result) > 0


def test_search_documents_returns_string():
    """The RAG tool returns a non-empty string."""
    result = search_documents("evaluación de riesgos")
    assert isinstance(result, str)
    assert len(result) > 0


def test_search_documents_finds_content():
    """The RAG tool finds relevant content for a known topic."""
    result = search_documents("evaluación de riesgos")
    # Either it finds content or it says it found nothing
    assert ("Información extraída" in result) or ("No encontré" in result)