# GitHub Copilot Instructions

## Project Overview
This is an **Application Tracker** web application that helps users track and manage their job applications throughout the entire application process.

### Purpose & Functionality
The application enables users to:
- **Add Applications**: Users can create new job application records with comprehensive details
- **Track Progress**: Monitor application status changes from initial submission through final outcome
- **Manage Information**: Store and update application details, company information, and personal notes
- **Organize & Filter**: View all applications with sorting and filtering capabilities by various parameters
- **Detailed Tracking**: Access comprehensive application information including interview dates and application URLs


### Technical Stack
- **Backend**: FastAPI with Python 3.12, SQLAlchemy (async), PostgreSQL
- **Frontend**: React with TypeScript, Vite
- **Backend Architecture**: Onion Architecture with clean separation of concerns
- **Frontend Architecture**: Feature-Sliced Design (FSD) for scalable component organization
- **Deployment**: Docker containers with dev container support

## Code Style & Standards

### Python Backend
- Use **Python 3.12** features and type hints
- Follow **PEP 8** with **ruff** formatting (line length: 120)
- Use **async/await** for all database operations
- Prefer **Pydantic v2** models with `ConfigDict`
- Use **SQLAlchemy 2.0** ORM syntax with async sessions

### TypeScript Frontend
- Use **TypeScript strict mode**
- Follow **React functional components** with hooks
- Use **ESLint** and **Prettier** for formatting
- Prefer **async/await** over promises

### General Principles
- **DRY (Don't Repeat Yourself)**: Extract common logic into utilities
- **SOLID principles**: Single responsibility, dependency injection
- **Type safety**: Use strict typing throughout
- **Error handling**: Comprehensive exception handling with custom exceptions

## Pre-commit Compliance Rules

### File Formatting Standards
- **No trailing whitespace**: Remove all trailing spaces and tabs from lines
- **End-of-file newline**: Always end files with a single newline character
- **No large files**: Avoid committing files larger than reasonable size limits

### Python Code Standards
- **Ruff compliance**: All Python code must pass `ruff check` and `ruff format`
- **MyPy compliance**: All Python code must pass type checking with `mypy`
- **Import sorting**: Use ruff's import sorting (`--select I --fix`)

### Frontend Code Standards
- **ESLint compliance**: All TypeScript/JavaScript code must pass ESLint rules
- **Prettier formatting**: All frontend code must be formatted with Prettier
- **Supported file types**: Apply formatting to `.js`, `.ts`, `.tsx`, `.jsx`, `.json`, `.yaml`, `.html`, `.css`

### Code Generation Guidelines
When generating code, ensure:

1. **Python files**:
   - No trailing whitespace on any line
   - End file with exactly one newline
   - Follow ruff formatting standards
   - Include proper type hints for mypy compliance
   - Use proper import ordering

2. **Template files** (HTML/Jinja2):
   - No trailing whitespace
   - End file with exactly one newline
   - Apply Prettier formatting for HTML structure
   - Use consistent indentation (2 spaces for HTML)

3. **Configuration files** (JSON/YAML):
   - No trailing whitespace
   - End file with exactly one newline
   - Apply Prettier formatting
   - Use consistent indentation

## Architecture Guidelines

### Backend: Onion Architecture Layers
The backend follows **Onion Architecture** principles with clean separation of concerns:

1. **Domain Layer** (`core/domain/`): Pure business entities and enums
2. **Application Layer** (`core/services/`): Business logic and orchestration
3. **Infrastructure Layer** (`infrastructure/`): External concerns (DB, auth, etc.)
4. **Presentation Layer** (`routers/`): HTTP endpoints and API contracts

### Frontend: Feature-Sliced Design (FSD)
The frontend follows **Feature-Sliced Design** methodology for scalable architecture:

**FSD Layers (from top to bottom):**
- **App** (`src/app/`): Application initialization, providers, global configuration
- **Pages** (`src/pages/`): Route-level components and page logic
- **Features** (`src/features/`): User-facing functionality and business features
- **Entities** (`src/entities/`): Business entities and their representations
- **Shared** (`src/shared/`): Reusable infrastructure code, UI kit, utilities

**FSD Segments within each layer:**
- `ui/` - User interface components
- `api/` - API calls and data fetching logic
- `model/` - Business logic, stores, types
- `lib/` - Infrastructure utilities
- `config/` - Configuration and constants

### Key Patterns
- **Repository Pattern**: Abstract data access with interfaces
- **Dependency Injection**: Use FastAPI's dependency system
- **Service Layer**: Keep business logic in services, not endpoints
- **DTO Pattern**: Separate internal models from API contracts

### Database
- Use **async SQLAlchemy** with proper session management
- Define **relationships** with `back_populates`
- Use **enum types** for status fields
- Include **audit fields** (`time_create`, `time_update`)

## Testing Standards

### Test Structure
- Use **BaseTest** class for common test utilities
- Organize tests by feature: `TestApplicationUpdate`, `TestApplicationDelete`
- Use **pytest fixtures** with proper dependency injection
- Follow **AAA pattern**: Arrange, Act, Assert

## Commit Message Standards

### Conventional Commits
All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification:

**Format:**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Required Types:**
- `feat:` - A new feature for the user
- `fix:` - A bug fix for the user
- `docs:` - Documentation changes
- `style:` - Code formatting (no logic changes)
- `refactor:` - Code restructuring (no new features or bug fixes)
- `perf:` - Performance improvements
- `test:` - Adding or updating tests
- `build:` - Build system or dependency changes
- `ci:` - CI/CD configuration changes
- `chore:` - Maintenance tasks

**Optional Scope:**
- Use parentheses to specify the area of change: `feat(auth):`, `fix(db):`, `docs(api):`

**Breaking Changes:**
- Add `!` after type/scope: `feat!:` or `feat(api)!:`
- Or use footer: `BREAKING CHANGE: description`

**Examples:**
```
feat(auth): add JWT token refresh functionality
fix(db): resolve connection pool timeout issue
docs: update API documentation for user endpoints
test(auth): add unit tests for login validation
refactor!: restructure user service architecture

BREAKING CHANGE: User service constructor now requires logger parameter
```
