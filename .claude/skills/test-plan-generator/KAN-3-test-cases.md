# Test Cases — KAN-3: Cart - Add Products to Cart and Verify Quantity & Price Calculation

Site under test: https://automationexercise.com/

## Test Case Summary

| Test Case ID | Priority | Test Case Name |
| --- | --- | --- |
| TC-01 | P0 | Add a single product to the cart from the product listing |
| TC-02 | P0 | Cart displays correct item details after adding a product |
| TC-03 | P0 | Item Total equals Unit Price x Quantity |
| TC-04 | P0 | Cart subtotal is correct for multiple products |
| TC-05 | P0 | Remove an item from the cart dynamically |
| TC-06 | P1 | "Continue Shopping" keeps the item in the cart |
| TC-07 | P1 | "View Cart" navigates to the cart page |
| TC-08 | P1 | Add the same product to the cart twice |
| TC-09 | P1 | Removing all items shows the empty-cart state |
| TC-10 | P1 | Add product with increased quantity from the product detail page |
| TC-11 | P2 | Cart contents persist after a page refresh |
| TC-12 | P2 | Add-to-cart control is operable via keyboard only |

---

# Test Case: TC-01 - Add a single product to the cart from the product listing

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-01 |
| **Test Case Name** | Add a single product to the cart from the product listing |
| **Precondition** | `/products` is loaded and lists at least one purchasable product. |
| **Description** | Verify that hovering over a product card and clicking "Add to cart" adds the product and shows the confirmation modal. |
| **Expected Result** | The product is added to the cart and a confirmation modal is displayed with "Continue Shopping" and "View Cart" options. |

---

## Test Steps

1. Navigate to `/products` — the product listing page loads with product cards visible.
2. Hover over a product card — an "Add to cart" overlay button appears on the card.
3. Click "Add to cart" — a modal appears with the message "Your product has been added to cart." and Continue Shopping / View Cart options.

---

# Test Case: TC-02 - Cart displays correct item details after adding a product

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-02 |
| **Test Case Name** | Cart displays correct item details after adding a product |
| **Precondition** | One product has already been added to the cart (per TC-01). |
| **Description** | Verify that `/view_cart` shows the correct thumbnail, name, category, price, quantity, and total price for an added item. |
| **Expected Result** | The cart row matches the product that was added, with all required fields populated. |

---

## Test Steps

1. Click "View Cart" from the confirmation modal (or navigate to `/view_cart`) — the cart page loads.
2. Inspect the row for the added product — it shows item thumbnail, Name, Category, Price, Quantity, and Total Price matching the product added.

---

# Test Case: TC-03 - Item Total equals Unit Price x Quantity

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-03 |
| **Test Case Name** | Item Total equals Unit Price x Quantity |
| **Precondition** | A product with a known unit price and quantity is in the cart. |
| **Description** | Verify the per-row Total Price is calculated correctly. |
| **Expected Result** | Total Price for the row = Unit Price x Quantity. |

---

## Test Steps

1. Add a product to the cart with a known price — the product appears in the cart with Quantity = 1 by default.
2. On `/view_cart`, note the Price and Quantity columns for the row — both values are visible and legible.
3. Compute Price x Quantity and compare to the Total Price column — Total Price equals Price x Quantity exactly.

---

# Test Case: TC-04 - Cart subtotal is correct for multiple products

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-04 |
| **Test Case Name** | Cart subtotal is correct for multiple products |
| **Precondition** | Cart is empty; two distinct products with known prices are available in the catalog. |
| **Description** | Verify that adding two distinct products results in a correct overall cart subtotal. |
| **Expected Result** | Cart subtotal equals the sum of each row's Total Price. |

---

## Test Steps

1. Add the first product to the cart — a confirmation modal appears and the item is added.
2. Click "Continue Shopping" and add a second, different product — the confirmation modal appears again and the second item is added.
3. Navigate to `/view_cart` — both products are listed as separate rows with correct individual Total Price values.
4. Sum the Total Price of both rows — the sum equals the cart's overall subtotal.

---

# Test Case: TC-05 - Remove an item from the cart dynamically

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-05 |
| **Test Case Name** | Remove an item from the cart dynamically |
| **Precondition** | At least one item is in the cart. |
| **Description** | Verify that clicking the delete (X) control removes an item without a full page reload. |
| **Expected Result** | The item row disappears and remaining totals update, with no full page reload/navigation. |

---

## Test Steps

1. On `/view_cart`, note the current items and subtotal — the cart state before deletion is recorded.
2. Click the X (Delete) icon on one item's row — the row is removed from the table immediately, without a full page reload.
3. Re-check the subtotal/remaining rows — the subtotal reflects only the remaining items and the deleted item's price is no longer included.

---

# Test Case: TC-06 - "Continue Shopping" keeps the item in the cart

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-06 |
| **Test Case Name** | "Continue Shopping" keeps the item in the cart |
| **Precondition** | A product has just been added and the confirmation modal is visible. |
| **Description** | Verify that dismissing the confirmation modal via "Continue Shopping" does not lose the added item. |
| **Expected Result** | User returns to the product listing and the item remains in the cart. |

---

## Test Steps

1. Add a product to the cart — the confirmation modal appears.
2. Click "Continue Shopping" — the modal closes and the product listing page is shown.
3. Navigate to `/view_cart` — the previously added product is still present in the cart.

---

# Test Case: TC-07 - "View Cart" navigates to the cart page

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-07 |
| **Test Case Name** | "View Cart" navigates to the cart page |
| **Precondition** | A product has just been added and the confirmation modal is visible. |
| **Description** | Verify that the "View Cart" option in the confirmation modal navigates directly to the cart. |
| **Expected Result** | User is taken to `/view_cart` showing the added item. |

---

## Test Steps

1. Add a product to the cart — the confirmation modal appears.
2. Click "View Cart" — the user is navigated to `/view_cart`.
3. Inspect the cart contents — the added product is listed with correct details.

---

# Test Case: TC-08 - Add the same product to the cart twice

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-08 |
| **Test Case Name** | Add the same product to the cart twice |
| **Precondition** | Cart is empty. |
| **Description** | Verify cart behavior when the same product is added more than once (quantity increment vs. duplicate row) — behavior is not specified in the ticket, so this test documents actual behavior for review. |
| **Expected Result** | To be confirmed — either quantity increments on a single row, or a duplicate row is created. Flag as an open question in the test plan. |

---

## Test Steps

1. Add a product to the cart — the item appears in the cart with Quantity = 1.
2. Add the same product to the cart again — observe whether Quantity increments on the existing row or a new row is added.
3. Verify the subtotal against the observed behavior — the subtotal matches Unit Price x total Quantity for that product, regardless of row layout.

---

# Test Case: TC-09 - Removing all items shows the empty-cart state

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-09 |
| **Test Case Name** | Removing all items shows the empty-cart state |
| **Precondition** | One or more items are in the cart. |
| **Description** | Verify the cart's empty state after all items are removed — exact messaging is not specified in the ticket. |
| **Expected Result** | Cart displays an empty-state message/UI once all rows are removed; no stale totals remain. |

---

## Test Steps

1. On `/view_cart`, delete every item one at a time — each deletion removes its row without a full page reload.
2. After the last item is removed, inspect the cart — it shows an empty-cart message/state, and no leftover subtotal is displayed.

---

# Test Case: TC-10 - Add product with increased quantity from the product detail page

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-10 |
| **Test Case Name** | Add product with increased quantity from the product detail page |
| **Precondition** | A product detail page with a quantity selector is available. |
| **Description** | Verify that a quantity set on the product detail page (before clicking Add to Cart) is respected in the cart — not explicitly covered by the ticket's AC, included as boundary coverage. |
| **Expected Result** | Cart quantity for that product matches the quantity selected on the detail page, and Total Price reflects it. |

---

## Test Steps

1. Open a product's detail page from `/products` — the product detail page loads with a quantity input.
2. Set quantity to a value greater than 1 (e.g. 3) — the quantity field reflects the entered value.
3. Click "Add to Cart" — the confirmation modal appears.
4. Navigate to `/view_cart` — the cart row shows Quantity = 3 and Total Price = Unit Price x 3.

---

# Test Case: TC-11 - Cart contents persist after a page refresh

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-11 |
| **Test Case Name** | Cart contents persist after a page refresh |
| **Precondition** | At least one item is in the cart. |
| **Description** | Verify that reloading `/view_cart` does not lose cart contents within the same session — not covered by the ticket's AC, included as a gap from analysis. |
| **Expected Result** | Cart contents and totals are unchanged after a page refresh. |

---

## Test Steps

1. Add a product to the cart and navigate to `/view_cart` — the cart shows the added item and its total.
2. Refresh the page — the page reloads.
3. Inspect the cart contents — the same item(s) and totals are still present, unchanged.

---

# Test Case: TC-12 - Add-to-cart control is operable via keyboard only

| Field | Value / Details |
| :--- | :--- |
| **Test Case ID** | TC-12 |
| **Test Case Name** | Add-to-cart control is operable via keyboard only |
| **Precondition** | `/products` is loaded. |
| **Description** | Basic accessibility check that a product can be added to the cart without a mouse — not covered by the ticket's AC, included as a non-functional gap. |
| **Expected Result** | The "Add to cart" control can be focused and activated using only the keyboard. |

---

## Test Steps

1. Navigate to `/products` using the keyboard (Tab) only — focus moves visibly between interactive elements.
2. Tab to a product's "Add to cart" control — the control receives visible focus.
3. Activate it with Enter/Space — the product is added and the confirmation modal appears, same as with a mouse click.
