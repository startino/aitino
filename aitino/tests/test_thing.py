import pytest

from ..improver import improve_prompt

def test_improve_prompt():
    assert improve_prompt(100, "here's a test prompt haha", "generic", 0.0)  != "error"
