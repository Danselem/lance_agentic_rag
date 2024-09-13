from llama_index.vector_stores.lancedb import LanceDBVectorStore

class VectorStoreManager:
    def __init__(self, uri: str, mode: str = "overwrite"):
        """
        Initializes the VectorStoreManager with the base URI and mode for vector stores.
        
        :param uri: Base URI for the LanceDB vector stores.
        :param mode: Mode to open the vector store. Default is 'overwrite'.
        """
        self.uri = uri
        self.mode = mode

    def create_vector_store(self, table_name: str):
        """
        Creates a LanceDBVectorStore instance for a given table.
        
        :param table_name: The name of the table for the vector store.
        :return: LanceDBVectorStore instance.
        """
        return LanceDBVectorStore(
            uri=self.uri,
            table_name=table_name,
            mode=self.mode,
        )

# Usage
vector_store_manager = VectorStoreManager(uri='./lancedb')

# Create vector stores
problems_vector_store = vector_store_manager.create_vector_store('problems_table')
parts_vector_store = vector_store_manager.create_vector_store('parts_table')
diagnostics_vector_store = vector_store_manager.create_vector_store('diagnostics_table')
cost_estimates_vector_store = vector_store_manager.create_vector_store('cost_estimates_table')
maintenance_schedules_vector_store = vector_store_manager.create_vector_store('maintenance_schedules_table')
cars_vector_store = vector_store_manager.create_vector_store('car_maintenance_table')