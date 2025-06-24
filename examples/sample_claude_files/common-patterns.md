---
title: "Common Claude Code Patterns"
created: "2024-06-17"
updated: "2024-06-17"
version: "1.0"
category: "patterns"
status: "active"
tags: [claude, patterns, prompts, workflows]
---

# Common Claude Code Patterns

## Effective Prompt Patterns

### Code Generation Pattern
```
Generate [language] code for [specific functionality] that:
- Follows [specific standards/patterns]
- Includes [requirements like error handling, tests, docs]
- Uses [specific libraries/frameworks]
- Considers [constraints like performance, security]

Context: [brief project context]
Example: [input/output example if helpful]
```

### Code Review Pattern
```
Review this [language] code for:
- Code quality and best practices
- Potential bugs or security issues
- Performance optimizations
- Adherence to [style guide/patterns]

Code:
[paste code here]

Project context: [brief context about the project]
```

### Debugging Pattern
```
Help debug this issue:

Problem: [clear description of the issue]
Expected behavior: [what should happen]
Actual behavior: [what is happening]

Code: [relevant code snippet]
Error message: [if any]
Environment: [relevant details like Python version, OS, etc.]

I've tried: [list of attempted solutions]
```

### Architecture Design Pattern
```
Design a [type of system/component] for [use case] that:
- Handles [specific requirements]
- Scales to [scale requirements]
- Integrates with [existing systems]
- Follows [architectural patterns]

Constraints:
- [technical constraints]
- [business constraints]

Please provide:
- High-level architecture
- Key components and their responsibilities
- Data flow
- Technology recommendations
```

## Code Generation Commands

### FastAPI Endpoint Generation
```
Generate a FastAPI endpoint for [resource] that:
- Follows RESTful conventions
- Includes proper Pydantic models
- Has error handling
- Includes authentication dependency
- Has proper status codes and responses
- Includes docstring with example
```

### React Component Generation
```
Create a React TypeScript component for [purpose] that:
- Uses functional component with hooks
- Has proper TypeScript interfaces
- Includes error boundaries
- Is accessible (ARIA compliant)
- Has proper styling structure
- Includes unit test template
```

### Database Model Generation
```
Create SQLAlchemy model for [entity] with:
- Proper relationships to [related entities]
- Appropriate indexes for [query patterns]
- Data validation
- Timestamps (created_at, updated_at)
- Soft delete capability
- Include migration script
```

### Test Generation
```
Generate comprehensive tests for [component/function] including:
- Unit tests for core functionality
- Edge case testing
- Error condition testing
- Mock dependencies
- Test fixtures
- Follow [testing framework] patterns
```

## Analysis and Review Patterns

### Performance Analysis
```
Analyze this code for performance bottlenecks:
[code here]

Focus on:
- Time complexity
- Memory usage
- Database query efficiency
- I/O operations
- Caching opportunities

Suggest specific optimizations with examples.
```

### Security Review
```
Review this code for security vulnerabilities:
[code here]

Check for:
- Input validation
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization issues
- Data exposure risks
- OWASP Top 10 compliance

Provide specific remediation steps.
```

### Code Quality Assessment
```
Assess this code quality:
[code here]

Evaluate:
- Readability and maintainability
- SOLID principles adherence
- DRY principle compliance
- Error handling adequacy
- Documentation quality
- Testing coverage

Suggest improvements with examples.
```

## Documentation Patterns

### API Documentation
```
Generate comprehensive API documentation for:
[endpoint/function details]

Include:
- Clear description
- Parameters with types and validation rules
- Response format with examples
- Error codes and messages
- Usage examples in multiple languages
- Authentication requirements
```

### Code Documentation
```
Generate docstrings/comments for this code:
[code here]

Include:
- Clear function/class purpose
- Parameter descriptions with types
- Return value description
- Usage examples
- Any side effects or important notes
- Follow [documentation standard] format
```

## Troubleshooting Workflows

### Error Investigation
1. **Describe the error clearly**
   - What were you trying to do?
   - What happened instead?
   - Any error messages?

2. **Provide context**
   - Relevant code snippets
   - Environment details
   - Recent changes

3. **Share investigation steps**
   - What you've already tried
   - Current theories about the cause

### Performance Issues
1. **Establish baseline**
   - Current performance metrics
   - Expected performance

2. **Identify bottlenecks**
   - Profiling results
   - Slow operations

3. **Request optimization strategy**
   - Specific areas to improve
   - Implementation approach

## Rapid Prototyping Commands

### Quick API Setup
```
Create a minimal FastAPI application for [use case] with:
- [list specific endpoints]
- Basic error handling
- CORS configuration
- Health check endpoint
- Docker setup
- README with setup instructions
```

### Frontend Prototype
```
Create a React prototype for [feature] with:
- [list specific components]
- Mock data structure
- Basic styling
- Navigation between views
- State management setup
- TypeScript configuration
```

### Database Schema
```
Design database schema for [domain] including:
- [list entities]
- Relationships between entities
- Indexes for common queries
- Migration scripts
- Sample data for testing
```

## Best Practices for Claude Interactions

### Be Specific
- Provide clear requirements and constraints
- Include relevant context about your project
- Specify the format you want for responses

### Iterate Effectively
- Start with basic implementation
- Request improvements in follow-up prompts
- Ask for explanations of complex parts

### Validate Suggestions
- Test generated code thoroughly
- Ask for explanations of unfamiliar patterns
- Request alternative approaches when needed

### Maintain Context
- Reference previous conversations when relevant
- Provide updates on what worked/didn't work
- Build on successful patterns
