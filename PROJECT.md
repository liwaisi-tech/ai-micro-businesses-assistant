# Domain-Driven Design Guide for AI Business Assistant

## Table of Contents
1. [Project Overview](#project-overview)
2. [Domain-Driven Design Principles](#domain-driven-design-principles)
3. [Project Structure](#project-structure)
4. [Step-by-Step Implementation Guide](#step-by-step-implementation-guide)
5. [Database Design](#database-design)
6. [Agent Design with Langgraph](#agent-design-with-langgraph)
7. [API Design with FastAPI](#api-design-with-fastapi)
8. [Testing Strategy](#testing-strategy)
9. [Deployment Considerations](#deployment-considerations)

## Project Overview

This project aims to build an AI assistant for a micro-business that offers various products and services configured in a relational database. The system will use:

- **FastAPI** for the web framework
- **Uvicorn** as the ASGI server
- **Native SQL** for database operations (no ORM)
- **Langgraph** for agent orchestration
- **OpenAI** via LangChain for AI capabilities
- **Prompt templates** for structured AI interactions
- **Model context protocol** for managing information flow

The application will follow Domain-Driven Design (DDD) principles to ensure a clean separation of concerns and a maintainable codebase.

## Domain-Driven Design Principles

Domain-Driven Design focuses on:

1. **Ubiquitous Language**: Creating a shared language between technical and domain experts
2. **Bounded Contexts**: Defining clear boundaries for different parts of the system
3. **Domain Model**: Creating a model that reflects business reality
4. **Layered Architecture**: Separating concerns into distinct layers

For this project, we'll identify the following key bounded contexts:
- Product/Service Catalog
- Customer Interaction
- AI Assistant
- Database Access

## Project Structure

```
business_assistant/
├── pyproject.toml                  # Project metadata and dependencies
├── README.md                       # Project documentation
├── .env.example                    # Example environment variables
├── .gitignore                      # Git ignore file
├── src/
│   ├── business_assistant/         # Main package
│   │   ├── __init__.py
│   │   ├── domain/                 # Domain layer - core business logic
│   │   │   ├── __init__.py
│   │   │   ├── models/             # Domain entities and value objects
│   │   │   │   ├── __init__.py
│   │   │   │   ├── product.py
│   │   │   │   ├── service.py
│   │   │   │   ├── customer.py
│   │   │   │   └── conversation.py
│   │   │   ├── events/             # Domain events
│   │   │   │   ├── __init__.py
│   │   │   │   └── events.py
│   │   │   └── exceptions.py       # Domain-specific exceptions
│   │   │
│   │   ├── application/            # Application layer - use cases
│   │   │   ├── __init__.py
│   │   │   ├── services/           # Application services
│   │   │   │   ├── __init__.py
│   │   │   │   ├── product_service.py
│   │   │   │   ├── service_service.py
│   │   │   │   └── customer_service.py
│   │   │   ├── dtos/               # Data Transfer Objects
│   │   │   │   ├── __init__.py
│   │   │   │   ├── product_dto.py
│   │   │   │   ├── service_dto.py
│   │   │   │   └── customer_dto.py
│   │   │   └── interfaces/         # Service interfaces
│   │   │       ├── __init__.py
│   │   │       └── repository_interfaces.py
│   │   │
│   │   ├── infrastructure/         # Infrastructure layer - technical details
│   │   │   ├── __init__.py
│   │   │   ├── persistence/        # Database-related code
│   │   │   │   ├── __init__.py
│   │   │   │   ├── connection.py   # Database connection management
│   │   │   │   ├── repositories/   # SQL implementations of repositories
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── product_repository.py
│   │   │   │   │   ├── service_repository.py
│   │   │   │   │   └── customer_repository.py
│   │   │   │   └── queries/        # SQL query templates
│   │   │   │       ├── __init__.py
│   │   │   │       ├── product_queries.py
│   │   │   │       ├── service_queries.py
│   │   │   │       └── customer_queries.py
│   │   │   │
│   │   │   ├── ai/                 # AI-related code
│   │   │   │   ├── __init__.py
│   │   │   │   ├── llm_config.py   # LLM configuration
│   │   │   │   ├── prompts/        # Prompt templates
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── product_prompts.py
│   │   │   │   │   ├── service_prompts.py
│   │   │   │   │   └── conversation_prompts.py
│   │   │   │   └── context.py      # Context management for models
│   │   │   │
│   │   │   └── langgraph/          # Agent orchestration
│   │   │       ├── __init__.py
│   │   │       ├── agents/         # Agent definitions
│   │   │       │   ├── __init__.py
│   │   │       │   ├── product_agent.py
│   │   │       │   ├── service_agent.py
│   │   │       │   └── assistant_agent.py
│   │   │       ├── workflows/      # Agent workflows
│   │   │       │   ├── __init__.py
│   │   │       │   └── conversation_workflow.py
│   │   │       └── nodes/          # Langgraph nodes
│   │   │           ├── __init__.py
│   │   │           └── conversation_nodes.py
│   │   │
│   │   ├── interface/              # Interface layer - APIs, UI
│   │   │   ├── __init__.py
│   │   │   ├── api/                # FastAPI routes
│   │   │   │   ├── __init__.py
│   │   │   │   ├── v1/             # API version 1
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── routes/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── product_routes.py
│   │   │   │   │   │   ├── service_routes.py
│   │   │   │   │   │   └── assistant_routes.py
│   │   │   │   │   └── models/     # API models (Pydantic)
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── product_models.py
│   │   │   │   │       ├── service_models.py
│   │   │   │   │       └── request_models.py
│   │   │   │   └── dependencies.py # FastAPI dependencies
│   │   │   └── middlewares/        # API middlewares
│   │   │       ├── __init__.py
│   │   │       └── auth.py
│   │   │
│   │   └── config/                 # Configuration
│   │       ├── __init__.py
│   │       ├── settings.py         # Application settings
│   │       └── logging_config.py   # Logging configuration
│   │
│   └── main.py                     # Application entry point
│
├── tests/                          # Tests directory
│   ├── __init__.py
│   ├── conftest.py                 # Test fixtures
│   ├── unit/                       # Unit tests
│   │   ├── __init__.py
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/                # Integration tests
│   │   ├── __init__.py
│   │   ├── persistence/
│   │   └── api/
│   └── e2e/                        # End-to-end tests
│       ├── __init__.py
│       └── test_assistant.py
│
├── migrations/                     # Database migrations
│   ├── __init__.py
│   └── versions/                   # Migration versions
│
└── scripts/                        # Utility scripts
    ├── seed_data.py                # Database seeding
    └── setup_db.py                 # Database setup
```

## Step-by-Step Implementation Guide

### 1. Project Setup

1. **Create the project structure**:
   - Create all the necessary directories according to the structure above
   - Set up initial files like README.md, .gitignore, etc.

2. **Set up the Python environment**:
   - Create a virtual environment
   - Activate the virtual environment

3. **Create pyproject.toml with dependencies**:
   - Include all necessary dependencies:
     - FastAPI, Uvicorn for the web framework
     - LangChain, OpenAI for AI capabilities
     - Langgraph for agent orchestration
     - Database driver (e.g., psycopg2 for PostgreSQL)
     - Development dependencies (pytest, black, etc.)

4. **Install dependencies**:
   - Install all dependencies from pyproject.toml

5. **Set up environment variables**:
   - Create .env.example with all required variables
   - Set up database connection details
   - Configure OpenAI API key
   - Set environment-specific settings

### 2. Domain Layer Implementation

1. **Define domain entities**:
   - Create core domain models in `src/business_assistant/domain/models/`
   - Define value objects, aggregates, and entities
   - Implement domain events

2. **Build domain services**:
   - Implement domain-specific logic
   - Define validation rules
   - Create factory methods for complex entity creation

### 3. Application Layer Implementation

1. **Define application services**:
   - Implement use cases as application services
   - Create DTOs for data transfer between layers
   - Define repository interfaces

2. **Implement service logic**:
   - Handle complex business operations
   - Coordinate between different domain entities
   - Manage transactions and workflows

### 4. Infrastructure Layer Implementation

1. **Database setup**:
   - Create database connection management in `connection.py`
   - Implement SQL query templates
   - Create repository implementations using native SQL

2. **AI components setup**:
   - Configure LLM settings
   - Create prompt templates
   - Implement context management for AI models

3. **Langgraph implementation**:
   - Define agent types and behaviors
   - Create workflow graphs
   - Implement conversation nodes and transitions

### 5. Interface Layer Implementation

1. **API routes**:
   - Define FastAPI endpoints
   - Create request/response models using Pydantic
   - Implement API dependencies and middleware

2. **Assistant endpoints**:
   - Create conversation endpoints
   - Implement real-time chat functionality
   - Set up webhooks if needed

### 6. Testing

1. **Write unit tests**:
   - Test domain models and logic
   - Test application services
   - Test repository implementations

2. **Write integration tests**:
   - Test database operations
   - Test API endpoints
   - Test AI components

3. **Write end-to-end tests**:
   - Test complete workflows
   - Test assistant conversation capabilities

### 7. Database Setup

1. **Create database schema**:
   - Define tables for products, services, customers, etc.
   - Set up relationships and constraints
   - Create indexes for performance

2. **Write database migrations**:
   - Create initial schema migration
   - Set up migration versioning
   - Create seed data scripts

## Database Design

### Tables

1. **Products**:
   - id (primary key)
   - name (required)
   - description
   - price (required)
   - category
   - created_at, updated_at timestamps

2. **Services**:
   - id (primary key)
   - name (required)
   - description
   - base_price (required)
   - duration_minutes
   - category
   - created_at, updated_at timestamps

3. **Customers**:
   - id (primary key)
   - name (required)
   - email (required, unique)
   - phone
   - created_at, updated_at timestamps

4. **Conversations**:
   - id (primary key)
   - customer_id (foreign key to customers)
   - start_time, end_time timestamps
   - summary

5. **Messages**:
   - id (primary key)
   - conversation_id (foreign key to conversations)
   - is_from_assistant (boolean)
   - content (required)
   - timestamp

### Repository Implementation Strategy

1. **Define SQL query templates**:
   - Create separate files for different entity types
   - Include CRUD operations
   - Define specialized queries for business requirements

2. **Implement repository classes**:
   - Create classes that fulfill repository interfaces
   - Use connection pooling for efficiency
   - Implement error handling and retries

3. **Map database results to domain objects**:
   - Create mappers to convert database rows to domain entities
   - Handle relationships between entities

## Agent Design with Langgraph

1. **Define Agent State**:
   - Create a state model for conversation tracking
   - Include messages, customer information, and context
   - Track identified intents and recommendations

2. **Create Agent Nodes**:
   - Implement intent understanding node
   - Create product/service information retrieval node
   - Develop response generation node

3. **Build Workflow Graph**:
   - Connect nodes with appropriate transitions
   - Define conditional routing based on intents
   - Implement state management and persistence

## API Design with FastAPI

1. **Main Application Entry Point**:
   - Set up FastAPI application
   - Configure middleware and dependencies
   - Include all route modules

2. **API Routes Implementation**:
   - Create separate route modules for different domains
   - Define endpoints with appropriate HTTP methods
   - Implement request validation using Pydantic models

3. **Assistant API Endpoints**:
   - Create chat endpoint for conversation
   - Implement product/service query endpoints
   - Set up customer management endpoints

## Testing Strategy

1. **Unit Testing**:
   - Test individual components in isolation
   - Mock dependencies
   - Focus on business logic validation

2. **Integration Testing**:
   - Test interactions between components
   - Use test databases
   - Validate workflow correctness

3. **End-to-End Testing**:
   - Test complete user flows
   - Validate API responses
   - Ensure AI assistant behaves as expected

## Deployment Considerations

1. **Environment Configuration**:
   - Use environment variables for all configuration
   - Separate development, testing, and production settings
   - Secure storage of API keys and secrets

2. **Database Management**:
   - Use connection pooling for efficient database connections
   - Implement database migrations for schema updates
   - Set up backups and monitoring

3. **Scaling**:
   - Containerize application using Docker
   - Consider using Kubernetes for orchestration
   - Implement caching for frequently accessed data

4. **Monitoring and Logging**:
   - Set up comprehensive logging
   - Implement performance monitoring
   - Track AI model usage and performance