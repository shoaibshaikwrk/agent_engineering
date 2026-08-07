# Class 3 Acceptance Criteria

## Acceptance Checklist

- [x] **YAML Configurations**: `products.yaml`, `icp.yaml`, and `policies.yaml` exist and load valid YAML.
- [x] **Product Offerings**: At least 2 WidgetWare offerings are configured (3 included with Plant Safety AI).
- [x] **ICP Definition**: ICP includes fit dimensions (minimum employee count = 5000, preferred/excluded industries, preferred regions) and required account fields.
- [x] **Safety Boundaries**: Explicit safety rules prohibit messaging, email sending, CRM modifications, and pricing/contractual commitments without human approval.
- [x] **Inspectable Instructions**: System instructions are inspectable via `get_system_instructions()`.
- [x] **Context Builder**: `build_context()` returns a dictionary containing five separate context layers:
  1. `system_instructions`
  2. `business_context`
  3. `task_context`
  4. `retrieved_evidence`
  5. `state`
- [x] **Evidence Provenance**: Evidence items preserve provenance (claim, classification, source details).
- [x] **Unknown Handling**: Missing fields/information remain explicitly `unknown` without hallucinated values.
- [x] **Prompt Injection Defense**: Account notes and retrieved text are isolated as untrusted data and cannot modify instructions or policies.
- [x] **Scenarios & Testing**: Fixtures for qualified, unqualified, insufficient evidence, prompt injection, and conflicting evidence exist, and all automated tests pass.
- [x] **Out of Scope Adherence**: No ADK agent, LLM calls, web scraping, live API calls, CRM edits, or outreach actions exist.
