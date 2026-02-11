import requests
import os

# CONFIGURATION
API_URL = "https://player-backend.restream.io/public/videos/4f71cc555c994494b193a6da77542d72?instant=true"
HEADERS = {
    "Referer": "https://player.restream.io/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def update_playlist():
    try:
        print("Fetching API...")
        response = requests.get(API_URL, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        # Get the best available stream
        stream_url = data.get('backupVideoUrlHls') or data.get('videoUrlHls')
        
        if not stream_url:
            print("Error: No stream URL found in API response.")
            return

        print(f"Got Signed URL: {stream_url[:50]}...")

        # Create the M3U8 Content
        # We create a 'Master Playlist' that points to the Cloudflare URL
        m3u8_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720
{stream_url}"""

        # Save to file
        with open("stream.m3u8", "w") as f:
            f.write(m3u8_content)
        
        print("stream.m3u8 updated successfully.")

    except Exception as e:
        print(f"Failed to update: {e}")
        exit(1)

if __name__ == "__main__":
    update_playlist()
