from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class DeviceInfo:
    vendor: str
    model: Optional[str]
    hostname: Optional[str]
    serial_number: Optional[str]
    mac_address: Optional[str]
    ip_address: Optional[str]
    firmware: Optional[str]
    os_version: Optional[str]
    device_type: str


class BaseDeviceDriver(ABC):
    """
    Abstract base class for all device drivers.
    All vendor-specific drivers must inherit from this class.
    """

    def __init__(self, host: str, username: str, password: str, enable_secret: str = '', port: int = 22):
        self.host = host
        self.username = username
        self.password = password
        self.enable_secret = enable_secret
        self.port = port
        self._connection = None

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the device. Returns True on success."""
        pass

    @abstractmethod
    def disconnect(self):
        """Close the connection."""
        pass

    @abstractmethod
    def execute_command(self, command: str) -> str:
        """Execute a single command and return output."""
        pass

    @abstractmethod
    def get_device_info(self) -> DeviceInfo:
        """Return device identification info."""
        pass

    @abstractmethod
    def get_running_config(self) -> str:
        """Return the running configuration as a string."""
        pass

    @abstractmethod
    def get_startup_config(self) -> str:
        """Return the startup configuration as a string."""
        pass

    @abstractmethod
    def get_interfaces(self) -> List[Dict]:
        """Return list of interfaces with their status."""
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Return the device version information."""
        pass

    def backup_config(self) -> str:
        """Backup the running configuration. Returns config string."""
        return self.get_running_config()

    def get_health(self) -> Dict:
        """Return basic health metrics. Override in subclasses."""
        return {
            'cpu': None,
            'memory': None,
            'uptime': None,
            'temperature': None,
        }

    def is_connected(self) -> bool:
        return self._connection is not None
