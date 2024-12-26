#! /usr/bin/env bash

set -e # Finish script if any error occurs
set -x # Allow to print command into console before a command executes

cd backend
python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
cd ..
mv openapi.json frontend/
cd frontend
npm run generate-client
rm openapi.json
