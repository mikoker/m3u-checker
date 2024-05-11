import json, asyncio, aiohttp
from urllib.parse import urlparse, parse_qs
from tqdm import tqdm

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

async def fetch_data(url, username, password):
    url = f"{url}/player_api.php"
    headers = {
        "User-Agent": user_agent
    }
    try:
        async with aiohttp.ClientSession(headers=headers, connector=aiohttp.TCPConnector()) as session:
            async with session.get(url, params={"username": username, "password": password}) as response:
                return await response.json()
    except Exception as e:
        return None

async def main():
    file = input("Enter the input file name: ")
    output = input("Enter the output file name: ")
    with open(file, 'r') as f:
        data = json.load(f)

    sorted_links = {}
    with tqdm(total=len(data), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
        pbar.set_description("Processing links")
        for link in data:
            parsed_url = urlparse(link)
            host = "http://"+parsed_url.netloc
            params = {k: v[0] for k, v in parse_qs(parsed_url.query).items()}
            if host not in sorted_links:
                sorted_links[host] = []
            response = await fetch_data(host, params['username'], params['password'])
            if not response:
                continue
            user_info = response.get('user_info')
            if user_info["auth"] != 1:
                continue
            exp_date = user_info.get('exp_date')
            allowed_output_formats = user_info.get('allowed_output_formats')
            link_info = {**params}
            if exp_date:
                link_info['exp_date'] = exp_date
            if allowed_output_formats:
                link_info['allowed_output_formats'] = allowed_output_formats
            sorted_links[host].append(link_info)
            pbar.update()

    with open(output, 'w') as f:
        json.dump(sorted_links, f, indent=4)

if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())