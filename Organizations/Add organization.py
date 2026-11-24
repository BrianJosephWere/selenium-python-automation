from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import random

# --- Setup ---
options = Options()
options.accept_insecure_certs = True
driver = webdriver.Firefox(options=options)

# Initialize WebDriver & Waiter
driver.set_page_load_timeout(60)
wait = WebDriverWait(driver, 15)  # Wait up to 15 seconds

print("Opening login page...")
driver.get('https://69.62.113.171:8086/#/auth/login')
driver.maximize_window()

try:
    # --- Login Step ---
    print("Logging in...")
    username_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Username']")))
    username_field.send_keys('Superadmin')

    password_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Password']")))
    password_field.send_keys('Admin!23')

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(span, 'Login')]")))
    login_button.click()
    print("Login successful.")

    # --- Navigate to Organization ---
    print("Navigating to Organization...")

    # Per your note, this is a top-level menu item
    # We use the href from the screenshot URL for a very stable locator
    organization_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@href='#/organization']")))
    organization_link.click()

    # --- Add New Organization ---
    print("Adding a new Organization...")

    # Step 1: Click the '+ Organization' button
    create_org_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Organization')]")))
    create_org_button.click()
    print("Clicked '+ Organization' button.")

    # Step 2: Fill the form fields

    # Organization Name
    org_name_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-1']")))
    unique_org_name = f"Org_{int(time.time())}"
    org_name_input.send_keys(unique_org_name)

    # Country Code
    org_code_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-2']")))
    unique_code = str(random.randint(100, 999))
    org_code_input.send_keys(unique_code)

    # City
    city_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-3']")))
    city_input.send_keys("Test City")  # Using a hardcoded value

    # Step 3: Handle the Country Dropdown
    # --- THIS PART REQUIRES YOUR INPUT ---
    # Click the dropdown to open the options panel.
    # The 'formcontrolname' is a guess; you may need to update it.
    print("Opening Country dropdown...")
    country_dropdown = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".mat-select-placeholder.mat-select-min-line.ng-tns-c142-33.ng-star-inserted")))  # <-- Verify this locator
    country_dropdown.click()

    # Wait for an option to appear and click it.
    # 'Kenya' is an example; replace it with a real value from your list.
    print("Selecting a Country...")
    option_to_select = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='Rwanda']")))  # <-- Update this value
    option_to_select.click()

    # Step 4: Click the 'Add' button (not 'Submit')
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add')]")))
    submit_button.click()

    # --- Wait for Form Submission/Load ---
    # We wait for the 'Organizations Management' title to reappear.
    print("Waiting for submission to complete and return to management page...")
    wait.until(EC.presence_of_element_located((By.XPATH, "//h2[normalize-space()='Organizations Management']")))
    print("Organization creation complete.")

    # --- Logout Step ---
    print("Logging out...")

    user_menu = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='matero-username']")))

    print("Using JavaScript to click the User Menu...")
    driver.execute_script("arguments[0].click();", user_menu)

    logout_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'logout')]")))
    logout_button.click()
    print("Logout successful.")

    time.sleep(2)

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    print(f"{e}")
    driver.save_screenshot('error_screenshot_organization.png')
    print("Saved screenshot to 'error_screenshot_organization.png'")

finally:
    print("Test finished. Closing browser.")
    driver.quit()