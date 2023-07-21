from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains, ActionBuilder



rooms = {
    '100s': {
        '171': 2,        
        '173': 4,
        '174': 4,
        '177': 4,
        '178': 4,
        '179': 4,
        '172': 10,
        '176': 12,
    },
    '300s': {
        '360A': 2,
        '360B': 2,
        '360C': 2,
        '360D': 2,
        '360E': 2,
        '360J': 4,
        '360K': 4,
        '360L': 4,
        '360M': 4,
        '360N': 4,
        '380': 4,
        '371': 8,
        '372': 8,
        '373': 8,
        '377': 8,
        '378': 8,
        '379': 8,
        '386': 8,
        '387': 8,
        '388': 8,
        '389': 8, 
        '381': 10,
        '370A': 10,
        '370B': 10,
    },
    '400s': {
        '426' : 4,  
        '425' : 6, 
        '429' : 6, 
        '430' : 6, 
        '431' : 6, 
        '432' : 6,
        '407' : 8,
        '406' : 10,   
        '434' : 12,
    },
    # Add more 100s groups as needed
}

def safe_is_element_xpath_available(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True 
    except NoSuchElementException:
        return False

def safe_find_elements_by_xpath(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return None
def safe_find_element_by_xpath(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return None

def safe_countChildNodes(driver, xpath):
    try:
        x = safe_find_element_by_xpath(driver,xpath).get_attribute('childElementCount')
        return int(x)
    except Exception as e:
        print(e)
        return 1
def safe_click(element):
    if element.is_enabled() and element.is_displayed():
            element.click()
    else:
        print("not")
        return
# Configure ChromeOptions for headless mode
def date_change(driver, date):
    date_parts = date.split("-")
    date_button = safe_find_element_by_xpath(driver, '//*[@id="eq-time-grid"]/div[1]/div[1]/button[1]')
    safe_click(date_button)
    month_menu = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="equip_"]/div[5]/div[1]/table/thead/tr[2]/th[2]')))
    safe_click(month_menu)
    year_menu = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="equip_"]/div[5]/div[2]/table/thead/tr[2]/th[2]')))
    safe_click(year_menu)
    table_yXpath = '//*[@id="equip_"]/div[5]/div[3]/table/tbody/tr/td'
    relevant_year= WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,f'{table_yXpath}//span[contains(text(), "{str(int(date_parts[0]))}")]' )))
    safe_click(relevant_year)
    relevant_month= WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="equip_"]/div[5]/div[2]/table/tbody/tr/td/span[' +str(int(date_parts[1]))+ ']')))
    safe_click(relevant_month)
    table_dXpath = '//*[@id="equip_"]/div[5]/div[1]/table/tbody'
    td_element_xpath = f'{table_dXpath}//td[@class="day" and contains(text(), "{str(int(date_parts[2]))}")]'
    relevant_day = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, td_element_xpath)))
    safe_click(relevant_day)
def book_room(room, startTime,duration):
    print()
def rand_room(room_group,mincapacity):
    print()

# Set up the Chrome WebDriver
service = Service(executable_path=r"./chromedriver/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
#options.add_argument('--headless')  
driver = webdriver.Chrome(service=service, options=options)
# Perform actions using the headless browser
driver.get("https://ucf.libcal.com/reserve/generalstudyroom")
window_size = driver.get_window_size()
window_width = window_size['width']
window_height = window_size['height']
# Calculate the center coordinates
center_x = window_width // 2
center_y = window_height // 2
# Use ActionChains to move the cursor to the center of the webpage
# ... perform other actions, such as clicking elements, filling forms, etc.
#WebDriverWait(driver, 10) 
date_change(driver,"2023-07-22")
# WebDriverWait(driver, 10) 
#print("success")
# Close the browser when finished
#driver.quit()


#//*[@id="eq-time-grid"]/div[2]/div/table/tbody/tr/td[3]/div/div/div/table