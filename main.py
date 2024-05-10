from utils import Utils

def main():
    options = """
    1. Check links in a playlist
    2. Merge playlists
    3. Exit
    """
    print(options)
    choice = int(input("> "))
    if choice not in range(1, 4):
        print("Invalid choice")
        return
    match choice:
        case 1:
            path = input("Playlist: ")
            with open(path, 'r', encoding="utf-8") as file:
                playlist = Utils.parse_m3u(file)
            urls = [track['url'] for track in playlist]
            valid_urls = Utils.check_links(urls)
            valid_playlist = [track for track in playlist if track['url'] in valid_urls]
            print(f"Checked {len(urls)} links, {len(valid_urls)} are valid, {len(urls) - len(valid_urls)} are invalid.")
            if not valid_playlist:
                print("No valid links found")
                return
            with open('checked_'+path.split('/')[-1], 'w', encoding="utf-8") as file:
                print(f"Writing {len(valid_playlist)} valid links to {file.name}")
                Utils.generate_m3u(valid_playlist, file)
        case 2:
            playlists = []
            amount = int(input("How many playlists: "))
            for i in range(amount):
                playlist_file = input(f"Playlist {i+1}: ")
                with open(playlist_file, 'r', encoding="utf-8") as file:
                    playlist = Utils.parse_m3u(file)
                    playlists.append(playlist)
            output_file = input("Output file: ")
            merged_playlist = Utils.merge_playlists(*playlists)
            with open(output_file, 'w', encoding="utf-8") as file:
                Utils.generate_m3u(merged_playlist, file)
            print(f"Generated merged playlist with {len(merged_playlist)} tracks")
        case 3:
            print("Goodbye")
            return

if __name__ == "__main__":
    main()