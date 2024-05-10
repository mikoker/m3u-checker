#! /usr/bin/env python3
import asyncio, aiohttp, json
from tqdm import tqdm
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
        links = [a["href"] for a in soup.select("a.postlink")]
        return links

async def check_if_m3u(link):
    async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector(ssl=False)) as session:
        try:
            async with session.get(link) as response:
                content_type = response.headers.get("Content-Type", "")
                if not content_type == "application/octet-stream":
                    return False
                return link
        except Exception as e:
            print(f"Cannot connect to host {link}")
            return False

async def main():
    filename = input("Enter the file name: ")
    topic_url = "https://www.satworld-forum.com/viewtopic.php?t=8&start=70"
    links = await get_content(topic_url)
    m3u_links = []
    bad_m3u_links = []
    with tqdm(total=len(links), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        for link in links:
            if await check_if_m3u(link):
                m3u_links.append(link)
                pbar.set_description(f"Working: {len(m3u_links)}, Bad: {len(bad_m3u_links)}, Total: {len(links)}")
                pbar.update()
                tqdm.write(f"OK: {link}")
            else:
                bad_m3u_links.append(link)
                pbar.set_description(f"Working: {len(m3u_links)}, Bad: {len(bad_m3u_links)}, Total: {len(links)}")
                pbar.update()
                tqdm.write(f"BAD: {link}")
    if not m3u_links:
        return print("No m3u links found.")
    print(m3u_links)
    with open(filename, "w") as f:
        json.dump(m3u_links, f, indent=4)
    print(f"Saved {len(m3u_links)} links to {filename}")

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())