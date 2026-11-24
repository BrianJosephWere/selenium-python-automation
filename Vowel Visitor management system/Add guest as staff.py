import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Setup Firefox Driver
driver = webdriver.Firefox()
driver.maximize_window()

try:
    # Navigate to URL
    driver.get("http://197.220.114.46:8085/#/login")

    # Initialize Wait
    wait = WebDriverWait(driver, 10)

    # --- LOGIN ---
    # Wait for username field
    username = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[1]/input[1]")
    ))
    username.send_keys("Teststaff")

    password = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[2]/input[1]"
    )
    password.send_keys("12345")

    login_btn = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/app-evisitor-loader[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/div[3]/div[1]/button[1]"
    )
    login_btn.click()

    time.sleep(3)

    # --- NAVIGATION ---
    wait = WebDriverWait(driver, 15)

    print("Navigating to Visitor Menu...")

    visitor_menu = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[1]/a[1]"
    )))
    visitor_menu.click()

    add_visitor_link = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/app-sidebar[1]/app-sidebar-nav[1]/app-sidebar-nav-items[1]/app-sidebar-nav-dropdown[1]/app-sidebar-nav-items[1]/app-sidebar-nav-link[1]/a[1]/app-sidebar-nav-link-content[1]"
    )))
    add_visitor_link.click()

    # --- FILL FORM ---
    print("Filling Form...")

    wait.until(EC.visibility_of_element_located((
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[2]/div[1]/input[1]"
    )))

    # Guest Type
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[1]/div[1]/input[1]"
    ).click()

    # Name
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[2]/div[1]/input[1]"
    ).send_keys("John Doe")

    # Mode of Entry
    mode_entry = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[3]/div[1]/select[1]"
    )
    Select(mode_entry).select_by_visible_text("Walk-In")

    # Primary Number
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[4]/div[1]/div[1]/input[1]"
    ).send_keys("712345678")

    # Email
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[5]/div[1]/input[1]"
    ).send_keys("testvisitor@example.com")

    # Document Type
    doc_type = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[6]/div[1]/select[1]"
    )
    Select(doc_type).select_by_index(1)

    # ID Number
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[7]/div[1]/input[1]"
    ).send_keys("98765432")

    # Nationality
    nationality = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[8]/div[1]/select[1]"
    )
    # Changed to select the first available option by index
    Select(nationality).select_by_index(1)

    # Expected Date
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[9]/div[1]/input[1]"
    ).send_keys("30/12/2025 , 10:00")

    # Purpose of Visit
    driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[10]/div[1]/input[1]"
    ).send_keys("Business Meeting")

    # --- SUBMIT ---
    print("Submitting Form...")
    submit_btn = driver.find_element(
        By.XPATH,
        "/html[1]/body[1]/app-dashboard[1]/div[1]/main[1]/div[2]/app-add-expected-visitor[1]/app-evisitor-loader[1]/div[1]/div[1]/div[1]/div[1]/div[3]/button[1]"
    )
    submit_btn.click()

    print("Test Completed Successfully.")
    time.sleep(5)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()