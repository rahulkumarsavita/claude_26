---
name: jira-ticket-creator
description: >
  Turn a feature request, bug report, or informal ask into a review-ready
  JIRA ticket draft. Use when someone says "create a ticket for X", "file a
  bug for Y", "draft a JIRA story for Z", or describes work that needs to be
  tracked in JIRA.
license: MIT
metadata:
  author: QA Tester
  stlc-phase: Requirement Intake
  version: 1.0.0
---

# When to use

- Someone describes a bug, feature, or task and wants it turned into a JIRA ticket.
- Someone asks "create a ticket for ...", "file a bug: ...", "log this as a story".
- Someone pastes rough notes and wants them formalized into ticket fields.

### 1. Gather the raw input

- Take the user's description as given. If the project key or issue type is
  missing, ask — do not guess a project or invent a ticket type.
- Capture: summary, description, steps to reproduce (bugs), expected vs.
  actual (bugs), proposed acceptance criteria (stories), priority,
  component, labels, and related/linked issues.

### 2. Analyze & find the missing pieces

Run the input through `references/requiremnt-checklist.md`. For every item, mark:

- ✅ present / ⚠️ ambiguous / ❌ missing.
- Missing or vague acceptance criteria / repro steps
- Undefined priority, component, or issue type
- Ambiguous wording that two engineers could read two ways
- Unchecked duplicates or missing linked issues

### 3. Draft the ticket

- Fill `references/tempelates/jira_ticket_template.md` using only confirmed
  information.
- Flag every assumption inline rather than silently filling a field.

### 4. STOP for human review (mandatory)

End with a **Human Review Gate**:

- Summarize what you assumed and what you could not confirm.
- List the open questions from step 2 that block creation.
- Ask the requester to confirm/edit before the ticket is considered approved.
- Do **not** call `createJiraIssue` (or any ticket-creation tool/script)
  until a human explicitly approves the draft.

## Output shape

```text
## JIRA Draft — <Issue Type>: <Summary>
1. Proposed Fields (project, type, priority, component, labels)
2. Gaps & Questions for the requester   <--- surface missing pieces here
3. Draft Description / Acceptance Criteria / Repro Steps
4. Linked/Duplicate Issues Checked
5. Risks & Assumptions
--- HUMAN REVIEW GATE ---
Assumptions made / Open questions / "Approve or edit before I create this"
```

## Guardrails

- Never create the ticket in JIRA without explicit human approval of the draft.
- Never fabricate acceptance criteria, priority, or component — a missing
  field is a question, not a guess.
- Never include credentials, tokens, or `.env` contents in ticket output.
- Do not reveal personal information (PII) beyond what's necessary for the
  ticket (e.g. don't surface reporter email/token from `.env`).

## References

- `references/requiremnt-checklist.md` — the gap-analysis checklist for ticket completeness
- `references/tempelates/jira_ticket_template.md` — the ticket draft template to fill
- `assets/jira_info.txt` — worked example of a fully-drafted ticket (target quality bar)
- `scripts/fetch_jira.sh` — check for existing/duplicate tickets over the JIRA REST API
