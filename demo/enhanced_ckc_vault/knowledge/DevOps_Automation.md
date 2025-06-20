---
author: DevOps Team
claude_feature:
- code-generation
claude_model: []
complexity: intermediate
confidence: high
created: 2025-06-20 17:21:02.373542
domain:
- data-science
- testing
- web-dev
- security
- ai-ml
- automation
- devops
project: infrastructure
projects:
- infrastructure
purpose: null
status: draft
success_rate: null
tags:
- automation
- ci-cd
- deployment
- devops
- infrastructure
team: []
tech:
- aws
- git
- python
- typescript
title: DevOps Automation Strategies
type: prompt
updated: 2025-06-20 17:21:02.373548
version: '1.0'
---

# DevOps Automation Strategies

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: |
          ./deploy-staging.sh
```

## Infrastructure as Code

### Terraform Configuration
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1d0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
    Environment = "production"
  }
}
```

## Monitoring and Alerting

- Prometheus for metrics collection
- Grafana for visualization
- PagerDuty for incident management
- ELK stack for log aggregation