

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller  
import time

# Install latest ChromeDriver
chromedriver_autoinstaller.install()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")  # Comment this out to see the browser UI

# Initialize WebDriver
try:
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    driver.maximize_window()
    driver.get("http://fe.garibook.com/")

    # Wait for page load
    wait = WebDriverWait(driver, 25)

    # Click 'Car Rental' tab
    wait.until(EC.element_to_be_clickable((By.ID, "uncontrolled-tab-example-tab-carRental"))).click()

    # Select 'One Way'
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='trip-0']"))).click()

    # Select 'Sedan'
    sedan = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.single-car-type-box.text-center")))
    driver.execute_script("arguments[0].scrollIntoView();", sedan)  # Scroll into view
    sedan.click()

    # Click 'Continue'
    continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.gb-primary-solid-btn.bg-primary-gb.text-white")))
    driver.execute_script("arguments[0].click();", continue_btn)  # JavaScript click fallback
    time.sleep(10)

    # Input phone number and request OTP
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='mobile']"))).send_keys("01770988785")
    send_otp_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.theme-primary-btn")))
    send_otp_btn.click()

    # Extract OTP from alert (if available)
    try:
        otp_text = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert.alert-info"))).text
        otp_code = otp_text.split(": ")[-1]
        print("Extracted OTP:", otp_code)

    except Exception as e:
        print("Failed to extract OTP:", str(e))
        driver.quit()
        exit()

    # Enter OTP
    otp_fields = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.text-center.form-control")))
    for i in range(len(otp_code)):
        otp_fields[i].send_keys(otp_code[i])

    # Click Continue with OTP
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.theme-primary-btn"))).click()

    # Enter Pickup and Drop Off Locations
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='pickup_location']"))).send_keys("Dhaka University, Nilkhet Road, Dhaka, Bangladesh")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='drop_off_location']"))).send_keys("Dhaka Medical College Hospital, Secretariat Road, Dhaka, Bangladesh")

    # Enter Date & Time for the ride
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='pickup_date_time']"))).send_keys("2025-02-19 12:00 AM")

    # Enter Promo Code
    promo_code_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='promo_code']")))
    promo_code_input.send_keys("XXXX")

    # Click Request Your Trip
    request_trip_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.gb-primary-solid-btn.bg-primary-gb.text-white")))
    driver.execute_script("arguments[0].click();", request_trip_btn)  # JavaScript click fallback

    # Fill Name, Email, Date of Birth Dialog
    try:
        name_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Name']")))
        name_field.send_keys("Jannatun Nur Etu")
        

        date_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='DD/MM/YYYY']")))
        date_field.send_keys("23-Apr-2025")


        # Fill in the email
        email_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Type your mail']")))
        email_field.send_keys("jannatietu.nstu@gmail.com")

        # Select gender
        gender_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#femail")))  # Select female
        gender_field.click()

        # Click on the continue button
        continue_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        continue_btn.click()

    except Exception as e:
        print("No form page found or another error occurred:", str(e))

    try:
        # Wait for the Booking ID or success message
        booking_id_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span")))

        # Check if Booking ID is displayed
        if booking_id_element:
            booking_id = booking_id_element.text
            if "MBYV" in booking_id:
                print("Test Passed: Trip requested successfully! Booking ID:", booking_id)
            else:
                print("Test Failed: Booking ID not found.")
    except Exception as e:
            print("No booking id is found:", str(e))

    

except Exception as e:
    print("❌ An error occurred:", str(e))




