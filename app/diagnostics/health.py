from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class HealthCheck:
    name: str
    passed: bool
    value: str = ''
    message: str = ''


@dataclass
class HealthReport:
    device: str
    score: int = 0
    checks: List[HealthCheck] = field(default_factory=list)

    def calculate_score(self):
        if not self.checks:
            self.score = 0
            return
        passed = sum(1 for c in self.checks if c.passed)
        self.score = int((passed / len(self.checks)) * 100)


def evaluate_health(device_name: str, metrics: Dict) -> HealthReport:
    """
    Evaluate device health from raw metrics dict.
    Returns a HealthReport with a numeric score.
    """
    report = HealthReport(device=device_name)

    cpu = metrics.get('cpu')
    if cpu is not None:
        report.checks.append(HealthCheck(
            name='CPU Usage',
            passed=cpu < 85,
            value=f'{cpu}%',
            message='OK' if cpu < 85 else 'HIGH CPU usage detected'
        ))

    mem_free = metrics.get('memory_free')
    if mem_free is not None:
        mem_ok = mem_free > 10_000_000
        report.checks.append(HealthCheck(
            name='Memory',
            passed=mem_ok,
            value=f'{mem_free // 1024 // 1024} MB free',
            message='OK' if mem_ok else 'LOW memory'
        ))

    uptime = metrics.get('uptime')
    if uptime is not None:
        report.checks.append(HealthCheck(name='Uptime', passed=True, value=str(uptime)))

    report.calculate_score()
    return report
