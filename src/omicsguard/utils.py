import json
import logging
from pathlib import Path
from typing import Any, Dict, Union

import yaml

logger = logging.getLogger(__name__)

def load_yaml_or_json(source: Union[str, Path]) -> Dict[str, Any]:
    """
    Loads and parses JSON or YAML content from a file path or direct string.

    This function attempts to detect if the input is a valid file path. If it is,
    it reads the file; otherwise, it treats the input as raw content.

    Args:
        source: A file path (str or Path) or the raw content string.

    Returns:
        A dictionary containing the parsed data.

    Raises:
        ValueError: If the content cannot be parsed as valid JSON or YAML.
        IOError: If a file path is provided but cannot be read.
    """
    content: str = ""

    # Determine if source is a path or content
    if isinstance(source, Path):
        try:
            content = source.read_text(encoding="utf-8")
        except OSError as e:
            logger.error(f"Failed to read file at {source}: {e}")
            raise
    else:
        # Heuristic: if it's a string that looks like a path and exists, read it.
        # Check for newlines to quickly rule out raw content being interpreted as a path.
        if "\n" not in source and len(source) < 4096:
            path_obj = Path(source)
            if path_obj.is_file():
                try:
                    content = path_obj.read_text(encoding="utf-8")
                except OSError as e:
                    logger.error(f"Failed to read file at {path_obj}: {e}")
                    raise
            else:
                content = source
        else:
            content = source

    # Attempt parsing
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        logger.debug("JSON decode failed, attempting YAML.")
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            logger.error("Failed to decode content as both JSON and YAML.")
            raise ValueError("Content is not valid JSON or YAML") from e
