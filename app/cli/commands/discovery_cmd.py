from rich.console import Console
from rich.prompt import Prompt
from app.discovery.usb import detect_usb_serial

console = Console()

def run_discovery():
    console.print("\n[bold cyan]--- DISCOVERY MODULE ---[/bold cyan]")
    console.print("1. Detect USB-Serial Devices")
    console.print("2. Network Discovery (ARP/SNMP)")
    
    choice = Prompt.ask("Select option", choices=["1", "2"])
    
    if choice == "1":
        console.print("[yellow]Buscando adaptadores USB...[/yellow]")
        devices = detect_usb_serial()
        if not devices:
            console.print("[red]⚠ No se encontraron dispositivos USB en rutas estándar.[/red]")
            return
            
        console.print("\n[bold green]USB DEVICE DETECTED[/bold green]")
        for d in devices:
            console.print(f"Port: {d['port']}")
            console.print(f"Manufacturer: {d.get('manufacturer', 'Unknown')}")
            console.print(f"Description: {d.get('description', 'Unknown')}")
            console.print("-" * 20)
    else:
        console.print("[yellow]Network discovery will be implemented in Phase 2.[/yellow]")
        Prompt.ask("Press Enter to return", default="")
