# NETAUTOLAB 🌐

> **Plataforma Modular de Automatización de Redes**
> Desarrollada para técnicos de campo. Modular, extensible y lista para producción.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://github.com/Ov3rclock97/AERO-AUTOMATIZACION/actions/workflows/tests.yml/badge.svg)

---

## ¿Qué es NETAUTOLAB?

NETAUTOLAB es una plataforma CLI de automatización de redes orientada a técnicos que necesitan detectar, diagnosticar, respaldar y configurar equipos de red en campo, desde un computador o directamente desde un celular Android con Termux.

## ✨ Características

- **Detección automática** de dispositivos USB-Serial y de red
- **Identificación** de fabricante, modelo, MAC, hostname y firmware
- **Conexión** vía SSH, Telnet o USB-Serial (consola)
- **Drivers** para Cisco IOS, Huawei, Ruckus y Cambium
- **Backups** con comparación de diferencias (diff)
- **Plantillas YAML/Jinja2** para generación de configuraciones
- **Diagnósticos** de salud de red con score numérico
- **Inventario local** SQLite
- **Simulador** para desarrollo sin hardware físico
- **Capa de IA** lista para conectar Ollama o cualquier API compatible
- **API REST** con FastAPI *(en desarrollo)*
- **Compatible con Termux** en Android

---

## 🚀 Instalación rápida

```bash
git clone https://github.com/Ov3rclock97/AERO-AUTOMATIZACION.git
cd AERO-AUTOMATIZACION

# Crear entorno virtual
python -m venv .venv

# Activar (Linux/Mac/Termux)
source .venv/bin/activate

# Activar (Windows)
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar y configurar variables de entorno
cp .env.example .env

# Ejecutar
python -m app.cli.main
```

---

## 📱 Instalación en Android (Termux)

```bash
# Dentro de Termux
pkg install git python
git clone https://github.com/Ov3rclock97/AERO-AUTOMATIZACION.git
cd AERO-AUTOMATIZACION
bash scripts/install-termux.sh
python app/cli/main.py
```

---

## 🖥️ Uso

### Menú interactivo
```bash
python -m app.cli.main
```

```
╔════════════════════════════════════╗
║          NETAUTOLAB                ║
║     NETWORK AUTOMATION PLATFORM    ║
╚════════════════════════════════════╝

1. Detect Device (USB/Network)
2. Connect
3. Diagnostics
4. Backup
5. Configuration
6. Templates
7. Inventory
8. Reports
9. AI Assistant
10. Simulation
0. Exit
```

### Comandos directos (CLI)
```bash
# Detectar dispositivos USB/red
python -m app.cli.main discover

# Modo simulación (sin hardware)
python -m app.cli.main simulate
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

Los tests están diseñados para correr **sin hardware físico** usando el simulador.

---

## 🏛️ Arquitectura

```
app/
├── cli/           → CLI con Typer + Rich
├── api/           → API REST con FastAPI
├── core/          → Configuración y logging
├── discovery/     → Detección USB y de red
├── connections/   → Gestión de conexiones SSH/Telnet/Serial
├── drivers/       → Drivers por fabricante (Cisco, Huawei, Ruckus, Cambium)
├── automation/    → Executor, Planner, Validator, Rollback
├── diagnostics/   → Health checks
├── backups/       → Backup y diff de configuraciones
├── templates/     → Motor de plantillas YAML/Jinja2
├── inventory/     → Base de datos local de dispositivos
├── reports/       → Generador de reportes
└── ai/            → Capa de análisis por IA (provider-agnostic)
```

---

## 🔧 Fabricantes Soportados

| Fabricante | Estado | Conexión |
|------------|--------|----------|
| Cisco IOS / IOS-XE | ✅ Implementado | SSH/Telnet/Serial |
| Huawei VRP | 🔧 En desarrollo | SSH/Telnet |
| Ruckus | 🔧 En desarrollo | SSH |
| Cambium | 🔧 En desarrollo | SSH/API |

---

## 🔒 Seguridad

- Nunca almacenes contraseñas en el código.
- Usa `.env` para credenciales (nunca subir `.env` a Git).
- Toda operación destructiva requiere confirmación explícita.
- Modo `--dry-run` disponible para ver cambios antes de aplicarlos.

---

## 📖 Documentación

Ver carpeta [`docs/`](docs/) para documentación detallada de cada módulo.

---

## 📜 Licencia

MIT License — Ver [LICENSE](LICENSE)
