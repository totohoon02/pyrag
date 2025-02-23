import pytest
from service.ollamaLLMService import OllamaLLMService
from service.elasticVectorDBService import ElasticVectorDBService
from elasticsearch.exceptions import NotFoundError


@pytest.fixture
def vectorDBService():
	return ElasticVectorDBService()


@pytest.fixture
def llmService():
	return OllamaLLMService()


@pytest.fixture(scope="class")
def cached_result():
	return {"embedding": None}


class Test_EsService:
	def test_인덱스_생성(self, vectorDBService):
		assert vectorDBService.create_index() != "created"

	def test_문서_추가(self, vectorDBService, llmService, cached_result):
		result = self.add_document(vectorDBService, llmService, cached_result)

		assert isinstance(result, dict)
		assert result["id"] is not None

	def test_문서_읽기(self, vectorDBService, llmService, cached_result):
		result = self.add_document(vectorDBService, llmService, cached_result)
		id = result["id"]

		readed = vectorDBService.read_doucument(id)
		assert readed is not None
		assert readed["_source"]["text"] == "hello"

	def test_문서_검색(self, vectorDBService, llmService, cached_result):
		self.add_document(vectorDBService, llmService, cached_result)

		prompt = "hello2"
		embedding = llmService.embedding(prompt)
		result = vectorDBService.search_document(embedding)
		assert result is not None

	def test_문서_삭제(self, vectorDBService, llmService, cached_result):
		result = self.add_document(vectorDBService, llmService, cached_result)
		id = result["id"]
		vectorDBService.delete_document(id)

		with pytest.raises(NotFoundError):
			vectorDBService.read_doucument(id)

	# helper function
	def add_document(self, vectorDBService, llmService, cached_result):
		prompt = "hello"

		if cached_result["embedding"] is not None:
			embedding = llmService.embedding(prompt)
			cached_result["embedding"] = embedding
		result = vectorDBService.add_document(prompt, cached_result["embedding"])

		return result
