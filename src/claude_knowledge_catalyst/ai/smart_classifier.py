"""Intelligent content classification system for pure tag-centered approach."""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum

from ..core.metadata import KnowledgeMetadata
from ..core.tag_standards import TagStandardsManager


class ConfidenceLevel(Enum):
    """Confidence levels for AI classifications."""
    VERY_HIGH = 0.9
    HIGH = 0.75
    MEDIUM = 0.6
    LOW = 0.4
    VERY_LOW = 0.2


@dataclass
class ClassificationResult:
    """Result of content classification."""
    tag_type: str
    suggested_value: str
    confidence: float
    reasoning: str
    evidence: List[str]


class SmartContentClassifier:
    """AI-powered content classifier using pattern recognition and NLP."""
    
    def __init__(self):
        self.tag_standards = TagStandardsManager()
        self._initialize_patterns()
    
    def _initialize_patterns(self) -> None:
        """Initialize pattern recognition dictionaries."""
        
        # Technology patterns with confidence weights
        self.tech_patterns = {
            'python': {
                'high_confidence': ['def ', 'import ', 'from ', '__init__', 'pip install', '.py', 'python'],
                'medium_confidence': ['py', 'conda', 'virtual environment', 'venv'],
                'keywords': ['django', 'flask', 'fastapi', 'pandas', 'numpy', 'scipy', 'matplotlib']
            },
            'javascript': {
                'high_confidence': ['const ', 'let ', 'var ', 'function(', '=>', 'npm install', '.js'],
                'medium_confidence': ['js', 'node', 'javascript'],
                'keywords': ['react', 'vue', 'angular', 'express', 'typescript', 'webpack']
            },
            'typescript': {
                'high_confidence': ['interface ', 'type ', ': string', ': number', '.ts', '.tsx'],
                'medium_confidence': ['typescript', 'ts'],
                'keywords': ['angular', 'nest', 'type definition']
            },
            'react': {
                'high_confidence': ['jsx', 'component', 'props', 'state', 'usestate', 'useeffect'],
                'medium_confidence': ['react'],
                'keywords': ['hook', 'render', 'virtual dom']
            },
            'docker': {
                'high_confidence': ['dockerfile', 'docker build', 'docker run', 'container'],
                'medium_confidence': ['docker'],
                'keywords': ['image', 'compose', 'kubernetes', 'containerize']
            },
            'aws': {
                'high_confidence': ['aws-cli', 's3 bucket', 'ec2 instance', 'lambda function'],
                'medium_confidence': ['aws', 'amazon web services'],
                'keywords': ['cloudformation', 'iam', 'vpc', 'rds', 'cloudwatch']
            },
            'git': {
                'high_confidence': ['git clone', 'git commit', 'git push', 'git pull', 'git merge'],
                'medium_confidence': ['git'],
                'keywords': ['github', 'gitlab', 'repository', 'branch', 'merge request']
            }
        }
        
        # Domain patterns
        self.domain_patterns = {
            'web-dev': {
                'high_confidence': ['frontend', 'backend', 'web application', 'api endpoint', 'http request'],
                'medium_confidence': ['web', 'server', 'client'],
                'keywords': ['rest', 'graphql', 'microservice', 'spa', 'ssr']
            },
            'data-science': {
                'high_confidence': ['data analysis', 'machine learning', 'dataset', 'model training'],
                'medium_confidence': ['data', 'analytics', 'ml'],
                'keywords': ['pandas', 'numpy', 'scikit-learn', 'jupyter', 'visualization']
            },
            'devops': {
                'high_confidence': ['ci/cd', 'deployment', 'infrastructure', 'monitoring'],
                'medium_confidence': ['devops'],
                'keywords': ['jenkins', 'terraform', 'ansible', 'kubernetes', 'docker']
            },
            'mobile-dev': {
                'high_confidence': ['mobile app', 'ios development', 'android development'],
                'medium_confidence': ['mobile'],
                'keywords': ['react native', 'flutter', 'swift', 'kotlin', 'app store']
            },
            'cybersecurity': {
                'high_confidence': ['security vulnerability', 'penetration testing', 'encryption'],
                'medium_confidence': ['security', 'secure'],
                'keywords': ['authentication', 'authorization', 'ssl', 'https', 'firewall']
            }
        }
        
        # Content type patterns
        self.type_patterns = {
            'prompt': {
                'high_confidence': ['claude', 'gpt', 'ai assistant', 'prompt:', 'ask the ai'],
                'medium_confidence': ['prompt', 'generate', 'ai'],
                'keywords': ['instruction', 'query', 'request', 'question']
            },
            'code': {
                'high_confidence': ['```', 'def ', 'function', 'class ', 'import ', 'const '],
                'medium_confidence': ['code', 'script', 'program'],
                'keywords': ['algorithm', 'implementation', 'snippet', 'example']
            },
            'concept': {
                'high_confidence': ['concept:', 'theory', 'principle', 'methodology'],
                'medium_confidence': ['concept', 'explanation', 'overview'],
                'keywords': ['definition', 'understanding', 'approach', 'framework']
            },
            'resource': {
                'high_confidence': ['resource:', 'link:', 'reference:', 'documentation:'],
                'medium_confidence': ['resource', 'link', 'reference'],
                'keywords': ['tool', 'library', 'framework', 'guide', 'tutorial']
            }
        }
        
        # Claude feature patterns
        self.claude_feature_patterns = {
            'code-generation': {
                'high_confidence': ['generate code', 'create function', 'write script'],
                'medium_confidence': ['generate', 'create', 'build'],
                'keywords': ['implement', 'develop', 'program']
            },
            'analysis': {
                'high_confidence': ['analyze', 'review', 'examine', 'evaluate'],
                'medium_confidence': ['analysis', 'assessment'],
                'keywords': ['investigate', 'study', 'inspect']
            },
            'debugging': {
                'high_confidence': ['debug', 'troubleshoot', 'fix error', 'resolve issue'],
                'medium_confidence': ['debug', 'error', 'bug'],
                'keywords': ['problem', 'issue', 'failure', 'exception']
            },
            'documentation': {
                'high_confidence': ['document', 'readme', 'guide', 'manual'],
                'medium_confidence': ['documentation', 'docs'],
                'keywords': ['explain', 'describe', 'instruction', 'how-to']
            },
            'optimization': {
                'high_confidence': ['optimize', 'improve performance', 'enhance'],
                'medium_confidence': ['optimization', 'performance'],
                'keywords': ['efficient', 'faster', 'better', 'speed up']
            }
        }
        
        # Complexity indicators
        self.complexity_indicators = {
            'beginner': {
                'keywords': ['beginner', 'basic', 'simple', 'easy', 'introduction', 'getting started'],
                'content_patterns': ['step by step', 'tutorial', 'how to'],
                'length_threshold': 500
            },
            'intermediate': {
                'keywords': ['intermediate', 'moderate', 'standard', 'common'],
                'content_patterns': ['best practices', 'implementation', 'example'],
                'length_threshold': 1500
            },
            'advanced': {
                'keywords': ['advanced', 'complex', 'sophisticated', 'deep dive'],
                'content_patterns': ['architecture', 'performance', 'scalability'],
                'length_threshold': 3000
            },
            'expert': {
                'keywords': ['expert', 'cutting-edge', 'research', 'novel'],
                'content_patterns': ['experimental', 'bleeding edge', 'state-of-the-art'],
                'length_threshold': 5000
            }
        }
    
    def classify_content(self, content: str, existing_metadata: Optional[KnowledgeMetadata] = None) -> List[ClassificationResult]:
        """Classify content and return suggestions with confidence scores."""
        results = []
        content_lower = content.lower()
        
        # Classify technology tags
        tech_results = self._classify_technology(content_lower)
        results.extend(tech_results)
        
        # Classify domain
        domain_results = self._classify_domain(content_lower)
        results.extend(domain_results)
        
        # Classify content type
        type_results = self._classify_content_type(content_lower)
        results.extend(type_results)
        
        # Classify Claude features
        feature_results = self._classify_claude_features(content_lower)
        results.extend(feature_results)
        
        # Classify complexity
        complexity_results = self._classify_complexity(content, content_lower)
        results.extend(complexity_results)
        
        # Classify confidence level
        confidence_results = self._classify_confidence(content_lower)
        results.extend(confidence_results)
        
        # Sort by confidence and remove duplicates
        results = self._deduplicate_results(results)
        results.sort(key=lambda x: x.confidence, reverse=True)
        
        return results[:15]  # Return top 15 suggestions
    
    def _classify_technology(self, content: str) -> List[ClassificationResult]:
        """Classify technology tags."""
        results = []
        
        for tech, patterns in self.tech_patterns.items():
            confidence = 0.0
            evidence = []
            
            # Check high confidence patterns
            for pattern in patterns['high_confidence']:
                if pattern in content:
                    confidence = max(confidence, ConfidenceLevel.HIGH.value)
                    evidence.append(f"Found '{pattern}'")
            
            # Check medium confidence patterns
            for pattern in patterns['medium_confidence']:
                if pattern in content:
                    confidence = max(confidence, ConfidenceLevel.MEDIUM.value)
                    evidence.append(f"Contains '{pattern}'")
            
            # Check keyword patterns
            keyword_matches = sum(1 for keyword in patterns['keywords'] if keyword in content)
            if keyword_matches > 0:
                confidence = max(confidence, ConfidenceLevel.MEDIUM.value - 0.1)
                evidence.append(f"Related keywords: {keyword_matches} matches")
            
            if confidence > ConfidenceLevel.LOW.value:
                reasoning = f"Technology patterns detected for {tech}"
                results.append(ClassificationResult(
                    tag_type="tech",
                    suggested_value=tech,
                    confidence=confidence,
                    reasoning=reasoning,
                    evidence=evidence
                ))
        
        return results
    
    def _classify_domain(self, content: str) -> List[ClassificationResult]:
        """Classify domain tags."""
        results = []
        
        for domain, patterns in self.domain_patterns.items():
            confidence = 0.0
            evidence = []
            
            # Check high confidence patterns
            for pattern in patterns['high_confidence']:
                if pattern in content:
                    confidence = max(confidence, ConfidenceLevel.HIGH.value)
                    evidence.append(f"Found '{pattern}'")
            
            # Check medium confidence patterns
            for pattern in patterns['medium_confidence']:
                if pattern in content:
                    confidence = max(confidence, ConfidenceLevel.MEDIUM.value)
                    evidence.append(f"Contains '{pattern}'")
            
            # Check keyword patterns
            keyword_matches = sum(1 for keyword in patterns['keywords'] if keyword in content)
            if keyword_matches > 0:
                confidence = max(confidence, ConfidenceLevel.MEDIUM.value - 0.1)
                evidence.append(f"Domain keywords: {keyword_matches} matches")
            
            if confidence > ConfidenceLevel.LOW.value:
                reasoning = f"Domain patterns detected for {domain}"
                results.append(ClassificationResult(
                    tag_type="domain",
                    suggested_value=domain,
                    confidence=confidence,
                    reasoning=reasoning,
                    evidence=evidence
                ))
        
        return results
    
    def _classify_content_type(self, content: str) -> List[ClassificationResult]:
        """Classify content type."""
        results = []
        
        for content_type, patterns in self.type_patterns.items():
            confidence = 0.0
            evidence = []
            
            # Check high confidence patterns
            for pattern in patterns['high_confidence']:
                if pattern in content:
                    confidence = max(confidence, ConfidenceLevel.HIGH.value)
                    evidence.append(f"Found '{pattern}'")
            
            # Check medium confidence patterns
            for pattern in patterns['medium_confidence']:
                if pattern in content:
                    confidence = max(confidence, ConfidenceLevel.MEDIUM.value)
                    evidence.append(f"Contains '{pattern}'")
            
            # Check keyword patterns
            keyword_matches = sum(1 for keyword in patterns['keywords'] if keyword in content)
            if keyword_matches > 0:
                confidence = max(confidence, ConfidenceLevel.MEDIUM.value - 0.1)
                evidence.append(f"Type keywords: {keyword_matches} matches")
            
            if confidence > ConfidenceLevel.LOW.value:
                reasoning = f"Content type patterns detected for {content_type}"
                results.append(ClassificationResult(
                    tag_type="type",
                    suggested_value=content_type,
                    confidence=confidence,
                    reasoning=reasoning,
                    evidence=evidence
                ))
        
        return results
    
    def _classify_claude_features(self, content: str) -> List[ClassificationResult]:
        """Classify Claude features."""
        results = []
        
        for feature, patterns in self.claude_feature_patterns.items():
            confidence = 0.0
            evidence = []
            
            # Check high confidence patterns
            for pattern in patterns['high_confidence']:
                if pattern in content:
                    confidence = max(confidence, ConfidenceLevel.HIGH.value)
                    evidence.append(f"Found '{pattern}'")
            
            # Check medium confidence patterns
            for pattern in patterns['medium_confidence']:
                if pattern in content:
                    confidence = max(confidence, ConfidenceLevel.MEDIUM.value)
                    evidence.append(f"Contains '{pattern}'")
            
            # Check keyword patterns
            keyword_matches = sum(1 for keyword in patterns['keywords'] if keyword in content)
            if keyword_matches > 0:
                confidence = max(confidence, ConfidenceLevel.MEDIUM.value - 0.1)
                evidence.append(f"Feature keywords: {keyword_matches} matches")
            
            if confidence > ConfidenceLevel.LOW.value:
                reasoning = f"Claude feature patterns detected for {feature}"
                results.append(ClassificationResult(
                    tag_type="claude_feature",
                    suggested_value=feature,
                    confidence=confidence,
                    reasoning=reasoning,
                    evidence=evidence
                ))
        
        return results
    
    def _classify_complexity(self, content: str, content_lower: str) -> List[ClassificationResult]:
        """Classify complexity level."""
        results = []
        content_length = len(content)
        
        for complexity, indicators in self.complexity_indicators.items():
            confidence = 0.0
            evidence = []
            
            # Check keywords
            keyword_matches = sum(1 for keyword in indicators['keywords'] if keyword in content_lower)
            if keyword_matches > 0:
                confidence = max(confidence, ConfidenceLevel.MEDIUM.value)
                evidence.append(f"Complexity keywords: {keyword_matches} matches")
            
            # Check content patterns
            pattern_matches = sum(1 for pattern in indicators['content_patterns'] if pattern in content_lower)
            if pattern_matches > 0:
                confidence = max(confidence, ConfidenceLevel.MEDIUM.value - 0.1)
                evidence.append(f"Content patterns: {pattern_matches} matches")
            
            # Check length-based heuristics
            if complexity == 'beginner' and content_length < indicators['length_threshold']:
                confidence = max(confidence, ConfidenceLevel.LOW.value + 0.1)
                evidence.append(f"Short content ({content_length} chars)")
            elif complexity == 'expert' and content_length > indicators['length_threshold']:
                confidence = max(confidence, ConfidenceLevel.LOW.value + 0.1)
                evidence.append(f"Long content ({content_length} chars)")
            elif complexity in ['intermediate', 'advanced']:
                if indicators['length_threshold'] * 0.5 < content_length < indicators['length_threshold'] * 2:
                    confidence = max(confidence, ConfidenceLevel.LOW.value)
                    evidence.append(f"Moderate length ({content_length} chars)")
            
            if confidence > ConfidenceLevel.LOW.value:
                reasoning = f"Complexity indicators suggest {complexity} level"
                results.append(ClassificationResult(
                    tag_type="complexity",
                    suggested_value=complexity,
                    confidence=confidence,
                    reasoning=reasoning,
                    evidence=evidence
                ))
        
        return results
    
    def _classify_confidence(self, content: str) -> List[ClassificationResult]:
        """Classify confidence level based on content quality indicators."""
        results = []
        
        # High confidence indicators
        high_confidence_patterns = [
            'tested', 'proven', 'production', 'verified', 'validated',
            'best practice', 'recommended', 'standard', 'official'
        ]
        
        # Low confidence indicators
        low_confidence_patterns = [
            'draft', 'experimental', 'wip', 'work in progress', 'todo',
            'untested', 'rough', 'initial', 'placeholder'
        ]
        
        high_matches = sum(1 for pattern in high_confidence_patterns if pattern in content)
        low_matches = sum(1 for pattern in low_confidence_patterns if pattern in content)
        
        if high_matches > low_matches and high_matches > 0:
            results.append(ClassificationResult(
                tag_type="confidence",
                suggested_value="high",
                confidence=ConfidenceLevel.MEDIUM.value,
                reasoning="Quality indicators suggest high confidence",
                evidence=[f"Found {high_matches} quality indicators"]
            ))
        elif low_matches > high_matches and low_matches > 0:
            results.append(ClassificationResult(
                tag_type="confidence",
                suggested_value="low",
                confidence=ConfidenceLevel.MEDIUM.value,
                reasoning="Draft/experimental indicators found",
                evidence=[f"Found {low_matches} draft indicators"]
            ))
        else:
            results.append(ClassificationResult(
                tag_type="confidence",
                suggested_value="medium",
                confidence=ConfidenceLevel.LOW.value + 0.1,
                reasoning="No clear confidence indicators",
                evidence=["Default medium confidence"]
            ))
        
        return results
    
    def _deduplicate_results(self, results: List[ClassificationResult]) -> List[ClassificationResult]:
        """Remove duplicate suggestions, keeping the highest confidence."""
        seen = {}
        
        for result in results:
            key = (result.tag_type, result.suggested_value)
            if key not in seen or result.confidence > seen[key].confidence:
                seen[key] = result
        
        return list(seen.values())
    
    def batch_classify_files(self, file_paths: List[Path], progress_callback=None) -> Dict[Path, List[ClassificationResult]]:
        """Batch classify multiple files."""
        results = {}
        
        for i, file_path in enumerate(file_paths):
            if progress_callback:
                progress_callback(i, len(file_paths), file_path.name)
            
            try:
                content = file_path.read_text(encoding="utf-8")
                classifications = self.classify_content(content)
                results[file_path] = classifications
            except Exception as e:
                # Log error but continue processing
                results[file_path] = []
        
        return results
    
    def get_classification_summary(self, results: Dict[Path, List[ClassificationResult]]) -> Dict[str, any]:
        """Generate summary statistics for batch classification."""
        summary = {
            "total_files": len(results),
            "files_with_suggestions": 0,
            "top_technologies": {},
            "top_domains": {},
            "content_types": {},
            "confidence_distribution": {"high": 0, "medium": 0, "low": 0}
        }
        
        for file_path, classifications in results.items():
            if classifications:
                summary["files_with_suggestions"] += 1
                
                for classification in classifications:
                    # Count technologies
                    if classification.tag_type == "tech":
                        tech = classification.suggested_value
                        summary["top_technologies"][tech] = summary["top_technologies"].get(tech, 0) + 1
                    
                    # Count domains
                    elif classification.tag_type == "domain":
                        domain = classification.suggested_value
                        summary["top_domains"][domain] = summary["top_domains"].get(domain, 0) + 1
                    
                    # Count content types
                    elif classification.tag_type == "type":
                        content_type = classification.suggested_value
                        summary["content_types"][content_type] = summary["content_types"].get(content_type, 0) + 1
                    
                    # Count confidence levels
                    if classification.confidence >= ConfidenceLevel.HIGH.value:
                        summary["confidence_distribution"]["high"] += 1
                    elif classification.confidence >= ConfidenceLevel.MEDIUM.value:
                        summary["confidence_distribution"]["medium"] += 1
                    else:
                        summary["confidence_distribution"]["low"] += 1
        
        return summary