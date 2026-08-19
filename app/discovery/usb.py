import os
import sys
from typing import List, Dict


def detect_usb_serial() -> List[Dict]:
    """
    Detect USB-Serial adapters on Linux/Android/Termux.
    Returns list of detected port info dicts.
    """
    found = []
    is_termux = 'com.termux' in os.environ.get('PREFIX', '')
    is_linux = sys.platform.startswith('linux')
    is_windows = sys.platform == 'win32'

    if is_windows:
        return _detect_windows()
    elif is_linux or is_termux:
        return _detect_linux()
    else:
        return []


def _detect_linux() -> List[Dict]:
    found = []
    candidates = []
    for prefix in ['/dev/ttyUSB', '/dev/ttyACM']:
        for i in range(5):
            candidates.append(f'{prefix}{i}')

    for path in candidates:
        if os.path.exists(path):
            found.append({
                'port': path,
                'manufacturer': 'Unknown',
                'description': 'USB-Serial Adapter',
            })
    return found


def _detect_windows() -> List[Dict]:
    """Windows detection using serial.tools.list_ports."""
    try:
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        usb_ports = [p for p in ports if 'USB' in (p.description or '').upper() or 'USB' in (p.device or '').upper()]
        return [{
            'port': p.device,
            'manufacturer': p.manufacturer or 'Unknown',
            'description': p.description or 'Unknown',
        } for p in usb_ports]
    except Exception as e:
        return []
