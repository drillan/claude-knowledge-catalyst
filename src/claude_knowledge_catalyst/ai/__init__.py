"""AI assistance module for Claude Knowledge Catalyst."""

from .ai_assistant import AIKnowledgeAssistant, create_ai_assistant
from .smart_classifier import SmartContentClassifier
from .yake_extractor import (
    YAKEConfig,
    YAKEKeywordExtractor,
    Keyword,
    create_yake_extractor,
    YAKE_AVAILABLE
)

__all__ = [
    "AIKnowledgeAssistant",
    "create_ai_assistant",
    "SmartContentClassifier",
    "YAKEConfig",
    "YAKEKeywordExtractor", 
    "Keyword",
    "create_yake_extractor",
    "YAKE_AVAILABLE"
]