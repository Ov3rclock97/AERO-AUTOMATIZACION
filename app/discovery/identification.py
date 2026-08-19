import re
from typing import Optional, Dict


class DeviceIdentifier:
    """
    Identifies vendor, model and key attributes from device output.
    Supports Cisco, Huawei, Ruckus, Cambium.
    """

    VENDOR_PATTERNS = {
        'cisco': [r'Cisco', r'IOS', r'Catalyst', r'Aironet'],
        'huawei': [r'Huawei', r'VRP', r'HUAWEI'],
        'ruckus': [r'Ruckus', r'RUCKUS', r'ICX'],
        'cambium': [r'Cambium', r'ePMP', r'cnPilot'],
    }

    def identify(self, raw_output: str) -> Dict:
        vendor = self._detect_vendor(raw_output)
        model = self._detect_model(raw_output, vendor)
        hostname = self._detect_hostname(raw_output)
        serial = self._detect_serial(raw_output)
        mac = self._detect_mac(raw_output)
        firmware = self._detect_firmware(raw_output)

        return {
            'vendor': vendor,
            'model': model,
            'hostname': hostname,
            'serial_number': serial,
            'mac_address': mac,
            'firmware': firmware,
            'device_type': 'unknown',
        }

    def _detect_vendor(self, output: str) -> str:
        for vendor, patterns in self.VENDOR_PATTERNS.items():
            for p in patterns:
                if re.search(p, output, re.IGNORECASE):
                    return vendor
        return 'generic'

    def _detect_model(self, output: str, vendor: str) -> Optional[str]:
        patterns = [
            r'Model[\s:]+([A-Za-z0-9-]+)',
            r'Model Number[\s:]+([A-Za-z0-9-]+)',
            r'(?:Cisco|HUAWEI)\s+([A-Za-z0-9-]+)',
            r'Hardware[\s:]+([A-Za-z0-9-]+)',
        ]
        for p in patterns:
            m = re.search(p, output, re.IGNORECASE)
            if m:
                return m.group(1)
        return None

    def _detect_hostname(self, output: str) -> Optional[str]:
        m = re.search(r'^([A-Za-z0-9_-]+)(?:\s*#|\s*>)', output, re.MULTILINE)
        if m:
            return m.group(1)
        return None

    def _detect_serial(self, output: str) -> Optional[str]:
        m = re.search(r'Serial(?:\s+Number)?[\s:]+([A-Za-z0-9]+)', output, re.IGNORECASE)
        return m.group(1) if m else None

    def _detect_mac(self, output: str) -> Optional[str]:
        m = re.search(r'([0-9a-fA-F]{2}[:\-]){5}[0-9a-fA-F]{2}|([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}', output)
        return m.group(0) if m else None

    def _detect_firmware(self, output: str) -> Optional[str]:
        m = re.search(r'(?:Version|Firmware)[\s:]+([\d\.\(\)A-Za-z]+)', output, re.IGNORECASE)
        return m.group(1) if m else None
