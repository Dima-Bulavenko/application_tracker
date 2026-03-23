#!/usr/bin/env bash

set -e

SCHEMA_FILE="frontend/openapi.json"

if [ ! -f "$SCHEMA_FILE" ]; then
    echo "ERROR: $SCHEMA_FILE does not exist."
    echo "Run 'scripts/generate-client.sh' to generate it."
    exit 1
fi

# Generate a fresh schema from the current backend code
FRESH_SCHEMA=$(cd backend && uv run python -c "import app.main; import json; print(json.dumps(app.main.app.openapi(), indent=2))")

# Compare against the committed schema
if ! echo "$FRESH_SCHEMA" | diff -q "$SCHEMA_FILE" - > /dev/null 2>&1; then
    echo "ERROR: $SCHEMA_FILE is out of date."
    echo ""
    echo "The committed schema does not match the current backend."
    echo "Run 'scripts/generate-client.sh' and commit the updated $SCHEMA_FILE."
    echo ""
    echo "Diff (committed vs current):"
    echo "$FRESH_SCHEMA" | diff "$SCHEMA_FILE" - || true
    exit 1
fi
