import os

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
BROWSER = os.getenv("BROWSER", "chrome")  # chrome | firefox
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
IMPLICIT_WAIT = 0  # explicit waits only, see pages/base_page.py
EXPLICIT_WAIT_TIMEOUT = int(os.getenv("EXPLICIT_WAIT_TIMEOUT", "10"))

PRODUCTS_URL = f"{BASE_URL}/products"
VIEW_CART_URL = f"{BASE_URL}/view_cart"
PRODUCT_DETAILS_URL = f"{BASE_URL}/product_details/{{product_id}}"
