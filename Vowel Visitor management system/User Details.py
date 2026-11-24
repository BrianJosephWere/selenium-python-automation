from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random
import os  # For managing screenshot file paths

# --- Configuration ---
LOGIN_URL = "http://197.220.114.46:8085/#/login"
TEST_USERNAME = "testpm"
TEST_PASSWORD = "12345"

# --- Test Data for New User ---
# Generate unique name and username
TEST_USER_NAME = f"Test User {random.randint(100, 999)}"
TEST_USER_USERNAME = f"user_{int(time.time())}"
TEST_USER_PASSWORD = "password123"
TEST_ROLE = "Web User"
TEST_GROUP = "Webusers"
TEST_DIALING_CODE = "93 (Afghanistan)"
TEST_MOBILE_NUMBER = str(random.randint(100000000, 999999999))
TEST_GENDER = "Male"
TEST_COUNTRY = "Albania"
TEST_COUNTY = "Test County"  # NEW
TEST_CITY = "Test City"  # NEW

# XPaths for Login/Logout
PROFILE_ICON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/a[1]/img[1]"
LOGOUT_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/div[1]/a[4]"

# --- XPaths for User Details Navigation (Confirmed) ---
ADMINISTRATION_MENU_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[1]/a[1]"
USER_DETAILS_SUBMENU_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[1]/app-sidebar-nav-items[1]/app-sidebar-nav-link[2]/a[1]/app-sidebar-nav-link-content[1]"
ADD_BUTTON_ON_LIST_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-user-list[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[1]"

# --- XPaths for Add User Form (Updated) ---
NAME_INPUT_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[2]/div[1]/input[1]"
USERNAME_INPUT_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[3]/div[1]/input[1]"
PASSWORD_INPUT_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[4]/div[1]/input[1]"
ROLE_DROPDOWN_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[5]/div[1]/select[1]"
GROUP_DROPDOWN_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[6]/div[1]/select[1]"
DIALING_CODE_DROPDOWN_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[7]/div[1]/div[1]/div[1]/select[1]"
MOBILE_NUMBER_INPUT_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[7]/div[1]/div[1]/input[1]"
GENDER_RADIO_MALE_XPATH = "//input[@type='radio' and @value='Male']"
COUNTRY_DROPDOWN_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[11]/div[1]/select[1]"
COUNTY_INPUT_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[12]/div[1]/input[1]"  # NEW
CITY_INPUT_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[13]/div[1]/input[1]"  # VERIFIED
ACTIVE_CHECKBOX_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[15]/div[1]/div[1]/input[1]"
SUBMIT_ADD_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-user[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[3]/button[1]"

# --- Verification XPATH (Confirmed) ---
USER_LIST_CONTAINER_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-user-list[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]"


def take_screenshot(driver, error_name):
    """Captures a screenshot and saves it to a 'screenshots' folder."""
    try:
        # Create a directory for screenshots if it doesn't exist
        screenshot_dir = 'screenshots'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        # Format the filename with timestamp and error name
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshot_dir}/{error_name}_{timestamp}.png"

        driver.save_screenshot(filename)
        print(f"📷 Screenshot captured: {filename}")

    except Exception as e:
        print(f"⚠️ Failed to take screenshot: {e}")


# --- Main Test Function ---
def run_user_details_test():
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

        # Locate and enter Username and Password
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

        # --- 2. Create New User ---
        print("\n--- STARTING ADD USER TEST ---")

        # 2a. Navigation: Administration -> User Details
        admin_menu = wait.until(EC.element_to_be_clickable((By.XPATH, ADMINISTRATION_MENU_XPATH)))
        admin_menu.click()
        user_details_link = wait.until(EC.element_to_be_clickable((By.XPATH, USER_DETAILS_SUBMENU_XPATH)))
        user_details_link.click()
        add_button_list = wait.until(EC.element_to_be_clickable((By.XPATH, ADD_BUTTON_ON_LIST_XPATH)))
        add_button_list.click()
        print("Navigated to 'Add User' form.")

        # 2b. Fill Form Fields

        # Name
        wait.until(EC.presence_of_element_located((By.XPATH, NAME_INPUT_XPATH))).send_keys(TEST_USER_NAME)
        # Username
        wait.until(EC.presence_of_element_located((By.XPATH, USERNAME_INPUT_XPATH))).send_keys(TEST_USER_USERNAME)
        # Password
        wait.until(EC.presence_of_element_located((By.XPATH, PASSWORD_INPUT_XPATH))).send_keys(TEST_USER_PASSWORD)
        print(f"Filled Name, Username, and Password.")

        # Role Dropdown
        role_select = Select(wait.until(EC.element_to_be_clickable((By.XPATH, ROLE_DROPDOWN_XPATH))))
        role_select.select_by_visible_text(TEST_ROLE)
        print(f"Selected Role: {TEST_ROLE}")

        # Group Dropdown
        group_select = Select(wait.until(EC.element_to_be_clickable((By.XPATH, GROUP_DROPDOWN_XPATH))))
        group_select.select_by_visible_text(TEST_GROUP)
        print(f"Selected Group: {TEST_GROUP}")

        # Primary Number: Dialing Code
        dialing_code_select = Select(wait.until(EC.element_to_be_clickable((By.XPATH, DIALING_CODE_DROPDOWN_XPATH))))
        dialing_code_select.select_by_visible_text(TEST_DIALING_CODE)

        # Primary Number: Mobile Number
        wait.until(EC.presence_of_element_located((By.XPATH, MOBILE_NUMBER_INPUT_XPATH))).send_keys(TEST_MOBILE_NUMBER)
        print(f"Entered Primary Number: {TEST_DIALING_CODE} {TEST_MOBILE_NUMBER}")

        # Gender (Male)
        wait.until(EC.element_to_be_clickable((By.XPATH, GENDER_RADIO_MALE_XPATH))).click()
        print(f"Selected Gender: {TEST_GENDER}")

        # Country Dropdown
        country_select = Select(wait.until(EC.element_to_be_clickable((By.XPATH, COUNTRY_DROPDOWN_XPATH))))
        country_select.select_by_visible_text(TEST_COUNTRY)
        print(f"Selected Country: {TEST_COUNTRY}")

        # County Input (NEW LOGIC)
        wait.until(EC.presence_of_element_located((By.XPATH, COUNTY_INPUT_XPATH))).send_keys(TEST_COUNTY)
        print(f"Filled County: {TEST_COUNTY}")

        # City Input (NEW LOGIC)
        wait.until(EC.presence_of_element_located((By.XPATH, CITY_INPUT_XPATH))).send_keys(TEST_CITY)
        print(f"Filled City: {TEST_CITY}")

        # Skip Upload Image. Check Active Checkbox.
        active_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, ACTIVE_CHECKBOX_XPATH)))
        if not active_checkbox.is_selected():
            active_checkbox.click()
            print("Checked 'Active' checkbox.")
        else:
            print("'Active' checkbox was already checked.")

        # 2c. Click Submit Button
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, SUBMIT_ADD_BUTTON_XPATH)))
        submit_button.click()
        print("Clicked final 'Add' button to submit form.")

        # 2d. Verification (Wait for the list page container to appear)
        wait.until(EC.presence_of_element_located((By.XPATH, USER_LIST_CONTAINER_XPATH)))
        print("✅ User creation successful. Redirected to User List page.")

        # --- Requested Pause ---
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
        print("❌ Error: A required element did not appear within the time limit.")
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
run_user_details_test()