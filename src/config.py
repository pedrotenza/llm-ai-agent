# src/config.py

# . Router        → agent/agent.py
# . Embedding     → agent/agent.py + rag/embeddings.py
# . RAG           → rag/pdf_loader.py + rag/rag_pipeline.py
# . API           → api/client.py
# . Memory        → agent/memory.py
# . LLM           → agent/agent.py


# --- SEMANTIC ROUTER CONFIGURATION ---
ROUTER_THRESHOLD = 0.45                          # minimum similarity question-router examples to accept a label        → src/agent/agent.py

ROUTER_NONE_THRESHOLD = 0.70                     # Minimum score for NONE (higher to avoid false positives)             → src/agent/agent.py

# --- EMBEDDING CONFIGURATION ---
                                                 # Multilingual embedding model used by both the Semantic Router and the RAG pipeline.
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"                                                              #→ src/agent/agent.py, src/rag/embeddings.py

# --- RAG CONFIGURATION ---
RAG_CHUNK_SIZE = 200                             # Number of words per chunk when splitting PDF text                    → src/rag/pdf_loader.py

RAG_CHUNK_OVERLAP = 50                           # Number of words that overlap between consecutive chunks              → src/rag/pdf_loader.py

RAG_MIN_SCORE = 0.4                              # Minimum similarity score question-retrieved chunk to keep it         → src/rag/rag_pipeline.py

RAG_TOP_K = 3                                    # Number of chunks to retrieve per query                               → src/rag/rag_pipeline.py

# --- API CONFIGURATION (YOUR LOCAL SERVER!) ---
API_BASE_URL = "http://127.0.0.1:8000"           #                                              → src/api/client.py

# --- MEMORY CONFIGURATION ---

MEMORY_MAX_HISTORY = 10                          # Maximum number of exchanges to keep in memory (sliding window)       → src/agent/memory.py

# --- LLM CONFIGURATION ---
LLM_MODEL = "llama3.2:3b"                        #                                                                      → src/agent/agent.py
TEMPERATURE = 0                                  # if the model is serious (0) or creative (1)                          → src/agent/agent.py
NUM_CTX = 4096                                   # total context window (input + output tokens)                         → src/agent/agent.py
NUM_PREDICT = 300                                # maximum number of output tokens                                      → src/agent/agent.py