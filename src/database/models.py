"""
Database models for the Aika AI System.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Agent types."""
    MARKET_RESEARCH = "market_research"
    REGULATORY_COMPLIANCE = "regulatory_compliance"
    DATA_PREPROCESSING = "data_preprocessing"
    MODEL_TRAINING = "model_training"
    CUSTOMER_SERVICE = "customer_service"
    RISK_ASSESSMENT = "risk_assessment"
    POLICY_MANAGEMENT = "policy_management"
    CLAIMS_PROCESSING = "claims_processing"


class AgentStatus(str, Enum):
    """Agent status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"


class Agent(BaseModel):
    """Agent model."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    type: AgentType
    status: AgentStatus = AgentStatus.ACTIVE
    capabilities: List[str]
    model_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationStatus(str, Enum):
    """Conversation status."""
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class Message(BaseModel):
    """Message model."""
    id: UUID = Field(default_factory=uuid4)
    conversation_id: UUID
    sender_id: Union[UUID, str]  # Can be user ID or agent ID
    sender_type: str  # "user" or "agent"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict] = None


class Conversation(BaseModel):
    """Conversation model."""
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    status: ConversationStatus = ConversationStatus.ACTIVE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[dict] = None
    messages: List[Message] = []


class User(BaseModel):
    """User model."""
    id: UUID = Field(default_factory=uuid4)
    email: str
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    preferences: Optional[dict] = None
