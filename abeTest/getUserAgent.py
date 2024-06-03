import random

def read_user_agents(file_path):
    try:
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file if line.strip()]
        return user_agents
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

def get_random_user_agent(file_path):
    user_agents = read_user_agents(file_path)
    if user_agents:
        return random.choice(user_agents)
    else:
        print("No user Agent found.")
        return None


# file_path = './data/user_agents.txt'  # Đường dẫn đầy đủ đến file proxy
# random_proxy = get_random_user_agent(file_path)
# print(random_proxy)
