# AI-Agent
![image](https://github.com/user-attachments/assets/fea95636-bb61-4a61-a656-71f58f648bd7)

### RAG application with

- Python, FastAPI
- Ollama
- Elasticsearch 8.17.1

### Persue best-practice of FastAPI, Use

- injector / MVC Pattern
- pytest
- ruff

### Ollama Models

- Embedding
  - jeffh/intfloat-multilingual-e5-large-instruct:f16
- Chat
  - gemma2:2b
- for KR language.

### Setup

```bash
pip install -r requirements.txt

ollama pull ~ # better run with GPU

docker run --name es8 -d -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.17.1
```

```bash
# .env
EMBEDDING_MODEL="jeffh/intfloat-multilingual-e5-large-instruct:f16"
CHAT_MODEL="gemma2:2b"
ES_URL="http://localhost:9200"
ES_USERNAME="elastic"
ES_PASSWORD="changeme"
ES_INDEX_NAME="vector1"
```
