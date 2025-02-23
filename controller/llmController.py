from fastapi import APIRouter
from config import injector
from service.inf.vectorDBService import VectorDBService
from service.inf.llmService import LLMService

router = APIRouter(prefix="/llm", tags=["LLM"])

llmService = injector.get(LLMService)
esService = injector.get(VectorDBService)


@router.post("/index")
def index():
	return esService.create_index()


@router.post("/add")
def embedding(prompt: str):
	embedding = llmService.embedding(prompt)
	return esService.add_document(prompt, embedding)


@router.get("/read")
def read(id: str):
	return esService.read_document(id)


@router.get("/search")
def search(prompt: str):
	embedding = llmService.embedding(prompt)
	return esService.search_document(embedding)


@router.delete("/delete")
def delete(id: str):
	return esService.delete_document(id)


@router.get("/chat")
def chat(content: str):
	return llmService.chat(content)
