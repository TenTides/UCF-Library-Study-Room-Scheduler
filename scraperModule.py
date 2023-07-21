from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains, ActionBuilder

rooms = [
    {
        '171': 2,
        '172': 10,
        '173': 4,
        '174': 4,
        '176': 12,
        '177': 4,
        '178': 4,
        '179': 4,
    },
    {
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
        '370A': 10,
        '370B': 10,
        '371': 8,
        '372': 8,
        '373': 8,
        '377': 8,
        '378': 8,
        '379': 8,
        '380': 4,
        '381': 10,
        '386': 8,
        '387': 8,
        '388': 8,
        '389': 8,
    },
    { 
        '406': 10,
        '407': 8,
        '425': 6,
        '426': 4,
        '429': 6,
        '430': 6,
        '431': 6,
        '432': 6,
        '434': 12
    },
    #9  #40 total
    # Add more 100s groups as needed
]

def safe_is_element_xpath_available(driver, xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True 
    except NoSuchElementException:
        return False

def safe_find_element_by_xpath(driver, xpath):
    try:
        return driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return None

def safe_click(element):
    try:
        if element.is_enabled() and element.is_displayed():
                element.click()
        return True
    except Exception as e:
        return False
    
def roomIndex(roomNum):
    room_group = int(roomNum[0]) // 2
    room_index = sum(len(rooms[x]) for x in range(room_group)) # -1
    room_index += list(rooms[room_group].keys()).index(roomNum) + 1
    return room_index

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
    hour = int(startTime[0:2])
    startTime = startTime[2:] + ("pm" if hour >= 12 else "am")
    hour = hour if hour < 12 else hour - 12
    startTime = (str(hour)) +  startTime
    
    room_index = roomIndex(room)
    grandTbl = '//*[@id="eq-time-grid"]/div[2]/div/table/tbody/tr/td[3]/div/div/div/table/tbody/tr['+str(room_index)+']'
    relevantStartElementPath = f'{grandTbl}/td/div/div[2]/div/a[contains(@aria-label, "' +startTime +'") and contains(@aria-label, "Available")]/div/div/div'
    print(relevantStartElementPath)

    relevantStartElement =  WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, relevantStartElementPath)))
    driver.execute_script("arguments[0].scrollIntoView();", relevantStartElement)

    #TODO
    if not safe_click(relevantStartElement):
        print("room for that time is already booked")
        return
    
    selsect_elementPath = '//*[@id="bookingend_1"]'
    select_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, selsect_elementPath)))
    driver.execute_script("arguments[0].scrollIntoView();", select_element)
    select = Select(select_element)

    try:
        select.select_by_index(int(duration*2-1))
    except Exception as e: # can be circumvented if an additional parameter is addded to the html that takes 
        return             # a strict val boolean, which autofills for the closset possible appointment at that start time
        
#TODO
def rand_room(room_group,mincapacity):
    print()

# # Set up the Chrome WebDriver
service = Service(executable_path=r"./chromedriver/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--headless')  
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://ucf.libcal.com/reserve/generalstudyroom")
date_change(driver,"2023-07-22")
book_room("434","10:00",3.5)
#driver.quit()


