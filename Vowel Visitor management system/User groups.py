from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# --- Configuration ---
LOGIN_URL = "http://197.220.114.46:8085/#/login"
TEST_USERNAME = "testpm"
TEST_PASSWORD = "12345"

# XPaths for Login/Logout
PROFILE_ICON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/a[1]/img[1]"
LOGOUT_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/div[1]/a[4]"

# XPaths for User Group Creation (Confirmed Working)
ADMINISTRATION_MENU_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[1]/a[1]"
USER_GROUP_DETAILS_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[1]/app-sidebar-nav-items[1]/app-sidebar-nav-link[1]/a[1]/app-sidebar-nav-link-content[1]"
ADD_BUTTON_ON_LIST_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-group-list[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[1]/i[1]"
ADD_GROUP_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-group[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[3]/button[1]/i[1]"
GROUP_TYPE_DROPDOWN_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-group[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[2]/div[1]/select[1]"
GROUP_NAME_INPUT_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-group[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[3]/div[1]/input[1]"
ACTIVE_CHECKBOX_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-group[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[4]/div[1]/div[1]/input[1]"

# --- NEW VERIFICATION XPATH ---
GROUP_LIST_CONTAINER_XPATH = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-group-list[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]"

# Test Data for New Group
NEW_GROUP_TYPE = "MOBILE"
NEW_GROUP_NAME = f"TestGroup_{int(time.time())}"


# --- Main Test Function ---
def run_vowel_test():
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

        # --- 2. Create User Group ---
        print("\n--- STARTING ADD USER GROUP TEST ---")

        # 2a. Navigation
        admin_menu = wait.until(EC.element_to_be_clickable((By.XPATH, ADMINISTRATION_MENU_XPATH)))
        admin_menu.click()
        user_group_link = wait.until(EC.element_to_be_clickable((By.XPATH, USER_GROUP_DETAILS_XPATH)))
        user_group_link.click()
        add_button_list = wait.until(EC.element_to_be_clickable((By.XPATH, ADD_BUTTON_ON_LIST_XPATH)))
        add_button_list.click()
        print("Navigated to 'Add Group' form.")

        # 2d. Interact with the 'Add Group' form
        print(f"Creating group: {NEW_GROUP_NAME} (Type: {NEW_GROUP_TYPE})...")

        # Select Group Type
        group_type_element = wait.until(EC.element_to_be_clickable((By.XPATH, GROUP_TYPE_DROPDOWN_XPATH)))
        group_type_select = Select(group_type_element)
        group_type_select.select_by_visible_text(NEW_GROUP_TYPE)
        print(f"Selected Group Type: {NEW_GROUP_TYPE}")

        # Enter Group Name
        group_name_input = wait.until(EC.presence_of_element_located((By.XPATH, GROUP_NAME_INPUT_XPATH)))
        group_name_input.send_keys(NEW_GROUP_NAME)
        print(f"Entered Group Name: {NEW_GROUP_NAME}")

        # Handle 'Active' Checkbox
        active_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, ACTIVE_CHECKBOX_XPATH)))
        if not active_checkbox.is_selected():
            active_checkbox.click()
            print("Checked 'Active' checkbox.")
        else:
            print("'Active' checkbox was already checked.")

        # 2e. Click Final 'Add' Button
        final_add_button = wait.until(EC.element_to_be_clickable((By.XPATH, ADD_GROUP_BUTTON_XPATH)))
        final_add_button.click()
        print("Clicked final 'Add' button to submit form.")

        # 2f. Verification (Wait for the list page container to appear)
        wait.until(EC.presence_of_element_located((By.XPATH, GROUP_LIST_CONTAINER_XPATH)))
        print("✅ User Group creation successful. Redirected to Group List page.")

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
        print(
            "❌ Error: A required element did not appear within the time limit. Check if form submission failed.")
    except NoSuchElementException as e:
        print(f"❌ Error: Could not find a required element on the page.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    finally:
        # Ensure the browser is closed
        if driver:
            print("\nClosing the browser.")
            driver.quit()


# Execute the main test function
run_vowel_test()