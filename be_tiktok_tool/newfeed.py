import time
import json
import utils

class NewFeed:
    
    def __init__(self, driver, insGPM) -> None:
        self.driver = self.runNewfeed(driver=driver, insGPM=insGPM)

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
    
    def get_list_acctions(action_name, file_path):
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
    
    def likeVideo(self,ins,xpaths):
        xpath_like_btn = xpaths['xpath_like_icon']
        ins.click(xpath_like_btn)
    def follow(self,ins,xpaths):
        xpath_follow_btn = xpaths['xpath_follow_icon']
        ins.click(xpath_follow_btn)
    def share(self,ins,xpaths):
        xpath_share_btn = xpaths['xpath_share_icon']
        ins.click(xpath_share_btn)

    def runNewfeed(self, driver, insGPM):
        print(insGPM)
        list_acc = self.get_list_acctions('interactNewfeed', utils.CONFIG_ACCTION_TIKTOK)
        print(list_acc)
        print()
        xpaths = self.get_xpath_list(utils.XPATH_CONFIG_INTERACTION_JSON,'newfeed')
        driver.get('https://www.tiktok.com')

        self.likeVideo(driver, xpaths)
        time.sleep(20)
        insGPM.close()
    