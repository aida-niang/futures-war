"""
Pydantic models for request/response validation.
Aligned with openapi.json specification.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TranscriptionRequest(BaseModel):
    """Speech-to-text request (legacy base64)"""
    audio_base64: str = Field(..., description="Audio file encoded as base64")


class TranscriptionResponse(BaseModel):
    """Speech-to-text response"""
    text: str = Field(..., description="Transcribed text")
    confidence: float = Field(default=0.9, description="Confidence score (0-1)")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class PromptToImageRequest(BaseModel):
    """Prompt-to-image request (Aligned with OpenAPI)"""
    prompt: str = Field(..., description="Description of image to generate")
    model: Optional[str] = Field(
        default="Tongyi-MAI/Z-Image-Turbo",
        description="Model choice: Tongyi-MAI/Z-Image-Turbo or Tongyi-MAI/Z-Image"
    )
    steps: Optional[int] = Field(default=9, description="Number of sampling steps")
    guidance_scale: Optional[float] = Field(default=1.0, description="Guidance scale")
    height: Optional[int] = Field(default=1024, description="Image height in pixels")
    width: Optional[int] = Field(default=1024, description="Image width in pixels")
    negative_prompt: Optional[str] = Field(default=None, description="What to avoid")
    seed: Optional[int] = Field(default=None, description="Random seed")


class PromptToImageResponse(BaseModel):
    """Prompt-to-image response (Aligned with OpenAPI)"""
    images: List[str] = Field(..., description="Generated images (base64 or URLs)")
    model: str = Field(..., description="Model used")


class ModerationRequest(BaseModel):
    """Content moderation request"""
    text: str = Field(..., description="Text to moderate")


class ModerationResponse(BaseModel):
    """Content moderation response"""
    is_safe: bool = Field(..., description="Whether content is safe")
    reason: str = Field(..., description="Safety reason/explanation")
    flagged_content: Optional[List[str]] = Field(default=None, description="Flagged keywords")


class EnrichmentRequest(BaseModel):
    """Prompt enrichment request"""
    text: str = Field(..., description="Original text to enrich")


class EnrichmentResponse(BaseModel):
    """Prompt enrichment response"""
    original: str = Field(..., description="Original text")
    enriched: str = Field(..., description="Enriched prompt")
    vocabulary_added: List[str] = Field(default=[], description="Vocabulary items added")


class ProcessRequest(BaseModel):
    """Complete pipeline request (audio → text → image)"""
    audio_base64: str = Field(..., description="Audio as base64")


class ProcessResponse(BaseModel):
    """Complete pipeline response"""
    original_text: str = Field(..., description="Transcribed text")
    enriched_prompt: str = Field(..., description="Enriched prompt")
    is_safe: bool = Field(..., description="Safety check result")
    image_url: str = Field(..., description="Generated image URL")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class SystemStatsResponse(BaseModel):
    """System statistics response"""
    cpu: Dict[str, Any] = Field(..., description="CPU info")
    ram: Dict[str, Any] = Field(..., description="RAM info")
    gpus: Optional[List[Dict[str, Any]]] = Field(default=[], description="GPU info")
    disk: Optional[Dict[str, Any]] = Field(default=None, description="Disk info")
    uptime_seconds: Optional[float] = Field(default=None, description="System uptime")
    whisper: Dict[str, str] = Field(..., description="Whisper config")
    ollama: Dict[str, str] = Field(..., description="Ollama config")
    zimage: Dict[str, Any] = Field(..., description="Z-Image config")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ChatCompletionMessage(BaseModel):
    """Chat message"""
    role: str = Field(..., description="Role: system, user, or assistant")
    content: str = Field(..., description="Message content")


class ChatCompletionRequest(BaseModel):
    """Chat completions request (OpenAI format)"""
    model: str = Field(..., description="Model name (e.g., llama3.2:1b)")
    messages: List[ChatCompletionMessage] = Field(..., description="Message history")
    stream: bool = Field(default=False, description="Stream response")
    temperature: Optional[float] = Field(default=0.7, description="Temperature (0-2)")
    max_tokens: Optional[int] = Field(default=None, description="Max output tokens")


class ChatCompletionChoice(BaseModel):
    """Chat completion choice"""
    index: int
    message: ChatCompletionMessage
    finish_reason: str


class ChatCompletionUsage(BaseModel):
    """Token usage"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """Chat completions response (OpenAI format)"""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str = Field(..., description="Error message")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())