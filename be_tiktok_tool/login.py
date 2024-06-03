import time
import json
import utils

class Login:
    
    def __init__(self, driver, insGPM, account_group) -> None:
        self.driver = self.runLogin(driver=driver, insGPM=insGPM, account_group=account_group)

    def extract_xpaths_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            xpath_list = data.get("xpath_list", [])
            xpaths = {key: value for item in xpath_list for key, value in item.items()}
        return xpaths

    def runLogin(self, driver, insGPM, account_group):
        print(account_group)
        email = account_group[0][0]
        password = account_group[0][1]
        print(email, password)
        xpaths = self.extract_xpaths_from_file(utils.XPATH_LOGIN_JSON)
        driver.get('https://www.tiktok.com/login/phone-or-email/email')
        xpath_input_username = xpaths['xpath_input_username']
        insGPM.input_(xpath_input_username, email)

        xpath_input_password = xpaths['xpath_input_password']
        insGPM.input_(xpath_input_password, password)
        
        xpath_login_btn = xpaths['xpath_submit_btn']
        insGPM.click(xpath_login_btn)

        time.sleep(30)
        insGPM.close()
