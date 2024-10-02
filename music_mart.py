from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Assuming you have a WebDriver instance (e.g., Chrome)
driver = webdriver.Chrome()

# Navigate to the webpage
driver.get("https://musicmart.co.il/")
driver.maximize_window()
# Wait for the page to fully load
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# Check if the 'flashy-popup' element exists before trying to access the shadow DOM
try:
    flashy_popup = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "flashy-popup"))
    )
    print("Flashy popup element found.")

    # Access the shadow DOM of the flashy-popup element
    shadow_root_script = """
    return document.querySelector('flashy-popup').shadowRoot;
    """
    shadow_root = driver.execute_script(shadow_root_script)

    # If the shadow root is successfully retrieved, look for the close button
    if shadow_root:
        # Locate the 'a' tag that serves as the close button
        close_button = shadow_root.find_element(By.CSS_SELECTOR, "a.fls-close.close-on-click.fls-top-right")

        # Click on the close button
        if close_button:
            close_button.click()
            print("Popup closed by clicking the close button.")
        else:
            print("Close button not found inside shadow DOM.")
    else:
        print("Shadow root not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# Now proceed with the rest of the script
try:
    guitar_strings = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/div/div[5]/div[1]/div/a/div/div[2]/div/h5"))
    )
    guitar_strings.click()
except Exception as e:
    print(f"An error occurred while trying to click on the guitar strings link: {e}")
input('x')
# Close the driver
driver.quit()
