from pathlib import Path
import os
from openai import OpenAI



def improve_prompt(prompt: str) -> str:
    with open(Path(os.getcwd(), "aitino", "prompts", "improve-prompt.md"), "r", encoding="utf-8") as f:
        system_prompt = f.read()
    
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
        temperature=0)
    return result.choices[0].message.content

