# ADR-003: Anomaly Detection

**Status:** Proposed  
**Date:** October 2025  

## Context
After comparing Superset data, we want to find unusual values or trends automatically.

## Decision
| Option | Pros | Cons |
|---------|------|------|
| **PyOD** | Many ready-to-use anomaly algorithms | Few built-in graphs |
| **Scikit-learn** | Popular ML library, explainable models | Fewer anomaly tools |
| **Azure ML / Vertex AI** | Scalable cloud services | Paid, complex setup |
| **ELK Stack** | Great for time-series logs | Too heavy for this use |

**Chosen:** **PyOD**, because it’s easy to use with Pandas and works offline.

## Consequences
✅ Quick tests with many algorithms.  
⚠️ For very large data, may need faster frameworks later.
