## Test Plan — KAN-3: Cart - Add Products to Cart and Verify Quantity & Price Calculation

### 1. Scope & Objectives

- Objective: Verify that a customer can add products to the cart on automationexercise.com, that cart line-item and subtotal calculations are correct, and that items can be removed dynamically.
- Application under test: https://automationexercise.com/
- In scope: adding products from `/products`, the add-to-cart confirmation modal, cart contents/pricing on `/view_cart`, and item removal.
- Out of scope: checkout/payment flow (AE-103 equivalent), login/signup, product search (AE-101 equivalent), coupon/discount logic.
- Priority: Highest (per KAN-3)
- Risk assumption: Medium — pricing calculations are a common source of regressions.

### 2. Gaps & Questions for the author

- KAN-3's acceptance criteria use illustrative prices (Product 1 = $500, Product 2 = $400, subtotal = $900). The actual product catalog on automationexercise.com has its own real product IDs/prices — these need to be confirmed against the live site before execution; do not assume the ticket's example prices are the real catalog values.
- No guest-vs-logged-in distinction is stated — confirm whether cart behavior must be verified for both guest and logged-in users, or guest only.
- No behavior is specified for increasing/decreasing quantity *after* an item is already in the cart (the AC only covers adding and full removal) — confirm if in-cart quantity editing is in scope for this ticket.
- No behavior is specified for what happens when the cart is emptied entirely (empty-cart state/messaging).
- No performance, accessibility, or browser-matrix expectations are stated for this ticket.
- Non-functional/cross-cutting items below are carried over from the ticket's own gaps (Component/Fix Version fields were not available in this JIRA project and were only noted as free text on the ticket).

### 3. Test Scenarios (P0/P1/P2)

**P0 — Core acceptance criteria**

- P0-01: Add a single product to the cart from `/products` and verify the confirmation modal.
- P0-02: Verify cart line-item details (thumbnail, name, category, price, quantity, total) on `/view_cart`.
- P0-03: Verify per-row Item Total = Unit Price × Quantity.
- P0-04: Verify cart subtotal across multiple distinct products.
- P0-05: Remove an item via the delete (X) control and verify it updates without a full page reload.

**P1 — Secondary paths implied by the AC**

- P1-01: "Continue Shopping" from the modal returns to the product listing with the item still in the cart.
- P1-02: "View Cart" from the modal navigates directly to `/view_cart`.
- P1-03: Add the same product a second time and verify quantity/total behavior.
- P1-04: Remove all items and verify the resulting empty-cart state.
- P1-05: Increase quantity on the product detail page before adding, and verify the cart reflects that quantity.

**P2 — Gaps / edge cases surfaced during analysis**

- P2-01: Cart contents persist after a page refresh (same session).
- P2-02: Add-to-cart control is operable via keyboard only (basic accessibility check).

### 4. Test Data & Environment

- Environment: Production (https://automationexercise.com/)
- Test data: at least two distinct, currently-listed products with known catalog prices (to be confirmed live, not assumed from the ticket's example figures).
- Preconditions: site is reachable; no login required for cart scenarios (guest checkout is supported on this site) unless Q2 above says otherwise.

### 5. Risks & Assumptions

- Risk: price/quantity calculation bugs are the primary regression risk for this feature.
- Risk: since this is a public demo site, catalog contents/prices may change over time, which would invalidate hard-coded test data.
- Assumption: cart scenarios are tested as a guest user unless told otherwise.
- Assumption: "dynamically... without a full page refresh" (AC) means an AJAX-style DOM update; this plan treats a visible full navigation/reload on delete as a failure.

### 6. Entry / Exit criteria

**Entry criteria**
- automationexercise.com is reachable and `/products` lists purchasable items.
- At least two distinct products are available to use as test data.

**Exit criteria**
- All P0 scenarios pass.
- Cart totals/subtotals are arithmetically correct in every executed scenario.
- No full-page reload occurs on item removal.
- Open questions in section 2 are answered or explicitly deferred by the requester.

--- HUMAN REVIEW GATE ---

Assumptions made / Open questions

- Treating this as a guest-cart flow with no login requirement, and assuming real catalog prices will be substituted for the ticket's illustrative $500/$400 example once confirmed against the live site.
- The five open questions in section 2 (guest vs. logged-in, in-cart quantity editing, empty-cart state, catalog data, and non-functional scope) are not yet answered.

Approve or edit before I continue — this plan and the test cases below are drafts, not final. Confirm the open questions, or tell me to proceed with the stated assumptions.
