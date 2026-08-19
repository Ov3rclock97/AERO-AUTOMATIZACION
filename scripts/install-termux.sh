#!/data/data/com.termux/files/usr/bin/bash
# NETAUTOLAB - Termux Installation Script
set -e
echo "======================================"
echo "  NETAUTOLAB - Termux Setup"
echo "======================================"
echo "[1/4] Updating packages..."
pkg update -y && pkg upgrade -y
echo "[2/4] Installing system dependencies..."
pkg install -y python clang libffi openssl termux-api git
echo "[3/4] Installing Python libraries..."
python -m pip install pyserial rich typer pydantic pydantic-settings python-dotenv pyyaml pytest
echo "[4/4] Setup complete!"
echo ""
echo "Run: python -m app.cli.main"
