# Automation Draft — KAN-3: Cart - Add Products to Cart and Verify Quantity & Price Calculation

Site under test: https://automationexercise.com/
Source test cases: `.claude/skills/test-case-automation/references/KAN-3-test-cases.md` (TC-01–TC-12)
Framework generated at: `automation_exercise_framework/`

---

## 1. Source Test Cases Used

| Test Case ID | Priority | Test Case Name | Automated? |
| --- | --- | --- | --- |
| TC-01 | P0 | Add a single product to the cart from the product listing | Yes |
| TC-02 | P0 | Cart displays correct item details after adding a product | Yes |
| TC-03 | P0 | Item Total equals Unit Price x Quantity | Yes |
| TC-04 | P0 | Cart subtotal is correct for multiple products | Yes |
| TC-05 | P0 | Remove an item from the cart dynamically | Yes |
| TC-06 | P1 | "Continue Shopping" keeps the item in the cart | Yes |
| TC-07 | P1 | "View Cart" navigates to the cart page | Yes |
| TC-08 | P1 | Add the same product to the cart twice | Yes |
| TC-09 | P1 | Removing all items shows the empty-cart state | Yes |
| TC-10 | P1 | Add product with increased quantity from the product detail page | Yes |
| TC-11 | P2 | Cart contents persist after a page refresh | Yes |
| TC-12 | P2 | Add-to-cart control is operable via keyboard only | Yes (expected to fail — see Findings) |

---

## 2. Verified Facts

All locators below were confirmed against the **live** site on 2026-08-19 — not recalled from memory — via `curl` fetches and a real session round-trip (GET `/view_cart` for a session cookie → GET `/add_to_cart/<id>` against that cookie → re-fetch `/view_cart` to inspect the server-rendered rows), plus reading the site's own `static/js/cart.js`.

| # | Fact | Source |
| --- | --- | --- |
| 1 | Product card add-to-cart: `a.add-to-cart[data-product-id="<id>"]`, one inside `.productinfo`, one inside `.product-overlay .overlay-content` | `curl /products` |
| 2 | Confirmation modal: `#cartModal`; "Continue Shopping" = `.close-modal`; "View Cart" = `a[href='/view_cart']` inside the modal | `curl /products` |
| 3 | Product name/price on listing: `.productinfo p` (name), `.productinfo h2` (price) | `curl /products` |
| 4 | Cart AJAX endpoints: `GET /add_to_cart/<id>`, `GET /delete_cart/<id>` | `static/js/cart.js` |
| 5 | Cart table: `#cart_info_table`; row id `#product-<id>`; cells `.cart_price`, `.cart_quantity button`, `.cart_total_price`; delete control `.cart_quantity_delete[data-product-id]` | `static/js/cart.js` + live `/view_cart` after seeding a session cart |
| 6 | Empty-cart state: `#empty_cart` (shown), `#cart_info_table` hidden — toggled by `cart.js` once the last row is deleted | `static/js/cart.js` |
| 7 | Product detail page: quantity input `#quantity`, hidden `#product_id`, add-to-cart button `button.cart` | `curl /product_details/1` |
| 8 | **TC-08 resolved**: adding the same product twice increments `Quantity` on the existing `#product-<id>` row (confirmed 2 → same row, quantity `2`) — it does **not** create a duplicate row | Live session test: two `GET /add_to_cart/1` calls, one cookie jar |
| 9 | Product fixtures: `product_id=1` → "Blue Top", Rs. 500; `product_id=2` → "Men Tshirt", Rs. 400 | Live `/products` + `/view_cart` |
| 10 | Cart is session/cookie-backed: items added under one cookie jar were still present on a later `/view_cart` fetch using the same cookies | Live session test |

---

## 3. Missing / Unknown Information

| # | Item | Why it's flagged | Handling in the generated code |
| --- | --- | --- | --- |
| 1 | Whether `driver.refresh()` specifically (vs. a fresh request with the same cookies) preserves cart state | Only cross-request persistence was verified via `curl`; a real browser refresh was not executed in this environment (no Selenium runtime here) | TC-11's test is written per the documented expected result — **Inference (high confidence)** from fact #10, not a guess |
| 2 | Whether the "Add to cart" anchor is reachable via Tab in a real browser | The live markup has no `href`/`tabindex` on `a.add-to-cart`, so per the HTML spec it is excluded from the default tab order | See Finding below — test asserts the *documented* expected result, not the observed markup, and is expected to fail |
| 3 | ~~Actual test execution results (pass/fail)~~ | Resolved — the user asked for the suite to be installed and run against the live site; see §8 | — |

Nothing else needed guessing: TC-06/07 modal behavior, TC-05/09 delete behavior, and TC-02/03/04 price math were all directly observable from the verified facts above.

---

## 4. Framework Structure Generated

```text
automation_exercise_framework/
├── config/
│   └── config.py               # BASE_URL, browser, headless flag, explicit-wait timeout
├── pages/
│   ├── base_page.py            # Common Selenium actions (click, type_text, get_text, hover, waits)
│   ├── products_page.py        # /products: add-to-cart, modal, keyboard-focusability check (TC-12)
│   ├── product_detail_page.py  # /product_details/<id>: quantity input + add-to-cart (TC-10)
│   └── cart_page.py            # /view_cart: row/price/quantity/total/delete/empty-state
├── tests/
│   └── test_cart.py            # TC-01–TC-12, one pytest function per Test Case ID
├── utils/
│   └── driver_factory.py       # Chrome/Firefox WebDriver via webdriver-manager, headless option
├── screenshots/                # Failure screenshots (gitignored, .gitkeep only)
├── reports/                    # pytest-html output (gitignored, .gitkeep only)
├── conftest.py                 # driver fixture + screenshot-on-failure hook wired to pytest-html
├── pytest.ini                  # pythonpath = . (so pages/config/utils import cleanly)
├── requirements.txt            # selenium, pytest, pytest-html, webdriver-manager
├── .gitignore
└── automation-result.md        # this file
```

Not generated: `home_page.py`, `login_page.py`, `test_signup.py` — the source test-case document (KAN-3) covers only the cart flow, so signup/login page objects would be untraced additions per the skill's guardrails. Add them in a follow-up pass if signup/login test cases are supplied.

---

## 5. Traceability Map

| Test Case ID | pytest test function | File |
| --- | --- | --- |
| TC-01 | `test_tc01_add_single_product_to_cart` | `tests/test_cart.py` |
| TC-02 | `test_tc02_cart_shows_correct_item_details` | `tests/test_cart.py` |
| TC-03 | `test_tc03_item_total_equals_price_times_quantity` | `tests/test_cart.py` |
| TC-04 | `test_tc04_cart_subtotal_correct_for_multiple_products` | `tests/test_cart.py` |
| TC-05 | `test_tc05_remove_item_from_cart_dynamically` | `tests/test_cart.py` |
| TC-06 | `test_tc06_continue_shopping_keeps_item_in_cart` | `tests/test_cart.py` |
| TC-07 | `test_tc07_view_cart_navigates_to_cart_page` | `tests/test_cart.py` |
| TC-08 | `test_tc08_add_same_product_twice_increments_quantity` | `tests/test_cart.py` |
| TC-09 | `test_tc09_removing_all_items_shows_empty_cart_state` | `tests/test_cart.py` |
| TC-10 | `test_tc10_add_product_with_increased_quantity_from_detail_page` | `tests/test_cart.py` |
| TC-11 | `test_tc11_cart_contents_persist_after_refresh` | `tests/test_cart.py` |
| TC-12 | `test_tc12_add_to_cart_control_is_keyboard_operable` | `tests/test_cart.py` |

---

## 6. Findings (surfaced by verification, not invented)

| Finding | Detail | Recommendation |
| --- | --- | --- |
| TC-08 ambiguity resolved | Live behavior increments quantity on the existing row rather than duplicating it | Update `KAN-3-test-cases.md`'s TC-08 Expected Result from "To be confirmed" to the confirmed behavior |
| TC-12 likely fails as written | `a.add-to-cart` has no `href`/`tabindex`, so it's outside the default Tab order in a real browser — the control is currently **not** keyboard-operable | Either fix the markup (add `href="#"` or `tabindex="0"` + a keydown handler) or revise TC-12's expected result to match intended (not actual) behavior — flagging for human decision, not silently changed |

---

## 7. Self-Validation Check

- Re-scanned every locator in `pages/*.py` against the Verified Facts table — no locator appears that isn't sourced from item #1–#10 above.
- Every `tests/test_cart.py` function is named `test_tc<NN>_...` and its docstring cites the source Test Case ID — no untraced "bonus" tests were added.
- No credentials, tokens, or PII appear anywhere in the framework (cart/browse flows only — no login required).
- `py_compile` passed for all 8 generated `.py` files (no syntax errors).
- Executed against the live site with real ChromeDriver — see §8. Pass/fail status is now a runtime result, not a prediction.

---

## 8. Live Execution Results (2026-08-19)

Run with `pip install -r requirements.txt && pytest --html=reports/report.html --self-contained-html`, headless Chrome via `webdriver-manager`, against the live `https://automationexercise.com/`.

| Test Case ID | pytest function | Result | Notes |
| --- | --- | --- | --- |
| TC-01 | `test_tc01_add_single_product_to_cart` | ✅ PASS | |
| TC-02 | `test_tc02_cart_shows_correct_item_details` | ✅ PASS | |
| TC-03 | `test_tc03_item_total_equals_price_times_quantity` | ✅ PASS | |
| TC-04 | `test_tc04_cart_subtotal_correct_for_multiple_products` | ✅ PASS | |
| TC-05 | `test_tc05_remove_item_from_cart_dynamically` | ✅ PASS | |
| TC-06 | `test_tc06_continue_shopping_keeps_item_in_cart` | ✅ PASS | |
| TC-07 | `test_tc07_view_cart_navigates_to_cart_page` | ✅ PASS | |
| TC-08 | `test_tc08_add_same_product_twice_increments_quantity` | ✅ PASS | Confirms the Finding in §6 |
| TC-09 | `test_tc09_removing_all_items_shows_empty_cart_state` | ✅ PASS | |
| TC-10 | `test_tc10_add_product_with_increased_quantity_from_detail_page` | ✅ PASS | |
| TC-11 | `test_tc11_cart_contents_persist_after_refresh` | ✅ PASS | One earlier run timed out on this test when executed back-to-back with the full suite (11th of 12 browser sessions against the live external server); reran in isolation and standalone in a full run and it passed both times. Treated as network flakiness against a live third-party site, not a locator/logic defect — no code change was needed. |
| TC-12 | `test_tc12_add_to_cart_control_is_keyboard_operable` | ❌ FAIL (expected) | Confirms the Finding in §6 — `assert False`, `is_add_to_cart_keyboard_focusable()` returns `False` because the live `add-to-cart` anchor has no `href`/`tabindex`. Reproduced consistently across 3 runs. |

**Result: 11/12 passed, 1 expected failure (TC-12).** Full HTML report with the TC-12 failure screenshot: `automation_exercise_framework/reports/report.html`.

**Bug fixed during the first run:** `conftest.py`'s screenshot-on-failure hook initially passed raw PNG bytes to `pytest_html.extras.image()`, which crashed report generation (`AttributeError: 'bytes' object has no attribute 'encode'`) on `pytest-html` 4.2.0 — that version expects base64-encoded text. Fixed by base64-encoding the screenshot before attaching it, and updated the deprecated `report.extra` attribute to `report.extras` while in there.

---

## --- HUMAN REVIEW GATE ---

**Unverified assumptions:** none remaining — TC-11's refresh persistence is now directly confirmed by a real `driver.refresh()` call, not just inferred.

**Open questions:**
- Confirm the intended fix for TC-08's original "To be confirmed" language (now resolved — see Findings).
- **TC-12 needs a decision**: the suite confirms the Add to cart control is not currently keyboard-operable. Either fix the site markup (add `href="#"`/`tabindex="0"` + keydown handling) or revise TC-12's expected result to match current behavior. Until decided, this test will keep failing on every run — that's intentional, not a framework bug.

**Approve, or edit the flagged items above, before this framework is considered final.**
