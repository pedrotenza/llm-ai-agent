# src/config.py

# --- LLM CONFIGURATION ---
LLM_MODEL = "llama3.2:3b"                       # → src/agent/agent.py
TEMPERATURE = 0                                  # → src/agent/agent.py
NUM_CTX = 4096                                   # → src/agent/agent.py
NUM_PREDICT = 300                                # → src/agent/agent.py

# --- API CONFIGURATION (YOUR LOCAL SERVER!) ---
API_BASE_URL = "http://127.0.0.1:8000"           # → src/api/client.py

# --- SEMANTIC ROUTER CONFIGURATION ---
# Minimum similarity score to accept a label from the semantic router.
ROUTER_THRESHOLD = 0.45                          # → src/agent/agent.py

# Minimum score for NONE (higher to avoid false positives).
ROUTER_NONE_THRESHOLD = 0.70                     # → src/agent/agent.py

# --- MEMORY CONFIGURATION ---
# Maximum number of exchanges to keep in memory (sliding window).
MEMORY_MAX_HISTORY = 10                          # → src/agent/memory.py

# --- EMBEDDING CONFIGURATION ---
# Multilingual embedding model used by both the Semantic Router and the RAG pipeline.
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"   # → src/agent/agent.py, src/rag/embeddings.py

# --- RAG CONFIGURATION ---
# Number of words per chunk when splitting PDF text.
RAG_CHUNK_SIZE = 200                             # → src/rag/pdf_loader.py

# Number of words that overlap between consecutive chunks.
RAG_CHUNK_OVERLAP = 50                           # → src/rag/pdf_loader.py

# Minimum similarity score to keep a retrieved chunk.
RAG_MIN_SCORE = 0.4                              # → src/rag/rag_pipeline.py

# Number of chunks to retrieve per query.
RAG_TOP_K = 3                                    # → src/rag/rag_pipeline.py