# ADR-005: AI Reporting

**Status:** Proposed  
**Date:** October 2025  

## Context
After anomalies are found, managers need clear explanations.  
An AI tool can write short summaries automatically.

## Decision
| Option | Pros | Cons |
|---------|------|------|
| **LangChain + OpenAI API** | Easy to add, good quality text | API cost, needs prompts |
| **Hugging Face (local)** | Works offline, free | Needs GPU, slower |
| **Azure OpenAI** | Enterprise-ready | Expensive |
| **No AI layer** | Simple | Manual reporting only |

**Chosen:** **LangChain + OpenAI API** for first tests.  
Later we can use a local model.

## Consequences
✅ Readable automatic summaries.  
⚠️ Need to watch cost and accuracy.
