import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt
import sys

from app.core.logging import logger

app = typer.Typer(no_args_is_help=False, invoke_without_command=True)
console = Console()

HEADER = """[bold blue]
╔════════════════════════════════════╗
║          NETAUTOLAB                ║
║     NETWORK AUTOMATION PLATFORM    ║
╚════════════════════════════════════╝
[/bold blue]"""

def interactive_menu():
    while True:
        console.clear()
        console.print(HEADER)
        console.print("\n[bold green]Menú Principal:[/bold green]")
        console.print("1. Detect Device (USB/Network)")
        console.print("2. Connect")
        console.print("3. Diagnostics")
        console.print("4. Backup")
        console.print("5. Configuration")
        console.print("6. Templates")
        console.print("7. Inventory")
        console.print("8. Reports")
        console.print("9. AI Assistant")
        console.print("10. Simulation")
        console.print("0. Exit")
        
        choice = IntPrompt.ask("\n[bold yellow]Selecciona una opción[/bold yellow]", choices=[str(i) for i in range(11)])
        
        if choice == 0:
            console.print("[bold red]Saliendo...[/bold red]")
            sys.exit(0)
        elif choice == 1:
            from app.cli.commands import discovery_cmd
            discovery_cmd.run_discovery()
        elif choice == 10:
            from app.cli.commands import simulate_cmd
            simulate_cmd.run_simulation()
        else:
            console.print("[bold yellow]⚠ Función en desarrollo (Fase posterior)[/bold yellow]")
            IntPrompt.ask("Presiona Enter para continuar", default=0, show_default=False)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    NETAUTOLAB - Plataforma Modular de Automatización de Redes.
    """
    if ctx.invoked_subcommand is None:
        interactive_menu()

@app.command("discover")
def discover():
    """Detect network or USB devices."""
    from app.cli.commands import discovery_cmd
    discovery_cmd.run_discovery()

@app.command("simulate")
def simulate():
    """Run simulation mode without hardware."""
    from app.cli.commands import simulate_cmd
    simulate_cmd.run_simulation()

if __name__ == "__main__":
    app()
