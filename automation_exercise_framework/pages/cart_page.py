import re

from selenium.webdriver.common.by import By

from config import config
from pages.base_page import BasePage


class CartPage(BasePage):
    """https://automationexercise.com/view_cart

    Locators verified 2026-08-19 by round-tripping the site's own session:
    GET /view_cart to obtain a session cookie, GET /add_to_cart/<id> against
    that cookie (the same AJAX call cart.js fires from the product listing),
    then re-fetching /view_cart to inspect the server-rendered row markup.
    Source: static/js/cart.js (confirms #cart_info_table, #empty_cart,
    .cart_quantity_delete) and the rendered <tr id="product-{id}"> rows.
    """

    CART_TABLE = (By.ID, "cart_info_table")
    CART_INFO = (By.ID, "cart_info")
    EMPTY_CART = (By.ID, "empty_cart")

    @staticmethod
    def _row_locator(product_id):
        return (By.ID, f"product-{product_id}")

    @staticmethod
    def _name_locator(product_id):
        return (By.CSS_SELECTOR, f"#product-{product_id} .cart_description h4 a")

    @staticmethod
    def _category_locator(product_id):
        return (By.CSS_SELECTOR, f"#product-{product_id} .cart_description p")

    @staticmethod
    def _thumbnail_locator(product_id):
        return (By.CSS_SELECTOR, f"#product-{product_id} .cart_product img")

    @staticmethod
    def _price_locator(product_id):
        return (By.CSS_SELECTOR, f"#product-{product_id} .cart_price p")

    @staticmethod
    def _quantity_locator(product_id):
        return (By.CSS_SELECTOR, f"#product-{product_id} .cart_quantity button")

    @staticmethod
    def _total_locator(product_id):
        return (By.CSS_SELECTOR, f"#product-{product_id} .cart_total_price")

    @staticmethod
    def _delete_locator(product_id):
        return (
            By.CSS_SELECTOR,
            f".cart_quantity_delete[data-product-id='{product_id}']",
        )

    def open(self):
        super().open(config.VIEW_CART_URL)

    def is_row_present(self, product_id):
        return len(self.driver.find_elements(*self._row_locator(product_id))) > 0

    def get_name(self, product_id):
        return self.get_text(self._name_locator(product_id))

    def get_category(self, product_id):
        return self.get_text(self._category_locator(product_id))

    def is_thumbnail_displayed(self, product_id):
        return self.is_displayed(self._thumbnail_locator(product_id))

    def get_price(self, product_id):
        return self._to_int(self.get_text(self._price_locator(product_id)))

    def get_quantity(self, product_id):
        return int(self.get_text(self._quantity_locator(product_id)))

    def get_row_total(self, product_id):
        return self._to_int(self.get_text(self._total_locator(product_id)))

    def get_cart_subtotal(self, product_ids):
        return sum(self.get_row_total(pid) for pid in product_ids)

    def delete_item(self, product_id):
        """TC-05/TC-09: remove a row via its AJAX delete control (no page reload)."""
        self.click(self._delete_locator(product_id))
        self.wait.until(lambda d: not self.is_row_present(product_id))

    def is_empty_state_shown(self):
        return self.is_displayed(self.EMPTY_CART)

    @staticmethod
    def _to_int(price_text):
        """'Rs. 500' -> 500"""
        digits = re.sub(r"[^\d]", "", price_text)
        return int(digits)
