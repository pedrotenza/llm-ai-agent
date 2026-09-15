# src/config.py

# --- LLM CONFIGURATION ---
LLM_MODEL = "llama3.2:3b"   
TEMPERATURE = 0
NUM_CTX = 4096
NUM_PREDICT = 300

# --- API CONFIGURATION (YOUR LOCAL SERVER!) ---
API_BASE_URL = "http://127.0.0.1:8000"

# --- SEMANTIC ROUTER CONFIGURATION ---
# Minimum similarity score to accept a label from the semantic router.
ROUTER_THRESHOLD = 0.45

# Minimum score for NONE (higher to avoid false positives).
ROUTER_NONE_THRESHOLD = 0.70