import sqlite3
from typing import List, Optional
from app.inventory.models import Device


class InventoryDB:
    """
    SQLite-based device inventory.
    Passwords are NEVER stored here.
    """

    def __init__(self, db_path: str = 'inventory.db'):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS devices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hostname TEXT,
                    vendor TEXT,
                    model TEXT,
                    ip_address TEXT,
                    mac_address TEXT,
                    serial_number TEXT,
                    firmware TEXT,
                    device_type TEXT,
                    site TEXT,
                    last_backup TEXT,
                    last_diagnostic TEXT,
                    created_at TEXT,
                    notes TEXT
                )
            ''')

    def add_device(self, device: Device) -> int:
        with self._conn() as conn:
            cursor = conn.execute('''
                INSERT INTO devices
                (hostname, vendor, model, ip_address, mac_address,
                 serial_number, firmware, device_type, site, created_at, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                device.hostname, device.vendor, device.model,
                device.ip_address, device.mac_address, device.serial_number,
                device.firmware, device.device_type, device.site,
                device.created_at, device.notes
            ))
            return cursor.lastrowid

    def list_devices(self) -> List[Device]:
        with self._conn() as conn:
            rows = conn.execute('SELECT * FROM devices').fetchall()
            return [self._row_to_device(r) for r in rows]

    def _row_to_device(self, row) -> Device:
        cols = [
            'id', 'hostname', 'vendor', 'model', 'ip_address', 'mac_address',
            'serial_number', 'firmware', 'device_type', 'site',
            'last_backup', 'last_diagnostic', 'created_at', 'notes'
        ]
        return Device(**dict(zip(cols, row)))
