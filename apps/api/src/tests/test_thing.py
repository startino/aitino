from unittest.mock import patch

import pytest

from ..improver import InvalidPromptTypeError, improve_prompt


class MockContent:
    content: str


class MockMessage:
    message: MockContent


class MockResponse:
    def __init__(self):
        self.choices: list[MockMessage] = []


class MockCompletions:
    def create(
        self, messages, model, temperature, frequency_penalty, presence_penalty
    ) -> MockResponse:
        response = MockResponse()
        message = MockMessage()
        content = MockContent()

        content.content = "yes sir"
        message.message = content
        response.choices.append(message)

        return response


class MockFailingCompletions:
    def create(
        self, messages, model, temperature, frequency_penalty, presence_penalty
    ) -> MockResponse:
        response = MockResponse()
        message = MockMessage()
        content = MockContent()

        content.content = ""
        message.message = content
        response.choices.append(message)

        return response
