#!/bin/bash
# Script to generate tools.yaml with environment variables

# Set default values if environment variables are not set
POSTGRES_HOST=${POSTGRES_HOST:-db}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
POSTGRES_DB=${POSTGRES_DB:-business_assistant_db}
POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}

# Path to the tools.yaml file
CONFIG_FILE="/config/tools.yaml"
TEMPLATE_FILE="/config/tools.template.yaml"

# Check if template exists, if not create it from the current tools.yaml
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Creating template file from current tools.yaml..."
    cp "$CONFIG_FILE" "$TEMPLATE_FILE"
fi

# Create a new tools.yaml with the database credentials
cat > "$CONFIG_FILE" << EOF
sources:
  postgres_source:
    kind: postgres
    host: $POSTGRES_HOST
    port: $POSTGRES_PORT
    database: $POSTGRES_DB
    user: $POSTGRES_USER
    password: $POSTGRES_PASSWORD
EOF

# Append the tools section from the template
sed -n '/^tools:/,$p' "$TEMPLATE_FILE" >> "$CONFIG_FILE"

echo "Successfully generated tools.yaml with database credentials"
