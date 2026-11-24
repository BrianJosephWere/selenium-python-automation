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

    # --- Navigate to Project Types ---
    print("Navigating to Project Types...")

    # Step 1: Click the parent menu item (GLOBAL CONFIGURATIONS)
    global_config_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='GLOBAL CONFIGURATIONS']")))
    global_config_link.click()
    print("Expanded GLOBAL CONFIGURATIONS menu.")

    # Step 2: Click the Project Types link (Using the reliable text locator)
    project_types_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(., 'Project Types')]")))
    project_types_link.click()

    # --- Add New Project Type ---
    print("Adding a new Project Type...")

    # Step 1: Click the '+ Project Type' button
    create_project_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Project Type')]")))
    create_project_button.click()

    # Step 2: Wait for the input field to appear and send unique keys
    # Locator targets the input following the 'Project Type *' label.
    project_type_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-1']")))

    unique_project_name = f"Project_{int(time.time())}"
    project_type_input.send_keys(unique_project_name)

    # Step 3: Click the Submit button
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
    submit_button.click()

    # --- Wait for Form Submission/Load ---
    # We wait for the 'Project Types Management' title to reappear/load.
    print("Waiting for submission to complete and return to management page...")
    wait.until(EC.presence_of_element_located((By.XPATH, "//h2[normalize-space()='Project Types Management']")))
    print("Project Type creation complete.")

    time.sleep(10)

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
    driver.save_screenshot('error_screenshot_project_type.png')
    print("Saved screenshot to 'error_screenshot_project_type.png'")

finally:
    print("Test finished. Closing browser.")
    driver.quit()