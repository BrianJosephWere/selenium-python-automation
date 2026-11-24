from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random
import openpyxl
from openpyxl.utils import get_column_letter

# --- Configuration ---
LOGIN_URL = "http://197.220.114.46:8085/#/login"
TEST_USERNAME = "testpm"
TEST_PASSWORD = "12345"
XLSX_FILENAME = "staff_details_import.xlsx"

# --- XPaths ---
PROFILE_ICON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/a[1]/img[1]"
LOGOUT_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/div[1]/a[4]"
LOADING_OVERLAY_XPATH = "//div[contains(@class, 'pf-spinner-backdrop') and contains(@class, 'ng-star-inserted')]"

# --- XPaths for Navigation & Actions ---
PROPERTY_MANAGEMENT_MENU_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[2]/a[1]"
STAFF_DETAILS_MENU_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[2]/app-sidebar-nav-items[1]/app-sidebar-nav-link[2]/a[1]/app-sidebar-nav-link-content[1]"
IMPORT_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-employee-list[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[1]"
FILE_INPUT_FIELD_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-import-employee[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]/input[1]"
SUBMIT_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-import-employee[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[3]/button[1]"

# --- Verification XPATHs ---
# New XPath for success message on the import page (after submit)
SUCCESS_MESSAGE_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-import-employee[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]/strong[1]"
# XPath for Staff List Container (used to confirm return to list page before logout)
STAFF_LIST_CONTAINER_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-employee-list[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]"


# --- Test Data Generation Function (Unchanged) ---
def generate_staff_data(num_records=5):
    """Generates an XLSX file of staff records matching the required structure."""

    headers = ["Full Name", "Username", "Staff ID", "Document Type", "Identity No",
               "Dialing Code", "Primary No", "System Code", "Gender",
               "Staff Profile", "Employment", "Nationality", "Expected Time In",
               "Expected Time Out"]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "StaffData"
    ws.append(headers)

    for i in range(1, num_records + 1):
        timestamp = int(time.time() * 1000) % 100000
        row_data = [
            f"Staff Member {i}_{timestamp}",
            f"staffuser_{timestamp}_{i}",
            f"EMP{timestamp}{i}",
            "Passport",
            str(random.randint(10000000, 99999999)),
            "91",
            str(random.randint(1000000000, 9999999999)),
            random.choice(["5", "4"]),  # Using 5 and 4 as per your updated code
            random.choice(["Male", "Female"]),
            "Manager",
            "Full Time",
            "Indian",
            "09:00:00",
            "17:00:00"
        ]
        ws.append(row_data)

    file_path = os.path.abspath(XLSX_FILENAME)
    try:
        wb.save(file_path)
        print(f"✅ Generated import file: {file_path} with {num_records} staff records.")
        return file_path
    except Exception as e:
        print(f"❌ Failed to generate XLSX file: {e}")
        return None


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
def run_staff_import_test():
    driver = None
    csv_file_path = generate_staff_data(5)

    if not csv_file_path:
        print("Test aborted due to file generation failure.")
        return

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

        # --- 2. Navigate to Staff Import Page ---
        print("\n--- STARTING STAFF IMPORT TEST ---")

        # 2a. Navigation: Property Management -> Staff Details
        prop_management_menu = wait.until(EC.element_to_be_clickable((By.XPATH, PROPERTY_MANAGEMENT_MENU_XPATH)))
        prop_management_menu.click()
        staff_details_link = wait.until(EC.element_to_be_clickable((By.XPATH, STAFF_DETAILS_MENU_XPATH)))
        staff_details_link.click()
        print("Navigated to 'Staff Details' list page.")

        # Wait for the loading overlay to disappear
        print("Waiting for any loading spinners to vanish...")
        wait.until(EC.invisibility_of_element_located((By.XPATH, LOADING_OVERLAY_XPATH)))

        # 2b. Click 'Import' button
        import_button = wait.until(EC.element_to_be_clickable((By.XPATH, IMPORT_BUTTON_XPATH)))
        import_button.click()
        print("Clicked 'Import' button to go to upload page.")

        # 2c. Upload the XLSX file
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, FILE_INPUT_FIELD_XPATH)))
        file_input.send_keys(csv_file_path)
        print(f"Uploaded file: {XLSX_FILENAME}")

        # 2d. Click the 'Submit' button
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, SUBMIT_BUTTON_XPATH)))
        submit_button.click()
        print("Clicked 'Submit' button to initiate import.")

        # 2e. Verification (Wait for success message on the same page)
        print("Waiting for success message on the import page (5 seconds)...")
        # We use presence of element for verification
        wait.until(EC.presence_of_element_located((By.XPATH, SUCCESS_MESSAGE_XPATH)))
        print("✅ Staff Import successful. Success message found.")

        # 2f. Force Navigation Back to Staff List Page
        # Since the page doesn't redirect, we must navigate manually to proceed to logout.
        print("Manually navigating back to Staff List page.")
        # Re-click the Property Management dropdown
        prop_management_menu = wait.until(EC.element_to_be_clickable((By.XPATH, PROPERTY_MANAGEMENT_MENU_XPATH)))
        prop_management_menu.click()
        # Click the Staff Details submenu link
        staff_details_link = wait.until(EC.element_to_be_clickable((By.XPATH, STAFF_DETAILS_MENU_XPATH)))
        staff_details_link.click()

        # Wait for the list container to confirm successful navigation back
        wait.until(EC.presence_of_element_located((By.XPATH, STAFF_LIST_CONTAINER_XPATH)))
        print("Successfully returned to Staff List page.")

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
            "❌ Error: A required element did not appear within the time limit. The script timed out during login, menu navigation, verification, or logout.")
        take_screenshot(driver, "Timeout_Error")
    except NoSuchElementException as e:
        print(f"❌ Error: Could not find a required element on the page. Check XPaths.")
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
        # Clean up the generated file
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)
            print(f"Cleaned up temporary file: {XLSX_FILENAME}")


# Execute the main test function
run_staff_import_test()