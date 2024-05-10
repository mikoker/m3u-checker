#! /usr/bin/env python3
from utils import Utils
import os

def main():
    """Check all m3u lists from folder."""
    path = "downloads"
    files = os.listdir(path)
    m3u_files = [file for file in files if file.endswith(".m3u")]
    not_m3u_files = [file for file in files if not file.endswith(".m3u")]
    for file in not_m3u_files:
        os.remove(os.path.join(path, file))
    valid_playlists = []
    print(m3u_files)
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
            os.remove(full_path)
            m3u_files.remove(file)
            continue
        valid_playlists.append(valid_playlist)
    print("All playlists checked.")
    if valid_playlists:
        print("Merging playlists...")
        merged_playlist = Utils.merge_playlists(*valid_playlists)
        with open(os.path.join(path, 'merged_playlist.m3u'), 'w', encoding="utf-8") as f:
            Utils.generate_m3u(merged_playlist, f)
        print(f"Generated merged playlist with {len(merged_playlist)} tracks")
if __name__ == "__main__":
    main()