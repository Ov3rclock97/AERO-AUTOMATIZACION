# AERO-AUTOMATIZACION

Este proyecto permite conectar un dispositivo (como un celular con Termux) a un equipo de red a través de un cable consola (adaptador USB a Serial), y extraer de forma automática información valiosa como el modelo del equipo y su dirección MAC.

## Requisitos

- **Python 3**: Para ejecutar el script.
- **pyserial**: Librería de Python para interactuar con puertos seriales.
- **Adaptador OTG + Cable Serial**: Para conectar el celular al equipo de red.

## Instalación en Termux (Android)

1. **Instalar dependencias del sistema:**
   ```bash
   pkg update
   pkg install python
   pkg install clang libffi
   ```

2. **Permitir acceso a USB en Termux:**
   Dependiendo de la versión de Android, puede que necesites usar la API de Termux para obtener permisos sobre el dispositivo USB.
   ```bash
   pkg install termux-api
   ```

3. **Clonar/Descargar este repositorio:**
   ```bash
   cd ~/
   # Si lo copias manualmente al almacenamiento:
   # termux-setup-storage
   # cp -r /sdcard/REPOSITORIO\ GIT/AERO-AUTOMATIZACION ~/
   cd AERO-AUTOMATIZACION
   ```

4. **Instalar dependencias de Python:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Conecta el cable consola al adaptador USB a Serial.
2. Conecta el adaptador al puerto de tu celular usando un cable OTG.
3. Enciende o asegúrate de que el equipo de red (Router, Switch) esté encendido.
4. Ejecuta el script:
   ```bash
   python main.py
   ```

El script intentará detectar automáticamente el puerto USB, se conectará a 9600 baudios, ejecutará comandos de diagnóstico (tipo `show version` y `show interfaces`) y extraerá el Modelo y la dirección MAC usando expresiones regulares.

## Notas

*   Los comandos de extracción actuales están basados en una heurística general tipo Cisco. Si utilizas otros equipos (MikroTik, Huawei, Juniper), es probable que debas ajustar los comandos `ser.write(b'comando\r\n')` en `main.py`.
