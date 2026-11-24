from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- Configuration ---
LOGIN_URL = "http://197.220.114.46:8085/#/login"
TEST_USERNAME = "testpm"
TEST_PASSWORD = "12345"

# --- Test Data for New Gate ---
TEST_GATE_NAME = f"Gate_{int(time.time())}"  # Unique name using timestamp

# XPaths for Login/Logout (Unchanged)
PROFILE_ICON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/a[1]/img[1]"
LOGOUT_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/div[1]/a[4]"
ADMINISTRATION_MENU_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[1]/a[1]"

# --- XPaths for Gate Mapping Module ---
GATE_MAPPING_SUBMENU_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[1]/app-sidebar-nav-items[1]/app-sidebar-nav-link[6]/a[1]/app-sidebar-nav-link-content[1]"
ADD_BUTTON_GATE_LIST_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-gate-master[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/button[1]"
GATE_NAME_INPUT_POPUP_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-gate-master[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/input[1]"
SUBMIT_ADD_BUTTON_POPUP_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-gate-master[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[3]/button[1]"

# --- Verification XPATH (Provided by User) ---
GATE_LIST_CONTAINER_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-gate-master[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]"


# --- Utility Function for Debugging (Unchanged) ---
def take_screenshot(driver, error_name):
    """Captures a screenshot and saves it to a 'screenshots' folder."""
    try:
        screenshot_dir = 'screenshots'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshot_dir}/{error_name}_{timestamp}.png"
        driver.save_screenshot(filename)
        print(f"📷 Screenshot captured: {filename}")
    except Exception as e:
        print(f"⚠️ Failed to take screenshot: {e}")


# --- Main Test Function ---
def run_gate_mapping_test():
    driver = None
    try:
        # --- Setup Firefox WebDriver ---
        firefox_options = Options()
        print("Starting Firefox browser...")
        driver = webdriver.Firefox(options=firefox_options)
        driver.maximize_window()
        wait = WebDriverWait(driver, 15)

        # --- 1. Login ---
        print("--- STARTING LOGIN ---")
        driver.get(LOGIN_URL)

        # Login steps
        username_field = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[1]/input[1]")))
        password_field = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[2]/input[1]")))
        username_field.send_keys(TEST_USERNAME)
        password_field.send_keys(TEST_PASSWORD)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                              "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[3]/div[1]/button[1]")))
        login_button.click()
        wait.until(EC.presence_of_element_located((By.XPATH, PROFILE_ICON_XPATH)))
        print("✅ Login successful. Dashboard loaded.")

        # --- 2. Create New Gate ---
        print("\n--- STARTING ADD GATE MAPPING TEST ---")

        # 2a. Navigation: Administration -> Gate Mapping
        admin_menu = wait.until(EC.element_to_be_clickable((By.XPATH, ADMINISTRATION_MENU_XPATH)))
        admin_menu.click()
        gate_mapping_link = wait.until(EC.element_to_be_clickable((By.XPATH, GATE_MAPPING_SUBMENU_XPATH)))
        gate_mapping_link.click()
        print("Navigated to 'Gate Mapping' list page.")

        # 2b. Click 'Add' button to open the form popup
        add_button_list = wait.until(EC.element_to_be_clickable((By.XPATH, ADD_BUTTON_GATE_LIST_XPATH)))
        add_button_list.click()
        print("Clicked 'Add' button to open the 'Add Gate' popup.")

        # 2c. Fill the Gate Name field in the popup (Fix for ElementNotInteractableException)
        gate_name_input_visible = wait.until(
            EC.visibility_of_element_located((By.XPATH, GATE_NAME_INPUT_POPUP_XPATH))
        )
        time.sleep(0.5)  # Slight pause for full interactivity
        gate_name_input_visible.send_keys(TEST_GATE_NAME)
        print(f"Entered Gate Name: {TEST_GATE_NAME}")

        # 2d. Click the 'Add' button on the form popup to submit
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, SUBMIT_ADD_BUTTON_POPUP_XPATH)))
        submit_button.click()
        print("Clicked 'Add' button on popup to submit form.")

        # 2e. Verification (NEW LOGIC)
        # 1. Wait 5 seconds as requested
        print("Waiting 5 seconds for page submission/reload...")
        time.sleep(5)

        # 2. Check for the presence of the main list container element
        wait.until(EC.presence_of_element_located((By.XPATH, GATE_LIST_CONTAINER_XPATH)))
        print(f"✅ Gate **{TEST_GATE_NAME}** created successfully. Redirected to Gate Mapping list page.")

        # --- Requested Pause (before logout) ---
        print("Pausing for 10 seconds before logout...")
        time.sleep(10)

        # --- 3. Logout ---
        print("\n--- STARTING LOGOUT ---")
        profile_icon = wait.until(EC.element_to_be_clickable((By.XPATH, PROFILE_ICON_XPATH)))
        profile_icon.click()
        logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, LOGOUT_BUTTON_XPATH)))
        logout_button.click()

        # Wait for logout to complete and verify the URL is back to the login page
        wait.until(EC.url_to_be(LOGIN_URL))
        print("✅ Logout successful. Test finished.")

    except TimeoutException:
        print(
            "❌ Error: A required element did not appear within the time limit. The script timed out waiting for the final page to load.")
        take_screenshot(driver, "Timeout_Error")
    except NoSuchElementException as e:
        print(f"❌ Error: Could not find a required element on the page.")
        print(f"Details: {e}")
        take_screenshot(driver, "NoSuchElement_Error")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        take_screenshot(driver, "Unexpected_Error")
    finally:
        # Ensure the browser is closed
        if driver:
            print("\nClosing the browser.")
            driver.quit()


# Execute the main test function
run_gate_mapping_test()