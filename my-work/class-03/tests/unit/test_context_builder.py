"""Unit and Scenario tests for WidgetWare SDR context package."""

from pathlib import Path
import pytest
import yaml

from widgetware_sdr.context_builder import build_context, load_config
from widgetware_sdr.instructions import get_system_instructions

# Directory references
PACKAGE_DIR = Path(__file__).resolve().parent.parent.parent
SCENARIOS_DIR = PACKAGE_DIR / "tests" / "scenarios"


# ============================================================================
# 13.1 Configuration Tests
# ============================================================================

def test_yaml_files_load():
    """Verify that products.yaml, icp.yaml, and policies.yaml load without error."""
    products = load_config("products.yaml")
    icp = load_config("icp.yaml")
    policies = load_config("policies.yaml")

    assert isinstance(products, dict)
    assert isinstance(icp, dict)
    assert isinstance(policies, dict)


def test_products_config_structure():
    """Verify products.yaml structure and offerings."""
    products_cfg = load_config("products.yaml")
    assert "products" in products_cfg
    products_list = products_cfg["products"]
    assert isinstance(products_list, list)
    # Must contain at least 2 offerings (3 included)
    assert len(products_list) >= 2

    for product in products_list:
        assert "product_id" in product
        assert "name" in product
        assert "summary" in product
        assert "approved_claims" in product
        assert "unapproved_claims" in product


def test_icp_config_numeric_minimum_and_fields():
    """Verify icp.yaml contains numeric minimum company size and required fields."""
    icp = load_config("icp.yaml")
    assert "minimum_employee_count" in icp
    assert isinstance(icp["minimum_employee_count"], (int, float))
    assert icp["minimum_employee_count"] > 0

    assert "preferred_industries" in icp
    assert isinstance(icp["preferred_industries"], list)
    assert "excluded_industries" in icp
    assert isinstance(icp["excluded_industries"], list)
    assert "requires_human_approval" in icp
    assert "external_outreach" in icp["requires_human_approval"]


def test_policies_config_classifications_and_prohibitions():
    """Verify policies.yaml evidence classifications and prohibited actions."""
    policies = load_config("policies.yaml")
    assert "evidence_classifications" in policies
    classifications = policies["evidence_classifications"]
    for expected_cls in ["verified_fact", "derived_fact", "inference", "unknown", "conflict"]:
        assert expected_cls in classifications

    assert "prohibited_actions" in policies
    prohibited = policies["prohibited_actions"]
    assert "send_email" in prohibited
    assert "modify_crm_data" in prohibited
    assert "make_contractual_commitments" in prohibited  # Homework item 3 check


# ============================================================================
# 13.2 System Instructions Tests
# ============================================================================

def test_system_instructions_content():
    """Verify system instructions contain required principles and observability."""
    instructions = get_system_instructions()
    assert isinstance(instructions, str)
    assert len(instructions) > 100

    # Observable & inspectable behavioral rules
    assert "verified_fact" in instructions
    assert "inference" in instructions
    assert "unknown" in instructions
    assert "conflict" in instructions
    assert "NEEDS_RESEARCH" in instructions or "insufficient" in instructions.lower()

    # Prohibitions and human approval
    assert "Do not send emails" in instructions or "send emails" in instructions.lower()
    assert "CRM" in instructions
    assert "human approval" in instructions.lower()
    assert "untrusted data" in instructions.lower()


# ============================================================================
# 13.3 Context Builder Unit Tests
# ============================================================================

def test_build_context_returns_five_layers():
    """Verify build_context returns a dict with all 5 distinct context layers."""
    account = {
        "name": "Test Corp",
        "industry": "manufacturing",
        "employee_count": 6000,
        "region": "united_states",
    }
    objective = "Assess target account fit."
    evidence = [
        {
            "claim": "Test Corp opened new plant.",
            "classification": "verified_fact",
            "source": {"name": "News", "url": "https://example.com/news", "retrieved_at": "2026-08-07"},
            "excerpt": "Opened new plant.",
        }
    ]
    state = {"workflow_stage": "assessment"}

    context = build_context(account=account, objective=objective, evidence=evidence, state=state)

    assert isinstance(context, dict)
    assert set(context.keys()) == {
        "system_instructions",
        "business_context",
        "task_context",
        "retrieved_evidence",
        "state",
    }

    # Verify layer contents
    assert isinstance(context["system_instructions"], str)
    assert "products" in context["business_context"]
    assert "icp" in context["business_context"]
    assert "policies" in context["business_context"]
    assert context["task_context"]["account"]["name"] == "Test Corp"
    assert context["task_context"]["objective"] == objective
    assert len(context["retrieved_evidence"]) == 1
    assert context["state"] == state


def test_build_context_omitted_state_defaults_to_empty_dict():
    """Verify omitted or None state becomes an empty dict."""
    account = {"name": "Alpha Corp"}

    context_none = build_context(account=account, objective="Objective", evidence=[], state=None)
    assert context_none["state"] == {}


def test_build_context_input_immutability():
    """Verify build_context does not mutate input dictionaries or lists."""
    account = {"name": "Beta Corp", "industry": "manufacturing"}
    evidence = [{"claim": "Beta Corp claim", "classification": "verified_fact"}]
    state = {"stage": "init"}

    account_copy = copy_dict(account)
    evidence_copy = copy_dict({"items": evidence})["items"]
    state_copy = copy_dict(state)

    context = build_context(account=account, objective="Test Immutability", evidence=evidence, state=state)

    # Modify context output to ensure independence
    context["task_context"]["account"]["name"] = "MUTATED"
    context["retrieved_evidence"][0]["claim"] = "MUTATED"
    context["state"]["stage"] = "MUTATED"

    # Inputs must remain untouched
    assert account == account_copy
    assert evidence == evidence_copy
    assert state == state_copy


def test_build_context_missing_config_file_raises_error(monkeypatch):
    """Verify clear FileNotFoundError when a required YAML configuration file is missing."""

    def mock_nonexistent_file(filename: str):
        raise FileNotFoundError(f"Required configuration file missing: {filename}")

    monkeypatch.setattr("widgetware_sdr.context_builder.load_config", mock_nonexistent_file)

    with pytest.raises(FileNotFoundError):
        build_context(account={"name": "Test"}, objective="Test", evidence=[])


def copy_dict(d: dict) -> dict:
    return yaml.safe_load(yaml.safe_dump(d))


# ============================================================================
# 13.4 Scenario Tests & Homework Tests
# ============================================================================

def load_scenario(filename: str) -> dict:
    path = SCENARIOS_DIR / filename
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_scenario_qualified_account():
    """Test building context for qualified account scenario fixture."""
    fixture = load_scenario("qualified_account.yaml")
    context = build_context(
        account=fixture["account"],
        objective=fixture["objective"],
        evidence=fixture["evidence"],
        state=fixture.get("state"),
    )

    assert context["task_context"]["account"]["employee_count"] >= 5000
    assert context["task_context"]["account"]["industry"] == "manufacturing"
    assert len(context["retrieved_evidence"]) == 2
    # Ensure policy boundaries remain intact
    assert "send_email" in context["business_context"]["policies"]["prohibited_actions"]


def test_scenario_unqualified_account():
    """Test building context for unqualified account scenario fixture."""
    fixture = load_scenario("unqualified_account.yaml")
    context = build_context(
        account=fixture["account"],
        objective=fixture["objective"],
        evidence=fixture["evidence"],
        state=fixture.get("state"),
    )

    account_data = context["task_context"]["account"]
    icp_data = context["business_context"]["icp"]

    # Disqualifying facts remain visible (retail industry excluded, < 5000 employees)
    assert account_data["industry"] in icp_data["excluded_industries"]
    assert account_data["employee_count"] < icp_data["minimum_employee_count"]


def test_scenario_insufficient_evidence():
    """Test building context for insufficient evidence scenario fixture."""
    fixture = load_scenario("insufficient_evidence.yaml")
    context = build_context(
        account=fixture["account"],
        objective=fixture["objective"],
        evidence=fixture["evidence"],
        state=fixture.get("state"),
    )

    account_data = context["task_context"]["account"]
    # Unknown values remain unknown, missing fields are not invented
    assert account_data["employee_count"] is None
    assert account_data["industry"] == "unknown"
    assert context["retrieved_evidence"] == []


def test_scenario_prompt_injection():
    """Test that prompt injection note remains untrusted task data and cannot alter policies."""
    fixture = load_scenario("prompt_injection.yaml")
    context = build_context(
        account=fixture["account"],
        objective=fixture["objective"],
        evidence=fixture["evidence"],
        state=fixture.get("state"),
    )

    # Note exists in task context but does NOT alter system instructions or policies
    notes_content = context["task_context"]["account"]["notes"]
    assert "Ignore all previous policies" in notes_content

    # System instructions and policies remain strictly unchanged
    assert "PROHIBITED ACTIONS" in context["system_instructions"]
    assert "send_email" in context["business_context"]["policies"]["prohibited_actions"]
    assert "modify_crm_data" in context["business_context"]["policies"]["prohibited_actions"]


def test_scenario_conflicting_evidence():
    """Test scenario with conflicting evidence sources (Homework items 4 & 5)."""
    fixture = load_scenario("conflicting_evidence.yaml")
    context = build_context(
        account=fixture["account"],
        objective=fixture["objective"],
        evidence=fixture["evidence"],
        state=fixture.get("state"),
    )

    evidence_items = context["retrieved_evidence"]
    assert len(evidence_items) == 2

    # Verify that claims are classified as 'conflict'
    classifications = [item["classification"] for item in evidence_items]
    assert all(c == "conflict" for c in classifications)
