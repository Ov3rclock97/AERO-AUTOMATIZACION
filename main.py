import serial
import serial.tools.list_ports
import time
import re
import sys

def detect_serial_port():
    print("[*] Buscando adaptadores USB-Serial conectados...")
    ports = list(serial.tools.list_ports.comports())
    
    usb_ports = [p for p in ports if 'USB' in p.description.upper() or 'USB' in p.device.upper()]
    
    if not usb_ports:
        print("[-] No se detectó ningún adaptador USB-Serial.")
        # Como fallback (útil en Termux con termux-usb o proot) listamos todos
        if ports:
            print("[!] Puertos disponibles encontrados:")
            for i, p in enumerate(ports):
                print(f"  {i+1}: {p.device} - {p.description}")
            return ports[0].device
        return None
        
    print("[+] Adaptadores USB encontrados:")
    for i, p in enumerate(usb_ports):
        print(f"  {i+1}: {p.device} - {p.description}")
        
    # Por defecto tomamos el primero
    return usb_ports[0].device

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
