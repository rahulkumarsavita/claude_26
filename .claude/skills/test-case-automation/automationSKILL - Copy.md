---
name: test-case-automation
description: >
  Turn approved test cases (e.g. produced by the test-plan-generator skill)
  into a modular Python Selenium WebDriver + Pytest automation framework
  using the Page Object Model. Use when someone says "automate these test
  cases", "build a Selenium framework for X", "turn this test plan into
  automated tests", or asks to scaffold a pytest + Selenium project.
license: MIT
metadata:
  author: QA Tester
  stlc-phase: Test Automation
  version: 1.0.0
---

# When to use

- Approved test cases exist (a `*-test-cases.md` file such as `test-plan-generator/KAN-3-test-cases.md`, or pasted cases) and someone wants them automated.
- Someone asks to "build a Selenium framework", "automate this test plan", "scaffold a pytest + POM project for <site>".
- Someone wants automated tests wired to an HTML report with failure screenshots.

### 1. Gather inputs — do not skip

- Locate the source test cases and note which Test Case IDs are in scope. Do not automate untraced test cases — every generated test must map back to a Test Case ID.
- Identify the application under test: base URL and the pages/flows involved.
- Collect **real** element locators for every action referenced in the test steps — inspect the live page (fetch its HTML) or ask the user to paste DOM snippets / existing locators. **Never invent a locator, endpoint, or UI element.**
- If credentials are needed (login/signup tests), ask for env var names — never hardcode or fabricate credentials.

Apply `assets/ch_01_anti_hallucination.md` for this entire step: only use facts explicitly present in the test cases, the fetched HTML/DOM, or user input. A locator or behavior that can't be confirmed goes in "Missing / Unknown Information" — it does not get guessed into code.

### 2. Scaffold the framework

Follow the architecture in `assets/Automation_Exercise_Framework_Prompt.md`:

```text
<project>/
├── config/
│   └── config.py               # Base URL, browser, timeout, implicit wait
├── pages/
│   ├── base_page.py            # Common Selenium actions + explicit waits
│   └── <page>_page.py          # Locators & methods, one file per page
├── tests/
│   └── test_<feature>.py       # One pytest module per source test-case document
├── utils/
│   └── driver_factory.py       # WebDriver init (Chrome/Firefox, headless option)
├── screenshots/                # Failure screenshots (gitignored)
├── conftest.py                 # driver fixture + screenshot-on-failure hook
└── requirements.txt            # selenium, pytest, pytest-html, webdriver-manager
```

- `base_page.py` wraps `WebDriverWait`-based `click`, `type_text`, `get_text`, `is_displayed` — no raw Selenium calls anywhere else.
- Page classes inherit `BasePage`; locators are `By.XPATH` / `By.CSS_SELECTOR` constants sourced from step 1 only.
- `conftest.py`: a function/session-scoped `driver` fixture with `driver.quit()` teardown, plus a `pytest_runtest_makereport` hook that captures `save_screenshot()` on failure and attaches it via `pytest-html` extras.
- Standard run command: `pytest --html=reports/report.html --self-contained-html`.

### 3. Generate the tests — traceable, not invented

- One pytest function per source Test Case ID (e.g. `def test_tc01_add_single_product_to_cart():`), with the ID and expected result in the docstring.
- Test bodies only call page-object methods and assert on the Expected Result from the source test case — no logic that bypasses the POM layer.
- Any step whose locator/behavior is unverified: leave `# TODO: unverified locator — <what's needed>` instead of guessing, and surface it in the Missing/Unknown section of the output.

### 4. Self-validation (mandatory)

Before presenting the draft, run the Step 3/4 self-check from `assets/ch_01_anti_hallucination.md`: re-scan the generated code for any locator, endpoint, or assertion that isn't traceable to a verified fact from step 1. Fix it or flag it — don't ship an unflagged guess.

### 5. STOP for human review (mandatory)

End with a **Human Review Gate**:

- List every unverified locator/assumption and the file it's in.
- Do **not** run the generated suite against a live/production site until the user confirms it's safe — flows like checkout, signup, or cart mutation have real side effects.
- Ask for approval before the framework is considered final.

## Output shape

```text
## Automation Draft — <feature/JIRA-KEY>
1. Source Test Cases Used (file + IDs covered)
2. Verified Facts (locators/behavior confirmed, with source)
3. Missing / Unknown Information (flagged, not guessed)
4. Framework Structure Generated (file tree + purpose per file)
5. Traceability Map (Test Case ID -> pytest test function)
6. Self-Validation Check
--- HUMAN REVIEW GATE ---
Unverified assumptions / Open questions / "Approve before running against the live site"
```

## Guardrails

- Never invent element locators, API endpoints, error messages, or UI behavior not present in the test cases, fetched DOM, or user input — mark as "Insufficient information to determine" instead (per `assets/ch_01_anti_hallucination.md`).
- Every generated test function must trace to a source Test Case ID; don't add untraced "bonus" tests without calling them out as additions.
- Enforce POM strictly: no direct `driver.find_element` calls inside `tests/`.
- Never hardcode credentials or PII; use environment variables / fixtures.
- Never execute the generated suite against a live/production target without explicit user confirmation.
- Keep `screenshots/` and generated `reports/` out of version control (call out the need for a `.gitignore` entry).

## References

- `assets/Automation_Exercise_Framework_Prompt.md` — target framework architecture/spec to scaffold
- `assets/ch_01_anti_hallucination.md` — anti-hallucination rules governing locator/behavior verification
- `test-plan-generator` skill — typical source of the input test-case documents (e.g. `KAN-3-test-cases.md`)
