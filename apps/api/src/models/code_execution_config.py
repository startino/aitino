from pydantic import BaseModel, Field


class CodeExecutionConfig(BaseModel):
    """Data model for Code Execution Config for AutoGen"""

    last_n_messages: int = 4
    work_dir: str
    use_docker: bool = True
