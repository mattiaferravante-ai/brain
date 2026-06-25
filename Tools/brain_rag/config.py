from pathlib import Path

BRAIN_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
STATE_FILE = DATA_DIR / "index_state.json"

EMBEDDING_MODEL = "intfloat/multilingual-e5-base"

CHUNK_MAX_TOKENS = 500
CHUNK_OVERLAP_TOKENS = 50

EXCLUDE_DIRS = {".git", ".claude", ".obsidian", "Tools", "node_modules", "__pycache__"}

COLLECTION_NAME = "brain"
TOP_K = 5
