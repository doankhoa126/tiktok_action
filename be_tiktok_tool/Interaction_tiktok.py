import time
import json
import utils
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
class InteractionTikok:
    
    def __init__(self, driver, insGPM, account_group) -> None:
        self.driver = self.run(driver=driver, insGPM=insGPM, account_group=account_group)
    
    @staticmethod
    def get_list_acction(action_name, file_path):
        try:
            with open(file_path, "r") as json_file:
                config_data = json.load(json_file)
            
            for action in config_data.get("actions", []):
                if action.get("nameAcction") == action_name:
                    return action.get("listAcc", [])
            
            return None  

        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON.")
            return None 
    
    def extract_xpaths_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            xpath_list = data.get("xpath_list", [])
            xpaths = {key: value for item in xpath_list for key, value in item.items()}
        return xpaths
  

    def run(self, driver, insGPM, account_group):
        while True:
            try:
                xpaths_newfeed = self.extract_xpaths_from_file(utils.XPATH_NEWFEED_JSON)
                list_acc = self.get_list_acction('interactNewfeed', utils.CONFIG_ACCTION_TIKTOK)
                topic_data = list_acc[0]
                print(topic_data)

                  
                repeat = topic_data.get('repeat', '1')
                if repeat == '':
                    repeat = 1 
               
                email = account_group[0][0]
                password = account_group[0][1]
                xpaths = self.extract_xpaths_from_file(utils.XPATH_LOGIN_JSON)
                driver.get('https://www.tiktok.com/login/phone-or-email/email')
                time.sleep(2)
                try:
                    xpath_input_username = xpaths['xpath_input_username']
                    insGPM.input_(xpath_input_username, email)
                except: 
                    print('No found xpath input username')
                
                try:
                    xpath_input_username = '/html/body/div[1]/div/div/div[1]/form/div[1]/input'
                    insGPM.input_(xpath_input_username, email)
                except: 
                    print('No found xpath input username')
                
                try:
                    xpath_input_password = xpaths['xpath_input_password']
                    insGPM.input_(xpath_input_password, password)
                except: 
                    print('No found xpath input pass')

                try:
                    xpath_input_password = '/html/body/div[1]/div/div/div[1]/form/div[2]/div/input'
                    insGPM.input_(xpath_input_password, password)
                except: 
                    print('No found xpath input pass')
                
                try:
                    xpath_login_btn = xpaths['xpath_submit_btn']
                    insGPM.click(xpath_login_btn)
                except:
                    print('No found xpath login')
                    
                try:
                    xpath_login_btn = '/html/body/div[1]/div/div/div[1]/form/button'
                    insGPM.click(xpath_login_btn)
                except:
                    print('No found xpath login')
              
                try:
                    role_text = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[3]/span').text
                    print(role_text)

                    if role_text == 'Bạn truy cập dịch vụ của chúng tôi quá thường xuyên.' or role_text == 'Người dùng không tồn tại' or role_text == 'Rất tiếc, đã xảy ra lỗi, vui lòng thử lại sau':

                        insGPM.click(xpath_login_btn)  # Retry login
                        time.sleep(5)
                        print('click1')
                        if role_text == 'Bạn truy cập dịch vụ của chúng tôi quá thường xuyên.' or role_text == 'Người dùng không tồn tại' or role_text == 'Rất tiếc, đã xảy ra lỗi, vui lòng thử lại sau':
                            insGPM.click(xpath_login_btn)
                            time.sleep(3)
                            print('click2')
                            if role_text == 'Bạn truy cập dịch vụ của chúng tôi quá thường xuyên.' or role_text == 'Người dùng không tồn tại' or role_text == 'Rất tiếc, đã xảy ra lỗi, vui lòng thử lại sau':
                                insGPM.click(xpath_login_btn)
                                print('click3')  # R   # Retry again

                except Exception as e:
                    print(f"Exception while checking role text: {e}")

                print('Login successful')
                time.sleep(25)

                for i in range(int(repeat)):
                    print(f'Iteration {i + 1} of {repeat}')
                  
                    username_or_base = topic_data.get('usernameOrBase')
                    print('username_or_base', username_or_base)
                    if username_or_base:
                        values = username_or_base.splitlines()
                        if len(values) > 1:
                            random_value_topic = random.choice(values)
                            print(f"Selected topic: {random_value_topic}")
                    else:
                        random_value_topic = '1' 
                        print("The 'usernameOrBase' key is empty or not present.")

                    time.sleep(8)
                    try:
                        xpath_first_video = '/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]'
                        insGPM.click(xpath_first_video)
                    except:
                        print('No found xpath')
                    time.sleep(1)
                    try:
                        xpath_first_video2 = '/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div'
                        insGPM.click(xpath_first_video2)
                    except:
                        print('No found xpath')

                       
                    try:
                        xpath_first_video3 = '/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div[1]/div/div[1]/div[2]'
                        insGPM.click(xpath_first_video3)
                    except:
                        print('No found xpath')

                    time.sleep(3)
                    xpath_auto_down_btn = '/html/body/div[1]/div[2]/div[4]/div/div[1]/div[4]/div'
                    insGPM.click(xpath_auto_down_btn)
                    print('Clicked on video')

                    # Interact with the video
                    for item in list_acc:
                        numberOfLike = int(item.get('numberOflike', 0))
                        numberOffollow = int(item.get('numberOffollow', 0))

                        for _ in range(max(numberOfLike, numberOffollow)):
                            time.sleep(10)

                            if _ < numberOfLike:
                                print(f'Performing like action {_ + 1} of {numberOfLike}')
                                xpath_like_btn = '/html/body/div[1]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[1]/button[1]/span'
                                insGPM.click(xpath_like_btn)
                                time.sleep(5)
                                print('Waiting after like')

                            time.sleep(15)

                            if _ < numberOffollow:
                                print(f'Performing follow action {_ + 1} of {numberOffollow}')
                                xpath_follow_btn = '/html/body/div[1]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/button'
                                insGPM.click(xpath_follow_btn)
                                time.sleep(5)
                                print('Waiting after follow')

                        time.sleep(5)

                    # Close the video
                    xpath_close_video = '/html/body/div[1]/div[2]/div[4]/div/div[1]/button[1]'
                    insGPM.click(xpath_close_video)

                    # Check if random_value_topic is empty
                    if random_value_topic != '1':
                       
                        # Input topic and find
                        xpath_input_topic = '/html/body/div[1]/div[1]/div/div[2]/div/form/input'
                        insGPM.input_(xpath_input_topic, random_value_topic)

                        xpath_find_btn = '/html/body/div[1]/div[1]/div/div[2]/div/form/button'
                        insGPM.click(xpath_find_btn)
                        time.sleep(3)
                        try:
                            first_video_find = '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div[1]/div/div/a/div/div[1]'
                            insGPM.click(first_video_find)
                            print('Found topic')
                        except Exception as e:
                            print(e)
                        
                        try: 
                            first_video_find = '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div/div/div[3]/div[1]/div/div/a/div'
                            insGPM.click(first_video_find)
                            print('Found topic')
                            time.sleep(3)
                        except Exception as e:
                            print(e)
                        # Interact with the video again
                        for item in list_acc:
                            numberOfLike = int(item.get('numberOflike', 0))
                            numberOffollow = int(item.get('numberOffollow', 0))

                            for _ in range(max(numberOfLike, numberOffollow)):
                                time.sleep(10)

                                if _ < numberOfLike:
                                    print(f'Performing like action {_ + 1} of {numberOfLike}')
                                    xpath_like_btn = '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[1]/div[1]/button[1]/span'
                                    insGPM.click(xpath_like_btn)
                                    time.sleep(5)
                                    print('Waiting after like')

                                time.sleep(15)

                                if _ < numberOffollow:
                                    print(f'Performing follow action {_ + 1} of {numberOffollow}')
                                    xpath_follow_btn = '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[1]/div[1]/div/button'
                                    insGPM.click(xpath_follow_btn)
                                    time.sleep(5)
                                    print('Waiting after follow')

                        print('Success')
                        time.sleep(5)

                        # Go back to main page
                    driver.get('https://www.tiktok.com/')

                # Close the browser instance
                insGPM.close()
                break  # Exit the while loop if no exception occurred

            except Exception as e:
                print(f"Error: {e}")

                # Attempt to close the driver
                try:
                    driver.close()
                except Exception as quit_exception:
                    print(f"Error while quitting driver: {quit_exception}")

                # Wait and then retry initialization
                time.sleep(10)
                driver = self.initialize_driver()
                insGPM.driver = driver
                driver.close()

                break

                