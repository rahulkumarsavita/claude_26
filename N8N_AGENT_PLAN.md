# n8n Multi-Agent Plan — JIRA → Test Plan → Automation

Status: DRAFT for review. Nothing here has been built yet. This plan sticks strictly to what exists today in `.claude/skills/` — no invented n8n nodes, credentials, or hosting details.

## 1. What exists today (source of truth)

Three Claude Code skills were analyzed directly from their `SKILL.md` files:

| Skill | Folder | Input | Output | Human gate? |
|---|---|---|---|---|
| **Jira-ticket-creator** | `.claude/skills/Jira-ticket-creator/` | Rough feature/bug description + JIRA project name | Draft JIRA ticket, issue type fixed to **Story** (fields + description/AC), using `references/tempelates/jira_ticket_template.md` | Yes — stops before calling `createJiraIssue`, requires human approval |
| **test-plan-generator** | `.claude/skills/test-plan-generator/` | A JIRA key (e.g. `KAN-2`) or pasted ticket body | Test plan (`.md`) + test cases (`.md` + `.csv`), via `scripts/fetch_jira.sh` and templates in `references/` | Yes — stops before writing test cases/automation, requires human approval |
| **test-case-automation** | `.claude/skills/test-case-automation/` | Approved test-case file (e.g. `KAN-3-test-cases.md`) | Pytest + Selenium POM framework per `assets/Automation_Exercise_Framework_Prompt.md`, self-checked against `assets/ch_01_anti_hallucination.md` | Yes — stops before running the suite against a live site, requires human approval |

All three skills already enforce, in writing:
- No fabricated fields, locators, endpoints, or acceptance criteria — unknowns are surfaced as questions, never guessed.
- A mandatory **Human Review Gate** before the artifact is treated as final / before the next stage consumes it.
- No credentials, tokens, or PII in outputs.

This plan preserves all three gates — it does not automate past a human approval step, because the skills explicitly forbid that.

## 2. Goal

Wrap these three skills as three cooperating agents inside a single n8n workflow, so a user can:
1. Submit a raw request → get a JIRA ticket draft.
2. Approve it → get a test plan + test cases for that ticket.
3. Approve those → get an automated Selenium/Pytest framework for those test cases.

...through one UI, with each stage gated by explicit human approval (matching the skills' existing guardrails).

## 3. Open questions (must be answered before build — not assumed)

These are not in the skill files or repo, so per anti-hallucination rules I'm not guessing them. **Resolved by user instruction:**

- ✅ **Trigger**: n8n **Form Trigger** node (confirmed) — this also answers "approval mechanism" for the initial submission: the workflow starts from a form.
- ✅ **Issue type**: fixed to **Story** (confirmed) — Agent 1 no longer asks "bug or story", it always drafts a Story.
- ✅ **JIRA project**: the Form Trigger asks for **JIRA project name** as a required field, and the ticket is created in that project (confirmed) — this also resolves the skill's "ask if project key is missing" step: the form is where it's asked.

**Still open:**

1. **How does n8n get Claude Code's skill behavior?** The skills are Markdown instruction files consumed by Claude Code, not a callable API. n8n needs an actual invocation path — e.g. an HTTP node calling the Claude/Anthropic API with the skill's `SKILL.md` + references injected as the system/context prompt, or a node that shells out to `claude` CLI. **Which of these is available in your n8n environment?**
2. **JIRA connectivity**: `scripts/fetch_jira.sh` expects `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_TOKEN`. Does n8n have its own JIRA credentials/node, or should it call the same script/env vars?
3. **Where does automation actually run?** `test-case-automation` produces a Pytest project; n8n does not execute Selenium/browser tests natively. Do you want n8n to (a) just generate the framework files, or (b) also trigger a runner (e.g. shell/CI job) to execute `pytest` and produce the `.html` report shown in your sketch?
4. **Approval mechanism for gates #2 and #3** (after the initial Form Trigger kicks things off): still needs a wait/approve step — another n8n form (`n8n-nodes-base.form` "Wait for form submission"), Slack, or email? The sketch's later buttons ("Enable button to run automation", "create link for result view") suggest these could also be additional form steps in the same UI, but that's not yet confirmed.
5. **File storage/hosting** for the CSV/XLSX downloads and the HTML report link shown in your sketch — local disk, S3, or n8n binary data passed through the UI?

I will not invent answers to the still-open items; the plan below marks each affected step with **[NEEDS DECISION]** and gives the most likely default only as a labeled option, not a commitment.

## 4. Proposed n8n architecture (3 agents, matching the 3 skills 1:1)

```
[Form Trigger: raw description + JIRA project name]
        │
        ▼
┌─────────────────────────┐
│ Agent 1 — Ticket Agent   │  = Jira-ticket-creator skill
│ In: raw description +    │
│     JIRA project name    │
│ Issue type: Story (fixed)│
│ Out: JIRA ticket draft    │
└─────────────────────────┘
        │
   [Human Review Gate #1 — approve/edit draft]  ← required by skill, not skippable
        │  (on approval)
        ▼
┌─────────────────────────┐
│ Agent 2 — Test Plan Agent│  = test-plan-generator skill
│ In: approved JIRA key/body│
│ Out: test plan + test     │
│      cases (.md + .csv)   │
└─────────────────────────┘
        │
   [Human Review Gate #2 — approve/edit test cases]  ← required by skill
        │  (on approval)
        ▼
┌─────────────────────────┐
│ Agent 3 — Automation Agent│ = test-case-automation skill
│ In: approved test cases   │
│ Out: pytest+Selenium POM  │
│      framework + report   │
└─────────────────────────┘
        │
   [Human Review Gate #3 — approve before running against live site]  ← required by skill
        │  (on approval)
        ▼
[UI: run pytest, show .html report link]
```

Each "Agent" box = one n8n sub-workflow (or a set of nodes) whose prompt/context is that skill's `SKILL.md` + its `references/`/`assets/` files, invoked per **Open Question 1** above.

## 5. UI (matching your sketch, 3 panels)

| Panel in sketch | Maps to |
|---|---|
| "Upload all resources and documents" | The **Form Trigger** for Agent 1: fields for raw request/description **and JIRA project name** (required), plus optional file upload for supporting docs used as Agent 2/3 context |
| "Test Plan / Test cases details — download in .CSV — create button to download" | Output of Agent 2: download buttons for the `.md`/`.csv` test-plan and test-case files it already produces |
| "Enable button to run automation / show results in .html / link for result view" | Trigger for Agent 3 + a run step (per Open Question 3), surfacing `pytest --html=reports/report.html --self-contained-html` as a link |

Each panel needs its own **approve/reject** control before advancing, to preserve each skill's Human Review Gate — this is a hard requirement from the skill files, not optional polish.

## 6. Build steps (once Section 3 is answered)

1. Stand up the invocation mechanism chosen for Open Question 1 (n8n node that calls Claude with a skill's instructions as context).
2. Build the **Form Trigger** node: fields = description/request (required), JIRA project name (required), optional file upload.
3. Build Agent 1 sub-workflow: form input → Claude call w/ Jira-ticket-creator context, issue type hardcoded to **Story** → output draft → **wait-for-approval node**.
4. On approval, only then call the real JIRA creation step, targeting the project name captured in the form (the skill explicitly disallows creating the ticket pre-approval).
5. Build Agent 2 sub-workflow: takes the created/approved ticket key → fetch via JIRA (Open Question 2) → Claude call w/ test-plan-generator context → output `.md`/`.csv` → **wait-for-approval node**.
6. Build Agent 3 sub-workflow: takes approved test cases → Claude call w/ test-case-automation context → generate framework files → self-validation output → **wait-for-approval node**.
7. Build the remaining UI steps (approval mechanism per Open Question 4) with the 3 panels above, wired to trigger each sub-workflow and render each approval gate and each output/download link.
8. If in scope (Open Question 3): wire a run step that executes the generated Pytest suite and exposes the resulting `.html` report link.

## 7. Guardrails carried over unchanged from the skills

- No ticket is created, no test cases are finalized, and no automation suite is run against a live site without an explicit human approval click at each of the 3 gates.
- No fabricated locators, tickets fields, or acceptance criteria at any stage — unresolved items are surfaced as questions in the UI, not silently filled in.
- No credentials/tokens/PII rendered in any UI output.

---

**This is a draft plan only.** Before any n8n workflow is built, please answer the 5 open questions in Section 3 — particularly #1 (how n8n actually invokes Claude/the skills) and #3 (whether n8n should execute the tests or only generate the framework), since those decide the node types used throughout.
