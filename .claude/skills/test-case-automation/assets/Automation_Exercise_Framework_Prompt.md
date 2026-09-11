# Selenium Python Test Automation Framework Prompt

## System & Architecture Requirements
Act as a Senior Test Automation Architect. Create a modular Python test automation framework using **Selenium WebDriver** and **Pytest** with the **Page Object Model (POM)** pattern for the web application: `https://automationexercise.com/`.

---

## Folder & Project Structure

```text
automation_exercise_framework/
├── config/
│   └── config.py               # Base URL, browser timeout, implicit wait settings
├── pages/
│   ├── base_page.py            # Common Selenium actions (click, type, find, explicit waits)
│   ├── home_page.py            # Locators & methods for Home page
│   ├── login_page.py           # Locators & methods for Login/Signup page
│   └── cart_page.py            # Locators & methods for Shopping Cart page
├── tests/
│   ├── test_signup.py          # User Registration test cases
│   └── test_cart.py            # Add to cart / price calculation test cases
├── utils/
│   └── driver_factory.py       # WebDriver initialization (Chrome / Firefox headless option)
├── screenshots/                # Folder for captured failure screenshots
├── conftest.py                 # Pytest fixtures and screenshot hooks for pytest-html report
└── requirements.txt            # Dependency list (selenium, pytest, pytest-html, webdriver-manager)
```

---

## Technical Specifications

1. **Page Object Model (POM):**
   - `base_page.py` must encapsulate Selenium `WebDriverWait` explicit wait methods (e.g., `click_element`, `send_keys`, `get_text`, `is_displayed`).
   - Page classes must inherit from `BasePage` and use clean `By` locators (`By.XPATH`, `By.CSS_SELECTOR`).

2. **Fixtures & Hooks (`conftest.py`):**
   - Define a `driver` fixture with session/function-level scoping and clean setup/teardown (`driver.quit()`).
   - Implement the `pytest_runtest_makereport` hook to automatically capture a screenshot using `driver.get_screenshot_as_png()` or `save_screenshot()` whenever a test fails or errors out.
   - Attach the screenshot directly into the HTML report using `pytest-html` extra attachments (`pytest_html.extras.image` or HTML base64 embedding).

3. **Report Generation Setup:**
   - Standardize running tests via CLI: `pytest --html=reports/report.html --self-contained-html`.

4. **Sample Test Cases Implementation:**
   - **Test 1 (User Registration):** Verify navigation to Signup page, filling name + email, and verifying navigation to account creation page.
   - **Test 2 (Shopping Cart):** Navigate to `/products`, hover over first product, click "Add to cart", click "View Cart", and verify item is present in `/view_cart`.

---

Provide the complete code for every file in the framework with clear comments and exact pip requirements.
