import ollama
from service.inf.llmService import LLMService
import os
from dotenv import load_dotenv


class OllamaLLMService(LLMService):
	def __init__(self):
		load_dotenv()

	def embedding(self, prompt):
		return ollama.embeddings(
			model=os.getenv("EMBEDDING_MODEL"),
			prompt=prompt,
		)["embedding"]

	def chat(self, content):
		response = ollama.generate(
			model=os.getenv("CHAT_MODEL"),
			prompt=f"""
				질문에 답변

				## 질문
				{content}
			"""
		)
		return response["response"]
