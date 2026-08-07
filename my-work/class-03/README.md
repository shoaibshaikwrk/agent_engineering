# WidgetWare SDR Context Builder Package (Class 3)

This package implements the deterministic, 5-layer context builder for the WidgetWare Sales Development Representative (SDR) Account Qualification Assistant.

---

## The 5 Context Layers

The architecture strictly isolates information into five distinct context layers:

1. **System Instructions (`system_instructions`)**:
   Stable, non-overridable behavioral instructions. Defines the SDR assistant's role, objectives, scope, evidence rules, uncertainty handling, prohibited actions, and human escalation requirements.

2. **Business Context (`business_context`)**:
   Stable WidgetWare domain knowledge loaded from YAML configurations:
   - `products.yaml`: WidgetWare product offerings, approved claims, and prohibited claims.
   - `icp.yaml`: Ideal Customer Profile rules, company size thresholds, preferred/excluded industries, and required fields.
   - `policies.yaml`: Evidence classifications (`verified_fact`, `derived_fact`, `inference`, `unknown`, `conflict`), prohibited actions, and human approval boundaries.

3. **Task Context (`task_context`)**:
   Assignment specifics containing the target `account` profile, research `objective`, and free-text account notes. Untrusted inputs are isolated here and can never alter system instructions or business policies.

4. **Retrieved Evidence (`retrieved_evidence`)**:
   List of evidence records provided to the builder, preserving full provenance metadata (claim, classification, source name/URL/date, and excerpt).

5. **Workflow State (`state`)**:
   Information about the current execution state, prior decisions, and workflow stage. Defaults to an empty object `{}` when omitted.

---

## Project Structure

```text
my-work/class-03/
├── README.md
├── SPEC.md
├── pyproject.toml
├── .env.example
├── config/
│   ├── products.yaml
│   ├── icp.yaml
│   └── policies.yaml
├── docs/
│   ├── widgetware-business-brief.md
│   └── acceptance-criteria.md
├── src/
│   └── widgetware_sdr/
│       ├── __init__.py
│       ├── instructions.py
│       └── context_builder.py
└── tests/
    ├── unit/
    │   └── test_context_builder.py
    └── scenarios/
        ├── qualified_account.yaml
        ├── unqualified_account.yaml
        ├── insufficient_evidence.yaml
        ├── prompt_injection.yaml
        └── conflicting_evidence.yaml
```

---

## Setup and Verification

### 1. Install Dependencies

```bash
cd my-work/class-03
pip install -e .[dev]
```

### 2. Run Test Suite

```bash
python -m pytest -v
```
