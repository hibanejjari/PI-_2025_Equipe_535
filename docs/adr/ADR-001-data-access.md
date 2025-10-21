# ADR-001: Data Access

**Status:** Proposed  
**Date:** October 2025  

## Context
We need a place to store both reference data and Superset dashboard results.  
It should work well with Python, be easy to query, and scale later if needed.

## Decision
| Option | Pros | Cons |
|---------|------|------|
| **PostgreSQL** | Free, open-source, works with Superset and Python | Needs tuning for big data |
| **Snowflake** | Cloud-based, very scalable, secure | Paid service |
| **BigQuery** | Fast and serverless | Google-only platform |
| **SQLite** | Very simple for small tests | Not good for multi-user work |

**Chosen:** **PostgreSQL** for now. **Snowflake** if the company wants a cloud version later.

## Consequences
✅ Easy to start, connects with everything.  
⚠️ Might need performance tuning when the project grows.
