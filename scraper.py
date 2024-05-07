import asyncio, aiohttp, ssl
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
        links = []
        attachment_links = []  # new list for attachment links
        last_page_num = 0
        last_page_link = ""
        if page_body:
            posts = page_body.find_all("div", class_="post has-profile bg2")
            for post in posts:
                link_element = post.find("a", class_="postlink")
                if link_element:
                    links.append(link_element.get("href"))
                # new code to find attachment links
                attachments = post.find_all("dl", class_="file")
                for attachment in attachments:
                    attachment_link_element = attachment.find("a", class_="postlink")
                    if attachment_link_element:
                        attachment_links.append(attachment_link_element.get("href"))
            pagination = soup.find("div", class_="pagination")
            if pagination:
                page_links = pagination.find_all("a", class_="button")
                if page_links:
                    last_page_link_element = page_links[-2] # change from -1 to -2
                    last_page_link = last_page_link_element.get("href")
                    last_page_num = int(last_page_link_element.text)
        return last_page_num, last_page_link, links, attachment_links  # return attachment links as well

async def main():
    url = "https://sat-forum.net/viewtopic.php?t=424"
    base_url = "https://sat-forum.net/"
    page = "&start=" # co 10
    last_page_num, last_page_link, links, attachment_links = await get_content(url)
    print(last_page_num)
    for i in range(1, last_page_num):
        #print(i)
        url = base_url + last_page_link + page + str(i * 10)
        _, _, new_links, new_attachment_links = await get_content(url)  # get new_attachment_links
        #print(new_links)
        links.extend(new_links)
        attachment_links.extend(new_attachment_links)  # extend attachment_links with new_attachment_links

    full_links = [base_url + link.replace("./", "") if link.startswith("./") else link for link in links]
    full_attachment_links = [base_url + link.replace("./", "") if link.startswith("./") else link for link in attachment_links]  # create full_attachment_links

    for link in full_links:
        with open("links.txt", "a") as file:
            file.write(link + "\n")

    for link in full_attachment_links:  # print full_attachment_links
        with open("attachment_links.txt", "a") as file:
            file.write(link + "\n")

    common_links = set(full_links).intersection(full_attachment_links)

    for link in common_links:
        with open("common_links.txt", "a") as file:
            file.write(link + "\n")

asyncio.run(main())