# Agent
initializer 完成agent的初始化，返回的是一个封装了带有与tools相关的prompt的LLM和tools的AgentExecutor类
## 执行Agent
调用该agent的时候先调用了chains.base.Chain \_\_call\_\_ -> invoke -> agents.agent.AgentExecutor _call -> agents.agent Agent plan
