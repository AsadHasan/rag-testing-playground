#!/usr/bin/env python
import os

import chromadb
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.readers.wikipedia import WikipediaReader
from llama_index.vector_stores.chroma import ChromaVectorStore


def main() -> None:
    reader = WikipediaReader()
    documents = reader.load_data(
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
    Settings.embed_model = HuggingFaceEmbedding(model_name=os.getenv("HF_EMBEDDING_MODEL", "BAAI/bge-large-en-v1.5"))
    Settings.llm = Ollama(model=os.getenv("OLLAMA_LLM_MODEL", "llama3.2"), request_timeout=os.getenv("TIMEOUT", 300))
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="Wiki-pages")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query("What is AI?")
    print(response)


if __name__ == "__main__":
    main()
