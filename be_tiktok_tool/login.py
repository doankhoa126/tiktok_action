import time
import json
import utils
from PyQt6.QtCore import QObject, pyqtSignal

class Login(QObject):
    update_status_signal = pyqtSignal(int, str)
    def __init__(self, driver, insGPM, account_group) -> None:
        self.driver = self.runLogin(driver=driver, insGPM=insGPM, account_group=account_group)

    def get_xpath_list(file_path, interaction_name):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for interaction in data:
                    if interaction["name_interaction"] == interaction_name:
                        return interaction["xpath_list"]
                return None
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return None
    def runLogin(self, driver, insGPM, account_group):
      
        email = account_group[0][0]
        password = account_group[0][1]
        
        xpaths = self.get_xpath_list(utils.XPATH_LOGIN_JSON,'login')
        driver.get('https://www.tiktok.com/login/phone-or-email/email')
        self.update_status_signal.emit(account_group[0][2], "Login started")  # Assuming account_group contains index as third element
        exit()
        try:
            try:
                xpath_input_username = xpaths['xpath_input_username']
                insGPM.input_(xpath_input_username, email)
            except Exception as e:
                print('Error',e)
            
            try:
                xpath_input_username = '/html/body/div[1]/div/div/div[1]/form/div[1]/input'
                insGPM.input_(xpath_input_username, email)
            except Exception as e:
                print('Error',e)

        except:
            print('Lỗi nhập username')

        try:
            try:
                xpath_input_password = xpaths['xpath_input_password']
                insGPM.input_(xpath_input_password, password)
            except Exception as e:
                print('Error',e)
            
            try:
                xpath_input_password = '/html/body/div[1]/div/div/div[1]/form/div[2]/div/input'
                insGPM.input_(xpath_input_password, password)
            except Exception as e:
                print('Error',e)
        except:
            print('Lỗi nhập password')
        
        try:
            try:
                xpath_login_btn = xpaths['xpath_submit_btn']
                insGPM.click(xpath_login_btn)
            except Exception as e:
                print('Error',e)
            
            try:
                xpath_login_btn = '/html/body/div[1]/div/div/div[1]/form/button'
                insGPM.click(xpath_login_btn)
            except Exception as e:
                print('Error',e)
        except:
            print('Lỗi nhấn nút login')

        time.sleep(20)

        print('login successful')