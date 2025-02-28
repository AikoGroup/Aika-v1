"""
Base agent interface for the Aika AI System.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..utils.logging import get_logger

# Get logger
logger = get_logger(__name__)


class BaseAgent(ABC):
    """
    Base agent interface that all specialized agents must implement.
    """
    
    def __init__(self, agent_id: str, name: str, description: str, capabilities: List[str]):
        """
        Initialize the agent.
        
        Args:
            agent_id: Agent ID
            name: Agent name
            description: Agent description
            capabilities: Agent capabilities
        """
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.capabilities = capabilities
        
        logger.info(f"Initializing agent '{name}' ({agent_id})")
        
    @abstractmethod
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a request.
        
        Args:
            request: Request data
            
        Returns:
            Response data
        """
        pass
        
    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.
        
        Returns:
            Agent information
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
        }
        
    @abstractmethod
    async def can_handle(self, request: Dict[str, Any]) -> bool:
        """
        Check if the agent can handle the request.
        
        Args:
            request: Request data
            
        Returns:
            True if the agent can handle the request, False otherwise
        """
        pass


class AgentRegistry:
    """
    Registry for managing agent instances.
    """
    
    def __init__(self):
        """Initialize the agent registry."""
        self.agents: Dict[str, BaseAgent] = {}
        
    def register(self, agent: BaseAgent) -> None:
        """
        Register an agent.
        
        Args:
            agent: Agent instance
        """
        logger.info(f"Registering agent '{agent.name}' ({agent.agent_id})")
        self.agents[agent.agent_id] = agent
        
    def unregister(self, agent_id: str) -> None:
        """
        Unregister an agent.
        
        Args:
            agent_id: Agent ID
        """
        if agent_id in self.agents:
            logger.info(f"Unregistering agent '{self.agents[agent_id].name}' ({agent_id})")
            del self.agents[agent_id]
        else:
            logger.warning(f"Agent '{agent_id}' not found, cannot unregister")
            
    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get an agent by ID.
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent instance or None if not found
        """
        return self.agents.get(agent_id)
        
    def list(self) -> List[BaseAgent]:
        """
        List all registered agents.
        
        Returns:
            List of agent instances
        """
        return list(self.agents.values())
        
    async def find_agent_for_request(self, request: Dict[str, Any]) -> Optional[BaseAgent]:
        """
        Find an agent that can handle the request.
        
        Args:
            request: Request data
            
        Returns:
            Agent instance or None if no agent can handle the request
        """
        for agent in self.agents.values():
            if await agent.can_handle(request):
                return agent
                
        return None


# Singleton instance
_registry: Optional[AgentRegistry] = None


def get_agent_registry() -> AgentRegistry:
    """
    Get the agent registry instance.
    
    Returns:
        Agent registry instance
    """
    global _registry
    
    if _registry is None:
        _registry = AgentRegistry()
        
    return _registry
