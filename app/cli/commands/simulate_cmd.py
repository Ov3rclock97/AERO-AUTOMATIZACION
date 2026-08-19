from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from app.drivers.cisco.simulator import CiscoIOSSimulator

console = Console()


def run_simulation():
    console.clear()
    console.print(Panel(
        "[bold yellow]SIMULATION MODE\n[white]Trabaja sin hardware real. Cisco IOS simulado.",
        title="[bold blue]NETAUTOLAB SIMULATOR",
        border_style="yellow"
    ))

    driver = CiscoIOSSimulator(host='192.168.1.1', username='admin', password='secret')
    driver.connect()
    info = driver.get_device_info()

    info_table = Table(title="[bold green]DEVICE DETECTED [SIMULATED]", show_header=False)
    info_table.add_column("Key", style="cyan")
    info_table.add_column("Value", style="white")
    info_table.add_row("Vendor", info.vendor)
    info_table.add_row("Model", info.model or 'N/A')
    info_table.add_row("Hostname", info.hostname or 'N/A')
    info_table.add_row("IP", info.ip_address or 'N/A')
    info_table.add_row("Serial", info.serial_number or 'N/A')
    info_table.add_row("MAC", info.mac_address or 'N/A')
    info_table.add_row("Firmware", info.firmware or 'N/A')
    console.print(info_table)

    while True:
        console.print("\n1. show version\n2. show ip interface brief\n3. show running-config\n4. Custom command\n0. Back")
        choice = Prompt.ask("Select action", choices=["0","1","2","3","4"])
        if choice == "0":
            break
        elif choice == "1":
            console.print(driver.execute_command("show version"))
        elif choice == "2":
            console.print(driver.execute_command("show ip interface brief"))
        elif choice == "3":
            console.print(driver.execute_command("show running-config"))
        elif choice == "4":
            cmd = Prompt.ask("Enter command")
            console.print(driver.execute_command(cmd))

    driver.disconnect()
