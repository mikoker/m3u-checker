import requests, concurrent.futures, os, json

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def download_file(link, filename, path):
    headers = {
        "User-Agent": user_agent
    }
    response = requests.get(link, headers=headers)
    with open(os.path.join(path, filename), "wb") as f:
        f.write(response.content)

def main():
    file = input("Enter the file name: ")
    with open(file, "r") as f:
        data = json.load(f)
    path = "downloads"
    os.makedirs(path, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for item in data:
            link = item["link"]
            filename = item["filename"]
            executor.submit(download_file, link, filename, path)
        
if __name__ == "__main__":
    main()