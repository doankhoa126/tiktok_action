def read_proxies(file_path):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        return proxies
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

# # Ví dụ sử dụng:
file_path = 'C:/Dkhoa/TiktokTool/data/proxy.txt'  # Đường dẫn đầy đủ đến file proxy
proxies = read_proxies(file_path)
print(proxies)
