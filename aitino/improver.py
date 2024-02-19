from pathlib import Path
import os
from openai import OpenAI



def improve_prompt(word_limit: int, prompt: str) -> str:
    with open(Path(os.getcwd(), "aitino", "prompts", "improve-prompt.md"), "r", encoding="utf-8") as f:
        system_prompt = f.read()
    system_prompt += f"\n4. Limit the amount of words in the prompt to {word_limit} words"
    
    client = OpenAI()
    result = client.chat.completions.create(
        messages=[
            {
                "role" : "system",
                "content" : system_prompt
            },
            {
                "role" : "user",
                "content" : prompt
            }
        ], 
        model="gpt-4-turbo-preview", 
        temperature=0,
        frequency_penalty=0.1,
        presence_penalty=0.1)
    return result.choices[0].message.content

