import os
from pathlib import Path
from typing import Literal, Protocol

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

PromptType = Literal["generic", "system", "user"]


class InvalidPromptTypeError(BaseException): ...


class ContentProtocol(Protocol):
    content: str


class MessageProtocol(Protocol):
    message: ContentProtocol


class ResponseProtocol(Protocol):
    choices: list[MessageProtocol]


class CompletionsProtocol(Protocol):
    def create(
        self, messages, model, temperature, frequency_penalty, presence_penalty
    ) -> ResponseProtocol: ...


def improve_prompt(
    word_limit: int,
    prompt: str,
    prompt_type: PromptType,
    temperature: float = 0.0,
) -> str:
    """
    Take a prompt and improve it with the use of GPT-4 Turbo preview.

    params:
        word_limit: int, The word limit for the improved prompt the function returns
            (beware that small values will restrain the model from making a good prompt)
        prompt: str, The prompt the function improves
        prompt_type: PromptType, Literal PromptType with types "generic", "system" and "user", decides what type of prompt the function will produce
        temperature: float = 0.0, the "creativity" of the AI model, higher values lead to more randomness in the output
    returns:
        improved_prompt: str
    raises:
        InvalidPromptTypeError: Invalid Prompt Type: prompt_type
        ValueError: Word limit must be greater than 0
        ValueError: Temperature must be in between -2 and 2
    """
    if prompt_type not in ["generic", "system", "user"]:
        raise InvalidPromptTypeError(f"Invalid prompt type: {prompt_type}")

    if word_limit <= 0:
        raise ValueError("Word limit must be greater than 0")

    if temperature < -2.0 or temperature > 2.0:
        raise ValueError("Temperature must be in between -2 and 2")

    with open(
        Path(os.getcwd(), "src", "prompts", "improve", prompt_type + ".md"),
        "r",
        encoding="utf-8",
    ) as f:
        system_prompt = f.read()
        system_prompt += (
            f"\n4. Limit the amount of words in this prompt to {word_limit} words"
        )

    result = client.chat.completions.create(
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
    return content if content else "error"
