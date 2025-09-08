import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG = {
    "branch": os.getenv("CCA_BRANCH", "main"),
    "max_files": int(os.getenv("CCA_MAX_FILES", "1000")),
    "ignore_tests": os.getenv("CCA_IGNORE_TESTS", "True").lower() == "true",
    "ignore_patterns": os.getenv("CCA_IGNORE_PATTERNS", "assets,").split(','),
    "model": os.getenv("CCA_MODEL", "deepseek-coder:6.7b"),
    "enhancer_timeout": float(os.getenv("CCA_ENHANCER_TIMEOUT", "300")),
    "ollama_host": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    "log_level": os.getenv("LOG_LEVEL", "INFO"),
    "max_cache_size": os.getenv("MAX_CACHE_SIZE", 500),
    "cache_ttl": int(os.getenv("CACHE_TTL", "3600")),
}