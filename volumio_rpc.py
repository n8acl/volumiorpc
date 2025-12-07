import json
import time
import requests
import re
from pypresence import Presence

def load_config():
    with open("config.json") as f:
        return json.load(f)

def main():
    cfg = load_config()

    vol_ip = cfg["volumio_ip"]
    client_id = cfg["discord_client_id"]

    rpc = Presence(client_id)

    print("Waiting for Discord...")
    while True:
        try:
            rpc.connect()
            print("Connected to Discord RPC.")
            break
        except Exception:
            time.sleep(3)

    last_title = None

    while True:
        try:
            state = requests.get(f"http://{vol_ip}/api/v1/getState", timeout=3).json()

            title = state.get("title", "")
            artist = state.get("artist", "")
            album = state.get("album", "")
            play_state = state.get("status", "")

            # Normalize artist and album - treat 'None' string as empty
            if artist in ["None", None, ""]:
                artist = ""
            if album in ["None", None, ""]:
                album = ""

            # Check if this is an iHeart station
            if "text=" in title:
                artist_match = re.search(r'^(.+?)\s*-\s*text=', title)
                title_match = re.search(r'text="([^"]+)"', title)
                
                parsed_artist = artist_match.group(1) if artist_match else None
                parsed_title = title_match.group(1) if title_match else None
                
                # If artist field is null/empty, use parsed artist
                if not artist and parsed_artist:
                    artist = parsed_artist
                
                # Combine for title display
                if parsed_artist and parsed_title:
                    title = f"{parsed_artist} - {parsed_title}"
            
            # If no artist and title contains " - ", try to parse it
            elif not artist and " - " in title:
                parts = title.split(" - ", 1)
                artist = parts[0]
                title = parts[1]

            # Build the state field: Artist - Album (if both exist)
            state_text = ""
            if artist and album:
                state_text = f"{artist} - {album}"
            elif artist:
                state_text = artist
            elif album:
                state_text = album

            if play_state == "play" and title:
                if title != last_title:
                    # Only include state if we have artist or album info
                    if state_text:
                        rpc.update(
                            details=title,
                            state=state_text,
                            large_image="volumio.png",
                            large_text="Volumio"
                        )
                    else:
                        rpc.update(
                            details=title,
                            large_image="volumio.png",
                            large_text="Volumio"
                        )
                    print(f"Now playing: {title} - {state_text}")
                    last_title = title
            else:
                if last_title:
                    print("Playback stopped.")
                rpc.clear()
                last_title = None

        except Exception:
            # connection errors, timeout, etc.
            pass

        time.sleep(5)

if __name__ == "__main__":
    main()