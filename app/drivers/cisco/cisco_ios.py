from typing import Optional, List, Dict
from app.drivers.base import BaseDeviceDriver, DeviceInfo
from app.discovery.identification import DeviceIdentifier
import re

CISCO_COMMANDS = {
    'version': 'show version',
    'running_config': 'show running-config',
    'startup_config': 'show startup-config',
    'interfaces': 'show ip interface brief',
    'vlan': 'show vlan',
    'cdp': 'show cdp neighbors',
    'lldp': 'show lldp neighbors',
    'routes': 'show ip route',
    'inventory': 'show inventory',
    'processes_cpu': 'show processes cpu sorted 5sec',
    'memory': 'show processes memory sorted',
}


class CiscoIOSDriver(BaseDeviceDriver):
    """
    Driver for Cisco IOS / IOS-XE devices.
    Tested with: Catalyst, ISR, ASR families.
    """

    DRIVER_NAME = 'cisco_ios'
    VENDOR = 'Cisco'
    SUPPORTED_PLATFORMS = ['IOS', 'IOS-XE', 'Catalyst']

    def connect(self) -> bool:
        try:
            from netmiko import ConnectHandler
            self._connection = ConnectHandler(
                device_type=self.DRIVER_NAME,
                host=self.host,
                username=self.username,
                password=self.password,
                secret=self.enable_secret,
                port=self.port,
            )
            if self.enable_secret:
                self._connection.enable()
            return True
        except Exception as e:
            self._connection = None
            raise ConnectionError(f'Failed to connect to {self.host}: {e}') from e

    def disconnect(self):
        if self._connection:
            self._connection.disconnect()
            self._connection = None

    def execute_command(self, command: str) -> str:
        if not self._connection:
            raise RuntimeError('Not connected to device.')
        return self._connection.send_command(command)

    def get_version(self) -> str:
        return self.execute_command(CISCO_COMMANDS['version'])

    def get_running_config(self) -> str:
        return self.execute_command(CISCO_COMMANDS['running_config'])

    def get_startup_config(self) -> str:
        return self.execute_command(CISCO_COMMANDS['startup_config'])

    def get_interfaces(self) -> List[Dict]:
        output = self.execute_command(CISCO_COMMANDS['interfaces'])
        interfaces = []
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 6 and '.' in parts[0] or parts[0].startswith(('Gi', 'Fa', 'Te', 'Et', 'Vl')):
                interfaces.append({
                    'interface': parts[0],
                    'ip': parts[1] if len(parts) > 1 else '',
                    'status': parts[4] if len(parts) > 4 else '',
                    'protocol': parts[5] if len(parts) > 5 else '',
                })
        return interfaces

    def get_device_info(self) -> DeviceInfo:
        version_output = self.get_version()
        identifier = DeviceIdentifier()
        info = identifier.identify(version_output)
        return DeviceInfo(
            vendor='Cisco',
            model=info.get('model'),
            hostname=info.get('hostname'),
            serial_number=info.get('serial_number'),
            mac_address=info.get('mac_address'),
            ip_address=self.host,
            firmware=info.get('firmware'),
            os_version=info.get('firmware'),
            device_type='router_switch',
        )

    def get_health(self) -> Dict:
        cpu_out = self.execute_command(CISCO_COMMANDS['processes_cpu'])
        mem_out = self.execute_command(CISCO_COMMANDS['memory'])
        cpu_match = re.search(r'(\d+)%.*five seconds', cpu_out, re.IGNORECASE)
        mem_match = re.search(r'Processor.*?(\d+)\s+(\d+)', mem_out)
        return {
            'cpu': int(cpu_match.group(1)) if cpu_match else None,
            'memory_used': int(mem_match.group(1)) if mem_match else None,
            'memory_free': int(mem_match.group(2)) if mem_match else None,
        }
