import logging
from pathlib import Path
from typing import Any, Dict, Optional
import requests
import yaml

from .utils import load_yaml_or_json

logger = logging.getLogger(__name__)

class SchemaLoader:
    """
    Handles loading of schemas from local files or URLs.

    Attributes:
        cache_dir: Optional directory to cache remote schemas.
    """

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize the SchemaLoader.

        Args:
            cache_dir: Path to a directory for caching remote schemas. 
                       If None, caching is disabled (in-memory only).
        """
        self.cache_dir: Optional[Path] = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self._memory_cache: Dict[str, Dict[str, Any]] = {}

    def load_schema(self, location: str) -> Dict[str, Any]:
        """
        Load a schema from a local path or URL.

        Args:
            location: The local file path or URL of the schema.

        Returns:
            The parsed schema as a dictionary.

        Raises:
            ValueError: If the schema cannot be loaded or parsed.
        """
        if location in self._memory_cache:
            logger.debug(f"Schema found in memory cache: {location}")
            return self._memory_cache[location]

        logger.info(f"Loading schema from: {location}")
        
        try:
            if location.startswith(('http://', 'https://')):
                schema = self._load_remote(location)
            else:
                schema = self._load_local(location)
        except Exception as e:
            logger.error(f"Failed to load schema from {location}: {e}")
            raise ValueError(f"Could not load schema from {location}") from e

        self._memory_cache[location] = schema
        return schema

    def _load_local(self, path: str) -> Dict[str, Any]:
        """Loads a schema from the local filesystem."""
        return load_yaml_or_json(path)

    def _load_remote(self, url: str) -> Dict[str, Any]:
        """Loads a schema from a remote URL."""
        # Future improvement: Implement disk caching here if self.cache_dir is set.
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Use content-type header heuristic or try-except waterfall
            content_type = response.headers.get('Content-Type', '')
            
            if 'json' in content_type:
                return response.json()
            else:
                try:
                    return response.json()
                except ValueError:
                    # Fallback to YAML
                    return yaml.safe_load(response.text)
                    
        except requests.RequestException as e:
            logger.error(f"Network error fetching schema from {url}: {e}")
            raise ValueError(f"Failed to fetch schema from {url}") from e
