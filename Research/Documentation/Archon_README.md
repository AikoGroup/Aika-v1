# Archon - AI Agent Builder

<img src="public/Archon.png" alt="Archon Logo" />

<div align="center" style="margin-top: 20px;margin-bottom: 30px">

<h3>🚀 **CURRENT VERSION** 🚀</h3>

**[ V4 - Massive Streamlit UI Overhaul ]**
*Comprehensive dashboard interface for managing Archon with Streamlit*

</div>

Archon is an AI meta-agent designed to autonomously build, refine, and optimize other AI agents. 

It serves both as a practical tool for developers and as an educational framework demonstrating the evolution of agentic systems.
Archon will be developed in iterations, starting with just a simple Pydantic AI agent that can build other Pydantic AI agents,
all the way to a full agentic workflow using LangGraph that can build other AI agents with any framework.
Through its iterative development, Archon showcases the power of planning, feedback loops, and domain-specific knowledge in creating robust AI agents.

## Important Links

- The current version of Archon is V4 as mentioned above - see [V4 Documentation](iterations/v4-streamlit-ui-overhaul/README.md) for details.

- I **just** created the [Archon community](https://thinktank.ottomator.ai/c/archon/30) forum over in the oTTomator Think Tank! Please post any questions you have there!

- [GitHub Kanban board](https://github.com/users/coleam00/projects/1) for feature implementation and bug squashing.

## Vision

Archon demonstrates three key principles in modern AI development:

1. **Agentic Reasoning**: Planning, iterative feedback, and self-evaluation overcome the limitations of purely reactive systems
2. **Domain Knowledge Integration**: Seamless embedding of frameworks like Pydantic AI and LangGraph within autonomous workflows
3. **Scalable Architecture**: Modular design supporting maintainability, cost optimization, and ethical AI practices

## Getting Started with V4 (current version)

Since V4 is the current version of Archon, all the code for V4 is in both the main directory and `archon/iterations/v4-streamlit-ui-overhaul` directory.

### Prerequisites
- Python 3.11+
- Supabase account (for vector database)
- OpenAI/OpenRouter API key or Ollama for local LLMs

### Installation

1. Clone the repository:
```bash
git clone https://github.com/coleam00/archon.git
cd archon
```

2. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Quick Start

1. Start the Streamlit UI:
```bash
streamlit run streamlit_ui.py
```

2. Follow the guided setup process in the Intro section of the Streamlit UI:
   - **Environment**: Configure your API keys and model settings
   - **Database**: Set up your Supabase vector database
   - **Documentation**: Crawl and index the Pydantic AI documentation
   - **Agent Service**: Start the agent service for generating agents
   - **Chat**: Interact with Archon to create AI agents
   - **MCP** (optional): Configure integration with AI IDEs

The Streamlit interface will guide you through each step with clear instructions and interactive elements.
There are a good amount of steps for the setup but it goes quick!

## Project Evolution

### V1: Single-Agent Foundation
- Basic RAG-powered agent using Pydantic AI
- Supabase vector database for documentation storage
- Simple code generation without validation
- [Learn more about V1](iterations/v1-single-agent/README.md)

### V2: Agentic Workflow (LangGraph)
- Multi-agent system with planning and execution separation
- Reasoning LLM (O3-mini/R1) for architecture planning
- LangGraph for workflow orchestration
- Support for local LLMs via Ollama
- [Learn more about V2](iterations/v2-agentic-workflow/README.md)

### V3: MCP Support
- Integration with AI IDEs like Windsurf and Cursor
- Automated file creation and dependency management
- FastAPI service for agent generation
- Improved project structure and organization
- [Learn more about V3](iterations/v3-mcp-support/README.md)

### V4: Current - Streamlit UI Overhaul
- Comprehensive Streamlit interface for managing all aspects of Archon
- Guided setup process with interactive tabs
- Environment variable management through the UI
- Database setup and documentation crawling simplified
- Agent service control and monitoring
- MCP configuration through the UI
- [Learn more about V4](iterations/v4-streamlit-ui-overhaul/README.md)

### Future Iterations
- V5: Self-Feedback Loop - Automated validation and error correction
- V6: Tool Library Integration - Pre-built external tool incorporation
- V7: Multi-Framework Support - Framework-agnostic agent generation
- V8: Autonomous Framework Learning - Self-updating framework adapters

### Future Integrations
- Docker
- LangSmith
- Other frameworks besides Pydantic AI
- Other vector databases besides Supabase

## Architecture

### Core Files
- `streamlit_ui.py`: Comprehensive web interface for managing all aspects of Archon
- `graph_service.py`: FastAPI service that handles the agentic workflow
- `mcp_server.py`: MCP server script for AI IDE integration
- `requirements.txt`: Project dependencies

### Archon Package
- `archon/`: Core agent and workflow implementation
  - `archon_graph.py`: LangGraph workflow definition and agent coordination
  - `pydantic_ai_coder.py`: Main coding agent with RAG capabilities
  - `crawl_pydantic_ai_docs.py`: Documentation crawler and processor

### Utilities
- `utils/`: Utility functions and database setup
  - `utils.py`: Shared utility functions
  - `site_pages.sql`: Database setup commands
  - `env_vars.json`: Environment variables defined in the UI are stored here (included in .gitignore, file is created automatically)

### Database Setup

The Supabase database uses the following schema:

```sql
CREATE TABLE site_pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    url TEXT,
    chunk_number INTEGER,
    title TEXT,
    summary TEXT,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(1536) -- Adjust dimensions as necessary (i.e. 768 for nomic-embed-text)
);
```

The Streamlit UI provides an interface to set up this database structure automatically.

## Contributing

We welcome contributions! Whether you're fixing bugs, adding features, or improving documentation, please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

---

For version-specific details:
- [V1 Documentation](iterations/v1-single-agent/README.md)
- [V2 Documentation](iterations/v2-agentic-workflow/README.md)
- [V3 Documentation](iterations/v3-mcp-support/README.md)
- [V4 Documentation](iterations/v4-streamlit-ui-overhaul/README.md)
