"""Template management system for knowledge files."""

from pathlib import Path
from typing import Any, Dict, List, Optional

from jinja2 import Environment, FileSystemLoader, Template

from ..core.metadata import KnowledgeMetadata


class TemplateManager:
    """Manager for template operations."""
    
    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize template manager.
        
        Args:
            template_dir: Directory containing template files
        """
        self.template_dir = template_dir or Path(__file__).parent / "templates"
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def _create_default_templates(self) -> None:
        """Create default template files."""
        templates = {
            "prompt.md": self._get_prompt_template(),
            "code_snippet.md": self._get_code_snippet_template(),
            "concept.md": self._get_concept_template(),
            "project_log.md": self._get_project_log_template(),
            "improvement_log.md": self._get_improvement_log_template(),
        }
        
        for filename, content in templates.items():
            template_path = self.template_dir / filename
            if not template_path.exists():
                template_path.write_text(content, encoding="utf-8")
    
    def get_template(self, template_name: str) -> Template:
        """Get a template by name.
        
        Args:
            template_name: Name of the template file
            
        Returns:
            Jinja2 Template object
        """
        return self.env.get_template(template_name)
    
    def list_templates(self) -> List[str]:
        """List available templates.
        
        Returns:
            List of template filenames
        """
        if not self.template_dir.exists():
            return []
        
        return [f.name for f in self.template_dir.glob("*.md")]
    
    def create_from_template(
        self,
        template_name: str,
        output_path: Path,
        variables: Dict[str, Any],
    ) -> bool:
        """Create a file from a template.
        
        Args:
            template_name: Name of the template to use
            output_path: Where to save the generated file
            variables: Variables to pass to the template
            
        Returns:
            True if successful, False otherwise
        """
        try:
            template = self.get_template(template_name)
            content = template.render(**variables)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            output_path.write_text(content, encoding="utf-8")
            return True
            
        except Exception as e:
            print(f"Error creating file from template: {e}")
            return False
    
    def create_prompt_file(
        self,
        title: str,
        purpose: str,
        output_path: Path,
        model: str = "Claude 3 Opus",
        category: str = "prompt",
        tags: Optional[List[str]] = None,
    ) -> bool:
        """Create a new prompt file from template.
        
        Args:
            title: Title of the prompt
            purpose: Purpose/description of the prompt
            output_path: Where to save the file
            model: Claude model to use
            category: Category for the prompt
            tags: List of tags
            
        Returns:
            True if successful
        """
        from datetime import datetime
        
        variables = {
            "title": title,
            "purpose": purpose,
            "model": model,
            "category": category,
            "tags": tags or [],
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "status": "draft",
        }
        
        return self.create_from_template("prompt.md", output_path, variables)
    
    def create_code_snippet_file(
        self,
        title: str,
        language: str,
        description: str,
        output_path: Path,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """Create a new code snippet file from template.
        
        Args:
            title: Title of the code snippet
            language: Programming language
            description: Description of the code
            output_path: Where to save the file
            tags: List of tags
            
        Returns:
            True if successful
        """
        from datetime import datetime
        
        variables = {
            "title": title,
            "language": language,
            "description": description,
            "tags": tags or [language.lower(), "code"],
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "status": "draft",
        }
        
        return self.create_from_template("code_snippet.md", output_path, variables)
    
    def create_concept_file(
        self,
        title: str,
        summary: str,
        output_path: Path,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """Create a new concept file from template.
        
        Args:
            title: Title of the concept
            summary: Brief summary
            output_path: Where to save the file
            tags: List of tags
            
        Returns:
            True if successful
        """
        from datetime import datetime
        
        variables = {
            "title": title,
            "summary": summary,
            "tags": tags or ["concept"],
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0",
            "status": "draft",
        }
        
        return self.create_from_template("concept.md", output_path, variables)
    
    def _get_prompt_template(self) -> str:
        """Get the default prompt template."""
        return '''---
title: "{{ title }}"
created: "{{ created_date }}"
updated: "{{ created_date }}"
version: {{ version }}
model: "{{ model }}"
category: "{{ category }}"
status: "{{ status }}"
success_rate: 0
purpose: "{{ purpose }}"
tags: [{{ tags | join(', ') }}]
---

# {{ title }}

## Purpose and Background
{{ purpose }}

## Prompt Text
```
[Your prompt text here]
```

## Expected Output
[Describe what you expect Claude to return]

## Usage Examples

### Example 1
**Input:**
```
[Example input]
```

**Claude Response:**
```
[Expected response]
```

## Evaluation and Analysis

### Success Criteria
- [ ] [Define success criteria]
- [ ] [Another criteria]

### Current Issues
- [List any current problems or limitations]

### Improvement Ideas
- [List potential improvements]

## Version History

### Version 1.0 ({{ created_date }})
- Initial version
- **Changes:** Initial creation
- **Success Rate:** TBD

## Related Links
- [[Related Prompt or Concept]]
- [[Another Related Item]]
'''
    
    def _get_code_snippet_template(self) -> str:
        """Get the default code snippet template."""
        return '''---
title: "{{ title }}"
created: "{{ created_date }}"
updated: "{{ created_date }}"
version: {{ version }}
language: "{{ language }}"
category: "code"
status: "{{ status }}"
tags: [{{ tags | join(', ') }}]
---

# {{ title }}

## Description
{{ description }}

## Code
```{{ language }}
# Your code here
```

## Usage
[Explain how to use this code snippet]

## Parameters
- `param1`: Description
- `param2`: Description

## Returns
[Describe what the code returns]

## Examples
```{{ language }}
# Example usage
```

## Notes
- [Any important notes or considerations]
- [Performance considerations]
- [Dependencies or requirements]

## Related Links
- [[Related Code or Concept]]
'''
    
    def _get_concept_template(self) -> str:
        """Get the default concept template."""
        return '''---
title: "{{ title }}"
created: "{{ created_date }}"
updated: "{{ created_date }}"
version: {{ version }}
category: "concept"
status: "{{ status }}"
tags: [{{ tags | join(', ') }}]
---

# {{ title }}

## Summary
{{ summary }}

## Key Points
- [Main point 1]
- [Main point 2]
- [Main point 3]

## Detailed Explanation
[Provide detailed explanation of the concept]

## Applications
- [Where/how this concept is used]
- [Practical applications]

## Examples
### Example 1
[Concrete example]

### Example 2
[Another example]

## Related Concepts
- [[Related Concept 1]]
- [[Related Concept 2]]

## Resources
- [External links or references]
- [Books, articles, documentation]

## Notes
[Any additional notes or personal insights]
'''
    
    def _get_project_log_template(self) -> str:
        """Get the default project log template."""
        return '''---
title: "{{ title }}"
created: "{{ created_date }}"
updated: "{{ created_date }}"
version: {{ version }}
category: "project_log"
status: "{{ status }}"
project: "{{ project_name | default('Unknown') }}"
tags: [{{ tags | join(', ') }}]
---

# {{ title }}

## Project Context
**Project:** {{ project_name | default('Unknown') }}
**Date:** {{ created_date }}
**Phase:** [Development/Testing/Deployment]

## Objective
[What were you trying to accomplish?]

## Actions Taken
1. [Action 1]
2. [Action 2]
3. [Action 3]

## Results
### What Worked
- [Successful outcomes]

### What Didn't Work
- [Issues encountered]

### Lessons Learned
- [Key insights or learnings]

## Claude Interactions
### Prompt Used
```
[The prompt you used with Claude]
```

### Claude Response Quality
**Rating:** [1-5 stars]
**Feedback:** [What was good/bad about the response]

## Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]

## Related Items
- [[Related Project Log]]
- [[Related Prompt]]
- [[Related Code]]
'''
    
    def _get_improvement_log_template(self) -> str:
        """Get the default improvement log template."""
        return '''---
title: "{{ title }}"
created: "{{ created_date }}"
updated: "{{ created_date }}"
version: {{ version }}
category: "improvement_log"
status: "{{ status }}"
original_item: "{{ original_item | default('') }}"
tags: [{{ tags | join(', ') }}]
---

# {{ title }}

## Original Item
**Reference:** [[{{ original_item }}]]
**Issue Date:** {{ created_date }}

## Problem Identified
[Describe the issue or area for improvement]

## Analysis
### Root Cause
[What caused the issue?]

### Impact
[How did this affect the outcome?]

## Improvement Strategy
### Approach
[How did you decide to fix this?]

### Changes Made
1. [Change 1]
2. [Change 2]
3. [Change 3]

## Results
### Before vs After
**Before:** [Previous performance/outcome]
**After:** [New performance/outcome]

### Metrics
- **Success Rate:** [Before] → [After]
- **Quality:** [Before] → [After]
- **Efficiency:** [Before] → [After]

## Validation
- [ ] [How you validated the improvement]
- [ ] [Additional testing performed]

## Lessons Learned
- [Key insights from this improvement process]
- [What would you do differently next time?]

## Related Improvements
- [[Related Improvement 1]]
- [[Related Improvement 2]]
'''