import asyncio, aiohttp, json
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

async def get_content(url):
    async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=False)) as session:
        html = await fetch(url, session)
        soup = BeautifulSoup(html, "html.parser")
        page_body = soup.find("div", id="page-body")
        data = []
        if page_body:
            posts = page_body.select("div", class_="post has-profile")
            for post in posts:
                link_element = post.find("a", class_="postlink")
                if link_element:
                    data.append({"link": link_element.get("href"), "filename": link_element.text})
        pagination = soup.find("div", class_="pagination")
        last_page_num = 0
        last_page_link = ""
        if pagination:
            page_links = pagination.find_all("a", class_="button")
            if page_links:
                last_page_link_element = page_links[-2]
                last_page_link = last_page_link_element.get("href")
                last_page_num = int(last_page_link_element.text)
        return last_page_num, last_page_link, data

async def main():
    filename = input("Enter the file name: ")
    topic_url = "https://sat-forum.net/viewtopic.php?t=424"
    base_url = "https://sat-forum.net/"
    page = "&start="
    last_page_num, last_page_link, data = await get_content(topic_url)
    results = set()
    results.update({(base_url + item["link"].replace("./", ""), item["filename"]) for item in data})
    for i in range(1, last_page_num):
        url = topic_url + page + str(i*10)
        _, _, data = await get_content(url)
        results.update({(base_url + item["link"].replace("./", ""), item["filename"]) for item in data})

    with open(filename, "w") as f:
        json.dump([{"link": link, "filename": filename} for link, filename in results], f, indent=4)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())