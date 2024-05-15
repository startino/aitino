from pydantic import BaseModel


class RagOptions(BaseModel):
    use_rag: bool
    task: str | None = None
    docs_path: str | list[str] | None = None
