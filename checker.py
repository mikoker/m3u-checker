from utils import Utils
import os

def main():
    """Check all m3u lists from folder."""
    path = "downloads"
    files = os.listdir(path)
    m3u_files = [file for file in files if file.endswith(".m3u")]
    for file in m3u_files:
        full_path = os.path.join(path, file)
        print(f"Checking {full_path}")
        with open(full_path, 'r', encoding="utf-8") as f:
            playlist = Utils.parse_m3u(f)
        urls = [track['url'] for track in playlist]
        valid_urls = Utils.check_links(urls)
        valid_playlist = [track for track in playlist if track['url'] in valid_urls]
        print(f"Checked {len(urls)} links, {len(valid_urls)} are valid, {len(urls) - len(valid_urls)} are invalid.")
        if not valid_playlist:
            print("No valid links found")
            return
        with open('checked_'+file, 'w', encoding="utf-8") as f:
            print(f"Writing {len(valid_playlist)} valid links to {f.name}")
            Utils.generate_m3u(valid_playlist, f)

if __name__ == "__main__":
    main()