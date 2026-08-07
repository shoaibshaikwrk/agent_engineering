# WidgetWare Business Brief

## Overview

WidgetWare sells software and services that help manufacturing and industrial-automation companies modernize plant operations and adopt AI-enabled automation.

## Business Challenge

Sales Development Representatives (SDRs) spend substantial time researching target accounts, evaluating ICP fit, and parsing unstructured signals from news, press releases, and internal notes. An AI SDR Agent can assist SDRs by assembling structured context and pre-qualifying accounts.

## Core Capabilities Required for the SDR Agent

A future WidgetWare SDR agent must be able to:
1. Receive a target account;
2. Compare that account with WidgetWare's Ideal Customer Profile (ICP);
3. Examine supplied evidence with strict provenance tracking;
4. Distinguish facts from inference and unknowns;
5. Identify whether more research is required when information is incomplete;
6. Prepare structured context for buyer hypothesis or outreach drafting;
7. Stop before taking any external action;
8. Require human approval before sending messages or modifying CRM data.

## Architectural Discipline: 5 Context Layers

To ensure security and reliability, the agent separates context into five distinct layers:
- **System Instructions**: Fixed, non-overridable behavioral instructions.
- **Business Context**: Stable company, product, ICP, and policy configurations.
- **Task Context**: Current account assignment, research objectives, and untrusted account notes.
- **Retrieved Evidence**: Categorized evidence items with full provenance metadata.
- **Workflow State**: State metrics and execution status (defaults to empty object `{}`).
