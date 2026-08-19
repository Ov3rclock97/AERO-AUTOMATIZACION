from enum import Enum
from typing import Optional
from app.drivers.base import BaseDeviceDriver


class ConnectionMethod(Enum):
    SSH = 'ssh'
    TELNET = 'telnet'
    SERIAL = 'serial'
    SIMULATION = 'simulation'


class ConnectionManager:
    """
    Decides the best connection method and returns the appropriate driver.
    Flow: SSH -> Telnet -> Error.
    """

    def __init__(self, host: str, username: str, password: str,
                 enable_secret: str = '', port: Optional[int] = None,
                 vendor: str = 'cisco', simulate: bool = False):
        self.host = host
        self.username = username
        self.password = password
        self.enable_secret = enable_secret
        self.port = port
        self.vendor = vendor.lower()
        self.simulate = simulate
        self.method: Optional[ConnectionMethod] = None
        self._driver: Optional[BaseDeviceDriver] = None

    def connect(self) -> BaseDeviceDriver:
        if self.simulate:
            return self._connect_simulation()
        driver = self._try_ssh()
        if driver:
            self.method = ConnectionMethod.SSH
            return driver
        driver = self._try_telnet()
        if driver:
            self.method = ConnectionMethod.TELNET
            return driver
        raise ConnectionError(
            f'Could not connect to {self.host} via SSH or Telnet. '
            'Check credentials, firewall, and device status.'
        )

    def _connect_simulation(self) -> BaseDeviceDriver:
        from app.drivers.cisco.simulator import CiscoIOSSimulator
        driver = CiscoIOSSimulator(
            host=self.host, username=self.username, password=self.password
        )
        driver.connect()
        self.method = ConnectionMethod.SIMULATION
        self._driver = driver
        return driver

    def _try_ssh(self) -> Optional[BaseDeviceDriver]:
        try:
            port = self.port or 22
            driver = self._get_driver(port)
            driver.connect()
            self._driver = driver
            return driver
        except Exception:
            return None

    def _try_telnet(self) -> Optional[BaseDeviceDriver]:
        try:
            port = self.port or 23
            driver = self._get_driver(port)
            driver.connect()
            self._driver = driver
            return driver
        except Exception:
            return None

    def _get_driver(self, port: int) -> BaseDeviceDriver:
        if self.vendor in ('cisco', 'cisco_ios'):
            from app.drivers.cisco.cisco_ios import CiscoIOSDriver
            return CiscoIOSDriver(
                host=self.host, username=self.username,
                password=self.password,
                enable_secret=self.enable_secret,
                port=port
            )
        raise ValueError(f'No driver available for vendor: {self.vendor}. Use simulate=True for testing.')
