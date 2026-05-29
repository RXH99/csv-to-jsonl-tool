from langchain_community.llms import Ollama

# 连接到本地 Ollama 服务，使用 qwen:4b 模型
llm = Ollama(model="qwen:4b")

# 向模型提问
question = "解释一下 Git 的三个工作区（工作目录、暂存区、仓库）是什么关系？"
print(f"问题: {question}\n")

response = llm.invoke(question)
print(f"回答: {response}")