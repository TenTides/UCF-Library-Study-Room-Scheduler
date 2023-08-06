from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class StudyRoomBooker:
    def __init__(self):
        # Set up the Chrome WebDriver
        self.logged_in = False
        self.service = Service(executable_path=r"./chromedriver/chromedriver.exe")
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("detach", True)
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.get("https://ucf.libcal.com/reserve/generalstudyroom")


        # Define the room capacity data
        self.rooms = [
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
        ]

    def safe_is_element_xpath_available(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            return True
        except NoSuchElementException:
            return False

    def safe_find_element_by_xpath(self, xpath):
        try:
            return self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return None

    def safe_click(self, element):
        try:
            if element.is_enabled() and element.is_displayed():
                element.click()
            return True
        except Exception as e:
            return False

    def roomIndex(self, roomNum):
        room_group = int(roomNum[0]) // 2
        room_index = sum(len(self.rooms[x]) for x in range(room_group))
        room_index += list(self.rooms[room_group].keys()).index(roomNum) + 1
        return room_index

    def date_change(self, date):
        date_parts = date.split("-")
        date_button = self.safe_find_element_by_xpath('//*[@id="eq-time-grid"]/div[1]/div[1]/button[1]')
        self.safe_click(date_button)
        month_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="equip_"]/div[5]/div[1]/table/thead/tr[2]/th[2]')))
        self.safe_click(month_menu)
        year_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="equip_"]/div[5]/div[2]/table/thead/tr[2]/th[2]')))
        self.safe_click(year_menu)
        table_yXpath = '//*[@id="equip_"]/div[5]/div[3]/table/tbody/tr/td'
        relevant_year= WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH,f'{table_yXpath}//span[contains(text(), "{str(int(date_parts[0]))}")]' )))
        self.safe_click(relevant_year)
        relevant_month= WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="equip_"]/div[5]/div[2]/table/tbody/tr/td/span[{str(int(date_parts[1]))}]')))
        self.safe_click(relevant_month)
        table_dXpath = '//*[@id="equip_"]/div[5]/div[1]/table/tbody'
        td_element_xpath = f'{table_dXpath}//td[@class="day" and contains(text(), "{str(int(date_parts[2]))}")]'
        relevant_day = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, td_element_xpath)))
        self.safe_click(relevant_day)

    def start_timeCheck(self, room, startTime):
        hour = int(startTime[0:2])
        startTime = startTime[2:] + ("pm" if hour >= 12 else "am")
        hour = hour if hour < 12 else hour - 12
        startTime = (str(hour)) +  startTime

        room_index = self.roomIndex(room)
        grandTbl = f'//*[@id="eq-time-grid"]/div[2]/div/table/tbody/tr/td[3]/div/div/div/table/tbody/tr[{str(room_index)}]'
        relevantStartElementPath = f'{grandTbl}/td/div/div[2]/div/a[contains(@aria-label, "{startTime}") and contains(@aria-label, "Available")]/div/div/div'
        relevantStartElement =  WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, relevantStartElementPath)))
        self.driver.execute_script("arguments[0].scrollIntoView();", relevantStartElement)

        if not self.safe_click(relevantStartElement):
            print("room for that time is already booked")
            return False
        else:
            return True
        
    def select_durationCheck(self, duration):
        selsect_elementPath = '//html/body/div[4]/main/div/div/div/div[5]/form/fieldset/div[1]/div/div/div/div/select'
        select_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, selsect_elementPath)))
        self.driver.execute_script("arguments[0].scrollIntoView();", select_element)
        select = Select(select_element)

        try:
            select.select_by_index(int(duration*2-1))
            time.sleep(2)
        except Exception as e: # can be circumvented if an additional parameter is addded to the html that takes 
            return False       # a strict val boolean, which autofills for the closest possible appointment at that start time
        return True

    def book_room(self,username,password,UCFID,date, room, startTime, duration):
        #print(date)
        self.date_change(date)
        # print("pass 1")
        # self.start_timeCheck(room, startTime)
        # self.select_durationCheck(duration)
        # self.login_sequence(username, password)
        # self.confirm_booking(UCFID)
        return True

    # Returns the room with the greatest positive capacity difference then the user specified mincapacity   
    def rand_room(self, room_group, min_capacity):
        roomGroupDict = self.rooms[int(room_group[0]) // 2]
        chosenRoom = "NULL"
        for key, value in roomGroupDict.items():
             if value >= min_capacity: 
                 chosenRoom = key
                 min_capacity = value
        return chosenRoom

    def login_sequence(self, username, password):
        #can only be called after first appointment is made on a single instance
        if not self.logged_in:
            #Infalible, will always execute successfully
            submit_dXpath = '//*[@id="submit_times"]'
            button1 = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, submit_dXpath)))
            self.driver.execute_script("arguments[0].scrollIntoView();", button1)
            self.safe_click(button1)
            self.driver.implicitly_wait(3)
            username_input = self.driver.find_element(By.ID,"userNameInput")
            password_input = self.driver.find_element(By.ID,"passwordInput")
            # Enter the username and password using send_keys method
            username_input.send_keys(f"{username}")
            password_input.send_keys(f"{password}")

            #Infalible, will always execute successfully
            submit_pXpath = '//*[@id="submitButton"]'
            button2 = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, submit_pXpath)))
            self.driver.execute_script("arguments[0].scrollIntoView();", button2)
            self.safe_click(button2)
            self.logged_in = True

    def confirm_booking(self,UCFID):
        # Check for if the password and username is correct here as this element won't be visable if it is wrong
        # makes for an easy check and confirmation rather than using a redirect detection or X path query
        try:
            submit_fXpath  = '//*[@id="terms_accept"]'
            button3 = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, submit_fXpath)))
            self.driver.execute_script("arguments[0].scrollIntoView();", button3)
            self.safe_click(button3)
        except Exception as e:
            return "Incorrect Username or Password"

        #Infalible, will always execute successfully
        nick_input = self.driver.find_element(By.ID,"nick")
        UCFID_input = self.driver.find_element(By.ID,"q2614")
        name_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="s-lc-eq-bform"]/fieldset/div[2]/div[2]/p'))).text
        nick_input.send_keys(f"{name_element}")
        UCFID_input.send_keys(f"{UCFID}")

        #Infalible will always execute successfully
        selsect_statusPath = '//*[@id="q2613"]'
        select_element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, selsect_statusPath)))
        self.driver.execute_script("arguments[0].scrollIntoView();", select_element)
        select = Select(select_element)
        select.select_by_index(1)
    
        submit_final_Button = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="btn-form-submit"]')))
        self.safe_click(submit_final_Button)

        try:
            success = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="s-lc-public-page-content"]/div/h1')))
        except Exception as e:
            return "Incorrect/Invalid UCFID"

        self.driver.get("https://ucf.libcal.com/reserve/generalstudyroom")
    def close(self):
        self.driver.quit()

if __name__ == "__main__": # only executed when run directly from scraperModule.py
    booker = StudyRoomBooker()
    booker.date_change("2023-08-7")
    booker.start_timeCheck("178","11:30")
    booker.select_durationCheck(4)
    booker.login_sequence("ty068421", "")
    booker.confirm_booking(5408209)
    booker.close()