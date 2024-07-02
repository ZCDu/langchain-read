from typing import List, Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field


# NOTE: 在LCEL语法中需要使用ChatMessageHistory来封装历史消息
# 追加了一个aget_messages方法，重写了add_message等方法
# 他和Memory的父类是一致的
# HACK: 我们完全可以重写这个类，实现更丰富的功能
class ChatMessageHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history.

    Stores messages in an in memory list.
    """

    messages: List[BaseMessage] = Field(default_factory=list)

    async def aget_messages(self) -> List[BaseMessage]:
        return self.messages

    def add_message(self, message: BaseMessage) -> None:
        """Add a self-created message to the store"""
        self.messages.append(message)

    async def aadd_messages(self, messages: Sequence[BaseMessage]) -> None:
        """Add messages to the store"""
        self.add_messages(messages)

    def clear(self) -> None:
        self.messages = []

    async def aclear(self) -> None:
        self.clear()
# NOTE: 新版的ChatMessageHistory位置发生了变化
from langchain_core.chat_history import InMemoryChatMessageHistory as ChatMessageHistory

__all__ = [
    "ChatMessageHistory",
]
