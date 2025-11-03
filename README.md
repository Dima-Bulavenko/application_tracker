# Application Tracker

A full-stack application tracker built with FastAPI (backend) and React (frontend).

## Project Setup

This project can be run in two ways: using a Dev Container (recommended) or directly on your host machine.

### Prerequisites

Before starting, you need to configure the environment variables:

1. **Environment Configuration**: Create a `.env` file from the example template:
   ```bash
   cp .env.example .env
   ```

   **Edit the `.env` file and set the following required variables:**
   - `POSTGRES_PASSWORD` - Set a secure password for your database
   - `SECRET_KEY` - Generate a long, random secret key for JWT authentication
   - `POSTGRES_HOST` - Use `postgres` for dev container or `localhost` for host setup
   - `POSTGRES_HOST_TEST` - Use `db-test` for dev container or `localhost` for host setup

   **Other important variables:**
   - `POSTGRES_USER`, `POSTGRES_DB` - Database name and user (can keep defaults)
   - `ALLOWED_ORIGINS` - CORS allowed hosts (adjust if needed)
   - `DEBUG` - Enable/disable debug mode

## Frontend API Client Generation

This project uses a script to automatically generate a TypeScript client for the frontend based on the FastAPI OpenAPI schema. The `scripts/generate-client.sh` script:

1. Extracts the OpenAPI JSON schema from the running FastAPI application
2. Uses the `hey-api` library to generate TypeScript client code
3. Creates type-safe API methods and models for the frontend

**Note**: The client generation requires the backend dependencies to be installed (Poetry) and is automatically run during dev container setup.

## Contributing

### Commit Message Convention

This project follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for commit messages. This ensures consistent, readable commit history and enables automated changelog generation.

**Format**: `<type>[optional scope]: <description>`

**Examples**:
- `feat(auth): add JWT token refresh functionality`
- `fix(db): resolve connection pool timeout issue`
- `docs: update API documentation for user endpoints`

See the full specification at: https://www.conventionalcommits.org/en/v1.0.0/

## Option 1: Dev Container Setup (Recommended)

**Requirements:**
- Docker Desktop
- Visual Studio Code
- Dev Containers extension for VS Code

**Steps:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dima-Bulavenko/application_tracker.git
   cd application_tracker
   ```

2. **Open in VS Code:**
   ```bash
   code .
   ```

3. **Start Dev Container:**
   - VS Code will detect the dev container configuration
   - Click "Reopen in Container" when prompted, or
   - Use Command Palette (`Ctrl+Shift+P`): "Dev Containers: Reopen in Container"

4. **Wait for container setup:**
   - The container will automatically:
     - Install Python 3.12 with Poetry
     - Install Node.js 23
     - Install all Python dependencies (backend)
     - Install all Node.js dependencies (frontend)
     - Generate frontend API client using hey-api
     - Set up PostgreSQL database
     - Configure pgAdmin for database management

5. **Start the application:**

   **Backend (FastAPI):**
   ```bash
   cd backend
   fastapi dev --host "0.0.0.0" --port "8000"
   ```

   **Frontend (React):**
   ```bash
   cd frontend
   npm run dev
   ```

### Services Available in Dev Container:

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **pgAdmin**: http://localhost:1654
  - Email: `admin@pgadmin.com`
  - Password: `password`
- **PostgreSQL**: localhost:5432
- **Test Database**: localhost:5435

## Option 2: Host Machine Setup

**Requirements:**
- Python 3.12
- Poetry 1.8.3
- Node.js 23
- PostgreSQL server

**Steps:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dima-Bulavenko/application_tracker.git
   cd application_tracker
   ```

2. **Update environment configuration:**
   Edit your `.env` file to use localhost for database connection:
   ```env
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   # Update other variables as needed
   ```

3. **Setup PostgreSQL:**
   - Install and start PostgreSQL on your system
   - Create databases:
     ```sql
     CREATE DATABASE app_tracker;
     CREATE DATABASE app_tracker_test;
     CREATE USER app_tracker_user WITH PASSWORD '123456';
     GRANT ALL PRIVILEGES ON DATABASE app_tracker TO app_tracker_user;
     GRANT ALL PRIVILEGES ON DATABASE app_tracker_test TO app_tracker_user;
     ```

4. **Install Backend Dependencies:**
   ```bash
   cd backend
   poetry install
   ```

5. **Install Frontend Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

6. **Generate Frontend API Client:**
   ```bash
   bash scripts/generate-client.sh
   ```

7. **Start the applications:**

   **Backend (in one terminal):**
   ```bash
   cd backend
   fastapi dev --host "0.0.0.0" --port "8000"
   ```

   **Frontend (in another terminal):**
   ```bash
   cd frontend
   npm run dev
   ```

### Services Available on Host:

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **PostgreSQL**: localhost:5432
