from getDriver import DriverGPM
from getProxy import read_proxies
from getUserAgent import get_random_user_agent
import time
import threading
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getOTP import verifiedTiktok
import json
class SignupTiktok():
    def save_account_info(self, username, password):
        account_info = {
            "username": username,
            "password": password
        }
        # Đọc dữ liệu từ tệp JSON để xác định danh sách các tài khoản đã có
        existing_accounts = {"total": 0, "accounts": []}
        try:
            with open('accountTiktok.json', 'r') as json_file:
                existing_accounts = json.load(json_file)
        except FileNotFoundError:
            pass

        # Thêm tài khoản mới vào danh sách
        existing_accounts["accounts"].append(account_info)
        existing_accounts["total"] += 1

        # Ghi lại toàn bộ danh sách vào tệp JSON
        with open('accountTiktok.json', 'w') as json_file:
            json.dump(existing_accounts, json_file)

    def signup_tiktok(self, proxy, user_agent, email, password):  
        instance = DriverGPM(proxy, user_agent)
        driver = instance.driver  # Use the driver from the instance
        driver.get('https://www.tiktok.com/signup/phone-or-email/email')

        # Month
        month = random.randint(1, 12)
        xpath_MonthBirthday = '//*[@id="loginContainer"]/div[1]/form/div[2]/div[1]/div[1]'
        MonthBirthday_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_MonthBirthday))
        )
        MonthBirthday_btn.click()

        xpath_ChooseMonthBirthday = f'//*[@id="Month-options-item-{month}"]'
        ChooseMonthBirthday_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_ChooseMonthBirthday))
        )
        ChooseMonthBirthday_btn.click()

        # Day
        day = random.randint(1, 28)
        xpath_DayBirthday = '//*[@id="loginContainer"]/div[1]/form/div[2]/div[2]/div[1]'
        DayBirthday_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_DayBirthday))
        )
        DayBirthday_btn.click()
        xpath_ChooseDayBirthday = f'//*[@id="Day-options-item-{day}"]'
        ChooseDayBirthday_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_ChooseDayBirthday))
        )
        ChooseDayBirthday_btn.click()

        # Year
        year = random.randint(23, 43)
        xpath_YearBirthday = '//*[@id="loginContainer"]/div[1]/form/div[2]/div[3]/div[1]'
        YearBirthday_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_YearBirthday))
        )
        YearBirthday_btn.click()

        xpath_ChooseYearBirthday = f'//*[@id="Year-options-item-{year}"]'
        ChooseYearBirthday_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_ChooseYearBirthday))
        )
        ChooseYearBirthday_btn.click()

        # Input email
        xpath_input_email = '//*[@id="loginContainer"]/div[1]/form/div[5]/div/input'
        inputEmail = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_input_email))
        )
        inputEmail.send_keys(email)

        # Input password
        xpath_input_password = '//*[@id="loginContainer"]/div[1]/form/div[6]/div/input'
        inputPassword = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_input_password))
        )
        passwordTiktok = f'{password}@12'
        inputPassword.send_keys(passwordTiktok)

        #sencode button
        xpath_sendCodeBtn ='/html/body/div[1]/div/div[2]/div[1]/form/div[7]/div/button'
        sendCodeBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_sendCodeBtn))
        )
        sendCodeBtn.click()
        button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-e2e="send-code-button"]'))
    )
    
    # Click vào button
        button.click()
        time.sleep(25)

        verified_code = verifiedTiktok(email, password)
        print(verified_code)
        # Add any additional steps required to complete the signup process here
        xpath_inputOTP = '//*[@id="loginContainer"]/div[1]/form/div[7]/div/div/input'
        inputOTP = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_inputOTP))
        )
        inputOTP.send_keys(verified_code)

        agreebtn_xpath = '//*[@id="loginContainer"]/div[1]/form/div[8]/div/label/i'
        agreebtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, agreebtn_xpath))
        )
        agreebtn.click()
        nextbtn_xpath ='//*[@id="loginContainer"]/div[1]/form/button'
        nextbtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, nextbtn_xpath))
        )
        nextbtn.click()

        self.save_account_info(email,passwordTiktok)
        time.sleep(50)

def thread_function(proxy, user_agent, email, password):
    interaction = SignupTiktok()
    interaction.signup_tiktok(proxy, user_agent, email, password)

def read_emails_passwords(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    email_password_pairs = []
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) == 2:  # Ensure there are exactly two parts
            email_password_pairs.append((parts[0], parts[1]))
        else:
            print(f"Skipping invalid line: {line.strip()}")
    return email_password_pairs

def main():
    file_path_proxy = '../data/proxy.txt'  
    file_path_user_agent = '../data/user_agents.txt'
    file_path_emails = '../data/hotmail.txt'

    user_agent = get_random_user_agent(file_path_user_agent)

    list_proxies = read_proxies(file_path_proxy)
    email_password_pairs = read_emails_passwords(file_path_emails)

    n = int(input("Enter the number of threads per proxy: "))

    threads = []
    for proxy in list_proxies:
        for _ in range(n):
            if not email_password_pairs:
                break
            email, password = email_password_pairs.pop(0)
            thread = threading.Thread(target=thread_function, args=(proxy, user_agent, email, password))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

    print("All threads completed.")

if __name__ == "__main__":
    main()
