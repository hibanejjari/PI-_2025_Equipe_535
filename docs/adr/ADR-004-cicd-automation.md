# ADR-004: CI/CD Automation

**Status:** Proposed  
**Date:** October 2025  

## Context
We want the validation and anomaly scripts to run automatically whenever code changes or on a schedule.

## Decision
| Option | Pros | Cons |
|---------|------|------|
| **GitLab CI/CD** | Works well with Python, stores reports, easy YAML config | Needs a runner to be set up |
| **GitHub Actions** | Simple, good for open projects | Limited storage on free tier |
| **Jenkins** | Very customizable | Harder to maintain |
| **Azure Pipelines** | Enterprise-grade | Cost, vendor lock-in |

**Chosen:** **GitLab CI/CD** — fits well with our repo and needs.

## Consequences
✅ Automatic checks and reports.  
⚠️ A bit more setup time for runners.
