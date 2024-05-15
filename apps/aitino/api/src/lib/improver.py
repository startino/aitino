import os
import logging

from pathlib import Path
from typing import Literal, Protocol
from uuid import UUID

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI
from src.interfaces import db

load_dotenv()
client = OpenAI()


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


ACCURACY = os.environ.get("MONETARY_DECIMAL_ACCURACY")
if not ACCURACY:
    raise ValueError("MONETARY_DECIMAL_ACCURACY environment variable not set")


def improve_prompt(
    prompt: str,
    word_limit: int,
    prompt_type: Literal["generic", "system", "user"],
    profile_id: UUID,
    temperature: float = 0.0,
) -> str:
    """
    Take a prompt and improve it with the use of GPT-4 Turbo.

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
    profile = db.get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if profile.funding <= 0:
        raise HTTPException(status_code=402, detail="Insufficient funds")

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
        model="gpt-4-turbo",
        temperature=temperature,
        frequency_penalty=0.1,
        presence_penalty=0.1,
    )
    logging.info(result)
    if not result.usage:
        raise HTTPException(
            status_code=500, detail='Result from OpenAI had no "usage" attribute'
        )

    input_cost = int(result.usage.prompt_tokens * 0.00001 * int(ACCURACY))
    output_cost = int(result.usage.completion_tokens * 0.00003 * int(ACCURACY))
    total_cost = input_cost + output_cost
    logging.info(
        f"Input cost: {input_cost}, Output cost: {output_cost}, total cost: {total_cost}"
    )

    # could consider adding margin to this
    # should also consider passing the profile id and funding
    # instead of making a db call to get the profile
    db.update_funding(profile_id, profile.funding - total_cost)

    content = result.choices[0].message.content
    return content if content else "error"
