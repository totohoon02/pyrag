from abc import ABC, abstractmethod


class VectorDBService(ABC):
	@abstractmethod
	def create_index(self):
		pass

	@abstractmethod
	def add_document(self, prompt, embedding):
		pass

	@abstractmethod
	def read_document(self, id: str):
		pass

	@abstractmethod
	def search_document(self, embedding: str):
		pass

	@abstractmethod
	def delete_document(self, id: str):
		pass
