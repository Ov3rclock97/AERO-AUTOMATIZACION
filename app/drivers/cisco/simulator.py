"""
Cisco IOS Simulator - Para desarrollo y pruebas sin hardware real.
Imita respuestas de un dispositivo Cisco IOS.
"""
from typing import List, Dict
from app.drivers.base import BaseDeviceDriver, DeviceInfo


SIM_VERSION = """Cisco IOS Software, Version 15.2(4)M7
Processor board ID FTX1524N1RK
Model: Cisco2911
Cisco CISCO2911/K9 (revision 1.0) with 491520K/32768K bytes of memory.
Uptime: 2 days, 3 hours, 41 minutes"""

SIM_INTERFACES = """Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES NVRAM  up                    up
GigabitEthernet0/1     10.0.0.1        YES NVRAM  up                    up
GigabitEthernet0/2     unassigned      YES unset  administratively down down"""

SIM_CONFIG = """!
version 15.2
hostname CISCO-SIM-001
!
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
!
interface GigabitEthernet0/1
 ip address 10.0.0.1 255.255.255.0
!
end"""


class CiscoIOSSimulator(BaseDeviceDriver):
    """
    Simulates a Cisco IOS device for testing.
    This driver returns fake but realistic outputs.
    """

    DRIVER_NAME = 'cisco_ios_simulator'
    VENDOR = 'Cisco (Simulated)'
    SUPPORTED_PLATFORMS = ['SIMULATION']

    def connect(self) -> bool:
        self._connection = True
        return True

    def disconnect(self):
        self._connection = None

    def execute_command(self, command: str) -> str:
        responses = {
            'show version': SIM_VERSION,
            'show ip interface brief': SIM_INTERFACES,
            'show running-config': SIM_CONFIG,
            'show startup-config': SIM_CONFIG,
        }
        return responses.get(command.strip(), f'% Command "{command}" simulated - no output defined.')

    def get_version(self) -> str:
        return SIM_VERSION

    def get_running_config(self) -> str:
        return SIM_CONFIG

    def get_startup_config(self) -> str:
        return SIM_CONFIG

    def get_interfaces(self) -> List[Dict]:
        return [
            {'interface': 'GigabitEthernet0/0', 'ip': '192.168.1.1', 'status': 'up', 'protocol': 'up'},
            {'interface': 'GigabitEthernet0/1', 'ip': '10.0.0.1', 'status': 'up', 'protocol': 'up'},
            {'interface': 'GigabitEthernet0/2', 'ip': 'unassigned', 'status': 'down', 'protocol': 'down'},
        ]

    def get_device_info(self) -> DeviceInfo:
        return DeviceInfo(
            vendor='Cisco',
            model='Cisco2911',
            hostname='CISCO-SIM-001',
            serial_number='FTX1524N1RK',
            mac_address='00:1A:2B:3C:4D:5E',
            ip_address='192.168.1.1',
            firmware='15.2(4)M7',
            os_version='IOS 15.2',
            device_type='router',
        )

    def get_health(self) -> Dict:
        return {'cpu': 12, 'memory_used': 134217728, 'memory_free': 369098752}
