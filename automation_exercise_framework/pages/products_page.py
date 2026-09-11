from selenium.webdriver.common.by import By

from config import config
from pages.base_page import BasePage


class ProductsPage(BasePage):
    """https://automationexercise.com/products

    Locators verified 2026-08-19 against the live page HTML (curl fetch of
    /products). Each product card renders TWO `a.add-to-cart` elements with
    the same `data-product-id`: one inside `.productinfo` (default state)
    and one inside `.product-overlay .overlay-content` (shown on hover per
    TC-01's documented behavior). Scope the selector to the overlay to match
    the documented "hover, then click" flow.
    """

    CART_MODAL = (By.ID, "cartModal")
    CONTINUE_SHOPPING_BTN = (By.CSS_SELECTOR, "#cartModal .close-modal")
    VIEW_CART_LINK = (By.CSS_SELECTOR, "#cartModal a[href='/view_cart']")

    @staticmethod
    def _card_locator(product_id):
        return (
            By.XPATH,
            f"//div[contains(@class,'product-image-wrapper')]"
            f"[.//a[@data-product-id='{product_id}']]",
        )

    @staticmethod
    def _overlay_add_to_cart_locator(product_id):
        return (
            By.CSS_SELECTOR,
            f".product-overlay a.add-to-cart[data-product-id='{product_id}']",
        )

    @staticmethod
    def _productinfo_name_price_locator(product_id):
        return (
            By.XPATH,
            f"//div[contains(@class,'product-image-wrapper')]"
            f"[.//a[@data-product-id='{product_id}']]//div[contains(@class,'productinfo')]",
        )

    def open(self):
        super().open(config.PRODUCTS_URL)

    def add_product_to_cart(self, product_id):
        """TC-01: hover the product card, then click its overlay 'Add to cart'."""
        card = self.find(self._card_locator(product_id))
        self.hover(card)
        self.click(self._overlay_add_to_cart_locator(product_id))

    def get_product_name_and_price(self, product_id):
        """Returns (name, price_text) as rendered on the listing, for TC-02/03/04 cross-checks."""
        scope = self.find(self._productinfo_name_price_locator(product_id))
        name = scope.find_element(By.TAG_NAME, "p").text.strip()
        price = scope.find_element(By.TAG_NAME, "h2").text.strip()
        return name, price

    def is_add_to_cart_keyboard_focusable(self, product_id):
        """TC-12: an element only receives Tab focus if it's natively focusable
        (a[href], button, input, select, textarea) or has tabindex >= 0.

        NOTE (verified 2026-08-19): the live `<a data-product-id=".." class="add-to-cart">`
        markup has NO `href` attribute and no `tabindex`, so per the HTML spec it is
        excluded from the default tab order. This check is expected to return False
        against the current live site -- see Missing/Unknown & Findings in the
        automation result doc. Written to assert the documented expected behavior,
        not the currently-observed one.
        """
        element = self.find(self._overlay_add_to_cart_locator(product_id))
        return self.driver.execute_script(
            """
            const el = arguments[0];
            const tag = el.tagName.toLowerCase();
            const tabindex = el.getAttribute('tabindex');
            if (tabindex !== null && parseInt(tabindex, 10) >= 0) return true;
            if (tag === 'a') return el.hasAttribute('href');
            return ['button', 'input', 'select', 'textarea'].includes(tag);
            """,
            element,
        )

    def is_cart_modal_visible(self):
        return self.is_displayed(self.CART_MODAL)

    def click_continue_shopping(self):
        """TC-06: dismiss the confirmation modal without leaving /products."""
        self.click(self.CONTINUE_SHOPPING_BTN)
        self.wait_until_invisible(self.CART_MODAL)

    def click_view_cart_from_modal(self):
        """TC-07: navigate to /view_cart via the confirmation modal's link."""
        self.click(self.VIEW_CART_LINK)
