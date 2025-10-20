# ADR-002 — dbt Data Validation and Testing Strategy

- **Status**: Proposed  
- **Date**: 2025-10-20  
- **Authors**: Adrien  
- **Related Systems**: dbt, ClickHouse, GitLab CI/CD, Superset 

---

## Context

Within the current DataOps workflow:

**Airflow → dltHub → ClickHouse → dbt → Superset**

the **transformation stage (dbt)** is a critical point where data quality issues often originate.  
Transformation logic errors, schema mismatches, or missing upstream data can cause invalid metrics to propagate into Superset dashboards, resulting in inaccurate visualizations.

The project aims to establish a **systematic validation strategy for dbt models**, tightly integrated into the **CI/CD pipeline** and complementary to the supervision service defined in ADR-001.

---

## Drivers

- Guarantee integrity and correctness of transformed datasets before visualization  
- Automate dbt model testing within GitLab pipelines  
- Detect and report transformation errors early (before merge/deployment)  
- Enable traceability of test results and reports  
- Provide a framework extensible to AI-assisted anomaly detection  

---

## Decision

Adopt a **multi-layer dbt validation strategy**, combining **built-in dbt tests**, **custom SQL assertions**, and **metadata-driven validation scripts** executed by the supervision service.

The validation process will run automatically in the GitLab CI/CD pipeline at each push or merge request.  
Results will be aggregated into a structured **validation report** (JSON/PDF) stored as an artifact and optionally published by the supervision service.

---

## Validation Layers

### 1. Schema & Referential Integrity
- Use dbt’s built-in tests:  
  - `unique`, `not_null`, `accepted_values`, `relationships`  
- Apply to all fact and dimension tables.  
- Fail the pipeline if any critical test fails.

### 2. Transformation Logic Checks
- Add **custom SQL tests** under `/tests` to verify business logic (e.g., KPI definitions, aggregation consistency).  
- Use dbt’s `test` blocks or Jinja macros for reusability.  
- Define severity levels (`warn`, `error`) for prioritization.

### 3. Freshness & Volume Monitoring
- Enable dbt’s `source freshness` to detect delayed or incomplete loads.  
- Integrate thresholds into GitLab job configuration.  
- Record last successful refresh timestamp in the report.

### 4. Data Consistency Across Environments
- Compare sample outputs between **staging** and **production** schemas.  
- Detect deltas via SQL diff scripts run by the supervision service.  
- Produce structured diff reports.

### 5. Optional AI-Assisted Validation (Future)
- Extend validation by using a generative or statistical model to:
  - detect outliers or inconsistent data patterns,  
  - suggest likely root causes,  
  - or generate human-readable validation summaries.

---

## Alternatives Considered

### A — Manual Validation via Ad-hoc Queries
**Pros:** Simple, no setup required  
**Cons:** Error-prone, unscalable, no automation or CI/CD integration  

### B — Basic dbt Tests Only (no CI/CD)
**Pros:** Minimal implementation effort  
**Cons:** Limited coverage, no version-controlled reports, issues detected late  

### C — Multi-layer Automated Validation *(chosen)*
**Pros:**  
- Comprehensive coverage (schema + logic + freshness)  
- Automated reporting  
- Easy integration with GitLab and supervision service  
**Cons:**  
- Requires initial setup and test definition effort  
- May increase pipeline runtime slightly  

---

## Rationale

The dbt transformation layer is the backbone of the pipeline.  
Embedding automated tests into the CI/CD lifecycle ensures that:
- data quality issues are detected before deployment,  
- dashboards always rely on validated datasets,  
- and the validation logic remains version-controlled.

The chosen multi-layer approach provides both **rigor and flexibility**, supporting incremental adoption of advanced validation (AI modules) later.

---

## Consequences

**Technical:**
- dbt project must include a comprehensive `tests/` directory.  
- GitLab CI/CD pipeline will execute `dbt run` followed by `dbt test`.  
- Results will be parsed and aggregated by the supervision service.  
- The supervision service will generate PDF/JSON reports.  

**Organizational:**
- Developers must write and maintain dbt test definitions alongside models.  
- DataOps team will monitor pipeline results and handle failures.  
- Cross-team collaboration (Data Engineering, DevOps, QA) is required.  

**Costs / Risks:**
- Slightly longer CI/CD execution time.  
- Need for test maintenance when models evolve.  
- False positives possible for dynamic data (mitigated via thresholds).

---

## Implementation Plan

| Step | Description | Responsible | Target |
|------|--------------|-------------|---------|
| 1 | Define test taxonomy (schema, logic, freshness) | ESILV & Citeos team | Week 1 |
| 2 | Implement dbt built-in tests | ESILV Team | Week 2–3 |
| 3 | Add custom SQL validation tests | ESILV Team | Week 4 |
| 4 | Integrate dbt test step into GitLab pipeline | ESILV Team | Week 5 |
| 5 | Parse and export dbt test results to supervision service | ESILV Team | Week 6 |
| 6 | Generate automated reports | ESILV Team | Week 7 |
| 7 | Evaluate AI-assisted validation prototype (optional) | ESILV Team | Phase 2 |

**Rollback Plan:**  
If test execution introduces excessive runtime or instability, revert to nightly batch validation until optimizations are applied.

---

## Future Work

- Incorporate **data drift detection** (statistical comparison between runs).  
- Introduce **AI-based test generation** using metadata and SQL lineage.  
- Add **visual validation dashboards** in Superset.  
- Automate **notification triggers** when dbt tests fail (Slack/email).

---

## Related ADRs

- ADR-001 — Error Supervision and Validation Service (defines integration layer and reporting)  
- ADR-003 — Superset Validation and API Testing *(planned)*  

---

## Notes

This decision ensures that **data quality becomes a first-class citizen** in the Project 110 DataOps lifecycle.  
By embedding dbt validation inside CI/CD, we achieve **continuous data reliability**, **traceable validation artifacts**, and a strong foundation for future AI-driven quality improvements.
