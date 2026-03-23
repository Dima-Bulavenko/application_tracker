#!/usr/bin/env bash

set -e # Finish script if any error occurs
set -x # Allow to print command into console before a command executes

# Generate OpenAPI schema from backend application code (no running server needed)
cd backend
uv run python -c "import app.main; import json; print(json.dumps(app.main.app.openapi(), indent=2))" > ../frontend/openapi.json
cd ..

# Generate TypeScript client from the schema
cd frontend
npm run generate-client
