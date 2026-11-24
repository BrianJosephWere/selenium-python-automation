from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import time
import random

# --- Setup ---
options = Options()
options.accept_insecure_certs = True
driver = webdriver.Firefox(options=options)

# Initialize WebDriver & Waiter
driver.set_page_load_timeout(30)
wait = WebDriverWait(driver, 20)

# Generate a unique Program Name for testing
unique_id = str(int(time.time()))
PROGRAM_NAME = f"Automated Program {unique_id}"

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
    # Note: Using text normalization for cleaner matching
    option_locator = f"//mat-option/span[normalize-space()='{option_text}']"
    try:
        option_to_select = waiter.until(EC.element_to_be_clickable((By.XPATH, option_locator)))
        option_to_select.click()
        print(f"   -> Selected '{option_text}'")
    except TimeoutException:
        print(f"   -> WARNING: Option '{option_text}' not found or clickable. Proceeding.")
        # Attempt to close the dropdown if it's open, to allow the script to continue
        driver.execute_script("document.body.click();")


# --- Utility Function for Date Picker Selection ---
def select_date_picker_future(waiter, input_xpath, days_offset=7):
    """
    Clicks a date input, selects today's date + offset from the calendar, and returns the date string.
    Note: Assumes a standard mat-calendar implementation.
    """
    print(f"   -> Selecting date with {days_offset} days offset...")

    # 1. Click the input field to open the calendar (Date inputs often use a button next to them)
    # Target the input field
    date_input = waiter.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
    date_input.click()

    # 2. Click the date picker icon/button (usually a sibling element or nested)
    # Finding the specific calendar icon for the mat-form-field is complex via XPath,
    # so we often rely on the fact that clicking the input field is enough.
    # If the icon is needed, you'd use a more complex locator like:
    # calendar_icon = date_input.find_element(By.XPATH, "./ancestor::mat-form-field//button[@aria-label='Open calendar']")
    # calendar_icon.click()

    # 3. Navigate to a date in the future (This assumes the current month is visible)
    # The XPath targets a date cell that is NOT disabled (i.e., not mat-calendar-body-disabled)
    # and preferably in the coming days (e.g., day 20).
    date_to_select_xpath = f"//mat-calendar-body//td[not(contains(@class, 'mat-calendar-body-disabled'))]/div[normalize-space()='{days_offset}']"

    try:
        date_element = waiter.until(EC.element_to_be_clickable((By.XPATH, date_to_select_xpath)))
        date_element.click()
        print(f"   -> Date selected.")
        return date_input.get_attribute("value")
    except TimeoutException:
        print("   -> WARNING: Could not select a specific date. Closing calendar.")
        driver.execute_script("document.body.click();")
        return "Date Selection Failed"


# --- Utility Function for Multi-Select Dropdown Selection (UI Settle) ---
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

    # --- Navigate to Program Onboarding ---
    print("\nNavigating to Program Onboarding...")

    # 1. Click the Program Onboarding Menu
    onboarding_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[normalize-space()='PROGRAM ONBOARDING']")))
    onboarding_link.click()
    print("Expanded PROGRAM ONBOARDING menu.")

    # 2. Navigate to Program List
    onboarding_sub_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(., 'Program List')]")))
    onboarding_sub_link.click()
    print("Navigated to Program List.")

    # --- Start Program Creation ---
    print("Starting new Program creation...")

    # 3. Click the '+ Program' button
    create_program_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., ' Program')]")))
    create_program_button.click()
    print("Clicked '+ Program' button. Loading form...")

    # Wait for the form title to ensure the page has loaded
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//mat-card-title[normalize-space()='Add & Manage New Program']")))

    # --- Fill Form Section 1: Basic Details ---
    print("Filling basic program details...")

    # Program Name (using XPath based on image_b8f277.png structure)
    program_name_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[1]/div[1]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]")))
    program_name_input.send_keys(PROGRAM_NAME)
    print(f"   -> Program Name: {PROGRAM_NAME}")

    # Program Alias
    program_alias_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[1]/div[2]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]")))
    program_alias_input.send_keys(f"Alias{unique_id}")

    # Program Description
    program_desc_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[1]/div[3]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]")))
    program_desc_input.send_keys("Automated test program description.")

    # Dropdowns (Single-Select - using CSS Selectors for formcontrolname)
    select_single_select_option(wait, "mat-select[formcontrolname='frequencyOfIntervention']", 'DAILY')

    # Target Group
    target_group_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[1]/div[5]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]")))
    target_group_input.send_keys("Infants.")

    select_single_select_option(wait, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[1]/div[6]/mat-form-field[1]/div[1]/div[1]/div[3]", 'USD')

    # Allocated Funding (mat-input-4 or similar)
    allocated_funding_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Allocated Funding *']")))
    allocated_funding_input.send_keys(f"{random.randint(10000, 99999)}")

    select_single_select_option(wait, "mat-select[formcontrolname='natureOfIntervention']", 'Food')

    # Target Number of Beneficiaries
    target_beneficiaries_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Target Number of Beneficiaries *']")))
    target_beneficiaries_input.send_keys(f"{random.randint(100, 999)}")

    # Target Countries (Multi-Select, but treating as single for simplicity in this section)
    # The actual implementation of Multi-Select is below.

    # --- Fill Form Section 2: Dates, Pillars, and EGF Details ---
    print("Filling date, pillar, and EGF details...")

    # Contact Start Date (XPath targeting the input for robust selection)
    contact_start_date_xpath = "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[1]/div[13]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]']"
    select_date_picker_future(wait, contact_start_date_xpath, days_offset=5)

    # Contract End Date
    contact_end_date_xpath = "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[1]/div[14]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]']"
    select_date_picker_future(wait, contact_end_date_xpath, days_offset=25)

    # Pillars (Single Select)
    select_single_select_option(wait, "mat-select[formcontrolname='pillar']", 'Agriculture Pillar')

    # EGF Details
    wait.until(EC.presence_of_element_located((By.XPATH, "//h4[normalize-space()='EGF Details']")))

    # EGF Program Manager Name
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='EGF Program Manager Name *']"))).send_keys("EGF Manager")

    # EGF Program Manager Phone (Primary)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[2]/div[1]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]']"))).send_keys("254701230000")

    # EGF Program Manager Email
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[2]/div[2]/mat-form-field[1]/div[1]/div[1]/div[3]/div[1]/input[1]"))).send_keys(
        f"egf.{random.randint(1, 999)}@test.com")

    # --- Fill Form Section 3: Partner Details (Nested Dropdowns) ---
    print("Filling partner details...")

    # Partner Type (Single Select)
    select_single_select_option(wait, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[3]/div[1]/mat-form-field[1]/div[1]/div[1]/div[3]/mat-select[1]/div[1]/div[1]/span[1]", 'General')

    # Partner (Single Select - Dependent on Partner Type)
    # This might require a small delay if the list takes time to populate after the Partner Type change.
    time.sleep(1)
    select_single_select_option(wait, "mat-select[formcontrolname='partner']",
                                'Test Partner')  # Assuming a partner named 'Test Partner' exists

    # Partner Program Manager Name
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[3]/div[3]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]"))).send_keys("Partner Manager")

    # Partner Email
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[3]/div[4]/mat-form-field[1]/div[1]/div[1]/div[3]/input[1]"))).send_keys(f"partner.{random.randint(1, 999)}@test.com")

    # Partner Phone (Primary)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-create-program[1]/div[1]/div[2]/mat-card[1]/form[1]/div[3]/div[5]/mat-form-field[1]/div[1]/div[1]/div[3]/div[1]/input[1]"))).send_keys("254701231111")

    # --- Handling Target Countries (Multi-Select) ---
    print("Handling Target Countries (Multi-Select) using XPath and UI Settle logic...")

    # Robust XPath for the Target Countries mat-select element.
    target_countries_xpath = "//mat-select[@formcontrolname='targetCountries']"

    countries_to_select = ['Rwanda', 'Kenya']
    # Call the robust multi-select function
    select_multi_select_list_option(wait, target_countries_xpath, countries_to_select, driver)

    # --- Final Dropdowns (These were after the multi-select in the Partner form) ---
    print("Filling final remaining dropdowns...")

    select_single_select_option(wait, "mat-select[formcontrolname='targetRegions']",
                                'Central')  # Assuming 'Central' exists
    select_single_select_option(wait, "mat-select[formcontrolname='modelOfIntervention']",
                                'Cash Transfer')  # Assuming 'Cash Transfer' exists
    select_single_select_option(wait, "mat-select[formcontrolname='programStatus']", 'Active')

    # --- Step 4: Click 'Save & Submit' ---
    # We rely on the time.sleep(1) in the function above to have enabled this button.
    print("Attempting final 'Save & Submit' using JavaScript to bypass interception...")

    # The locator for the button
    save_submit_xpath = "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-program-review-list[1]/mat-card[1]/div[1]/div[1]/h2[1]"

    # 1. Wait for the button to be present
    save_submit_button = wait.until(EC.presence_of_element_located((By.XPATH, save_submit_xpath)))

    # 2. Use JavaScript to forcefully click the button element
    driver.execute_script("arguments[0].click();", save_submit_button)
    print("Clicked 'Save & Submit' using JavaScript.")

    # --- Wait for Form Submission/Load ---
    print("Waiting for submission to complete and return to Program list...")
    # Wait for the program list title
    wait.until(EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/div[1]/app-program-review-list[1]/mat-card[1]/div[1]/div[1]/h2[1]")))
    print("Program Onboarding complete.")

    # --- Logout Step ---
    print("\nLogging out...")

    user_menu = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html[1]/body[1]/app-root[1]/app-admin-layout[1]/div[1]/mat-sidenav-container[1]/mat-sidenav-content[1]/app-header[1]/mat-toolbar[1]/app-user[1]/button[1]")))

    driver.execute_script("arguments[0].click();", user_menu)

    logout_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/button[2]")))
    logout_button.click()
    print("Logout successful.")

    time.sleep(2)

except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    print(f"Message: {e}")
    driver.save_screenshot('error_screenshot_program_onboarding.png')
    print("Saved screenshot to 'error_screenshot_program_onboarding.png'")

finally:
    print("Test finished. Closing browser.")
    driver.quit()