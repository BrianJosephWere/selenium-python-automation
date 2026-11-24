from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import time
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- Setup ---
options = Options()
options.accept_insecure_certs = True
driver = webdriver.Firefox(options=options)

# Initialize WebDriver & Waiter
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver, 20)
spinner_backdrop_xpath = "//div[contains(@class, 'pf-spinner-backdrop')]"  # Define the spinner XPath once

# Test Data
VISITOR_NAME = f"Test Visitor {random.randint(1000, 9999)}"
IDENTITY_NO = str(random.randint(10000000, 99999999))
PRIMARY_NUMBER = f"25471{random.randint(1000000, 9999999)}"
EMAIL_ADDRESS = f"visitor.{random.randint(1, 999)}@test.com"

print("Opening login page...")
# NOTE: Using the IP from the screenshots for this specific module
driver.get('http://197.220.114.46:8085/#/login')
driver.maximize_window()


# --------------------------------------------------------------------------------------------------
# --- Utility Functions ---
# --------------------------------------------------------------------------------------------------

def select_html_select_option(waiter, dropdown_xpath, option_value_or_text, by_type='text'):
    """
    Selects an option from a standard HTML <select> element using Select class.
    by_type should be the string 'text' (default) or 'value'.
    """

    # 1. Wait for the select element to be clickable
    select_element = waiter.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))

    # 2. Initialize the Select object
    select = Select(select_element)

    # 3. Select the option based on the string constant provided
    if by_type == 'text':
        select.select_by_visible_text(option_value_or_text)
        print(f"   -> Selected '{option_value_or_text}' by visible text.")
    elif by_type == 'value':
        select.select_by_value(option_value_or_text)
        print(f"   -> Selected '{option_value_or_text}' by value.")
    else:
        raise ValueError("Invalid 'by_type' provided. Must be 'text' or 'value'.")


def select_html_select_option_by_index(waiter, dropdown_xpath, index):
    """
    Selects an option from a standard HTML <select> element using its index.
    Index 1 usually corresponds to the first actual selectable option after the default.
    """
    try:
        # 1. Wait for the select element to be clickable
        select_element = waiter.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
        # 2. Initialize the Select object
        select = Select(select_element)
        # 3. Select the option by index
        select.select_by_index(index)
        print(f"   -> Selected option at index {index} (the first available option).")
    except Exception as e:
        # Raise a more specific error for easier debugging
        raise NoSuchElementException(f"Could not select option by index {index}. Error: {e}")


try:
    # --- Login Step (New Credentials) ---
    print("Logging in with 'testsec' credentials...")
    username_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Username']")))
    username_field.send_keys('testsec')

    password_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Password']")))
    password_field.send_keys('12345')

    # Using the XPath provided by the user for the login button
    login_button_xpath = "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[3]/div[1]/button[1]"
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
    login_button.click()
    print("Login successful.")

    # --- Navigation to Add Visitor ---
    print("\nNavigating to Add Visitor page...")

    # 1. Click the Visitor Menu (Expanded Menu)
    visitor_menu_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[2]/a[1]"
    visitor_menu_link = wait.until(EC.element_to_be_clickable((By.XPATH, visitor_menu_xpath)))
    visitor_menu_link.click()
    print("Expanded Visitor Menu.")
    time.sleep(1)  # Small wait for sub-menu to expand

    # 2. Click Add Visitor Sub-menu
    add_visitor_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[2]/app-sidebar-nav-items[1]/app-sidebar-nav-link[1]/a[1]/app-sidebar-nav-link-content[1]"
    add_visitor_link = wait.until(EC.element_to_be_clickable((By.XPATH, add_visitor_xpath)))
    add_visitor_link.click()
    print("Navigated to Add Random Visitor form.")

    # Wait for the form title to ensure the page has loaded
    wait.until(
        EC.presence_of_element_located((By.XPATH,
                                        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]/strong[1]")))

    # CRITICAL FIX 1: Wait for the pf-spinner-backdrop (loading screen) to disappear after page load
    print("   -> Waiting for the initial loading spinner to disappear...")
    try:
        wait.until(EC.invisibility_of_element_located((By.XPATH, spinner_backdrop_xpath)))
        print("   -> Initial loading spinner dismissed.")
    except TimeoutException:
        print("   -> WARNING: Initial spinner invisibility check timed out. Proceeding.")

    # --- Form Filling ---
    print("Filling visitor details...")

    # 1. Document Type (Select Dropdown)
    document_type_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]/select[1]"
    select_html_select_option(wait, document_type_xpath, 'National ID')

    # 2. Identity No (Input Field)
    identity_no_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[2]/div[1]/input[1]"
    wait.until(EC.presence_of_element_located((By.XPATH, identity_no_xpath))).send_keys(IDENTITY_NO)
    print(f"   -> Identity No: {IDENTITY_NO}")

    # 3. Group Type (Radio Button) - Select 'Individual'
    wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Individual')]"))).click()
    print("   -> Selected Group Type: Individual")

    # NEW FIX 2: Wait for overlay after Group Type selection
    print("   -> Waiting for overlay after Group Type selection...")
    try:
        wait.until(EC.invisibility_of_element_located((By.XPATH, spinner_backdrop_xpath)))
        print("   -> Overlay dismissed.")
    except TimeoutException:
        print("   -> WARNING: Overlay after Group Type timed out. Proceeding.")

    # 4. Whom to Meet (Radio Button) - Select 'Department'
    wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Department')]"))).click()
    print("   -> Selected Whom to Meet: Department")

    # NEW FIX 3: Wait for overlay after Whom to Meet selection
    print("   -> Waiting for overlay after Whom to Meet selection...")
    try:
        wait.until(EC.invisibility_of_element_located((By.XPATH, spinner_backdrop_xpath)))
        print("   -> Overlay dismissed.")
    except TimeoutException:
        print("   -> WARNING: Overlay after Whom to Meet timed out. Proceeding.")

    # 5. Department (Select Dropdown - Appears after Whom to Meet: Department)
    department_dropdown_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[5]/div[1]/select[1]"
    # FIX FOR NoSuchElementException: Select the first dynamic option (index 1)
    select_html_select_option_by_index(wait, department_dropdown_xpath, 1)

    # 6. Name (Input Field)
    name_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[6]/div[1]/input[1]"
    wait.until(EC.presence_of_element_located((By.XPATH, name_xpath))).send_keys(VISITOR_NAME)
    print(f"   -> Visitor Name: {VISITOR_NAME}")

    # 7. Mode of Entry (Select Dropdown) - Always select 'Walk-In'
    mode_of_entry_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[7]/div[1]/select[1]"
    select_html_select_option(wait, mode_of_entry_xpath, 'Walk-In')

    # 8. Primary Number (Input Field)
    primary_number_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[8]/div[1]/div[1]/input[1]"
    wait.until(EC.presence_of_element_located((By.XPATH, primary_number_xpath))).send_keys(PRIMARY_NUMBER)
    print(f"   -> Primary Number: {PRIMARY_NUMBER}")

    # 9. Email (Input Field)
    email_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[9]/div[1]/input[1]"
    wait.until(EC.presence_of_element_located((By.XPATH, email_xpath))).send_keys(EMAIL_ADDRESS)
    print(f"   -> Email: {EMAIL_ADDRESS}")

    # 10. Nationality (Select Dropdown)
    nationality_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[10]/div[1]/select[1]"
    select_html_select_option(wait, nationality_xpath, 'Kenya (Kenyan)')

    # 11. Purpose of Visit (Input Field)
    purpose_of_visit_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[13]/div[1]/input[1]"
    wait.until(EC.presence_of_element_located((By.XPATH, purpose_of_visit_xpath))).send_keys("Automated Testing Visit")

    # 12. Submit Button
    print("Attempting to click Submit button...")
    submit_button_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-random-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[3]/button[1]"
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))

    submit_button.click()
    print("Clicked Submit.")

    # --- Wait for Submission/Load ---
    print("Waiting for submission to complete and redirect...")
    time.sleep(5)
    print("Visitor creation process complete (5s wait for redirect/confirmation).")

    # --- Logout Step ---
    print("\nLogging out...")

    time.sleep(4)

    # Clicking the user menu (using generic text 'testsec')
    user_menu_xpath = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/a[1]/img[1]"
    user_menu = wait.until(EC.element_to_be_clickable((By.XPATH, user_menu_xpath)))

    driver.execute_script("arguments[0].click();", user_menu)  # Use JS click for menu dropdown

    logout_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/div[1]/a[4]")))
    logout_button.click()
    print("Logout successful.")

    time.sleep(2)

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    print(f"Message: {e}")
    driver.save_screenshot('error_screenshot_visitor_onboarding.png')
    print("Saved screenshot to 'error_screenshot_visitor_onboarding.png'")

finally:
    print("Test finished. Closing browser.")
    driver.quit()