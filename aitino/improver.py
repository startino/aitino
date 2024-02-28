import os
from pathlib import Path
from typing import Literal, Protocol

from openai import OpenAI

PromptType = Literal["generic", "system", "user"]

class InvalidPromptTypeError(BaseException):
    ...
class ContentProtocol(Protocol):
    content: str

class MessageProtocol(Protocol):
    message: ContentProtocol

class ResponseProtocol(Protocol):
    choices: list[MessageProtocol]
    
class CompletionsProtocol(Protocol):
    def create(self, messages, model, temperature, frequency_penalty, presence_penalty) -> ResponseProtocol:
        ...

def improve_prompt(
    word_limit: int, prompt: str, prompt_type: PromptType, client: CompletionsProtocol, temperature: float = 0.0
) -> str | None:
    if (word_limit <= 0):
        raise ValueError("Word limit must be greater than 0")

    if (prompt_type not in ["generic", "system", "user"]):
        raise InvalidPromptTypeError(f"Invalid prompt type: {prompt_type}")
    
    if (temperature < -2.0 or temperature > 2.0):
        raise ValueError("Temperature must be in between -2 and 2")

    with open(
        Path(os.getcwd(), "aitino", "prompts", "improve", prompt_type + ".md"),
        "r",
        encoding="utf-8",
    ) as f:
        system_prompt = f.read()
        system_prompt += (
            f"\n4. Limit the amount of words in this prompt to {word_limit} words"
        )

    result = client.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        model="gpt-4-turbo-preview",
        temperature=temperature,
        frequency_penalty=0.1,
        presence_penalty=0.1,
    )

    content = result.choices[0].message.content
    return content if content else None
