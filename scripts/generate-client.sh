#! /usr/bin/env bash

set -e # Finish script if any error occurs
set -x # Allow to print command into console before a command executes

# Generate OpenAPI schema from running backend application code
cd backend
python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
cd ..

# Move schema to frontend for client generation
mv openapi.json frontend/

cd frontend
npm run generate-client

# Clean up generated schema file (client lives in src/shared/api via config)
rm openapi.json
