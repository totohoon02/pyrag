import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import uuid

from service.inf.vectorDBService import VectorDBService


class ElasticVectorDBService(VectorDBService):
	def __init__(self):
		load_dotenv()
		self.es = Elasticsearch(
			os.getenv("ES_URL"),
			basic_auth=(os.getenv("ES_USERNAME"), os.getenv("ES_PASSWORD")),
		)
		self.index_name = os.getenv("ES_INDEX_NAME")

	def create_index(self):
		if self.es.indices.exists(index=self.index_name):
			self.es.indices.delete(index=self.index_name)

		index_mapping = {
			"mappings": {
				"properties": {
					"text": {"type": "text"},
					"embedding": {
						# 벡터 데이터 베이스 타입의 인덱스
						"type": "dense_vector",
						# 임베딩 모델의 출력 차원
						"dims": 1024,
						# 검색 가능하도록 설정
						"index": True,
						# 코사인 유사도 기반 검색
						"similarity": "cosine",
					},
				}
			}
		}

		if not self.es.indices.exists(index=self.index_name):
			res = self.es.indices.create(index=self.index_name, body=index_mapping)
			return res
		else:
			raise RuntimeError("Index alread exist")

	def add_document(self, prompt, embedding):
		self.__index_exist_check()
		document = {"text": prompt, "embedding": embedding}

		res = self.es.index(
			index=self.index_name, id=str(uuid.uuid4()), document=document
		)
		return {"id": res["_id"], "result": res["result"]}

	def read_document(self, id: str):
		self.__index_exist_check()
		return self.es.get(index=self.index_name, id=id)

	def search_document(self, embedding):
		self.__index_exist_check()
		search_body = {
			"query": {
				"script_score": {
					"query": {"match_all": {}},
					"script": {
						"source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
						"params": {"query_vector": embedding},
					},
				}
			}
		}
		res = self.es.search(index=self.index_name, body=search_body)
		return res["hits"]["hits"]

	def delete_document(self, id: str):
		self.__index_exist_check()
		res = self.es.delete(index=self.index_name, id=id)
		return res["result"]

	def __index_exist_check(self):
		if not self.es.indices.exists(index=self.index_name):
			raise RuntimeError("Index not Exist")
