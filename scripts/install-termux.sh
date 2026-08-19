#!/data/data/com.termux/files/usr/bin/bash
# NETAUTOLAB - Termux Installation Script (A prueba de fallos)
set -e

echo "======================================"
echo "  NETAUTOLAB - Termux Auto-Setup"
echo "======================================"

echo "[1/4] Actualizando paquetes base..."
pkg update -y && pkg upgrade -y

echo "[2/4] Instalando dependencias de red y criptografía nativas..."
# Instalamos la criptografía directamente desde Termux para evitar que pip intente compilar
pkg install -y python clang libffi openssl termux-api git rust binutils python-cryptography python-bcrypt python-pynacl

echo "[3/4] Limpiando requirements y configurando PIP..."
# Removemos cryptography de requirements.txt si existe, para que pip no lo descargue y use el de Termux
if [ -f "requirements.txt" ]; then
    sed -i '/cryptography/d' requirements.txt
    echo " -> Filtro de criptografía aplicado."
fi

# Instalamos el resto de la plataforma
python -m pip install typer rich pydantic pydantic-settings netmiko paramiko pyserial python-dotenv fastapi uvicorn scrapli pyyaml pytest

echo ""
echo "[4/4] ¡Instalación completada con éxito!"
echo "======================================"
echo "Para iniciar la consola ejecuta:"
echo "python -m app.cli.main"
echo "======================================"
