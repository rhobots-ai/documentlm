from typing import Dict, Any, List, Optional

from pydantic import BaseModel, Field

from .config import DEFAULT_SETTINGS


class ChatRequestModel(BaseModel):
    chat_input: Dict[str, Any] = {}
    chat_history: List[Any] = []
    user_id: str = ""
    settings: Dict[str, Any] = Field(default_factory=lambda: DEFAULT_SETTINGS)
    conv_id: Optional[str] = None
    conv_name: Optional[str] = None
    first_selector_choices: List[Any] = []
    is_conversation_flow: bool = False
    selecteds: List[Any] = []
    reasoning_type: Optional[str] = None
    llm_type: str = ""
    use_mind_map: bool = True
    use_citation: str = "highlight"
    language: str = "en"
    chat_state: Dict[str, Any] = Field(default_factory=lambda: {"app": {}})
    stream: bool = False


# These models are only for documentation, actual handling is more permissive
class DocumentRef(BaseModel):
    ref_id: str = ""
    document_name: str = ""
    page: int = 0
    citation_id: Optional[str] = None
    relevance_score: Dict[str, Any] = Field(default_factory=dict)
    preview_link: str = ""
    original_link_path: str = ""
    search_terms: str = ""
    is_highlighted: bool = False
    content: Dict[str, Any] = Field(default_factory=dict)
    citation_style: Optional[str] = None


class ChatResponseModel(BaseModel):
    chat_history: List[Dict[str, Any]] = []
    document_ref: List[Dict[str, Any]] = []
    token_usage: Optional[Dict[str, Any]] = None
    mindmap: Optional[Any] = None
    plot: Optional[Any] = None
    chat_state: Dict[str, Any] = Field(default_factory=lambda: {"app": {}})
    conv_id: Optional[str] = None
    chunk_id: Optional[str] = None
    conversation_name: Optional[str] = None
