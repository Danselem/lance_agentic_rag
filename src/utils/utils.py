import os
import json

from pathlib import Path
from dotenv import load_dotenv
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, StorageContext, Document


def _set_env(var: str):
    if not os.environ.get(var):
        dotenv_path = Path('../.env')
        load_dotenv(dotenv_path=dotenv_path)
        # os.environ[var] = getpass.getpass(f"{var}: ")
        os.environ[var] = os.getenv(f"{var}: ")


def load_and_index_document_from_file(file_path: str, vector_store: LanceDBVectorStore) -> VectorStoreIndex:
    """Load a document from a single file and index it."""
    with open(file_path, 'r') as f:
        data = json.load(f)
        document = Document(text=json.dumps(data))

    parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
    nodes = parser.get_nodes_from_documents([document])
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex(nodes, storage_context=storage_context)

def create_retriever(index: VectorStoreIndex) -> VectorIndexRetriever:
    """Create a retriever from the index."""
    return index.as_retriever(similarity_top_k=5)

