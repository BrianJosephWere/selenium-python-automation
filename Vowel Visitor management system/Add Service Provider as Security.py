from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

# --- Setup ---
options = Options()
options.accept_insecure_certs = True
driver = webdriver.Firefox(options=options)

# Initialize WebDriver & Waiter
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver, 20)
# Define common XPaths for overlays
spinner_backdrop_xpath = "//div[contains(@class, 'pf-spinner-backdrop')]"
autocomplete_overlay_xpath = "//div[contains(@class, 'autocomplete-overlay') and contains(@class, 'ng-star-inserted')]"

# Test Data for Service Provider
SP_NAME = f"Test SP {random.randint(1000, 9999)}"
SP_IDENTITY_NO = str(random.randint(20000000, 29999999))
SP_PRIMARY_NUMBER = str(random.randint(700000000, 799999999))
SP_EMAIL_ADDRESS = f"sp.{random.randint(1, 999)}@service.com"
SP_ADDRESS = f"123 Test Street, Nairobi"
SP_COMPANY_NAME = f"Test Company {random.randint(1, 10)}"
SP_COMPANY_ADDRESS = f"456 Tech Park, Test City"
SP_WORK_PROFILE = f"Technician {random.randint(1, 100)}"

# --- Define XPaths for fields (for re-entry fix) ---
name_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[2]/div[1]/input[1]"
document_type_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[3]/div[1]/select[1]"
identity_no_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[4]/div[1]/input[1]"
primary_number_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[5]/div[1]/div[1]/input[1]"
nationality_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[6]/div[1]/select[1]"
work_profile_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[13]/div[1]/ng-autocomplete[1]/div[1]/div[1]/input[1]"


# --------------------------------------------------------------------------------------------------
# --- Utility Functions ---
# --------------------------------------------------------------------------------------------------

def select_html_select_option_by_index(waiter, dropdown_xpath, index):
    """
    Selects an option from a standard HTML <select> element using its index via JavaScript.
    """
    global driver
    try:
        select_element = waiter.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))

        # Use JavaScript to select the option by index and dispatch a change event
        js_script = "arguments[0].selectedIndex = arguments[1]; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));"
        driver.execute_script(js_script, select_element, index)

        print(f"   -> Selected option at index {index}.")
    except Exception as e:
        # Re-raise the error to be caught in the main try-except block
        raise NoSuchElementException(f"Could not select option by index {index}. Error: {e}")


try:
    # --- Login Step ---
    print("Opening login page and logging in...")
    driver.get('http://197.220.114.46:8085/#/login')
    driver.maximize_window()

    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
    username_field.send_keys('testsec')

    password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']")))
    password_field.send_keys('12345')

    login_button_xpath = "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[3]/div[1]/button[1]"
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, login_button_xpath)))
    login_button.click()
    print("Login successful.")

    # --- Navigation to Add Service Provider ---
    print("\nNavigating to Add Service Provider page...")

    # 1. Click the Service Provider Menu (Dropdown)
    sp_menu_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[3]/a[1]"
    sp_menu_link = wait.until(EC.element_to_be_clickable((By.XPATH, sp_menu_xpath)))
    sp_menu_link.click()
    print("Expanded Service Provider Menu.")
    time.sleep(1)

    # 2. Click Add Service Provider Sub-menu
    add_sp_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[3]/app-sidebar-nav-items[1]/app-sidebar-nav-link[1]/a[1]/app-sidebar-nav-link-content[1]"
    add_sp_link = wait.until(EC.element_to_be_clickable((By.XPATH, add_sp_xpath)))
    add_sp_link.click()
    print("Navigated to Add Service Provider form.")

    # Wait for the form title/page load
    form_title_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[1]/strong[1]"
    wait.until(EC.presence_of_element_located((By.XPATH, form_title_xpath)))

    # Initial loading spinner wait
    print("   -> Waiting for the initial loading spinner to disappear...")
    try:
        wait.until(EC.invisibility_of_element_located((By.XPATH, spinner_backdrop_xpath)))
        print("   -> Initial loading spinner dismissed.")
    except TimeoutException:
        print("   -> WARNING: Initial spinner invisibility check timed out. Proceeding.")

    # --- Form Filling: Service Provider (Stabilized Order) ---
    print("Filling service provider details...")

    # 1. Mode (Select Dropdown - Using Index 1 for first option)
    mode_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]/select[1]"
    select_html_select_option_by_index(wait, mode_xpath, 1)

    # 2. Name (Input Field)
    wait.until(EC.presence_of_element_located((By.XPATH, name_xpath))).send_keys(SP_NAME)
    print(f"   -> SP Name: {SP_NAME}")

    # 3. Email (Input Field)
    email_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[8]/div[1]/input[1]"
    wait.until(EC.presence_of_element_located((By.XPATH, email_xpath))).send_keys(SP_EMAIL_ADDRESS)
    print(f"   -> Email: {SP_EMAIL_ADDRESS}")

    # 4. Address (Textarea)
    address_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[9]/div[1]/textarea[1]"
    wait.until(EC.presence_of_element_located((By.XPATH, address_xpath))).send_keys(SP_ADDRESS)
    print(f"   -> Address: {SP_ADDRESS}")

    # 5. Company Name (Input Field)
    company_name_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[11]/div[1]/ng-autocomplete[1]/div[1]/div[1]/input[1]"
    company_name_element = wait.until(EC.presence_of_element_located((By.XPATH, company_name_xpath)))
    company_name_element.send_keys(SP_COMPANY_NAME)
    print(f"   -> Company Name: {SP_COMPANY_NAME}")

    # 6. Company Address (Input Field)
    company_address_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[12]/div[1]/ng-autocomplete[1]/div[1]/div[1]/input[1]"
    company_address_element = wait.until(EC.presence_of_element_located((By.XPATH, company_address_xpath)))
    company_address_element.send_keys(SP_COMPANY_ADDRESS)
    print(f"   -> Company Address: {SP_COMPANY_ADDRESS}")

    # --- Start of Dropdowns and Unstable Fields ---

    # 7. Document Type (Select Dropdown - Using Index 1 for first option)
    select_html_select_option_by_index(wait, document_type_xpath, 1)

    # 8. Identity No (Input Field)
    wait.until(EC.presence_of_element_located((By.XPATH, identity_no_xpath))).send_keys(SP_IDENTITY_NO)
    print(f"   -> Identity No: {SP_IDENTITY_NO}")

    # 9. Primary Number (Requires Double-Click, highly unstable)
    primary_number_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, primary_number_xpath))
    )
    # Perform Double Click -> Clear -> Send Keys -> Tab
    ActionChains(driver).double_click(primary_number_element).perform()
    primary_number_element.clear()
    primary_number_element.send_keys(SP_PRIMARY_NUMBER)
    driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", primary_number_element)
    primary_number_element.send_keys(Keys.TAB)
    print(f"   -> Primary Number (Stabilized): {SP_PRIMARY_NUMBER}")

    # Wait for the spinner after the mobile number input
    print("   -> Waiting for overlay after Primary Number input...")
    try:
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.XPATH, spinner_backdrop_xpath)))
        print("   -> Overlay dismissed.")
    except TimeoutException:
        print("   -> WARNING: Overlay after Primary Number timed out. Proceeding.")

    # 10. Nationality (THE TRIGGERING FIELD)

    # Use 2 second explicit wait for stabilization
    print("   -> Explicit 2 second wait before Nationality selection...")
    time.sleep(2)

    select_html_select_option_by_index(wait, nationality_xpath, 1)

    # Wait for overlay after Nationality selection
    print("   -> Waiting for overlay after Nationality selection (crucial wait)...")
    try:
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.XPATH, spinner_backdrop_xpath)))
        print("   -> Overlay dismissed.")
    except TimeoutException:
        print("   -> WARNING: Overlay after Nationality timed out. Proceeding.")

    # --------------------------------------------------------------------------------------------------
    # --- CRITICAL FIX: DATA RE-ENTRY BLOCK ---
    # Re-enters data if the Nationality field triggered a form reset.
    # --------------------------------------------------------------------------------------------------
    print("\n*** Checking for form reset and re-entering cleared data ***")

    # Check the Name field for blank state
    name_element = wait.until(EC.presence_of_element_located((By.XPATH, name_xpath)))
    if name_element.get_attribute('value') == '':
        print("   -> DETECTED: Name field cleared. Re-entering stable data.")

        # Re-enter Name
        name_element.send_keys(SP_NAME)
        print("   -> Name re-entered.")

        # Re-select Document Type
        select_html_select_option_by_index(wait, document_type_xpath, 1)
        print("   -> Document Type re-selected.")

        # Re-enter Identity No
        wait.until(EC.presence_of_element_located((By.XPATH, identity_no_xpath))).send_keys(SP_IDENTITY_NO)
        print("   -> Identity No re-entered.")

        # Re-enter Primary Number (using action chains for robustness)
        primary_number_element_re = wait.until(EC.visibility_of_element_located((By.XPATH, primary_number_xpath)))
        ActionChains(driver).double_click(primary_number_element_re).perform()
        primary_number_element_re.clear()
        primary_number_element_re.send_keys(SP_PRIMARY_NUMBER)
        print("   -> Primary Number re-entered.")
    else:
        print("   -> Name field was not cleared. Continuing.")
    # --- END CRITICAL FIX ---
    # --------------------------------------------------------------------------------------------------

    # 11. Gender (Radio Button)
    # Use 2 second explicit wait for stabilization
    print("   -> Explicit 2 second wait before Gender selection...")
    time.sleep(2)

    gender_label_xpath = "//label[contains(., 'Male')]"
    wait.until(EC.element_to_be_clickable((By.XPATH, gender_label_xpath))).click()
    print("   -> Selected Gender: Male")

    # 12. Work Profile (LAST FIELD)
    work_profile_element = wait.until(EC.presence_of_element_located((By.XPATH, work_profile_xpath)))
    work_profile_element.send_keys(SP_WORK_PROFILE)
    print(f"   -> Work Profile (Last Field): {SP_WORK_PROFILE}")

    # --- Overlay Dismissal after Work Profile ---

    # ACTION 1: Force focus away by clicking the form title/header (stable, non-interactive element).
    wait.until(EC.element_to_be_clickable((By.XPATH, form_title_xpath))).click()
    print("   -> Clicked form title to forcefully dismiss autocomplete focus.")

    # ACTION 2: Wait strictly for the autocomplete overlay to disappear.
    print("   -> Waiting strictly for autocomplete overlay to disappear (Max 5s)...")
    try:
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.XPATH, autocomplete_overlay_xpath)))
        print("   -> Autocomplete overlay successfully dismissed.")
    except TimeoutException:
        print("FATAL ERROR: The Autocomplete Overlay remained visible and timed out.")
        pass

    # 13. Submit Button
    print("\nAttempting to click Submit button...")
    submit_button_xpath = "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-service-provider[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[3]/button[1]"
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_button_xpath)))

    submit_button.click()
    print("Clicked Submit.")

    # --- Wait for Submission/Load ---
    print("Waiting for submission to complete and redirect...")
    time.sleep(5)
    print("Service Provider creation process complete (5s wait for redirect/confirmation).")

    # --- Logout Step ---
    print("\nLogging out...")

    # Clicking the user menu (using generic text 'testsec')
    user_menu_xpath = "//span[contains(., 'testsec')]"
    user_menu = wait.until(EC.element_to_be_clickable((By.XPATH, user_menu_xpath)))

    driver.execute_script("arguments[0].click();", user_menu)

    logout_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'logout')]")))
    logout_button.click()
    print("Logout successful.")

    time.sleep(2)

except Exception as e:
    # Handle the error and save screenshot
    error_message = f"Message: {e}"
    if "ElementClickInterceptedException" in str(e):
        error_message = f"Message: Element Click Intercepted - Check for persistent overlays (like autocomplete or loading spinners).\nOriginal Error: {e}"
    elif "NoSuchElementException" in str(e):
        error_message = f"Message: Element not found or Selection failed. Check XPaths and ensure all previous form fields were successfully processed.\nOriginal Error: {e}"

    print(f"\n--- AN ERROR OCCURRED ---")
    print(error_message)
    driver.save_screenshot('error_screenshot_service_provider_onboarding_final.png')
    print("Saved screenshot to 'error_screenshot_service_provider_onboarding_final.png'")

finally:
    print("Test finished. Closing browser.")
    driver.quit()