import logging
import os
import sys
from pathlib import Path

import click

from .utils import load_yaml_or_json
from .validator import MetadataValidator

# Configure logging to stderr so as not to pollute stdout which we use for "true/false"
logging.basicConfig(level=logging.WARNING, stream=sys.stderr, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_SCHEMA_PATH = Path(__file__).parent / "schemas" / "default.json"

@click.command()
@click.option(
    '--schema', 
    required=False, 
    help='Path or URL to the JSON/YAML schema. Defaults to bundled Phenopacket schema.'
)
@click.option(
    '--data', 
    required=True, 
    help='Path to the data file (JSON/YAML) to validate.'
)
def main(schema: str, data: str):
    """
    OmicsGuard: Validate genomic metadata against a schema.
    
    This CLI tool validates a JSON or YAML data file against a specified schema.
    If no schema is provided, it uses the bundled default schema (GA4GH Phenopackets).
    
    Output:
      Prints 'true' to stdout if validation passes, 'false' otherwise.
      Validation errors are printed to stderr.
    """
    # Resolve schema path: user provided > default bundled
    schema_uri = schema if schema else str(DEFAULT_SCHEMA_PATH)
    
    logger.debug(f"Using schema: {schema_uri}")
    logger.debug(f"Validating data: {data}")

    try:
        # Load Data
        try:
            data_content = load_yaml_or_json(data)
        except (ValueError, OSError) as e:
            # Operational errors (file not found, bad json) are expected
            logger.error(f"Error loading data file: {e}")
            sys.exit(1)

        # Validate
        validator = MetadataValidator(schema_location=schema_uri)
        errors = validator.validate(data_content)
        
        if not errors:
            click.echo("true")
            sys.exit(0)
        else:
            click.echo("false")
            for err in errors:
                click.echo(f" - {err}", err=True)
            sys.exit(1)

    except Exception as e:
        # Unexpected errors (bugs in code, etc)
        logger.exception("An unexpected error occurred during validation.")
        sys.exit(1)

if __name__ == '__main__':
    main()
