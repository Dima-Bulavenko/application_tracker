# GitHub Copilot Instructions

## Project Overview
This is an **Application Tracker** web application built with:
- **Backend**: FastAPI with Python 3.12, SQLAlchemy (async), PostgreSQL
- **Frontend**: React with TypeScript, Vite
- **Architecture**: Onion Architecture with clean separation of concerns
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

## Architecture Guidelines

### Onion Architecture Layers
1. **Domain Layer** (`core/domain/`): Pure business entities and enums
2. **Application Layer** (`core/services/`): Business logic and orchestration
3. **Infrastructure Layer** (`infrastructure/`): External concerns (DB, auth, etc.)
4. **Presentation Layer** (`routers/`): HTTP endpoints and API contracts

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
