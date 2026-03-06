import os
import sys
import json
from dotenv import load_dotenv

# Add app to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

from app.tools.places_search import search_places

class DummyToolContext:
    def __init__(self):
        self.state = {}

ctx = DummyToolContext()
res = search_places("versova mumbai", "gym", radius_meters=1000, tool_context=ctx)

print(json.dumps(res, indent=2))
