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
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver, 20)

print("Opening login page...")
driver.get('https://69.62.113.171:8086/#/auth/login')
driver.maximize_window()


# --- Utility Function for Single-Select Dropdown Selection ---
def select_single_select_option(waiter, dropdown_css_selector, option_text):
    """Clicks a mat-select dropdown and selects a visible option (for single-select)."""
    # 1. Click the dropdown field
    dropdown = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_css_selector)))
    dropdown.click()

    # 2. Wait for the specific option to be clickable and click it
    option_locator = f"//mat-option/span[normalize-space()='{option_text}']"
    option_to_select = waiter.until(EC.element_to_be_clickable((By.XPATH, option_locator)))
    option_to_select.click()
    print(f"   -> Selected '{option_text}'")


# --------------------------------------------------------------------------------------------------
# --- Utility Function for Multi-Select Dropdown Selection (FINAL FIX: Guaranteed UI Settle) ---
# --------------------------------------------------------------------------------------------------
def select_multi_select_list_option(waiter, dropdown_locator, option_list, driver):
    """Clicks a mat-select dropdown, selects a LIST of visible options, and then CLOSES the dropdown by clicking the document body, followed by a guaranteed pause for form validation."""

    # 1. Click the dropdown field using By.XPATH (This opens the panel)
    dropdown = waiter.until(EC.element_to_be_clickable((By.XPATH, dropdown_locator)))
    dropdown.click()

    for option_text in option_list:
        # 2. Click each specific option/checkbox
        option_locator = f"//mat-option/span[normalize-space()='{option_text}']"

        # Add visibility check before clicking options
        waiter.until(EC.visibility_of_element_located((By.XPATH, option_locator)))
        option_to_select = waiter.until(EC.element_to_be_clickable((By.XPATH, option_locator)))
        option_to_select.click()
        print(f"   -> Selected '{option_text}'")

    # 3. Trigger close by clicking the document body using JavaScript.
    print("   -> Closing dropdown using JavaScript click on document body to trigger validation...")
    driver.execute_script("document.body.click();")

    # 4. CRITICAL FIX: Add a short, explicit sleep to allow Angular's change detection/validation
    # to recognize the field update and re-enable the Save & Submit button.
    print("   -> Waiting 1 second for the form state to update...")
    time.sleep(1)


try:
    # --- Login Step ---
    print("Logging in...")
    username_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Username']")))
    username_field.send_keys('Brian1')

    password_field = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[placeholder='Password']")))
    password_field.send_keys('Admin!23')

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(span, 'Login')]")))
    login_button.click()
    print("Login successful.")

    # --- Navigate to Partner Onboarding ---
    print("\nNavigating to Partner Onboarding...")

    onboarding_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='PARTNER ONBOARDING']")))
    onboarding_link.click()
    print("Expanded PARTNER ONBOARDING menu.")

    onboarding_sub_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(., 'Partner List')]")))
    onboarding_sub_link.click()
    print("Navigated to Partner List.")

    # --- Start Partner Creation ---
    print("Starting new Partner creation...")

    create_partner_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., ' Partner')]")))
    create_partner_button.click()
    print("Clicked '+ Partner' button. Loading form...")

    # Wait for the form title to ensure the page has loaded
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//mat-card-title[normalize-space()='Add & Manage New Partner']")))

    # --- Fill Form Section 1: Dropdowns and Entity Details (Using Single-Select Utility) ---
    print("Filling basic entity and type details...")

    # Dropdowns (Single-Select):
    select_single_select_option(wait, "mat-select[formcontrolname='country']", 'Kenya')
    select_single_select_option(wait, "mat-select[formcontrolname='partnerType']", 'General')
    select_single_select_option(wait, "mat-select[formcontrolname='entityType']", 'Partnership')

    # Entity Name (mat-input-1)
    entity_name = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-1']")))
    entity_name.send_keys(f"Test Partner {random.randint(100, 999)}")

    # Entity Alias (mat-input-2)
    entity_alias = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-2']")))
    entity_alias.send_keys(f"Alias{random.randint(100, 999)}")

    # Entity reference type (mat-input-4)
    # Using a more robust relative XPath to find the correct input field (based on form structure)
    entity_summary = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//mat-card//form//div[1]/div[6]//input")))
    entity_summary.send_keys("Test Ref Type")

    # Entity Registration No (mat-input-3)
    # Using a more robust relative XPath to find the correct input field
    reg_no = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//mat-card//form//div[1]/div[7]//input")))
    reg_no.send_keys(str(int(time.time())))

    # Entity Summary (mat-input-4)
    # Using a more robust relative XPath to find the correct input field
    entity_summary = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//mat-card//form//div[1]/div[8]//input")))
    entity_summary.send_keys("Automated Test Summary")


    # Country of Registration (Single-Select)
    select_single_select_option(wait, "mat-select[formcontrolname='countryOfRegistration']", 'Tanzania')

    # Unique Tax Payer Reference (mat-input-6)
    tax_ref = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-6']")))
    tax_ref.send_keys(f"TRef{random.randint(1000, 9999)}")

    # --- Fill Form Section 2: Director Details ---
    print("Filling Director details...")

    # Director Name (mat-input-14)
    director_name = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-14']")))
    director_name.send_keys("Jane Doe")

    # Identification Details (ID) (mat-input-15)
    id_details = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-15']")))
    id_details.send_keys(f"{random.randint(100000, 999999)}")

    # Director PIN (mat-input-16)
    director_pin = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-16']")))
    director_pin.send_keys(f"P{random.randint(1000, 9999)}")


    # --- Fill Form Section 3: Address Details ---
    print("Filling Address details...")

    # Address Line 1 (mat-input-7)
    addr_line_1 = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-7']")))
    addr_line_1.send_keys("123 Test Street")

    # State (mat-input-8)
    state_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-8']")))
    state_input.send_keys("Test State")

    # Town/City (mat-input-9)
    city_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-9']")))
    city_input.send_keys("Test City")

    # Postcode/Zip (mat-input-10)
    zip_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-10']")))
    zip_input.send_keys("10001")

    # Country of Operation (MULTI-SELECT - Using XPath for Dropdown)
    print("Handling Country of Operation (Multi-Select) using XPath...")

    # Robust XPath for the Country of Operation mat-select element.
    country_of_operation_xpath = "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-partner[1]/div[1]/div[2]/mat-card[1]/form[1]/div[3]/div[5]/mat-form-field[1]/div[1]/div[1]/div[3]/mat-select[1]/div[1]/div[1]/span[1]"

    countries_to_select = ['Rwanda', 'Kenya']
    # Call the updated function with the XPath and the driver object
    select_multi_select_list_option(wait, country_of_operation_xpath, countries_to_select, driver)

    # --- Fill Form Section 4: Contact Person ---
    print("Filling Contact Person details...")

    # Name (mat-input-11)
    contact_name = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//mat-card//form/div[4]/div[1]//input")))
    contact_name.send_keys("Contact Guy")

    # Telephone (mat-input-12)
    telephone = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-12']")))
    telephone.send_keys("254700123456")

    # Email Address (mat-input-13)
    email = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='mat-input-13']")))
    email.send_keys(f"test.{random.randint(1, 999)}@test.com")

    # --- Step 5: Click 'Save & Submit' ---
    # We rely on the time.sleep(1) in the function above to have enabled this button.
    print("Attempting final 'Save & Submit' using JavaScript to bypass interception...")

    # The locator for the button (now using a more robust XPATH)
    save_submit_xpath = "//mat-card//form/button[contains(., 'Save & Submit')]"

    # 1. Wait for the button to be present
    save_submit_button = wait.until(EC.presence_of_element_located((By.XPATH, save_submit_xpath)))

    # 2. Use JavaScript to forcefully click the button element (since standard click failed before)
    driver.execute_script("arguments[0].click();", save_submit_button)
    print("Clicked 'Save & Submit' using JavaScript.")

    # --- Wait for Form Submission/Load ---
    print("Waiting for submission to complete and return to Partner list...")
    # Wait for a unique element on the Partner List page
    wait.until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-partner-review-list[1]/mat-card[1]/div[1]/div[1]/h2[1]")))
    print("Partner Onboarding complete.")

    # --- Logout Step ---
    print("Logging out...")

    # Step 1: Click the User Menu (RELIABLE JS CLICK)
    user_menu = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='matero-username']")))

    print("Using JavaScript to click the User Menu...")
    driver.execute_script("arguments[0].click();", user_menu)

    print("Clicking the logout Button...")
    # Step 2: Click the Logout Drop down
    logout_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/button[2]")))
    logout_button.click()
    print("Logout successful.")

    time.sleep(2)

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    print(f"{e}")
    driver.save_screenshot('error_screenshot_partner_onboarding_final_ui_settle.png')
    print("Saved screenshot to 'error_screenshot_partner_onboarding_final_ui_settle.png'")

finally:
    print("Test finished. Closing browser.")
    driver.quit()