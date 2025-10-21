# ADR-002: Validation Layer

**Status:** Proposed  
**Date:** October 2025  

## Context
We need to check that numbers in Superset dashboards match our reference data.  
This layer compares the two and reports any mismatch.

## Decision
| Option | Pros | Cons |
|---------|------|------|
| **Python + Pandas** | Flexible, many libraries, works with Superset API | Uses more memory on large data |
| **dbt** | Good for big SQL pipelines | Needs SQL and database setup |
| **Airflow** | Handles complex scheduling | Too heavy for this project |
| **Talend / Power BI Flows** | No-code tools | Not open-source, less flexible |

**Chosen:** **Python (Pandas)** — simple, flexible, and easy to run in CI/CD.

## Consequences
✅ Fast to build and adjust.  
⚠️ Needs clean, well-tested code for long-term use.
