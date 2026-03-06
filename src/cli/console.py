"""
SK Framework — Interactive Console
Main REPL loop for interacting with the framework.
"""

import cmd
import sys
import asyncio
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.align import Align

from src.core.engine import SKEngine
from src.cli.ui.app import SKDashboard
from src.utils.logger import get_logger

log = get_logger("console")

# Initialize Rich Console
console = Console()

class SKConsole(cmd.Cmd):
    """
    Interactive command shell for SK Framework.
    """
    prompt = 'sk> '

    def __init__(self):
        super().__init__()
        self.engine = SKEngine()
        self.global_vars = {
            'TARGET': 'openai',
            'MODEL': 'gpt-4o',
            'TEMPERATURE': '0.7',
        }
        self.current_module = None
        self.module_instance = None
        self.module_vars = {}
        self._welcome_screen()

    def _welcome_screen(self):
        """Display the Matrix-themed ASCII welcome screen."""
        banner_text = r"""
   _____ _  __  ______                                           _    
  / ____| |/ / |  ____|                                         | |   
 | (___ | ' /  | |__ _ __ __ _ _ __ ___   _____      _____  _ __| | __
  \___ \|  <   |  __| '__/ _` | '_ ` _ \ / _ \ \ /\ / / _ \| '__| |/ /
  ____) | . \  | |  | | | (_| | | | | | |  __/\ V  V / (_) | |  |   < 
 |_____/|_|\_\ |_|  |_|  \__,_|_| |_| |_|\___| \_/\_/ \___/|_|  |_|\_\
                                                                      
        """
        
        # Matrix-green style
        banner = Panel(
            Align.center(
                Text(banner_text, style="bold green") + 
                Text("\n[ Offensive Security Framework for AI ]", style="italic green")
            ),
            subtitle="[ v0.1.0-alpha ]",
            border_style="green",
            padding=(1, 2)
        )
        
        console.print(banner)
        console.print("\nType [bold cyan]help[/bold cyan] or [bold cyan]?[/bold cyan] to list commands.\n")

    # ─── Core Commands ───

    def do_help(self, arg):
        """List available commands with stylized output."""
        if not arg:
            table = Table(title="SK Framework Commands", show_header=True, header_style="bold magenta")
            table.add_column("Command", style="cyan", no_wrap=True)
            table.add_column("Description", style="white")

            commands = {
                "help": "Show this help menu",
                "use": "Load an attack module (e.g., use prompt_injection/basic)",
                "set": "Set a global or module variable (e.g., set MODEL gpt-4o)",
                "show": "Display modules, options, or history",
                "run": "Execute the currently loaded module",
                "back": "Unload the current module",
                "exit": "Exit the console",
                "quit": "Exit the console"
            }

            for cmd_name, desc in commands.items():
                table.add_row(cmd_name, desc)
            
            console.print(table)
        else:
            # Fallback to standard cmd help for specific commands
            super().do_help(arg)

    def do_use(self, arg):
        """
        Load an exploit module.
        Usage: use <module_name>
        """
        if not arg:
            console.print("[bold red][!][/bold red] Usage: use <module_name>")
            return
        
        try:
            # Verify module exists
            module = self.engine.get_module(arg)
            self.current_module = arg
            self.module_instance = module
            self.module_vars = {}  # Reset module-specific variables
            
            # Extract display name from metadata for the prompt
            display_name = module.metadata.name.split('.')[-1]
            self.prompt = f'sk([bold red]{display_name}[/bold red])> '
            console.print(f"[bold green][+][/bold green] Loaded module: [bold cyan]{arg}[/bold cyan]")
        except ValueError as e:
            console.print(f"[bold red][-][/bold red] Error: {e}")

    def do_set(self, arg):
        """
        Set a variable.
        Usage: set <VARIABLE> <value>
        """
        parts = arg.split(maxsplit=1)
        if len(parts) != 2:
            console.print("[bold red][!][/bold red] Usage: set <VARIABLE> <value>")
            return
        
        var_name = parts[0].upper()
        var_value = parts[1]

        # Check if the variable belongs to the current module
        is_module_var = False
        if self.module_instance:
            module_opts = [opt.name.upper() for opt in self.module_instance.get_options()]
            if var_name in module_opts:
                self.module_vars[var_name] = var_value
                is_module_var = True
        
        # Fallback to global variables if not a module variable
        if not is_module_var:
            self.global_vars[var_name] = var_value
            console.print(f"[bold green][*][/bold green] {var_name} (global) => [bold cyan]{var_value}[/bold cyan]")
        else:
            console.print(f"[bold green][*][/bold green] {var_name} (module) => [bold cyan]{var_value}[/bold cyan]")

    def do_show(self, arg):
        """
        Display information.
        Usage: show <options|modules|history>
        """
        if arg == 'options':
            # 1. Show Global Options
            table = Table(title="Global Options", show_header=True, header_style="bold magenta")
            table.add_column("Option", style="cyan")
            table.add_column("Value", style="white")
            
            for k, v in self.global_vars.items():
                table.add_row(k, str(v))
            console.print(table)

            # 2. Show Module-Specific Options if a module is loaded
            if hasattr(self, 'module_instance') and self.module_instance:
                module_table = Table(title=f"Module Options: {self.current_module}", show_header=True, header_style="bold magenta")
                module_table.add_column("Option", style="cyan")
                module_table.add_column("Default", style="yellow")
                module_table.add_column("Value", style="white")
                module_table.add_column("Required", style="red")
                module_table.add_column("Description", style="white")

                for opt in self.module_instance.get_options():
                    # Prioritize module-specific value, then global, then default
                    current_val = self.module_vars.get(opt.name.upper())
                    if current_val is None:
                        current_val = self.global_vars.get(opt.name.upper())
                    if current_val is None:
                        current_val = opt.default
                    
                    module_table.add_row(
                        opt.name,
                        str(opt.default) if opt.default is not None else "",
                        str(current_val) if current_val is not None else "",
                        "yes" if opt.required else "no",
                        opt.description
                    )
                console.print(module_table)

        elif arg == 'modules':
            modules = self.engine.list_modules()
            table = Table(title="Available Modules", show_header=True, header_style="bold magenta")
            table.add_column("Name", style="cyan")
            table.add_column("Category", style="green")
            table.add_column("Difficulty", style="yellow")
            table.add_column("Description", style="white")

            for m in modules:
                table.add_row(m.name, m.category.value, m.difficulty.value, m.description)
            console.print(table)
        
        elif arg == 'history':
            console.print("[italic yellow][*] History feature coming soon...[/italic yellow]")
        
        else:
            console.print("[bold red][!][/bold red] Usage: show <options|modules|history>")

    def do_run(self, arg):
        """Execute the currently loaded module."""
        if not self.current_module:
            console.print("[bold red][-][/bold red] No module loaded. Use 'use <module>' first.")
            return

        # Resolve all module-specific options
        module_kwargs = {}
        if self.module_instance:
            for opt in self.module_instance.get_options():
                val = self.module_vars.get(opt.name.upper())
                if val is None:
                    val = self.global_vars.get(opt.name.upper())
                if val is not None:
                    module_kwargs[opt.name.lower()] = val

        target_provider = module_kwargs.get('target', self.global_vars.get('TARGET'))
        target_model = module_kwargs.get('model', self.global_vars.get('MODEL'))
        
        # Launch Textual Dashboard
        dashboard = SKDashboard(
            module_name=self.current_module,
            target=f"{target_provider}/{target_model}",
            engine_kwargs=module_kwargs
        )
        
        console.print(f"[bold yellow][*][/bold yellow] Launching cinematic dashboard for [bold cyan]{self.current_module}[/bold cyan]...")
        
        # Note: In Story 3.2 we will move the engine execution into a background task
        # within the dashboard. For now, we just launch the dashboard UI.
        dashboard.run()

    def do_back(self, arg):
        """Unload the current module."""
        self.current_module = None
        self.module_instance = None
        self.prompt = 'sk> '
        console.print("[bold yellow][*][/bold yellow] Module unloaded.")

    def do_exit(self, arg):
        """Exit the console."""
        console.print("[bold yellow]Shutting down SK Framework... Goodbye.[/bold yellow]")
        return True

    def do_quit(self, arg):
        """Exit the console."""
        return self.do_exit(arg)

    def emptyline(self):
        """Prevent repeating last command on empty line."""
        pass

    def default(self, line):
        """Handle unknown commands."""
        console.print(f"[bold red][!][/bold red] Unknown command: [italic]{line}[/italic]")

def main():
    """Main entry point for skconsole."""
    try:
        SKConsole().cmdloop()
    except KeyboardInterrupt:
        console.print("\n[bold yellow][*] Interrupted by user. Exiting...[/bold yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red][!] Critical error: {e}[/bold red]")
        log.exception("main_loop_error", error=str(e))
        sys.exit(1)

if __name__ == '__main__':
    main()
