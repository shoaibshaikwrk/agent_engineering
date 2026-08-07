# Class 3 Specification — WidgetWare SDR Context Package

## 1. Class purpose

Class 3 is the first implementation-focused class in the WidgetWare SDR course.

Students have already:

- learned what an AI agent is;
- reviewed the SDR sales process;
- understood where SDR work fits in the B2B sales lifecycle;
- reviewed WidgetWare's target-account and approval boundaries;
- installed and opened Antigravity IDE.

In this class, students will convert the business concepts into a structured, testable context package that a future agent can consume.

The class does **not** build the ADK agent yet.

---

## 2. Class outcome

By the end of Class 3, each student must have a working project under:

```text
my-work/class-03/
```

The project must contain:

- WidgetWare product configuration;
- Ideal Customer Profile configuration;
- operating and safety policies;
- stable future-agent instructions;
- a context builder;
- representative SDR scenarios;
- automated tests.

The resulting package will become the input to the first narrow WidgetWare SDR agent in Class 4.

---

## 3. Scope

### 3.1 In scope

Students must build:

- YAML configuration for products, ICP, and policies;
- Python instructions for the future agent;
- a deterministic context builder;
- scenario fixtures;
- unit and scenario tests;
- brief project documentation.

### 3.2 Out of scope

Students must not build:

- a Google ADK agent;
- Gemini or any other LLM call;
- web search;
- live account research;
- email delivery;
- social-message delivery;
- CRM integration;
- database persistence;
- deployment;
- autonomous external actions.

---

## 4. Required repository structure

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

## 5. Homework Extensions

Extend the Class 3 package by adding:

1. one additional WidgetWare product (`plant_safety_ai`);
2. one additional preferred industry (`energy_utilities`);
3. one additional prohibited action (`make_contractual_commitments`);
4. one scenario containing two credible but conflicting evidence sources (`conflicting_evidence.yaml`);
5. a test confirming that the claim is classified as `conflict`;
6. a short README explanation of the five context layers.
