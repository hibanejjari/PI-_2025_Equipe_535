# ADR-003 — Superset Validation and API Testing Strategy

- **Status**: Proposed  
- **Date**: 2025-10-20  
- **Authors**: Adrien   
- **Related Systems**: Apache Superset, GitLab CI/CD, dbt, ClickHouse  

---

## Context

Apache Superset is the visualization layer in the current DataOps pipeline:

**Airflow → dltHub → ClickHouse → dbt → Superset**

Dashboards are frequently updated, cloned, or customized for new clients.  
However, **configuration errors**—such as incorrect metrics, broken filters, outdated datasets, or inconsistent SQL queries—can cause dashboards to display wrong or stale data.  

Manual validation is time-consuming and error-prone.  
Therefore, an automated approach is needed to **validate Superset dashboards** and **detect discrepancies** between visualized data and reference values before deployment.

---

## Drivers

- Ensure dashboards display correct and up-to-date data  
- Validate Superset configurations automatically during CI/CD  
- Detect anomalies caused by schema changes or query errors  
- Provide machine-readable and human-readable validation reports  
- Support repeatable dashboard testing across clients and environments  

---

## Decision

Implement a **Superset Validation and API Testing Framework** as part of the existing supervision service (ADR-001).  
This framework will use the **Superset REST and SQL Lab APIs** to query dashboards, compare returned results with reference datasets, and generate validation reports automatically during the **GitLab CI/CD pipeline**.

Validation will cover:
- **Dataset and chart integrity**: Ensure queries execute successfully and match expected schemas.  
- **Metric correctness**: Compare aggregated values against reference data (ClickHouse or snapshots).  
- **Filter and parameter validation**: Test dashboard behavior under multiple filter combinations.  
- **Version control consistency**: Validate dashboards cloned or migrated to new environments.  

---

## Validation Workflow

1. **Test discovery:**  
   - Parse Superset metadata via the `/api/v1/chart` and `/api/v1/dashboard` endpoints.  
   - Identify charts and datasets to validate.

2. **Query execution:**  
   - Execute chart queries through the `/api/v1/chart/data` endpoint.  
   - Fetch result sets as JSON.

3. **Comparison and validation:**  
   - Compare returned values with expected reference datasets (CSV or ClickHouse queries).  
   - Apply tolerance thresholds for numeric metrics (configurable).

4. **Report generation:**  
   - Summarize validation results into JSON and PDF.  
   - Highlight discrepancies, missing charts, or failed queries.

5. **Pipeline integration:**  
   - Run automatically in GitLab CI/CD upon merge request.  
   - Store reports as GitLab artifacts for traceability.

---

## Alternatives Considered

### A — Manual Dashboard Validation
**Pros:** No additional development effort  
**Cons:** Slow, inconsistent, and error-prone — unsuitable for CI/CD integration  

### B — Snapshot Comparison (Visual Testing)
**Pros:** Detects UI or layout changes  
**Cons:** Heavy to maintain, does not validate data correctness  

### C — API-Based Validation *(chosen)*
**Pros:**  
- Reliable, data-centric validation  
- Easily automated and integrated with CI/CD  
- Extensible for AI-driven anomaly detection  
**Cons:**  
- Requires access to Superset APIs and authentication setup  
- Moderate implementation complexity  

---

## Rationale

An API-based validation strategy provides the right balance between **automation, flexibility, and maintainability**.  
It ensures that each dashboard or chart can be automatically tested against business-critical KPIs and prevents the release of incorrect visualizations.

By integrating this logic inside the supervision service, we maintain **centralized orchestration and unified reporting** across all pipeline stages (dbt + Superset).

---

## Consequences

**Technical:**
- The supervision service will include a Superset API client module.  
- GitLab CI/CD must authenticate to Superset (via access token or service account).  
- Reports (JSON/PDF) must summarize all test results and be archived in CI/CD artifacts.  
- Optional thresholds and test configurations stored in YAML (e.g., `/superset_tests/config.yml`).  

**Organizational:**
- Dashboard developers must define test expectations (reference datasets or SQL queries).  
- Validation will run automatically at each commit/merge to main.  
- Results will feed into the global “Dashboard Quality Report.”  

**Costs / Risks:**
- Slight increase in CI/CD runtime.  
- Requires API stability and proper Superset version management.  
- Need to maintain reference data samples.  

---

## Implementation Plan

| Step | Description | Responsible | Target |
|------|--------------|-------------|---------|
| 1 | Define Superset validation scenarios (metrics, filters, dashboards) | ESILV & Citeos Team | Week 1 |
| 2 | Develop Superset API client module in supervision service | ESILV Team | Week 2–3 |
| 3 | Implement comparison engine (reference vs. actual results) | ESILV Team | Week 4 |
| 4 | Integrate with GitLab CI/CD (job + report artifact) | ESILV Team | Week 5 |
| 5 | Add PDF/JSON report generation | ESILV Team | Week 6 |
| 6 | Optional: add AI module for pattern-based anomaly detection | ESILV Team | Phase 2 |

**Rollback Plan:**  
If the API-based validation introduces instability or latency, revert to periodic manual or semi-automated validation using Superset CLI exports.

---

## Future Work

- Implement **AI-based validation** to detect anomalies in metric evolution across time.  
- Create **Superset plugin or dashboard extension** to visualize validation status.  
- Add **alerting and notification** via Slack or email when dashboards fail tests.  
- Integrate with **Airflow monitoring** to correlate dashboard errors with pipeline issues.  

---

## Related ADRs

- ADR-001 — Error Supervision and Validation Service  
- ADR-002 — dbt Data Validation and Testing Strategy  

---

## Notes

This decision closes the validation loop for the entire Project 110 data pipeline:  
- ADR-001 defines the central supervision service.  
- ADR-002 secures data transformation integrity.  
- ADR-003 guarantees dashboard correctness and reliability.  

Together, they create a **robust, test-driven DataOps architecture** ensuring consistent, high-quality analytics for VINCI Energies’ smart-city and industrial environments.
