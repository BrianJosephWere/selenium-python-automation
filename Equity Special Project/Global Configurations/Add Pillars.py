from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import random # Import random for a slightly more reliable Country Code

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

    # --- Navigate to Pillars ---
    print("Navigating to Pillars...")
    global_config_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='GLOBAL CONFIGURATIONS']")))
    global_config_link.click()

    # Navigate to Pillars
    pillars_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[@href='#/Configurations/Pillars']")))
    pillars_link.click()

    # --- Add New Pillar ---
    print("Adding a new pillar...")
    create_pillar_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Create New Pillar')]")))
    create_pillar_button.click()

    pillar_input = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Pillars']")))
    unique_pillar_name = f"Utopia_{int(time.time())}"
    pillar_input.send_keys(unique_pillar_name)

    submit_pillar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Submit')]")))
    submit_pillar_button.click()

    # Wait for Pillar Dialog to Close
    print("Waiting for pillar creation dialog to close...")
    wait.until(EC.invisibility_of_element_located((By.XPATH, "//h2[contains(., 'Create New Pillar')]")))
    print("Pillar creation complete.")

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