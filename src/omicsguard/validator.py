import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import jsonschema

from .loader import SchemaLoader

logger = logging.getLogger(__name__)

@dataclass
class ValidationError:
    """
    Represents a single validation error found in the data.

    Attributes:
        message: A human-readable error message.
        path: The path to the invalid element in the data (e.g., "samples.0.id").
    """
    message: str
    path: str

    def __str__(self) -> str:
        return f"[{self.path}] {self.message}"

class MetadataValidator:
    """
    Validates dictionary data against a JSON schema.
    """

    def __init__(self, schema_location: Optional[str] = None, schema_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize the validator.

        Args:
            schema_location: Path or URL to the schema.
            schema_dict: Direct dictionary representation of the schema.

        Raises:
            ValueError: If neither schema_location nor schema_dict is provided.
        """
        self.loader = SchemaLoader()
        
        if schema_dict:
            self.schema = schema_dict
        elif schema_location:
            self.schema = self.loader.load_schema(schema_location)
        else:
            raise ValueError("Either schema_location or schema_dict must be provided.")

    def validate(self, data: Dict[str, Any]) -> List[ValidationError]:
        """
        Validates data against the loaded schema.

        Args:
            data: The dictionary data to validate.

        Returns:
            A list of ValidationError objects. If empty, validation passed.
        """
        validator = jsonschema.Draft7Validator(self.schema)
        errors: List[ValidationError] = []
        
        # Iterating through errors is lazy, which is efficient for large datasets
        for error in validator.iter_errors(data):
            # Format path as a dot-notation string (e.g., "samples.0.id")
            # This is more readable for end-users than deque([ 'samples', 0, 'id'])
            path_str = ".".join(str(p) for p in error.path) if error.path else "root"
            
            # Create our own simple error object
            val_error = ValidationError(message=error.message, path=path_str)
            errors.append(val_error)
            
        if errors:
            logger.info(f"Validation failed with {len(errors)} errors.")
        else:
            logger.debug("Validation successful.")
            
        return errors

def validate_metadata(data: Dict[str, Any], schema: Dict[str, Any]) -> List[ValidationError]:
    """
    Helper function for quick one-off validation.

    Args:
        data: The data to validate.
        schema: The schema dictionary.

    Returns:
        A list of ValidationError objects.
    """
    validator = MetadataValidator(schema_dict=schema)
    return validator.validate(data)
