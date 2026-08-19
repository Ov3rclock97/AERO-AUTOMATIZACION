import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.drivers.cisco.simulator import CiscoIOSSimulator
from app.drivers.base import DeviceInfo


class TestCiscoSimulator:
    def setup_method(self):
        self.driver = CiscoIOSSimulator(host='192.168.1.1', username='admin', password='test')

    def test_connect_returns_true(self):
        assert self.driver.connect() is True

    def test_is_connected(self):
        self.driver.connect()
        assert self.driver.is_connected() is True

    def test_disconnect_clears_connection(self):
        self.driver.connect()
        self.driver.disconnect()
        assert self.driver.is_connected() is False

    def test_get_device_info_returns_dataclass(self):
        self.driver.connect()
        info = self.driver.get_device_info()
        assert isinstance(info, DeviceInfo)
        assert info.vendor == 'Cisco'
        assert info.model == 'Cisco2911'

    def test_get_interfaces_returns_list(self):
        self.driver.connect()
        interfaces = self.driver.get_interfaces()
        assert isinstance(interfaces, list)
        assert len(interfaces) == 3

    def test_execute_command_show_version(self):
        self.driver.connect()
        result = self.driver.execute_command('show version')
        assert 'Cisco' in result

    def test_execute_unknown_command(self):
        self.driver.connect()
        result = self.driver.execute_command('unknown_cmd')
        assert 'simulated' in result.lower()

    def test_get_health_returns_dict(self):
        self.driver.connect()
        health = self.driver.get_health()
        assert isinstance(health, dict)
        assert 'cpu' in health
