from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Device:
    hostname: str = ''
    vendor: str = ''
    model: str = ''
    ip_address: str = ''
    mac_address: str = ''
    serial_number: str = ''
    firmware: str = ''
    device_type: str = ''
    site: str = ''
    notes: str = ''
    id: Optional[int] = None
    last_backup: Optional[str] = None
    last_diagnostic: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
