"""Tests for voice conversation continuation helpers."""

from voice_mode.cli import (
    _extract_voice_response,
    _is_conversation_stop_request,
    _is_no_speech_result,
)


def test_no_speech_is_not_a_stop_request():
    assert _is_no_speech_result("No speech detected")
    assert _is_no_speech_result("No speech detected | Timing: 1.2s")
    assert not _is_conversation_stop_request("No speech detected")


def test_extract_voice_response_ignores_metrics():
    result = "Voice response: Please keep going | Timing: total 1.0s"
    assert _extract_voice_response(result) == "Please keep going"


def test_stop_requests_require_explicit_stop_language():
    assert _is_conversation_stop_request("stop")
    assert _is_conversation_stop_request("end the conversation")
    assert _is_conversation_stop_request("termina la conversacion")
    assert _is_conversation_stop_request("cancelar la conversacion")


def test_general_spanish_request_does_not_stop_conversation():
    text = "Me gustaria que modifiques la logica adecuadamente"
    assert not _is_conversation_stop_request(text)
