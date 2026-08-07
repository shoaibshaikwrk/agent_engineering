"""Deterministic context builder for WidgetWare SDR Agent.

Assembles system instructions, business context, task context, retrieved evidence,
and workflow state into five strictly separated context layers.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

from widgetware_sdr.instructions import get_system_instructions

# Determine base directory containing config/
CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"


def load_config(filename: str) -> dict[str, Any]:
    """Load a YAML configuration file from the config directory.

    Args:
        filename: Name of the YAML file (e.g. 'products.yaml').

    Returns:
        dict[str, Any]: Loaded YAML dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration file is empty or invalid.
    """
    config_path = CONFIG_DIR / filename
    if not config_path.is_file():
        raise FileNotFoundError(f"Required configuration file missing: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        raise ValueError(f"Configuration file is empty: {config_path}")

    return data


def build_context(
    account: dict[str, Any],
    objective: str,
    evidence: list[dict[str, Any]],
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the 5-layer context dictionary for the WidgetWare SDR Agent.

    Args:
        account: Target account data dictionary.
        objective: Research objective or task goal description.
        evidence: List of evidence items with provenance metadata.
        state: Optional current workflow state dictionary.

    Returns:
        dict[str, Any]: A dictionary preserving all 5 context layers:
            - system_instructions (str)
            - business_context (dict)
            - task_context (dict)
            - retrieved_evidence (list)
            - state (dict)

    Raises:
        FileNotFoundError: If required YAML configuration files are missing.
        ValueError: If required configuration files are invalid.
    """
    # Load stable business configurations
    products_config = load_config("products.yaml")
    icp_config = load_config("icp.yaml")
    policies_config = load_config("policies.yaml")

    # System instructions layer
    system_instructions = get_system_instructions()

    # Business context layer
    business_context = {
        "products": copy.deepcopy(products_config),
        "icp": copy.deepcopy(icp_config),
        "policies": copy.deepcopy(policies_config),
    }

    # Task context layer (untrusted task data isolated here)
    task_context = {
        "account": copy.deepcopy(account),
        "objective": str(objective),
    }

    # Retrieved evidence layer (preserve provenance)
    retrieved_evidence = copy.deepcopy(evidence) if evidence else []

    # Workflow state layer (default to empty dict if omitted or None)
    workflow_state = copy.deepcopy(state) if state is not None else {}

    return {
        "system_instructions": system_instructions,
        "business_context": business_context,
        "task_context": task_context,
        "retrieved_evidence": retrieved_evidence,
        "state": workflow_state,
    }
