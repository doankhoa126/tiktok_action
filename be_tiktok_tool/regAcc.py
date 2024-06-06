from PyQt6.QtCore import pyqtSignal, QObject, QThread,QDateTime
from PyQt6 import QtCore
from selenium import webdriver
import time
import json 
import utils
import random
from concurrent.futures import ThreadPoolExecutor
from be_tiktok_tool.driverGPM import DriverGPM
from be_tiktok_tool.get_OTP import verifiedTiktok
import string
def generate_tiktok_password():
    lower_case = ''.join(random.choice(string.ascii_lowercase) for _ in range(7))
    special_char = '@'
    digits = ''.join(random.choice(string.digits) for _ in range(3))
    upper_case = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
    password = lower_case + special_char + digits + upper_case
    return password  
  
def get_user_agent(file_path):
    print('get_user_agent')
    with open(file_path, 'r') as file:
        user_agents = [line.strip() for line in file if line.strip()]
    
    if user_agents:
        return random.choice(user_agents)
    else:
        raise ValueError("Lỗi lấy user agents")

def get_proxy(file_path):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        
        if proxies:
            return random.choice(proxies)  # Chọn giá trị ngẫu nhiên từ danh sách
        else:
            raise ValueError("Lỗi lấy proxies")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None


class TikTokWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    update_status = pyqtSignal(int, str)
    update_password = pyqtSignal(int ,str)
    update_time = pyqtSignal(int ,str)

    def extract_xpaths_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            xpath_list = data.get("xpath_list", [])
            xpaths = {key: value for item in xpath_list for key, value in item.items()}
        return xpaths

    def __init__(self, reg_acc_data, thread_value, regAccTable):
        super().__init__()
        self.reg_acc_data = reg_acc_data
        self.thread_value = int(thread_value)  # Ensure thread_value is an integer
        self.regAccTable = regAccTable

    def run(self):
        self.progress.emit("Starting TikTok bot...")

        # Create and execute threads for each account
        with ThreadPoolExecutor(max_workers=self.thread_value) as executor:
            for account in self.reg_acc_data:
                executor.submit(self.process_account, account)

        self.progress.emit("All accounts processed.")
        self.finished.emit()

    def process_account(self, account):
        proxy = get_proxy(utils.PROXY_TXT)
        user_agent = get_user_agent(utils.USER_AGENT_TXT)
        print(proxy, user_agent)
        # instance = DriverGPM(proxy, user_agent)
        # driver = instance.driver
        
        driver = webdriver.Chrome()
        xpaths = self.extract_xpaths_from_file(utils.JSON_REG_ACC)
        
        try:
            self.update_status.emit(account['index'], f"Processing account {account['email']}")
            pass_tiktok = generate_tiktok_password()
            self.update_password.emit(account['index'], pass_tiktok)
            # Your account processing logic here
            # driver.get("https://www.tiktok.com/signup/phone-or-email/email")
            # time.sleep(3)
            # month = random.randint(1, 12)
            # self.update_status.emit(account['index'], "Choosing birthday month")
            # xpath_MonthBirthday = xpaths['xpath_MonthBirthday'] 
            # instance.click(xpath_MonthBirthday)

            # xpath_choose1 = xpaths['xpath_ChooseMonthBirthday']
            # xpath_ChooseMonthBirthday = xpath_choose1.format(month=month)
            # instance.click(xpath_ChooseMonthBirthday)
            # time.sleep(10)
            
            # # Choose day Birthday
            # day = random.randint(1, 28)
            # self.update_status.emit(account['index'], "Choosing birthday day")
            # xpath_DayBirthday = xpaths['xpath_DayBirthday'] 
            # instance.click(xpath_DayBirthday)

            # xpath_chooseDay = xpaths['xpath_ChooseDayBirthday']
            # xpath_ChooseDayBirthday = xpath_chooseDay.format(day=day)
            # instance.click(xpath_ChooseDayBirthday)
            
            # # Choose year Birthday
            # year = random.randint(23, 43)
            # self.update_status.emit(account['index'], "Choosing birthday year")
            # xpath_YearBirthday = xpaths['xpath_YearBirthday'] 
            # instance.click(xpath_YearBirthday)

            # xpath_chooseYear = xpaths['xpath_ChooseYearBirthday']
            # xpath_ChooseYearBirthday = xpath_chooseYear.format(year=year)
            # instance.click(xpath_ChooseYearBirthday)

            # # Input Email
            # self.update_status.emit(account['index'], "Entering email")
            # xpath_InputEmail = xpaths['xpath_input_email'] 
            # instance.input_(xpath_InputEmail, account['email'])

            # # Input password 
            # self.update_status.emit(account['index'], "Entering password")
            # passwordTiktok = f'{account["password"]}@123'
            # xpath_InputPassword = xpaths['xpath_input_password'] 
            # instance.input_(xpath_InputPassword, passwordTiktok)

            # # Click send code button
            # self.update_status.emit(account['index'], "Clicking send code button")
            # xpath_sendCodeBtn = xpaths['xpath_sendCodeBtn']
            # instance.click(xpath_sendCodeBtn)

            # time.sleep(30)
            # self.update_status.emit(account['index'], "Waiting for verification code")
            # verified_code = verifiedTiktok(account['email'], account['password'])
            
            # # Input OTP 
            # self.update_status.emit(account['index'], "Entering OTP")
            # xpath_InputOTP = xpaths['xpath_inputOTP'] 
            # instance.input_(xpath_InputOTP, verified_code)
            # self.update_status.emit(account['index'], "Account registered")

            # Simulate processing
            time.sleep(random.randint(5, 10))
        finally:
            driver.quit()
            self.update_status.emit(account['index'], f"Finished processing account {account['email']}")
            currentDateTime = QtCore.QDateTime.currentDateTime()
            currentDateTimeString = currentDateTime.toString("  dd/MM/yyyy  hh:mm:ss")
            self.update_time.emit(account['index'], str(currentDateTimeString))
# Ensure driver is closed after task completion

        # self.update_status.emit(batch_index, f"Batch {batch_index} completed.")

       # Choose month Birthday 
        