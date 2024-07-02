from typing import Any, Dict, List, Optional

from langchain_core.messages import BaseMessage, get_buffer_string
from langchain_core.pydantic_v1 import root_validator

from langchain.memory.chat_memory import BaseChatMemory, BaseMemory
from langchain.memory.utils import get_prompt_input_key


# NOTE: 可以发现，常用的对话记忆池的父类(他的父类才是BaseMemory)和langchian官网自定义Memoyr时候使用的父类不是一个
class ConversationBufferMemory(BaseChatMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    # NOTE: 不同的memory其实是通过这个memory_key进行区分的
    memory_key: str = "history"  #: :meta private:

    @property
    def buffer(self) -> Any:
        """String buffer of memory."""
        return self.buffer_as_messages if self.return_messages else self.buffer_as_str

    async def abuffer(self) -> Any:
        """String buffer of memory."""
        return (
            await self.abuffer_as_messages()
            if self.return_messages
            else await self.abuffer_as_str()
        )

    def _buffer_as_str(self, messages: List[BaseMessage]) -> str:
        return get_buffer_string(
            messages,
            human_prefix=self.human_prefix,
            ai_prefix=self.ai_prefix,
        )

    @property
    def buffer_as_str(self) -> str:
        """Exposes the buffer as a string in case return_messages is True."""
        return self._buffer_as_str(self.chat_memory.messages)

    async def abuffer_as_str(self) -> str:
        """Exposes the buffer as a string in case return_messages is True."""
        messages = await self.chat_memory.aget_messages()
        return self._buffer_as_str(messages)

    @property
    def buffer_as_messages(self) -> List[BaseMessage]:
        """Exposes the buffer as a list of messages in case return_messages is False."""
        return self.chat_memory.messages

    async def abuffer_as_messages(self) -> List[BaseMessage]:
        """Exposes the buffer as a list of messages in case return_messages is False."""
        return await self.chat_memory.aget_messages()

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.

        :meta private:
        """
        return [self.memory_key]

    # NOTE: 返回的是一个字典，对应memory_key: buffer的内容
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Return history buffer."""
        return {self.memory_key: self.buffer}

    async def aload_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Return key-value pairs given the text input to the chain."""
        buffer = await self.abuffer()
        return {self.memory_key: buffer}


class ConversationStringBufferMemory(BaseMemory):
    """Buffer for storing conversation memory."""

    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    """Prefix to use for AI generated responses."""
    buffer: str = ""
    output_key: Optional[str] = None
    input_key: Optional[str] = None
    memory_key: str = "history"  #: :meta private:

    @root_validator()
    def validate_chains(cls, values: Dict) -> Dict:
        """Validate that return messages is not True."""
        if values.get("return_messages", False):
            raise ValueError(
                "return_messages must be False for ConversationStringBufferMemory"
            )
        return values

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables.
        :meta private:
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Return history buffer."""
        return {self.memory_key: self.buffer}

    async def aload_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Return history buffer."""
        return self.load_memory_variables(inputs)

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save context from this conversation to buffer."""
        if self.input_key is None:
            prompt_input_key = get_prompt_input_key(inputs, self.memory_variables)
        else:
            prompt_input_key = self.input_key
        if self.output_key is None:
            if len(outputs) != 1:
                raise ValueError(f"One output key expected, got {outputs.keys()}")
            output_key = list(outputs.keys())[0]
        else:
            output_key = self.output_key
        human = f"{self.human_prefix}: " + inputs[prompt_input_key]
        ai = f"{self.ai_prefix}: " + outputs[output_key]
        self.buffer += "\n" + "\n".join([human, ai])

    async def asave_context(
        self, inputs: Dict[str, Any], outputs: Dict[str, str]
    ) -> None:
        """Save context from this conversation to buffer."""
        return self.save_context(inputs, outputs)

    def clear(self) -> None:
        """Clear memory contents."""
        self.buffer = ""

    async def aclear(self) -> None:
        self.clear()
