#!/usr/bin/env python3
"""
Script to generate tools.yaml configuration file with database credentials from environment variables.
"""
import os
import yaml
import sys

# Default values
DEFAULT_CONFIG = {
    "sources": {
        "postgres_source": {
            "kind": "postgres",
            "host": os.environ.get("POSTGRES_HOST", "db"),
            "port": int(os.environ.get("POSTGRES_PORT", "5432")),
            "database": os.environ.get("POSTGRES_DB", "business_assistant_db"),
            "user": os.environ.get("POSTGRES_USER", "postgres"),
            "password": os.environ.get("POSTGRES_PASSWORD", "postgres")
        }
    }
}

def main():
    """Generate tools.yaml with environment variables."""
    # Read existing tools.yaml to get the tools section
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "config", "tools.yaml")
    
    try:
        with open(config_path, 'r') as file:
            existing_config = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading existing config: {e}")
        sys.exit(1)
    
    # Merge the sources section with the existing tools section
    merged_config = DEFAULT_CONFIG.copy()
    if existing_config and "tools" in existing_config:
        merged_config["tools"] = existing_config["tools"]
    
    # Write the merged configuration back to tools.yaml
    try:
        with open(config_path, 'w') as file:
            yaml.dump(merged_config, file, default_flow_style=False)
        print(f"Successfully generated {config_path} with database credentials")
    except Exception as e:
        print(f"Error writing config: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
