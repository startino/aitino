from pydantic import BaseModel


class CodeExecutionConfig(BaseModel):
    """Data model for Code Execution Config for AutoGen"""

    last_n_messages: int = 6
    work_dir: str
    use_docker: bool = True
