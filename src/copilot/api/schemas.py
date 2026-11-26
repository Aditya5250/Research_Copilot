from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Application operational status")
    database: str = Field(default="unknown", description="Database connection health")
    environment: str = Field(default="development", description="Current runtime environment")
    version: str = Field(default="0.1.0", description="API version")


class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500, description="Research query or topic")
    max_loops: int = Field(default=3, ge=1, le=5, description="Maximum critic review iterations")
    enable_web: bool = Field(default=True, description="Enable Tavily web search")
    enable_rag: bool = Field(default=True, description="Enable local vector document search")
