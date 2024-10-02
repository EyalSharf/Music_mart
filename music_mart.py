import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://musicmart.co.il/")
driver.maximize_window()
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

try:
    flashy_popup = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "flashy-popup"))
    )
    print("Flashy popup element found.")

    shadow_root_script = """
    return document.querySelector('flashy-popup').shadowRoot;
    """
    shadow_root = driver.execute_script(shadow_root_script)

    if shadow_root:
        close_button = shadow_root.find_element(By.CSS_SELECTOR, "a.fls-close.close-on-click.fls-top-right")

        if close_button:
            close_button.click()
            print("Popup closed by clicking the close button.")
        else:
            print("Close button not found inside shadow DOM.")
    else:
        print("Shadow root not found.")
except Exception as e:
    print(f"An error occurred: {e}")

try:
    guitar_strings = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/div/div[5]/div[1]/div/a/div/div[2]/div/h5"))
    )
    guitar_strings.click()
except Exception as e:
    print(f"An error occurred while trying to click on the guitar strings link: {e}")

bass_strings = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "מיתרים לגיטרה בס"))
)
bass_strings.click()

filter_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='סנן']"))
)
filter_button.click()

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

product_elements = driver.find_elements(By.CSS_SELECTOR, ".product-small.box")

search_results = []

for product in product_elements:
    try:
        product_name_element = product.find_element(By.CSS_SELECTOR, "p.name.product-title")
        product_name = product_name_element.text.strip()
    except:
        try:
            product_name_element = product.find_element(By.CSS_SELECTOR, "a.woocommerce-LoopProduct-link")
            product_name = product_name_element.text.strip()
        except:
            product_name = "N/A"

    try:
        product_link_element = product.find_element(By.CSS_SELECTOR, "a.woocommerce-LoopProduct-link")
        product_link = product_link_element.get_attribute("href")
    except:
        product_link = "N/A"

    try:
        price_element = product.find_element(By.CSS_SELECTOR, "span.woocommerce-Price-amount.amount")
        price = price_element.text.strip()
    except:
        price = "N/A"

    search_results.append({"Name": product_name, "Link": product_link, "Price": price})

df = pd.DataFrame(search_results)

print(f"Found {len(search_results)} products")
print(df.head())
excel_file = "search_results.xlsx"
df.to_excel(excel_file, index=False)

print(f"Results have been written to {excel_file}")

input('Press any key to exit...')

driver.quit()
