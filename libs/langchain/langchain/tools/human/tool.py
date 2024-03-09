from langchain_community.tools.human.tool import HumanInputRun

<<<<<<< Updated upstream
__all__ = ["HumanInputRun"]
=======
from typing import Callable, Optional

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.pydantic_v1 import Field
from langchain.tools.base import BaseTool


def _print_func(text: str) -> None:
    print("\n")
    print(text)


# NOTE: 人反馈的tools类，这个类实现要求人记性输入
class HumanInputRun(BaseTool):
    """Tool that asks user for input."""

    name: str = "human"
    description: str = (
        "You can ask a human for guidance when you think you "
        "got stuck or you are not sure what to do next. "
        "The input should be a question for the human."
    )
    # NOTE: 简单的示例里并没有传入这2个参数，那么这2个参数并没有实现交互的功能
    prompt_func: Callable[[str], None] = Field(default_factory=lambda: _print_func)
    input_func: Callable = Field(default_factory=lambda: input)

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Human input tool."""
        # NOTE: 这里的默认功能就是展示下问题
        self.prompt_func(query)
        # NOTE: 可能是这个玩意实现了输入
        return self.input_func()
>>>>>>> Stashed changes
