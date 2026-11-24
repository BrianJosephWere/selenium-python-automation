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

    # --- Navigate to Countries ---
    print("Navigating to Countries...")

    # Click the parent menu item first
    global_config_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='GLOBAL CONFIGURATIONS']")))
    global_config_link.click()
    print("Expanded GLOBAL CONFIGURATIONS menu.")

    # *** FIX: Use visible text locator for Countries navigation ***
    countries_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(., 'Countries')]")))
    countries_link.click()

    # --- Add New Country ---
    print("Adding a new Country...")

    create_country_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Country')]")))
    create_country_button.click()

    country_name_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Country Name']")))
    unique_country_name = f"Test_{int(time.time())}"
    country_name_input.send_keys(unique_country_name)

    country_code_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Country Code']")))
    unique_code = str(random.randint(100, 999))
    country_code_input.send_keys(unique_code)

    submit_country_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
    submit_country_button.click()

    # --- Wait for Country Dialog to Close ---
    print("Waiting for country creation dialog to close...")
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//h2[contains(., 'Create New Country')]")))
    print("Country creation complete.")

    # --- Logout Step ---
    print("Logging out...")

    # Step 1: Click the User Menu (RELIABLE JS CLICK)
    user_menu = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='matero-username']")))

    print("Using JavaScript to click the User Menu...")
    driver.execute_script("arguments[0].click();", user_menu)

    # Step 2: Click the Logout Drop down
    logout_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'logout')]")))
    logout_button.click()
    print("Logout successful.")

    time.sleep(2)

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    print(f"{e}")
    driver.save_screenshot('error_screenshot.png')
    print("Saved screenshot to 'error_screenshot.png'")

finally:
    print("Test finished. Closing browser.")
    driver.quit()