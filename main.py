import serial
import time
import re
import sys
import os

def detect_serial_port():
    print("[*] Buscando adaptadores USB-Serial comunes en Android/Termux...")
    # Rutas comunes donde Android asigna los adaptadores USB a Serial
    posibles_puertos = [
        '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2',
        '/dev/ttyACM0', '/dev/ttyACM1'
    ]
    
    for puerto in posibles_puertos:
        if os.path.exists(puerto):
            print(f"[+] ¡Adaptador detectado en {puerto}!")
            return puerto
            
    print("[-] No se detectó ningún adaptador USB-Serial en las rutas estándar (/dev/ttyUSB0, etc).")
    print("[!] Es posible que necesites permisos de Termux o que tu dispositivo no esté reconociendo el cable OTG.")
    return None

def get_equipment_info(port):
    try:
        print(f"[*] Conectando al puerto {port} a 9600 baudios...")
        # Configuración por defecto de consola (9600 8N1)
        ser = serial.Serial(
            port=port,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2
        )
        
        if not ser.is_open:
            print("[-] No se pudo abrir el puerto.")
            return

        print("[+] Conexión establecida. Iniciando lectura...")
        
        # Enviar un par de 'Enters' para despertar la consola
        ser.write(b'\r\n\r\n')
        time.sleep(1)
        ser.read_all() # Limpiar buffer

        # Enviamos comando genérico de Cisco/Switch 'show version'
        # Dependiendo del equipo (MikroTik, Huawei), estos comandos cambiarán.
        print("[*] Obteniendo versión y modelo...")
        ser.write(b'show version\r\n')
        time.sleep(2)
        output = ser.read_all().decode('utf-8', errors='ignore')
        
        # Enviamos comando para MAC (Cisco: show interfaces, MikroTik: interface print, etc)
        ser.write(b'show interfaces\r\n')
        time.sleep(2)
        output_mac = ser.read_all().decode('utf-8', errors='ignore')
        
        ser.close()
        
        # --- Análisis Básico (Expresiones Regulares) ---
        
        # Modelo (Heurística genérica buscando "Model", "Hardware", o "Cisco")
        model = "Desconocido"
        model_match = re.search(r'(?i)(?:model number|hardware|cisco|hw type)\s*:?\s*([A-Za-z0-9-]+)', output)
        if model_match:
            model = model_match.group(1)
            
        # MAC Address (Heurística buscando formato xx:xx:xx:xx:xx:xx o xxxx.xxxx.xxxx)
        mac = "Desconocida"
        mac_match = re.search(r'(?i)([0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}[:-][0-9a-f]{2}|[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})', output_mac)
        if mac_match:
            mac = mac_match.group(1)

        print("\n" + "="*40)
        print(" RESUMEN DEL EQUIPO CONECTADO")
        print("="*40)
        print(f" Puerto Usado : {port}")
        print(f" Modelo Aprox : {model}")
        print(f" Dirección MAC: {mac}")
        print("="*40 + "\n")

    except Exception as e:
        print(f"[-] Error al interactuar con el puerto serie: {e}")

if __name__ == "__main__":
    print("=== AERO-AUTOMATIZACION ===")
    port = detect_serial_port()
    if port:
        get_equipment_info(port)
    else:
        print("[-] Abortando. Compruebe la conexión de su cable consola USB.")
