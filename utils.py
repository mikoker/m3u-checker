import requests, concurrent.futures, chardet

class Utils:
    """
    Utility class for handling M3U playlists.
    """

    @staticmethod
    def detect_encoding(path):
        """
        Detect the encoding of a file.

        Args:
            file (file): The file object to detect the encoding of.

        Returns:
            str: The detected encoding of the file.
        """
        with open(path, 'rb') as file:
            result = chardet.detect(file.read())
        return result['encoding']

    @staticmethod
    def parse_m3u(file):
        """
        Parse an M3U file and extract the playlist information.

        Args:
            file (file): The file object representing the M3U file.

        Returns:
            list: A list of dictionaries representing each track in the playlist.
        """
        playlist = []
        for line in file:
            line = line.strip()
            if line.startswith("#EXTINF:"):
                duration, title = line.split("#EXTINF:")[1].split(",", 1)
                playlist.append({"duration": duration, "title": title})
            elif not line.startswith("#") and playlist:
                playlist[-1]["url"] = line
        return playlist

    @staticmethod
    def generate_m3u(playlist, file):
        """
        Generate an M3U file based on the provided playlist.

        Args:
            playlist (list): A list of dictionaries representing each track in the playlist.
            file (file): The file object to write the generated M3U file to.
        """
        file.write("#EXTM3U\n")
        for track in playlist:
            try:
                required_keys = ["duration", "title", "url"]
                if not all(key in track for key in required_keys):
                    raise ValueError("Missing required fields in track:", required_keys)
                extinf_line = f"#EXTINF:{track['duration']}"
                for key in ["tvg-id", "tvg-name", "tvg-logo", "group-title", "timeshift", "catchup"]:
                    if key in track:
                        extinf_line += f' {key}="{track[key]}"'
                extinf_line += f",{track['title']}"
                file.write(extinf_line + "\n")
                file.write(f"{track['url']}\n")
            except ValueError as e:
                print(f"Skipping invalid track: {e}")

    @staticmethod
    def extract_links(playlist):
        """
        Extract the URLs of the tracks from the playlist.

        Args:
            playlist (list): A list of dictionaries representing each track in the playlist.

        Returns:
            list: A list of URLs extracted from the playlist.
        """
        links = [track["url"] for track in playlist]
        return links

    @staticmethod
    def check_link(link):
        """
        Check if a given link is valid and returns it if it meets the criteria.

        Args:
            link (str): The link to be checked.

        Returns:
            str or None: The valid link if it meets the criteria, otherwise None.
        """
        if link.startswith("#") or link in ["", " ", "\n", None]:
            return None
        try:
            response = requests.get(link, timeout=30, headers={"User-Agent": "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'"})
            content_type = response.headers.get("Content-Type", "")
            if response.status_code in [200, 302, 303] and any(substring in content_type for substring in ['audio', 'video', 'mpeg', 'stream', 'x-mpegurl']):
                print(f"OK: {link}")
                return link
        except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects, requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.RequestException) as e:    
            print(f"Error with {link}, error: {e}")
            pass
        print(f"BAD: {link}")
        return None

    @staticmethod
    def check_links(links):
        """
        Check a list of links and return the valid ones.

        Args:
            links (list): A list of links to be checked.

        Returns:
            list: A list of valid links.
        """
        valid_links = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_link = {executor.submit(Utils.check_link, link): link for link in links}
            for future in concurrent.futures.as_completed(future_to_link):
                link = future.result()
                if link is not None:
                    valid_links.append(link)
        return valid_links
    
    @staticmethod
    def merge_playlists(*playlists):
        """
        Merge multiple playlists into a single playlist, removing duplicate tracks.

        Args:
            *playlists (list): Variable number of playlists to be merged.

        Returns:
            list: The merged playlist with duplicate tracks removed.
        """
        merged_playlist = []
        seen = set()
        for playlist in playlists:
            for track in playlist:
                if track['title'] == '#EXTM3U':
                    continue
                track_details = (track['duration'], track['title'], track['url'])
                if track_details not in seen:
                    seen.add(track_details)
                    merged_playlist.append(track)
        return merged_playlist