# Pydantic AI Research

## Overview

This document provides in-depth research on Pydantic AI, a Python agent framework designed for building production-grade AI applications with strong typing and validation.

## What is Pydantic AI?

Pydantic AI is an agent framework developed by the team behind Pydantic (the validation layer used by OpenAI SDK, Anthropic SDK, LangChain, and many other AI frameworks). It's specifically designed to make it easier to build production-grade applications with generative AI by providing strong typing, validation, and structured interactions with language models.

## Key Features

### 1. Structured Responses

- **Type Safety**: Enforces strong typing for LLM outputs
- **Validation**: Automatically validates model outputs against defined schemas
- **Error Handling**: Provides reflection mechanisms to retry when validation fails
- **Consistency**: Ensures responses are consistent across different runs

### 2. Agent Architecture

- **Agent Definition**: Simple, declarative way to define AI agents
- **Tool Integration**: First-class support for tools and function calling
- **Dependency Injection**: Optional dependency injection system for providing data and services
- **Multi-step Reasoning**: Support for complex, multi-step interactions

### 3. Model Agnostic

- **Multiple LLM Support**: Works with various LLM providers:
  - Anthropic (Claude)
  - OpenAI
  - Google (Gemini)
  - Mistral
  - Ollama
  - Groq
  - Cohere
  - And more

### 4. Production Features

- **Retries and Fallbacks**: Built-in mechanisms for handling failures
- **Observability**: Integration with monitoring tools
- **Caching**: Support for response caching
- **Rate Limiting**: Handles API rate limits gracefully

## Core Concepts

### Agents

Agents are the primary interface for interacting with LLMs in Pydantic AI. They encapsulate:

1. **System Prompts**: Instructions for the LLM
2. **Tools**: Functions the agent can call
3. **Output Schemas**: Expected structure of responses

### Models

Models represent the connection to LLM providers. Pydantic AI supports multiple model providers through a unified interface:

```python
from pydantic_ai.models.anthropic import AnthropicModel

model = AnthropicModel("claude-3-opus-20240229")
```

### Tools

Tools are functions that agents can call to perform actions or retrieve information:

```python
from pydantic_ai import Tool
from pydantic import BaseModel

class WeatherRequest(BaseModel):
    location: str
    unit: str = "celsius"

class WeatherResponse(BaseModel):
    temperature: float
    conditions: str

@Tool(request_model=WeatherRequest, response_model=WeatherResponse)
def get_weather(request: WeatherRequest) -> WeatherResponse:
    # Implementation to fetch weather data
    return WeatherResponse(temperature=22.5, conditions="Sunny")
```

### Results

Results define the expected output structure from an agent:

```python
from pydantic import BaseModel
from typing import List

class InsuranceRecommendation(BaseModel):
    plan_name: str
    monthly_premium: float
    coverage_details: List[str]
    suitability_score: int
```

## Code Example: Building an Agent with Pydantic AI

Here's an example of creating a simple insurance recommendation agent using Pydantic AI and Anthropic's Claude:

```python
from pydantic_ai import Agent, Tool
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic import BaseModel
from typing import List, Optional

# Define models for the agent's input and output
class CustomerProfile(BaseModel):
    age: int
    occupation: str
    annual_income: float
    existing_coverage: Optional[List[str]] = None
    risk_factors: Optional[List[str]] = None

class InsuranceRecommendation(BaseModel):
    plan_name: str
    monthly_premium: float
    coverage_details: List[str]
    suitability_score: int  # 1-10
    rationale: str

# Define a tool for retrieving available insurance plans
class PlanQuery(BaseModel):
    min_coverage: Optional[float] = None
    max_premium: Optional[float] = None
    coverage_type: Optional[str] = None

class InsurancePlan(BaseModel):
    name: str
    monthly_premium: float
    coverage_amount: float
    coverage_type: str
    features: List[str]

@Tool(request_model=PlanQuery, response_model=List[InsurancePlan])
def get_available_plans(query: PlanQuery) -> List[InsurancePlan]:
    # In a real implementation, this would query a database
    # This is a simplified example with hardcoded data
    plans = [
        InsurancePlan(
            name="Basic Health",
            monthly_premium=200.0,
            coverage_amount=100000.0,
            coverage_type="health",
            features=["Emergency care", "Primary care", "Prescription drugs"]
        ),
        InsurancePlan(
            name="Premium Health",
            monthly_premium=400.0,
            coverage_amount=500000.0,
            coverage_type="health",
            features=["Emergency care", "Primary care", "Prescription drugs", "Specialist care", "Mental health"]
        ),
        # More plans would be defined here
    ]
    
    # Filter based on query parameters
    filtered_plans = plans
    if query.min_coverage is not None:
        filtered_plans = [p for p in filtered_plans if p.coverage_amount >= query.min_coverage]
    if query.max_premium is not None:
        filtered_plans = [p for p in filtered_plans if p.monthly_premium <= query.max_premium]
    if query.coverage_type is not None:
        filtered_plans = [p for p in filtered_plans if p.coverage_type == query.coverage_type]
    
    return filtered_plans

# Initialize the Claude model
model = AnthropicModel("claude-3-opus-20240229")

# Create the insurance recommendation agent
insurance_agent = Agent(
    model=model,
    system_prompt="""
    You are an AI insurance advisor. Your job is to recommend the most suitable insurance plan based on the customer's profile.
    
    Consider the following factors when making recommendations:
    1. Age and occupation affect risk assessment
    2. Income determines affordability
    3. Existing coverage should be complemented, not duplicated
    4. Risk factors may require specialized coverage
    
    Use the get_available_plans tool to retrieve insurance options, then analyze which plan best fits the customer's needs.
    Provide a clear rationale for your recommendation, including why the plan is suitable and any potential limitations.
    Rate the suitability of your recommendation on a scale of 1-10, where 10 is a perfect match.
    """,
    tools=[get_available_plans],
    result_type=InsuranceRecommendation
)

# Example usage
async def get_recommendation(customer: CustomerProfile) -> InsuranceRecommendation:
    result = await insurance_agent.run(
        f"Please recommend an insurance plan for this customer: {customer.json()}"
    )
    return result
```

## Integration with Aika AI System

For the Aika AI system, Pydantic AI offers several advantages:

1. **Structured Agent Definitions**: Define specialized insurance agents with strong typing
2. **Validation for Critical Data**: Ensure insurance recommendations and risk assessments are properly structured
3. **Multi-Model Support**: Flexibility to use Anthropic's Claude models as specified
4. **Production Readiness**: Built-in features for reliability and observability

### Implementation Strategy

1. **Define Core Data Models**:
   - Customer profiles
   - Insurance policies
   - Risk assessments
   - Recommendations

2. **Create Specialized Agents**:
   - Policy advisor agent
   - Risk assessment agent
   - Claims processing agent
   - Customer support agent

3. **Implement Tools**:
   - Database access tools
   - External API integrations
   - Document processing tools
   - Calculation and analysis tools

4. **Orchestrate with LangGraph**:
   - Use Pydantic AI for individual agents
   - Coordinate agents with LangGraph workflows

## Advantages Over Alternatives

### Compared to Raw LLM Calls

- **Structured Outputs**: Guaranteed valid, typed responses
- **Error Handling**: Automatic retries and validation
- **Tool Integration**: First-class support for function calling

### Compared to LangChain Agents

- **Type Safety**: Stronger typing and validation
- **Production Focus**: Better error handling and reliability features
- **Simplicity**: More focused API with less complexity

### Compared to Custom Solutions

- **Development Speed**: Faster to implement with pre-built components
- **Reliability**: Tested and maintained by the Pydantic team
- **Future-Proof**: Regular updates and model support

## Limitations and Considerations

1. **Newer Framework**: Less community content and examples compared to LangChain
2. **Learning Curve**: Requires understanding of Pydantic models and typing
3. **Integration Work**: May need custom integration with some services

## References

1. [Pydantic AI Official Documentation](https://ai.pydantic.dev/)
2. [Pydantic AI GitHub Repository](https://github.com/pydantic/pydantic-ai)
3. [Building Agents with Pydantic AI](https://medium.com/ai-agent-insider/pydantic-ai-agent-framework-02b138e8db71)
4. [Pydantic AI with Google Gemini](https://medium.com/google-cloud/how-i-built-an-agent-with-pydantic-ai-and-google-gemini-4887e5dd041d)
