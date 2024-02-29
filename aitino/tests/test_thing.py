import pytest

from ..improver import improve_prompt, InvalidPromptTypeError
from unittest.mock import patch

class MockContent:
    content: str

class MockMessage:
    message: MockContent

class MockResponse:
    def __init__(self):
        self.choices: list[MockMessage] = []

class MockCompletions():
    def create(self, messages, model, temperature, frequency_penalty, presence_penalty) -> MockResponse:
        response = MockResponse()
        message = MockMessage()
        content = MockContent()

        content.content = "yes sir"
        message.message = content
        response.choices.append(message)

        return response

class MockFailingCompletions():
    def create(self, messages, model, temperature, frequency_penalty, presence_penalty) -> MockResponse:
        response = MockResponse()
        message = MockMessage()
        content = MockContent()

        content.content = ""
        message.message = content
        response.choices.append(message)

        return response

def test_mock_failing_completions():
    assert not improve_prompt(100, "here's a test prompt", "generic", MockFailingCompletions(), 0.0)

def test_improve_prompt_word_limit():
    with pytest.raises(ValueError) as error: 
        improve_prompt(0, "here's a test prompt", "generic", MockCompletions(), 0.0)

    assert error

def test_improve_prompt_type():
    with pytest.raises(InvalidPromptTypeError) as error:
        improve_prompt(100, "here's a test prompt", "nottype", MockCompletions(), 0.0)
    
    assert error

def test_improve_prompt_temperature():
    with pytest.raises(ValueError):
        improve_prompt(100, "here's a test prompt", "generic", MockCompletions(), -2.1)
    
    with pytest.raises(ValueError):
        improve_prompt(100, "here's a test prompt", "generic", MockCompletions(), 2.1)
    
def test_improve_prompt():
    assert improve_prompt(100, "here's a test prompt", "generic", MockCompletions(), 0.0)
