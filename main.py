import serial
import time
import re
import sys
import os

def select_serial_port():
    print("\n--- SELECCIÓN DE PUERTO USB ---")
    posibles_puertos = [
        '/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2',
        '/dev/ttyACM0', '/dev/ttyACM1'
    ]
    
    encontrados = []
    for puerto in posibles_puertos:
        if os.path.exists(puerto):
            encontrados.append(puerto)
            
    if no encontrados:
        print("[-] No se detectó automáticamente ningún adaptador en las rutas comunes de Android.")
        print("[!] Verifica los permisos OTG o si necesitas usar termux-usb.")
        print("Puedes escribir manualmente la ruta de tu puerto (ej: /dev/ttyUSB0) o presionar Enter para salir.")
        rut = input(">> Ruta del puerto: ").strip()
        return rut if rut else None

    print("[+] Puertos detectados:")
    for i, p in enumerate(encontrados):
        print(f"  {i + 1}. {p}")
    print(f"  {len(encontrados) + 1}. Ingresar ruta manualmente")
    
    while True:
        opc = input("Selecciona una opción: ").strip()
        if opc.isdigit():
            idx = int(opc) - 1
            if 0 <= idx < len(encontrados):
                return encontrados[idx]
            elif idx == len(encontrados):
                rut = input(">> Ruta manual: ").strip()
                return rut if rut else None
        print("[-] Opción inválida.")

def select_vendor():
    print("\n--- TIPO DE EQUIPO ---")
    print("1. Cisco")
    print("2. MikroTik")
    print("3. Huawei")
    print("4. Genérico")
    
    while True:
        opc = input("Selecciona la marca del equipo: ").strip()
        if opc in ['1', '2', '3', '4']:
            return int(opc)
        print("[-] Opción inválida.")

def select_action():
    print("\n--- ACCIÓN A REALIZAR ---")
    print("1. Extraer Modelo")
    print("2. Extraer MAC Address")
    print("3. Extraer Ambos")
    print("4. Salir")
    
    while True:
        opc = input("Selecciona una acción: ").strip()
        if opc in ['1', '2', '3', '4']:
            return int(opc)
        print("[-] Opción inválida.")

def run_extraction(port, vendor, action):
    try:
        print(f"\n[*] Abriendo conexión serie en {port} a 9600 baudios...")
        ser = serial.Serial(
            port=port, baudrate=9600, bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2
        )
        
        if not ser.is_open:
            print("[-] No se pudo abrir el puerto.")
            return

        print("[+] Conectado. Despertando consola...")
        ser.write(b'\r\n\r\n')
        time.sleep(1)
        ser.read_all() # Limpiar
        
        # Configurar comandos según Vendor
        cmd_modelo = b'\r\n'
        cmd_mac = b'\r\n'
        regex_modelo = r''
        regex_mac = r'([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}|([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}'

        if vendor == 1: # Cisco
            cmd_modelo = b'show version\r\n'
            cmd_mac = b'show interfaces\r\n'
            regex_modelo = r'(?i)(?:cisco|model number|hardware)\s*:?\s*([A-Za-z0-9-]+)'
        elif vendor == 2: # MikroTik
            cmd_modelo = b'system resource print\r\n'
            cmd_mac = b'interface print\r\n'
            regex_modelo = r'(?i)board-name:\s*([A-Za-z0-9-]+)'
        elif vendor == 3: # Huawei
            cmd_modelo = b'display version\r\n'
            cmd_mac = b'display interface\r\n'
            regex_modelo = r'(?i)HUAWEI\s+([A-Za-z0-9-]+)\s+Routing'
        else:
            # Genérico
            cmd_modelo = b'show version\r\n'
            cmd_mac = b'show interfaces\r\n'
            regex_modelo = r'(?i)model\s*:?\s*([A-Za-z0-9-]+)'

        out_modelo = ""
        out_mac = ""

        # Extraer Modelo
        if action in [1, 3]:
            print("[*] Ejecutando comando de modelo...")
            ser.write(cmd_modelo)
            time.sleep(2)
            out_modelo = ser.read_all().decode('utf-8', errors='ignore')

        # Extraer MAC
        if action in [2, 3]:
            print("[*] Ejecutando comando de MAC...")
            ser.write(cmd_mac)
            time.sleep(2)
            out_mac = ser.read_all().decode('utf-8', errors='ignore')

        ser.close()

        # Mostrar Resultados
        print("\n" + "="*40)
        print(" RESULTADOS")
        print("="*40)
        if action in [1, 3]:
            m = re.search(regex_modelo, out_modelo)
            print(" Modelo : " + (m.group(1) if m else "No detectado (Intenta ajustar el regex)"))
        
        if action in [2, 3]:
            m = re.search(regex_mac, out_mac)
            print(" MAC    : " + (m.group(0) if m else "No detectada"))
        print("="*40 + "\n")

    except Exception as e:
        print(f"\n[-] Error de conexión o lectura: {e}")

if __name__ == "__main__":
    print("="*40)
    print(" AERO-AUTOMATIZACION - MODO INTERACTIVO")
    print("="*40)
    
    port = select_serial_port()
    if not port:
        print("[-] Saliendo...")
        sys.exit(0)
        
    vendor = select_vendor()
    
    while True:
        action = select_action()
        if action == 4:
            print("[-] Saliendo...")
            break
            
        run_extraction(port, vendor, action)
        
        cont = input("¿Deseas realizar otra acción en este mismo equipo? (s/n): ").strip().lower()
        if cont != 's':
            print("[-] Saliendo...")
            break
