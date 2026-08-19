import pytest
import sys
import os
from pathlib import Path
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backups.diff import config_diff, has_changes
from app.backups.manager import BackupManager


class TestDiff:
    def test_identical_configs_no_changes(self):
        config = 'hostname ROUTER\ninterface Gi0/0\n ip address 192.168.1.1 255.255.255.0'
        assert has_changes(config, config) is False

    def test_different_configs_has_changes(self):
        assert has_changes('hostname OLD', 'hostname NEW') is True

    def test_config_diff_returns_string(self):
        result = config_diff('hostname OLD', 'hostname NEW')
        assert isinstance(result, str)
        assert len(result) > 0

    def test_config_diff_empty_configs(self):
        result = config_diff('', '')
        assert result == ''


class TestBackupManager:
    def setup_method(self):
        self.tmpdir = tempfile.mkdtemp()
        self.mgr = BackupManager(backup_root=self.tmpdir)

    def test_save_creates_directory(self):
        path = self.mgr.save(
            vendor='Cisco', model='C2911', hostname='RTR-001',
            ip='10.0.0.1', running_config='hostname RTR-001'
        )
        assert path.exists()
        assert (path / 'running-config.txt').exists()
        assert (path / 'metadata.json').exists()

    def test_list_backups_empty(self):
        result = self.mgr.list_backups()
        assert isinstance(result, list)
