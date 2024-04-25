from pydantic import BaseModel

class RagOptions(BaseModel):
    use_rag: bool
    task: str
    docs_path: dict[str, list[str]] | None = None