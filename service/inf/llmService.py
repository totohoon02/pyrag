from abc import ABC, abstractmethod


class LLMService(ABC):
	@abstractmethod
	def embedding(self, prompt: str):
		pass

	@abstractmethod
	def chat(self, content: str):
		pass
