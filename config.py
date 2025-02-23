from injector import Injector, Module, singleton, provider

# inf
from service.inf.vectorDBService import VectorDBService
from service.inf.llmService import LLMService

# static
from service.ollamaLLMService import OllamaLLMService
from service.elasticVectorDBService import ElasticVectorDBService


class ServiceModule(Module):
	@singleton
	@provider
	def llmService(self) -> LLMService:
		return OllamaLLMService()

	@singleton
	@provider
	def vectorDBService(self) -> VectorDBService:
		return ElasticVectorDBService()


injector = Injector([ServiceModule()])
