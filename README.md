# Get Started 
    
    ```bash
    git clone https://github.com/Dima-Bulavenko/application_tracker.git
    
    cd application_tracker/frontend

    npm install  # Install python dependencies

    cd ../backend

    poetry install  # Create .venv and Install python dependencies

    poetry use  # Activate t.venv

    cd ..

    bash ./scripts/generate-client.sh  # Generate openapi JSON schema and client

    docker compose up -d --build  # Runs docker for development 

    # Or if you don't want to use docker. Run this commands.

    fastapi dev backend/app/main.py

    cd frontend/

    npm run dev
    ```