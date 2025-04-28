#!/usr/bin/env python
import os

import chromadb
from chromadb import Documents
from llama_index.core import Response, Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.vector_stores.chroma import ChromaVectorStore


def get_documents() -> list[Documents]:
    reader = WikipediaReader()
    return reader.load_data(
        pages=[
            "Artificial intelligence",
            "Deep learning",
            "Data science",
            "Statistics",
            "ML",
            "Artificial neural network",
            "RAG",
        ],
    )


def get_chroma_documents_index(documents: list[Documents]) -> VectorStoreIndex:
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="Wiki-pages")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_documents(documents, storage_context=storage_context)


def get_query_response(index: VectorStoreIndex, query: str) -> Response:
    query_engine = index.as_query_engine()
    return query_engine.query(query)


def main() -> None:
    documents = get_documents()
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=os.getenv("HF_EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5")
    )
    Settings.llm = Ollama(
        model=os.getenv("OLLAMA_LLM_MODEL", "llama3.2"),
        request_timeout=float(os.getenv("TIMEOUT", "300")),
        base_url=os.getenv("OLLAMA_URL", "http://ollama:11434"),
    )
    index = get_chroma_documents_index(documents)
    response = get_query_response(index, "What is AI?")
    print(response)


if __name__ == "__main__":
    main()
