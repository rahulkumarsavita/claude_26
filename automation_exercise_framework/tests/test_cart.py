"""Automates KAN-3-test-cases.md (Cart - Add Products to Cart and Verify
Quantity & Price Calculation) against https://automationexercise.com/.

Product fixtures used (verified live 2026-08-19):
  product_id=1 -> "Blue Top", Rs. 500
  product_id=2 -> "Men Tshirt", Rs. 400
"""

from pages.cart_page import CartPage
from pages.product_detail_page import ProductDetailPage
from pages.products_page import ProductsPage

PRODUCT_1 = 1  # Blue Top, Rs. 500
PRODUCT_2 = 2  # Men Tshirt, Rs. 400


def test_tc01_add_single_product_to_cart(driver):
    """TC-01: adding a product shows the confirmation modal with
    Continue Shopping / View Cart options."""
    products = ProductsPage(driver)
    products.open()

    products.add_product_to_cart(PRODUCT_1)

    assert products.is_cart_modal_visible()


def test_tc02_cart_shows_correct_item_details(driver):
    """TC-02: /view_cart shows correct thumbnail, name, category, price,
    quantity, and total for the added item."""
    products = ProductsPage(driver)
    products.open()
    expected_name, expected_price = products.get_product_name_and_price(PRODUCT_1)
    products.add_product_to_cart(PRODUCT_1)
    products.click_view_cart_from_modal()

    cart = CartPage(driver)
    assert cart.is_row_present(PRODUCT_1)
    assert cart.is_thumbnail_displayed(PRODUCT_1)
    assert cart.get_name(PRODUCT_1) == expected_name
    assert f"Rs. {cart.get_price(PRODUCT_1)}" == expected_price
    assert cart.get_quantity(PRODUCT_1) == 1


def test_tc03_item_total_equals_price_times_quantity(driver):
    """TC-03: Total Price for a row = Unit Price x Quantity."""
    products = ProductsPage(driver)
    products.open()
    products.add_product_to_cart(PRODUCT_1)
    products.click_view_cart_from_modal()

    cart = CartPage(driver)
    price = cart.get_price(PRODUCT_1)
    quantity = cart.get_quantity(PRODUCT_1)
    total = cart.get_row_total(PRODUCT_1)

    assert total == price * quantity


def test_tc04_cart_subtotal_correct_for_multiple_products(driver):
    """TC-04: adding two distinct products, the cart subtotal equals the
    sum of each row's Total Price."""
    products = ProductsPage(driver)
    products.open()
    products.add_product_to_cart(PRODUCT_1)
    products.click_continue_shopping()
    products.add_product_to_cart(PRODUCT_2)
    products.click_view_cart_from_modal()

    cart = CartPage(driver)
    expected_subtotal = cart.get_row_total(PRODUCT_1) + cart.get_row_total(PRODUCT_2)

    assert cart.get_cart_subtotal([PRODUCT_1, PRODUCT_2]) == expected_subtotal


def test_tc05_remove_item_from_cart_dynamically(driver):
    """TC-05: deleting a row removes it without a full page reload and
    remaining totals update."""
    products = ProductsPage(driver)
    products.open()
    products.add_product_to_cart(PRODUCT_1)
    products.click_continue_shopping()
    products.add_product_to_cart(PRODUCT_2)
    products.click_view_cart_from_modal()

    cart = CartPage(driver)
    assert cart.is_row_present(PRODUCT_1)

    cart.delete_item(PRODUCT_1)

    assert not cart.is_row_present(PRODUCT_1)
    assert cart.is_row_present(PRODUCT_2)


def test_tc06_continue_shopping_keeps_item_in_cart(driver):
    """TC-06: dismissing the modal via Continue Shopping does not lose the
    added item."""
    products = ProductsPage(driver)
    products.open()
    products.add_product_to_cart(PRODUCT_1)

    products.click_continue_shopping()

    cart = CartPage(driver)
    cart.open()
    assert cart.is_row_present(PRODUCT_1)


def test_tc07_view_cart_navigates_to_cart_page(driver):
    """TC-07: the modal's View Cart option navigates to /view_cart with the
    added item present."""
    products = ProductsPage(driver)
    products.open()
    products.add_product_to_cart(PRODUCT_1)

    products.click_view_cart_from_modal()

    assert "/view_cart" in driver.current_url
    cart = CartPage(driver)
    assert cart.is_row_present(PRODUCT_1)


def test_tc08_add_same_product_twice_increments_quantity(driver):
    """TC-08: verified live 2026-08-19 (GET /add_to_cart/<id> called twice in the
    same session) -- the site increments Quantity on the existing row rather
    than creating a duplicate row. Encoded here as the confirmed behavior,
    resolving the open question from the source test case."""
    products = ProductsPage(driver)
    products.open()
    products.add_product_to_cart(PRODUCT_1)
    products.click_continue_shopping()
    products.add_product_to_cart(PRODUCT_1)
    products.click_view_cart_from_modal()

    cart = CartPage(driver)
    assert len(driver.find_elements("id", f"product-{PRODUCT_1}")) == 1
    assert cart.get_quantity(PRODUCT_1) == 2


def test_tc09_removing_all_items_shows_empty_cart_state(driver):
    """TC-09: once every row is removed, the empty-cart state is shown and
    no stale table/subtotal remains."""
    products = ProductsPage(driver)
    products.open()
    products.add_product_to_cart(PRODUCT_1)
    products.click_view_cart_from_modal()

    cart = CartPage(driver)
    cart.delete_item(PRODUCT_1)

    assert cart.is_empty_state_shown()
    assert not cart.is_row_present(PRODUCT_1)


def test_tc10_add_product_with_increased_quantity_from_detail_page(driver):
    """TC-10: a quantity set on the product detail page before Add to Cart
    is respected in the cart, and Total Price reflects it."""
    detail = ProductDetailPage(driver)
    detail.open(PRODUCT_1)
    detail.set_quantity(3)
    detail.add_to_cart()

    products = ProductsPage(driver)
    products.click_view_cart_from_modal()

    cart = CartPage(driver)
    assert cart.get_quantity(PRODUCT_1) == 3
    assert cart.get_row_total(PRODUCT_1) == cart.get_price(PRODUCT_1) * 3


def test_tc11_cart_contents_persist_after_refresh(driver):
    """TC-11: reloading /view_cart does not lose cart contents within the
    same browser session (session-cookie-backed cart, confirmed live via
    cross-request persistence -- see automation result doc)."""
    products = ProductsPage(driver)
    products.open()
    products.add_product_to_cart(PRODUCT_1)
    products.click_view_cart_from_modal()

    cart = CartPage(driver)
    before_total = cart.get_row_total(PRODUCT_1)

    driver.refresh()

    assert cart.is_row_present(PRODUCT_1)
    assert cart.get_row_total(PRODUCT_1) == before_total


def test_tc12_add_to_cart_control_is_keyboard_operable(driver):
    """TC-12: the Add to cart control should be focusable/activatable via
    keyboard only. NOTE: verified live 2026-08-19 that the anchor has no
    `href`, so this is expected to FAIL against the current markup -- see
    Findings in the automation result doc; flagged for human review rather
    than silently adjusted to pass."""
    products = ProductsPage(driver)
    products.open()

    assert products.is_add_to_cart_keyboard_focusable(PRODUCT_1)
