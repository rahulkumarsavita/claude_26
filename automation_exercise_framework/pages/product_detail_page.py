from selenium.webdriver.common.by import By

from config import config
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """https://automationexercise.com/product_details/<id>

    Locators verified 2026-08-19 against the live page HTML
    (curl fetch of /product_details/1).
    """

    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button.cart")

    def open(self, product_id):
        super().open(config.PRODUCT_DETAILS_URL.format(product_id=product_id))

    def set_quantity(self, quantity):
        """TC-10: quantity set here before 'Add to Cart' must be respected in the cart."""
        self.type_text(self.QUANTITY_INPUT, str(quantity))

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)
