import os
from typing import List, Optional, Dict, Any
import logging
from llama_index.core import Settings

from llama_index.llms.groq import Groq
from llama_index.embeddings.nvidia import NVIDIAEmbedding
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


# LLM setup
llm = Groq(model="llama3-70b-8192",))

# Embedding model setup

embedder = NVIDIAEmbedding(model="NV-Embed-QA")

# Update the Settings with the new embedding model
Settings.embed_model = embedder
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