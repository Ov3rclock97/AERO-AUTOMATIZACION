import pytest
import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.inventory.database import InventoryDB
from app.inventory.models import Device


class TestInventoryDB:
    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db = InventoryDB(db_path=self.tmp.name)

    def teardown_method(self):
        try:
            os.unlink(self.tmp.name)
        except Exception:
            pass

    def test_add_device_returns_id(self):
        device = Device(hostname='SW-001', vendor='Cisco', model='C2960', ip_address='10.0.0.1')
        device_id = self.db.add_device(device)
        assert isinstance(device_id, int)
        assert device_id > 0

    def test_list_devices_empty(self):
        devices = self.db.list_devices()
        assert isinstance(devices, list)
        assert len(devices) == 0

    def test_add_and_list_device(self):
        device = Device(hostname='AP-001', vendor='Cisco', model='C9120', ip_address='10.0.0.5')
        self.db.add_device(device)
        devices = self.db.list_devices()
        assert len(devices) == 1
        assert devices[0].hostname == 'AP-001'
