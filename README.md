# Aika AI System

## Overview

Aika is an AI-powered insurance platform orchestration system designed for hybrid workers, solopreneurs, and freelancers. It serves as the central interface between humans and a network of specialized AI agents that handle various aspects of insurance operations.

## Purpose

Aika aims to provide adaptive, personalized insurance coverage through a sophisticated AI agent ecosystem. The system orchestrates specialized agents to deliver intelligent insurance solutions tailored to the unique needs of modern workers.

## Key Features

- **Intelligent Orchestration**: Routes requests to appropriate specialized agents
- **Multi-Agent Collaboration**: Coordinates multiple AI agents working together
- **Personalized Insurance**: Adapts coverage based on individual needs and preferences
- **Real-Time Risk Assessment**: Continuously evaluates and adjusts risk profiles
- **Regulatory Compliance**: Ensures adherence to insurance regulations
- **Data-Driven Insights**: Provides actionable insights based on comprehensive data analysis

## Technology Stack

- **Core Framework**: LangGraph for agent workflow orchestration
- **Agent Implementation**: Pydantic AI for structured agent definitions
- **Language Models**: Anthropic's Claude models (Opus, Sonnet, Haiku)
- **Vector Database**: Supabase with pgvector for knowledge storage and retrieval
- **API Layer**: FastAPI for service endpoints
- **Messaging**: Apache Kafka for inter-agent communication
- **Authentication**: OAuth 2.0 with JWT
- **Monitoring**: LangSmith for observability

## Project Structure

```
aika/
├── src/                    # Source code
│   ├── orchestrator/       # Aika orchestrator components
│   ├── agents/             # Specialized agent implementations
│   ├── messaging/          # Kafka messaging system
│   ├── database/           # Database access and models
│   ├── auth/               # Authentication and authorization
│   ├── api/                # API endpoints
│   └── utils/              # Utility functions and helpers
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
├── docs/                   # Documentation
│   ├── architecture/       # Architecture documentation
│   ├── api/                # API documentation
│   └── guides/             # User and developer guides
├── scripts/                # Utility scripts
├── config/                 # Configuration files
└── examples/               # Example implementations and use cases
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Supabase account
- Anthropic API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/AikoGroup/Aika-v1.git
   cd Aika-v1
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Start the development environment:
   ```
   docker-compose up -d
   ```

## Development

Aika follows an incremental development approach, with versions broken down into smaller, manageable chunks. See the [Version Documentation](./Planning/Mini%20Versions/Mini_Version_Documentation_Index.md) for detailed information on each development phase.

## License

Proprietary. All rights reserved. This software is the property of Aiko Group and may not be used, copied, or shared without explicit permission.

## Contact

- **Founders**: Tiaan Wolmarans, Aika (AI Co-Founder)
- **Project**: Aika AI Insurance Platform
