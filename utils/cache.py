import time
from typing import Any, Dict, Optional

from utils.settings import DEFAULT_CONFIG


class AnalysisCache:
    """Simple in-memory cache for analysis results."""

    def __init__(self):
        self.config = DEFAULT_CONFIG
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.timestamps: Dict[str, float] = {}

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get item from cache if it exists and isn't expired."""
        if key not in self.cache:
            return None

        # Check if item is expired
        if time.time() - self.timestamps[key] > self.config["cache_ttl"]:
            self.delete(key)
            return None

        return self.cache[key]

    def set(self, key: str, value: Dict[str, Any]) -> None:
        """Set item in cache with timestamp."""
        # Check cache size and remove oldest if needed
        if len(self.cache) >= self.config["max_cache_size"]:
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            self.delete(oldest_key)

        self.cache[key] = value
        self.timestamps[key] = time.time()

    def delete(self, key: str) -> None:
        """Delete item from cache."""
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]

    def clear_repository(self, repo_url: str) -> int:
        """Clear all cache entries for a repository."""
        count = 0
        keys_to_delete = [
            key for key in self.cache.keys() if key.startswith(f"{repo_url}:")
        ]

        for key in keys_to_delete:
            self.delete(key)
            count += 1

        return count

    def clear_all(self) -> int:
        """Clear all cache entries."""
        count = len(self.cache)
        self.cache.clear()
        self.timestamps.clear()
        return count
