# Volumio Discord RPC

Python-based Discord Rich Presence client for Volumio music players.

---

## Description

This is a Python-based, self-hosted Discord Rich Presence (RPC) client that displays your currently playing music from Volumio in your Discord profile status. Similar to how Spotify integration works, this will show what you're listening to on your Volumio device.

This application runs on your PC/laptop (where Discord is installed) and connects to your Volumio device over your local network to fetch playback information.

### Features

- **Real-time playback display**: Shows currently playing song title, artist, and album in your Discord status
- **Multiple format support**: Handles various metadata formats including iHeartRadio stations with embedded metadata
- **Smart parsing**: Automatically parses artist and title information even when stations combine them into a single field
- **Auto-reconnect**: Automatically reconnects to Discord if connection is lost
- **Lightweight**: Minimal resource usage, checks Volumio API every 5 seconds
- **Not a Volumio Plugin**: This runs on your local PC/Laptop, not on the Volumio device itself. 

### Display Format

The Discord Rich Presence card will show:
- **Details**: Song title
- **State**: Artist - Album (or just Artist/Album if one is missing)
- **Large Image**: Volumio logo (customizable in Discord Developer Portal)


---

## Prerequisites

- Python 3.7 or higher
- Discord desktop/web client running on the same machine
- A Volumio device on your local network
- Discord Application Client ID (see Setup section)

---

## Installation

1. **Clone or download this repository**
```bash
   git clone https://github.com/yourusername/volumio-discord-rpc.git
   cd volumio-discord-rpc
```

2. **Install Python dependencies**
```bash
   pip install -r requirements.txt
```

3. **Configure the application**
   
   Edit `config.json` with your settings:
```json
   {
       "volumio_ip": "192.168.1.100",
       "discord_client_id": "YOUR_DISCORD_CLIENT_ID"
   }
```

   - `volumio_ip`: The IP address of your Volumio device
   - `discord_client_id`: Your Discord Application Client ID (see Discord Setup below)

---

## Discord Setup

To use Discord Rich Presence, you need to create a Discord application:

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "Volumio")
3. Copy the "Application ID" - this is your `discord_client_id`
4. (Optional) Go to "Rich Presence" → "Art Assets" to upload a Volumio logo:
   - Upload an image and name it `volumio.png` (this matches the code)
   - You can upload multiple images for different states if desired

---

## Running the Application

### Manual Run (Testing)
```bash
python volumio_discord.py
```

### Run as Background Service (Linux - Recommended)

1. **Create the systemd service file:**
```bash
   mkdir -p ~/.config/systemd/user
   nano ~/.config/systemd/user/volumio-rpc.service
```

2. **Add the following content** (replace paths with your actual paths):
```ini
   [Unit]
   Description=Volumio Discord RPC
   After=network.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/volumiorpc/volumio_rpc.py
   WorkingDirectory=/home/YOUR_USERNAME/volumiorpc
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=default.target
```

3. **Enable and start the service:**
```bash
   systemctl --user daemon-reload
   systemctl --user enable volumio-rpc
   systemctl --user start volumio-rpc
```

4. **Check status:**
```bash
   systemctl --user status volumio-rpc
```

5. **View logs:**
```bash
   journalctl --user -u volumio-rpc -f
```

**Useful commands:**
- Stop: `systemctl --user stop volumio-rpc`
- Restart: `systemctl --user restart volumio-rpc`
- Disable: `systemctl --user disable volumio-rpc`

**Keep running after logout:**
```bash
sudo loginctl enable-linger $USER
```

### Run as Background Service (Windows)

**Using Task Scheduler:**

1. Open Task Scheduler
2. Create Basic Task → Name it "VolumioRPC"
3. Trigger: "When I log on"
4. Action: "Start a program"
5. Program: `python` or `pythonw` (for no console window)
6. Arguments: `C:\path\to\volumio_rpc.py`
7. Start in: `C:\path\to\volumiorpc\`

### Run as Background Service (macOS)

1. **Create LaunchAgent file:**
```bash
   nano ~/Library/LaunchAgents/com.volumio.rpc.plist
```

2. **Add the following content:**
```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.volumio.rpc</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/python3</string>
           <string>/Users/YOUR_USERNAME/volumiorpc/volumio_rpc.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
   </dict>
   </plist>
```

3. **Load the service:**
```bash
   launchctl load ~/Library/LaunchAgents/com.volumio.rpc.plist
```

---

## Troubleshooting

### "Failed to connect to Discord"
- Ensure Discord desktop client is running on the same machine
- Try restarting Discord
- Check that your Application ID is correct in `config.json`

### "Connection refused" or "Timeout" errors
- Verify your Volumio IP address is correct
- Ensure your computer and Volumio are on the same network
- Check that Volumio's web interface is accessible at `http://VOLUMIO_IP`

### No status showing in Discord
- Make sure you've uploaded an image named `volumio` to your Discord application's Art Assets
- Verify your Discord Application ID is correct
- Check that the script is running without errors

### Artist shows as "None"
This is a known issue with some radio stations. The script handles this automatically and will only display the title in these cases.

---

## API/Services Used

This application connects to:

| Service | Description | Endpoint |
|---------|-------------|----------|
| Volumio API | Fetches current playback state | `http://VOLUMIO_IP/api/v1/getState` |
| Discord RPC | Updates Discord Rich Presence | Local IPC connection |

---

## Notes

- **Privacy**: All data stays local. The script only communicates between your PC, Volumio device, and Discord client.
- **Network requirement**: Your PC and Volumio must be on the same local network (or Volumio must be accessible via network).
- **Discord client required**: Unlike Spotify integration, this requires Discord to be running on the same machine as the script due to how Discord RPC works.
- **Not a Volumio plugin**: This runs on your PC/laptop, not on the Volumio device itself.

---

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have feature requests!

---

## Contact

If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Discord: Ravendos
- Discord: @Ravendos
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net

Or open an issue on Github. I will respond to it, and of course you, when I can. Remember, this is a hobby and there are other daily distractors that come first, like work, school and family.

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Acknowledgments

- [Volumio](https://volumio.com/) - The amazing music player platform
- [pypresence](https://github.com/qwertyquerty/pypresence) - Python Discord RPC library