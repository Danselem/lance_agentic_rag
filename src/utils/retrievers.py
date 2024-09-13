from pathlib import Path
from vectors import VectorStoreManager
import utils

# Usage
vector_store_manager = VectorStoreManager(uri='./lancedb')

# Create vector stores
problems_vector_store = vector_store_manager.create_vector_store('problems_table')
parts_vector_store = vector_store_manager.create_vector_store('parts_table')
diagnostics_vector_store = vector_store_manager.create_vector_store('diagnostics_table')
cost_estimates_vector_store = vector_store_manager.create_vector_store('cost_estimates_table')
maintenance_schedules_vector_store = vector_store_manager.create_vector_store('maintenance_schedules_table')
cars_vector_store = vector_store_manager.create_vector_store('car_maintenance_table')

json_file_path = Path("../../json_files")
# Load and index documents directly from file paths
problems_index = utils.load_and_index_document_from_file(json_file_path/"problems.json", problems_vector_store)
parts_index = utils.load_and_index_document_from_file(json_file_path/"parts.json", parts_vector_store)
cars_index = utils.load_and_index_document_from_file(json_file_path/"cars_models.json", cars_vector_store)
diagnostics_index = utils.load_and_index_document_from_file(json_file_path/"diagnostics.json", diagnostics_vector_store)
cost_estimates_index = utils.load_and_index_document_from_file(json_file_path/"cost_estimates.json", cost_estimates_vector_store)
maintenance_schedules_index = utils.load_and_index_document_from_file(json_file_path/"maintenance.json", maintenance_schedules_vector_store)

# Create retrievers
problems_retriever = utils.create_retriever(problems_index)
parts_retriever = utils.create_retriever(parts_index)
cars_retriever = utils.create_retriever(cars_index)
diagnostics_retriever = utils.create_retriever(diagnostics_index)
cost_estimates_retriever = utils.create_retriever(cost_estimates_index)
maintenance_schedules_retriever = utils.create_retriever(maintenance_schedules_index)


def retrieve_problems(query: str) -> str:
    """Searches the problem catalog to find relevant automotive problems for the query."""
    docs = problems_retriever.retrieve(query)
    information = str([doc.text[:200]for doc in docs])
    return information

def retrieve_parts(query: str) -> str:
    """Searches the parts catalog to find relevant parts for the query."""
    docs = parts_retriever.retrieve(query)
    information = str([doc.text[:200]for doc in docs])
    return information

# def retrieve_car_details(make: str, model: str, year: int) -> str:
#     """Retrieves the make, model, and year of the car."""
#     docs = cars_retriever.retrieve(make, model, year)
#     information = str([doc.text[:200]for doc in docs])
#     return information

def diagnose_car_problem(symptoms: str) -> str:
    """Uses the diagnostics database to find potential causes for given symptoms."""
    docs = diagnostics_retriever.retrieve(symptoms)
    information = str([doc.text[:200]for doc in docs])
    return information

def estimate_repair_cost(problem: str) -> str:
    """Provides a cost estimate for a given car problem or repair."""
    docs = cost_estimates_retriever.retrieve(problem)
    information = str([doc.text[:200]for doc in docs])
    return information

def get_maintenance_schedule(mileage: int) -> str:
    """Retrieves the recommended maintenance schedule based on mileage."""
    docs = maintenance_schedules_retriever.retrieve(str(mileage))
    information = str([doc.text[:200]for doc in docs])
    return information
