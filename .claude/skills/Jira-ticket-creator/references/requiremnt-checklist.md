# Ticket Completeness Checklist

Use this checklist to check a feature/bug description for completeness
before drafting a JIRA ticket.

## Scoring

-   ✅ **Present** --- clearly specified.
-   ⚠️ **Ambiguous** --- unclear, incomplete, or open to interpretation.
-   ❌ **Missing** --- not specified.

**Rule:** Every ⚠️ or ❌ item becomes a question for the requester.

------------------------------------------------------------------------

## Core fields

-   [ ] Issue type identified (Bug / Story / Task / Epic)
-   [ ] Project key identified
-   [ ] Clear, specific summary (one line, concrete, no vague verbs)
-   [ ] Priority stated or reasonably inferable

------------------------------------------------------------------------

## Bug-specific (skip if not a bug)

-   [ ] Steps to reproduce
-   [ ] Expected result
-   [ ] Actual result
-   [ ] Environment (browser / OS / app version / build)
-   [ ] Severity / impact / frequency

------------------------------------------------------------------------

## Story / Task-specific (skip if a bug)

-   [ ] User story or clear goal ("As a ... I want ... so that ...")
-   [ ] Acceptance criteria are testable (observable pass/fail)
-   [ ] Out-of-scope behavior explicitly noted

------------------------------------------------------------------------

## Cross-cutting

-   [ ] Duplicate/related issues checked
-   [ ] Component / labels / fix version / sprint identified
-   [ ] Attachments or screenshots referenced if relevant
-   [ ] Assignee/reporter clear, or explicitly left for triage

------------------------------------------------------------------------

## Clarity

-   [ ] Unambiguous terminology
-   [ ] Expected behavior explicitly stated
-   [ ] No assumptions required to interpret the request
-   [ ] Open questions documented rather than guessed at

------------------------------------------------------------------------

## Gap-Analysis Output

For every requirement, record the following:

  Area             Status         Gap / Observation   Question for Requester
  ---------------- -------------- -------------------- -------------------------
  Core fields      ✅ / ⚠️ / ❌
  Bug/Story spec   ✅ / ⚠️ / ❌
  Cross-cutting    ✅ / ⚠️ / ❌
  Clarity          ✅ / ⚠️ / ❌

### Final Decision

-   [ ] Sufficiently complete to draft the ticket.
-   [ ] Needs clarification before drafting.
-   [ ] Critical gaps --- return to requester before drafting.

### Questions Generated from Gaps

List every question generated from an ⚠️ or ❌ item:

1.
2.
3.
4.
5.
