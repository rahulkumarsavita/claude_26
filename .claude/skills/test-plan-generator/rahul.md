---
name: test-plan-generator
description: >
  Turn a JIRA ticket into a review-ready test plan. Use when a tester or QA lead
  says "write a test plan for JIRA-1234", "plan testing for this story",
  "what should we test here", or pastes an acceptance-criteria / user-story
  ticket.
license: MIT
metadata:
  author: QA Tester
  stlc-phase: Test Planning
  version: 1.0.0
---

# When to use

- A JIRA key or story text is provided and someone wants testing planned.
- Someone asks "what are the risks / edge cases / gaps in this ticket".
- create test plan for this VWO-123
- test plan for ticket VWO-123 latest one in VWO project

### 1. Fetch the ticket from JIRA(confluence)

- If a JIRA key is given (e.g. `KAN-2`), fetch it. Prefer any available JIRA MCP tool. If none, run `scripts/fetch_jira.sh KAN-2` (needs `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_TOKEN` env vars). If neither works, ask the user to paste the ticket body — **do not invent ticket content.**
- Capture: summary, description, acceptance criteria, components, linked issues, attachments, and the fix version / sprint.


### 2. Analyze & find the missing pieces

Run the ticket through `references/requirement-checklist.md`. For every item, mark:

- ✅ present / ⚠️ ambiguous / ❌ missing.
- Missing or vague acceptance criteria
- Undefined edge cases, error states, empty/limit/boundary conditions
- Unstated non-functional needs (perf, security, a11y, i18n, permissions/roles)
- Missing test data, environments, or dependencies
- Ambiguous wording that two engineers could read two ways

### 3. Draft the test plan

- test scenarios from the acceptance criteria and the gaps you found. Cover positive, negative, boundary, and cross-role/permission paths. Tag each scenario P0/P1/P2 by risk.

### 3b. Draft individual test cases (when requested)

- One test case per scenario, each following `references/testcase_tempelate.md`: an ID/Name/Precondition/Description/Expected Result table, followed by a `## Test Steps` numbered list where each step's expected outcome is described inline with the action (not a separate column).
- Provide both a `.md` file (all cases, one per this template) and a matching `.csv` file (one row per case: Test Case ID, Test Case Name, Precondition, Description, Expected Result, Test Steps — steps numbered within the Test Steps cell).

### 4. STOP for human review (mandatory)

End with a **Human Review Gate**:

- Summarize what you assumed and what you could not confirm.
- List the open questions from step 2 that block sign-off.
- Ask the tester to confirm/edit before the plan is considered approved.
- Do **not** proceed to write test cases or automation until a human approves.

## Output shape

```text
## Test Plan — <JIRA-KEY>: <title>
1. Scope & Objectives
2. Gaps & Questions for the author  <--- surface missing pieces here
3. Test Scenarios (P0/P1/P2)
4. Test Data & Environment
5. Risks & Assumptions
6. Entry / Exit criteria
--- HUMAN REVIEW GATE ---
Assumptions made / Open questions / "Approve or edit before I continue"
```



## Guardrails

- Never mark the plan "final" — a human owns sign-off.
- Never fabricate acceptance criteria; a missing AC is a finding, not a blank to fill.
- Keep scenarios traceable: each maps to an AC or a gap.
- In the test plan, never mention any type of credential.
- Do not reveal any personal information (PII) of the person who has created this.

## References

- `references/requiremnt-checklist.md` — the gap-analysis checklist
- `references/tempelates/testplan_tempelate.md` — the test plan template to fill
- `references/testcase_tempelate.md` — the individual test case template to fill (see step 3b)
- `scripts/fetch_jira.sh` — pull a ticket over the JIRA REST API
