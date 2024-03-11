[//]: # (Copilot mi to generowal :3)
# m3u checker

This project is a Python application for managing M3U playlists. It provides functionalities to check the validity of links in a playlist, merge multiple playlists into one, and more.

## Installation
**Clone and install libraries**

```shell script
git clone https://github.com/mikoker/m3u-checker.git
cd m3u-checker
pip install -r requirements.txt
```

## Usage
The main entry point of the application is `main.py`. When you run this script, you will be presented with the following options:

1. Check links in a playlist
2. Merge playlists
3. Exit

#### Check Links in a Playlist
This option will ask you for a path to a playlist file. It will then check all the links in the playlist and generate a new playlist file containing only the valid links.

#### Merge Playlists
This option will ask you for the number of playlists you want to merge and the paths to the playlist files. It will then merge all the playlists into one and generate a new playlist file containing all the tracks from the input playlists.

### Utils Class
The Utils class provides several static methods for working with playlists:

- `detect_encoding(path: str) -> str:` Detects the encoding of a file.
- `parse_m3u(file: TextIO) -> List[Dict[str, str]]:` Parses an M3U file and returns a list of tracks.
- `check_link(link: str) -> str:` Check if a given link is valid and returns it if it meets the criteria.
- `check_links(links: List[str]) -> List[str]:` Checks a list of links and returns a list of the valid links.
- `generate_m3u(playlist: List[Dict[str, str]], file: TextIO) -> None:` Generates an M3U file from a list of tracks.
- `merge_playlists(*playlists: List[Dict[str, str]]) -> List[Dict[str, str]]:` Merges multiple playlists into one.
#### Example usage
```python
from utils import Utils

# Detect the encoding of a file
encoding = Utils.detect_encoding('path_to_your_file')
print(f'Encoding: {encoding}')

# Parse an M3U file
with open('path_to_your_m3u_file', 'r', encoding=encoding) as file:
    playlist = Utils.parse_m3u(file)
print(f'Playlist: {playlist}')

# Generate an M3U file
with open('path_to_your_output_file', 'w', encoding=encoding) as file:
    Utils.generate_m3u(playlist, file)

# Extract the URLs of the tracks from the playlist
links = Utils.extract_links(playlist)
print(f'Links: {links}')

# Check if a given link is valid and returns it if it meets the criteria.
valid_link = Utils.check_link('http://example.com')
print(f'Valid link: {valid_link}')

# Check a list of links and return the valid ones
valid_links = Utils.check_links(links)
print(f'Valid links: {valid_links}')

# Merge multiple playlists
merged_playlist = Utils.merge_playlists(playlist, playlist)
print(f'Merged playlist: {merged_playlist}')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

idc about it 