import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.discovery.usb import detect_usb_serial, _detect_linux
from app.discovery.identification import DeviceIdentifier


class TestUSBDetection:
    def test_detect_linux_no_devices(self):
        with patch('os.path.exists', return_value=False):
            result = _detect_linux()
            assert result == []

    def test_detect_linux_with_device(self):
        def mock_exists(path):
            return path == '/dev/ttyUSB0'
        with patch('os.path.exists', side_effect=mock_exists):
            result = _detect_linux()
            assert len(result) == 1
            assert result[0]['port'] == '/dev/ttyUSB0'

    def test_detect_usb_returns_list(self):
        with patch('os.path.exists', return_value=False):
            result = detect_usb_serial()
            assert isinstance(result, list)


class TestDeviceIdentifier:
    def setup_method(self):
        self.identifier = DeviceIdentifier()

    def test_identify_cisco(self):
        output = 'Cisco IOS Software, Version 15.2 Model: Cisco2911'
        result = self.identifier.identify(output)
        assert result['vendor'] == 'cisco'

    def test_identify_huawei(self):
        output = 'HUAWEI VRP Software Huawei S5700'
        result = self.identifier.identify(output)
        assert result['vendor'] == 'huawei'

    def test_identify_unknown(self):
        output = 'Some random output without vendor info'
        result = self.identifier.identify(output)
        assert result['vendor'] == 'generic'

    def test_detect_mac_address(self):
        output = 'Hardware Address: aa:bb:cc:dd:ee:ff'
        result = self.identifier.identify(output)
        assert result['mac_address'] == 'aa:bb:cc:dd:ee:ff'
