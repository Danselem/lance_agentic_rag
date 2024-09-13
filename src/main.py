import os
import tqdm
import json
import time
from typing import List, Optional, Dict, Any
from tqdm import tqdm
import logging
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings,
    Document,
)

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner
from utils import utils
from utils.retrievers import (retrieve_problems, retrieve_parts,
                              diagnose_car_problem,
                              estimate_repair_cost, get_maintenance_schedule)
from utils.tasks import CarCareCoordinator


os.environ["TOKENIZERS_PARALLELISM"] = "false"

utils._set_env("NVIDIA_API_KEY")
utils._set_env("GROQ_API_KEY")

OPENAI_API_KEY = "****"
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# LLM setup
llm = OpenAI(model="gpt-4", api_key=OPENAI_API_KEY)

# Embedding model setup
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Update the Settings with the new embedding model
Settings.embed_model = embed_model
Settings.chunk_size = 512


car_care = CarCareCoordinator()

## Create function tools
retrieve_problems_tool = FunctionTool.from_defaults(fn=retrieve_problems)
retrieve_parts_tool = FunctionTool.from_defaults(fn=retrieve_parts)
diagnostic_tool = FunctionTool.from_defaults(fn=diagnose_car_problem)
cost_estimator_tool = FunctionTool.from_defaults(fn=estimate_repair_cost)
maintenance_schedule_tool = FunctionTool.from_defaults(fn=get_maintenance_schedule)
comprehensive_diagnostic_tool = FunctionTool.from_defaults(fn=car_care.comprehensive_diagnosis)
maintenance_planner_tool = FunctionTool.from_defaults(fn=car_care.plan_maintenance)
calendar_invite_tool = FunctionTool.from_defaults(fn=car_care.create_calendar_invite)
car_care_coordinator_tool = FunctionTool.from_defaults(fn=car_care.coordinate_car_care)
retrieve_car_details_tool = FunctionTool.from_defaults(fn=car_care.retrieve_car_details)

tools = [
    retrieve_problems_tool,
    retrieve_parts_tool,
    diagnostic_tool,
    cost_estimator_tool,
    maintenance_schedule_tool,
    comprehensive_diagnostic_tool,
    maintenance_planner_tool,
    calendar_invite_tool,
    car_care_coordinator_tool,
    retrieve_car_details_tool
]


# Function to reset the agent's memory
def reset_agent_memory():
    global agent_worker, agent
    agent_worker = FunctionCallingAgentWorker.from_tools(
        tools,
        llm=llm,
        verbose=True
    )
    agent = AgentRunner(agent_worker)

# Initialize the agent
reset_agent_memory()

response = agent.chat(
    "My car has 60,000 miles on it. What maintenance should I be doing now, and how much will it cost?"
)

print(f"LLM Response : {response}")