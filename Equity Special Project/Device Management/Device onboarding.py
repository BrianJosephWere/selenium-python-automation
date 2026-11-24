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
    username_field.send_keys('Brian1')  # Assuming 'Superadmin' for this test

    password_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Password']")))
    password_field.send_keys('Admin!23')  # Assuming 'Admin!23'

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(span, 'Login')]")))
    login_button.click()
    print("Login successful.")

    # --- Navigate to Device Onboarding ---
    print("Navigating to Device Onboarding...")

    # Step 1: Click the parent menu item (DEVICE MANAGEMENT)
    device_mgmt_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='DEVICE MANAGEMENT']")))
    device_mgmt_link.click()
    print("Expanded DEVICE MANAGEMENT menu.")

    # Step 2: Click the Device Onboarding link
    onboarding_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(., 'Device Onboarding')]")))
    onboarding_link.click()

    # --- Add New Device ---
    print("Adding a new Device...")

    # Step 1: Click the '+ Device' button
    create_device_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., ' Device')]")))
    create_device_button.click()

    # Step 2: Fill the form

    # Device Mac Address
    mac_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-0']")))
    # Generate a random, valid MAC address string
    unique_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255),
                                              random.randint(0, 255),
                                              random.randint(0, 255))
    mac_input.send_keys(unique_mac)

    # Device Name
    name_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-1']")))
    unique_name = f"Device_{int(time.time())}"
    name_input.send_keys(unique_name)

    # Activate/Deactivate Checkbox
    # We find the label and click it, which is safer for toggling the checkbox
    activate_checkbox_label = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//label[contains(., 'Activate/Deactivate')]")))
    activate_checkbox_label.click()

    # Step 3: Click the 'Save & Submit' button
    submit_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Save & Submit')]")))
    submit_button.click()

    # --- Wait for Form Submission/Load ---
    # We wait for the 'Devices' management title to reappear.
    print("Waiting for submission to complete and return to management page...")
    wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., ' Device')]")))
    print("Device creation complete.")

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
        (By.XPATH, "//span[normalize-space()='logout']")))
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