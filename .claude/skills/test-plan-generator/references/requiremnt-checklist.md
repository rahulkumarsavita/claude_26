# Requirement Gap-Analysis Checklist

Use this checklist to analyze requirements for completeness and identify
gaps before creating test cases or automation.

## Scoring

Score every row:

-   ✅ **Present** --- the requirement is clearly specified.
-   ⚠️ **Ambiguous** --- the requirement is unclear, incomplete, or open
    to interpretation.
-   ❌ **Missing** --- the requirement is not specified.

**Rule:** Every ⚠️ or ❌ item becomes a question for the
ticket/requirement author.

------------------------------------------------------------------------

## Functional

-   [ ] Clear user story / goal ("As a ... I want ... so that ...")
-   [ ] Acceptance criteria are testable (observable pass/fail)
-   [ ] Happy path fully described
-   [ ] Negative / error paths described (bad input, failure responses)
-   [ ] Boundary & empty states described (0, 1, max, empty list, null)
-   [ ] State transitions / workflow steps enumerated

------------------------------------------------------------------------

## Data & Environment

-   [ ] Required test data specified or derivable
-   [ ] Environment / config / feature flags named
-   [ ] External dependencies & integrations listed
-   [ ] Preconditions / setup stated

------------------------------------------------------------------------

## Non-functional (often missing)

-   [ ] Performance / load expectations
-   [ ] Security / authorization (which roles can/can't)
-   [ ] Accessibility (a11y) expectations
-   [ ] Internationalization / localization
-   [ ] Audit / logging / observability

------------------------------------------------------------------------

## Cross-cutting

-   [ ] Impact on existing features (regression surface)
-   [ ] Backward compatibility / migration
-   [ ] Mobile / responsive / browser matrix
-   [ ] Rollback / feature-flag behavior

------------------------------------------------------------------------

## Clarity

Use this section to verify that the requirement is sufficiently clear
for implementation and testing.

-   [ ] Requirement uses clear and unambiguous terminology
-   [ ] Expected behavior is explicitly stated
-   [ ] Scope and out-of-scope behavior are identified
-   [ ] Inputs, outputs, and expected results are clear
-   [ ] No assumptions are required to interpret the requirement
-   [ ] Open questions and unresolved decisions are documented

------------------------------------------------------------------------

## Requirement Gap-Analysis Output

For every requirement, record the following:

  Area                 Status         Gap / Observation   Question for Requirement Author
  -------------------- -------------- ------------------- ---------------------------------
  Functional           ✅ / ⚠️ / ❌                       
  Data & Environment   ✅ / ⚠️ / ❌                       
  Non-functional       ✅ / ⚠️ / ❌                       
  Cross-cutting        ✅ / ⚠️ / ❌                       
  Clarity              ✅ / ⚠️ / ❌                       

### Final Decision

-   [ ] Requirement is sufficiently complete for test-case design.
-   [ ] Requirement needs clarification before test-case design.
-   [ ] Requirement has critical gaps and should be returned to the
    author.

### Questions Generated from Gaps

List every question generated from an ⚠️ or ❌ item:

1.  
2.  
3.  
4.  
5.  
