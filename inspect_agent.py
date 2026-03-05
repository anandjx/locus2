import sys
from pydantic import BaseModel

try:
    from google.adk.agents.llm_agent import Agent
    with open('agent_keys.txt', 'w') as f:
        f.write(str(list(Agent.model_fields.keys())))
except Exception as e:
    with open('agent_keys.txt', 'w') as f:
        f.write(f"Error: {e}")
