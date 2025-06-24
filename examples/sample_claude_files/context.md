---
title: "Project Context and Background"
created: "2024-06-17"
updated: "2024-06-17"
version: "1.0"
category: "context"
status: "active"
tags: [context, project-setup, background]
---

# Project Context and Background

## Project Overview
This project is a web application built with FastAPI and React that helps users manage their daily tasks and productivity workflows.

## Technology Stack
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: React 18 with TypeScript
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Deployment**: Docker containers on AWS ECS
- **CI/CD**: GitHub Actions

## Key Constraints
- Must support 10,000+ concurrent users
- Response time must be under 200ms for API calls
- Must be accessible (WCAG 2.1 AA compliance)
- All data must be encrypted at rest and in transit

## Team Structure
- 2 Backend developers
- 2 Frontend developers
- 1 DevOps engineer
- 1 Product manager

## Claude Usage Context
We primarily use Claude for:
- Code generation and optimization
- Architecture decision support
- Documentation writing
- Debugging complex issues
- API design and validation

## Development Workflow
1. Feature planning in weekly sprints
2. Code development with TDD approach
3. Peer reviews for all changes
4. Automated testing in CI/CD pipeline
5. Staging deployment for QA testing
6. Production deployment with blue-green strategy

## Common Patterns
- All API endpoints follow RESTful conventions
- Frontend components use TypeScript interfaces
- Database migrations are version controlled
- Configuration uses environment variables
- Logging follows structured JSON format
