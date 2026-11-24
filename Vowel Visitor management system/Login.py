from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuration ---
# The URL based on the screenshot (internal IP address)
LOGIN_URL = "http://197.220.114.46:8085/#/login"

# Sample credentials (Replace these with actual test credentials)
TEST_USERNAME = "testpm"
TEST_PASSWORD = "12345"

# XPaths for Logout Steps
PROFILE_ICON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/a[1]/img[1]"
LOGOUT_BUTTON_XPATH = "/html[1]/body[1]/app-dashboard[1]/app-header[1]/ul[1]/li[1]/div[1]/a[4]"

# --- Setup Firefox WebDriver ---
try:
    # Set up Firefox options
    firefox_options = Options()
    # firefox_options.add_argument("--headless") # Uncomment for headless mode

    # Initialize the Firefox driver
    print("Starting Firefox browser...")
    driver = webdriver.Firefox(options=firefox_options)
    driver.maximize_window()
    driver.get(LOGIN_URL)
    print(f"Navigated to: {LOGIN_URL}")

    # Use WebDriverWait for better stability
    wait = WebDriverWait(driver, 10)

    # --- Login Steps ---
    print("Attempting to log in...")

    # Locate and enter Username and Password using your XPaths
    username_field = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[1]/input[1]")))
    password_field = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[2]/input[1]")))

    username_field.send_keys(TEST_USERNAME)
    print(f"Entered Username: **{TEST_USERNAME}**")

    password_field.send_keys(TEST_PASSWORD)
    print(f"Entered Password: **{'*' * len(TEST_PASSWORD)}**")

    # Locate and click the Login button
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                          "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[3]/div[1]/button[1]")))
    login_button.click()
    print("Clicked the Login button.")

    # Wait for the dashboard to load after login
    print("Waiting for dashboard to load...")
    # Wait for the presence of the dashboard's main container or the profile icon itself
    wait.until(EC.presence_of_element_located((By.XPATH, PROFILE_ICON_XPATH)))
    print("Login successful. Dashboard loaded.")
    time.sleep(2)  # Short pause to visually confirm the dashboard load
    # --- Logout Steps ---
    print("Attempting to log out...")

    time.sleep(10)

    # 1. Click the Profile Icon to open the dropdown menu
    profile_icon = wait.until(EC.element_to_be_clickable((By.XPATH, PROFILE_ICON_XPATH)))
    profile_icon.click()
    print("Clicked the Profile Icon.")

    # 2. Click the Logout button in the dropdown
    logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, LOGOUT_BUTTON_XPATH)))
    logout_button.click()
    print("Clicked the Logout button.")

    # Wait for a few seconds and verify the URL is back to the login page
    print("Waiting for logout to complete and verifying...")
    wait.until(EC.url_to_be(LOGIN_URL))

    # --- Verification (Logout Check) ---
    current_url = driver.current_url
    if current_url == LOGIN_URL:
        print(f"✅ Test Passed: Logout successful. Returned to Login Page: {current_url}")
    else:
        print(f"⚠️ Test Failed: Logout may have failed. Current URL: {current_url}")

# --- Error Handling & Cleanup ---
except NoSuchElementException as e:
    print(f"❌ Error: Could not find a required element on the page during the process.")
    print(f"Details: {e}")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
finally:
    # Ensure the browser is closed
    if 'driver' in locals() and driver:
        print("Closing the browser.")
        driver.quit()