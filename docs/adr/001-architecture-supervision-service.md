# ADR-001 — Architecture Decision: Error Supervision and Validation Service for Data & Dashboard Pipelines

- **Status**: Proposed  
- **Date**: 2025-10-20  
- **Authors**: Adrien  
- **Related Systems**: Airflow, dltHub, ClickHouse, dbt, Apache Superset  

---

## Context

The current workflow architecture follows this pattern:

**Orchestration (Airflow)** → **Data Collection (dltHub)** → **Storage (ClickHouse)** → **Transformation (dbt)** → **Visualization (Apache Superset)**  

While this setup enables efficient data flow and visualization, **errors occur frequently during the transformation step (dbt)** and during **dashboard conception/configuration (Superset)**.  

These issues can lead to incorrect or inconsistent data being displayed, undermining trust in the analytics dashboards used for decision-making.

The project’s goal is to design and integrate a **software component** capable of automatically validating dashboard data integrity and transformation consistency within a **DataOps workflow**, ensuring continuous quality and reliability.

---

## Drivers

- Ensure reliability and correctness of dashboard data  
- Automate data validation in CI/CD to reduce manual errors  
- Provide clear, version-controlled error reports  
- Allow extension for AI-based anomaly detection  
- Maintain compatibility with existing Airflow/dbt/Superset architecture  

---

## Decision

We will **create a separate supervision service** responsible for automated validation and error reporting of the analytics pipeline.  
This service will integrate into the **GitLab CI/CD pipeline**, automatically executing quality checks and generating structured reports before each merge or deployment.

The service will:
- Run **tests on dbt transformations** (schema validation, freshness, consistency)
- Validate **Superset dashboards** by dynamically querying charts and comparing results with expected or reference data
- Produce **automated error reports** (PDF or structured logs) that summarize detected issues, deltas, and suggested corrections
- Optionally integrate **AI-based analysis** modules to detect anomalous data behavior or inconsistencies over time

---

## Alternatives Considered

### Alternative A — Integrate error checks directly within existing jobs
**Pros:**
- Easier to deploy (no new component)  
- Reuses existing Airflow/dbt testing capabilities  
**Cons:**
- Harder to maintain separation of concerns  
- Limited extensibility for AI or dashboard validation  
- May complicate pipeline debugging and CI/CD triggers  

### Alternative B — Create a dedicated supervision service *(chosen)*
**Pros:**
- Clear responsibility separation and modularity  
- Easy integration into CI/CD workflows  
- Extensible architecture (future AI modules, dashboard APIs, etc.)  
- Enables independent evolution and versioning  
**Cons:**
- Slightly higher initial development and maintenance effort  
- Requires service orchestration (containerization, deployment config)

---

## Rationale

The supervision logic must be **independent** from data transformation and visualization tasks to:
- Avoid coupling monitoring logic with production jobs  
- Enable fast iteration and separate deployment cycles  
- Facilitate integration with GitLab CI/CD for pre-merge validation  

Given the need for automated version-controlled validation and clear test reports, a standalone service provides the best flexibility and maintainability.

---

## Consequences

**Technical:**
- A new service (Python-based) must be developed and containerized.  
- GitLab CI/CD pipeline needs to trigger validation steps and collect artifacts (reports).  
- dbt and Superset APIs will be integrated for validation queries.  
- Logging and reporting mechanism (PDF, JSON) to be stored in GitLab artifacts or cloud storage.  

**Organizational:**
- Developers must define and maintain validation test cases.  
- The team must configure GitLab runners and permissions for the validation service.  
- Potential collaboration with AI/ML specialists for anomaly detection integration.  

**Cost / Complexity:**
- Medium development effort (2–3 sprints).  
- Added container to deploy/maintain.  
- Long-term gain in reliability and developer confidence.  

---

## Implementation Plan

| Action | Responsible | Target Date |
|--------|--------------|--------------|
| Define validation requirements & test types | ESILV & Citeos Team | Week 1 |
| Implement prototype of supervision service (Python) | ESILV Team | Week 2–4 |
| Integrate with GitLab CI/CD pipeline | ESILV Team | Week 5 |
| Generate automated validation reports (PDF/logs) | ESILV Team | Week 6 |
| Optional: Add AI anomaly detection module | ESILV Team | Phase 2 |

**Rollback Plan:**  
If the service introduces blocking complexity, revert to embedded dbt + Airflow test hooks while maintaining validation logic in scripts.

---

## Future Work

- Extend the supervision service to monitor real-time production jobs (integration with Airflow monitoring).
- Add AI/ML module to detect anomalies in transformed data or dashboard KPIs.
- Integrate Slack/email notifications for failed validation steps.
- Develop a dedicated “Dashboard Quality Report” Superset view.

---

## Related ADRs

- ADR-002 — Data Validation Strategy for dbt Models *(planned)*  
- ADR-003 — Superset API Integration for Automated Testing *(planned)*  

---

## Notes

This decision aligns with VINCI Energies’ DataOps vision of **industrialized, reliable, and test-driven data pipelines** supporting **smart city dashboards**.  
By externalizing supervision into a separate service and automating checks through CI/CD, we ensure both scalability and long-term maintainability.

---
