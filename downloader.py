import requests, concurrent.futures, random, os

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def download_files(links, folder):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_link = {executor.submit(download_file, link, folder): link for link in links}
        for future in concurrent.futures.as_completed(future_to_link):
            link = future_to_link[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error with {link}, error: {e}")

def download_file(link, folder):
    filename = str(random.randint(1, 9999)) + ".m3u"
    with requests.get(link, headers={"User-Agent": user_agent}, stream=True) as response:
        response.raise_for_status()
        with open(f"{folder}/{filename}", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def main():
    files = [
        "common_links.txt",
        "links.txt",
        "attachment_links.txt"
    ]

    path = "downloads"
    os.makedirs(path, exist_ok=True)

    for file in files:
        with open(file, "r") as f:
            links = f.read().splitlines()
            download_files(links, path)
        
if __name__ == "__main__":
    main()