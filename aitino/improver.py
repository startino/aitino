import os
from pathlib import Path
from typing import Literal

from openai import OpenAI


PromptType = Literal["generic", "system", "user"]


def improve_prompt(
    word_limit: int, prompt: str, temperature: float, prompt_type: PromptType
) -> str:
    with open(
        Path(os.getcwd(), "aitino", "prompts", "improve", prompt_type + ".md"),
        "r",
        encoding="utf-8",
    ) as f:
        system_prompt = f.read()
        system_prompt += (
            f"\n4. Limit the amount of words in this prompt to {word_limit} words"
        )

    client = OpenAI()
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
