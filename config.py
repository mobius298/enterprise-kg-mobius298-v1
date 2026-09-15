# config.py
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen-turbo")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.05"))

USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "False").lower() == "true" or not DASHSCOPE_API_KEY

MAX_TEXT_LENGTH = 6000
SUPPORTED_TYPES = ["txt", "pdf", "docx"]

CSV_FILE = "kg_triples.csv"
IMPORT_CQL = "import_neo4j.cql"

MAX_GRAPH_DISPLAY = 200