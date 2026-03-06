"""
SK Framework — Interactive Console
Main REPL loop for interacting with the framework.
"""

import cmd
import sys
import asyncio
from typing import Any

try:
    import readline
    # Support for macOS (which uses libedit by default)
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^[[3~ ed-delete-next-char")
        readline.parse_and_bind("bind ^? ed-delete-prev-char")
    else:
        readline.parse_and_bind("tab: complete")
        readline.parse_and_bind('bind "^[[3~" delete-char')
except ImportError:
    pass

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.tree import Tree
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
        self._set_prompt()
        self._welcome_screen()

    def _set_prompt(self, module_name: str = None):
        """Helper to set the prompt with rendered rich markup."""
        if module_name:
            # Extract display name
            display_name = module_name.split('.')[-1]
            markup = f"sk([bold red]{display_name}[/bold red])> "
        else:
            markup = "sk> "
        
        # Render markup to ANSI string
        # We wrap in \001 and \002 for readline to correctly calculate prompt length
        with console.capture() as capture:
            console.print(markup, end="")
        ansi_text = capture.get()
        
        # Standard readline trick: wrap escape codes in \001 (RL_PROMPT_START_IGNORE) 
        # and \002 (RL_PROMPT_END_IGNORE) so they don't break cursor positioning.
        self.prompt = ansi_text.replace("\x1b", "\001\x1b").replace("m", "m\002")

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

    # ─── Tab Completion ───

    def complete_use(self, text, line, begidx, endidx):
        """Complete module names with hierarchy support."""
        modules = [m.name for m in self.engine.list_modules()]
        
        # If the user has already typed some parts (e.g., "injection.")
        if '.' in text:
            # We want to suggest the next level
            # e.g., for "injection." suggest "injection.direct", "injection.indirect"
            prefix = text.rsplit('.', 1)[0] + '.'
            suggestions = [m for m in modules if m.startswith(text)]
            return suggestions
        
        # Top level categories
        categories = sorted(list(set([m.split('.')[0] for m in modules])))
        if not text:
            return categories
        
        # Suggest categories that start with text
        suggestions = [c for c in categories if c.startswith(text)]
        # If there's only one category match, maybe they want the full module names?
        if len(suggestions) == 1:
            full_matches = [m for m in modules if m.startswith(text)]
            return full_matches
            
        return suggestions

    def complete_set(self, text, line, begidx, endidx):
        """Complete variable names."""
        options = set(self.global_vars.keys())
        if self.module_instance:
            for opt in self.module_instance.get_options():
                options.add(opt.name.upper())
        
        parts = line.split()
        # If we're at the first part after 'set'
        if len(parts) == 1 or (len(parts) == 2 and not line.endswith(' ')):
            return [opt for opt in options if opt.startswith(text.upper())]
        
        # If we're completing the value, we can suggest some common ones for TARGET
        if len(parts) >= 2 and parts[1].upper() == 'TARGET':
            targets = ["openai", "anthropic", "google", "ollama"]
            return [t for t in targets if t.startswith(text.lower())]
        
        return []

    def complete_show(self, text, line, begidx, endidx):
        """Complete show subcommands."""
        options = ["options", "modules", "history"]
        if not text:
            return options
        return [opt for opt in options if opt.startswith(text)]

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
            
            # Use helper to set the stylized prompt
            self._set_prompt(arg)
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
            tree = Tree("[bold green]Exploit Library[/bold green]")
            
            # Group modules by their dotted path hierarchy
            hierarchy = {}
            for m in modules:
                parts = m.name.split('.')
                curr = hierarchy
                for part in parts[:-1]:
                    if part not in curr:
                        curr[part] = {}
                    curr = curr[part]
                
                if '_techniques' not in curr:
                    curr['_techniques'] = []
                curr['_techniques'].append(m)

            def add_to_tree(branch, data):
                # Add sub-categories (folders)
                for key, val in sorted(data.items()):
                    if key == '_techniques':
                        continue
                    sub_branch = branch.add(f"[bold cyan]📁 {key.upper()}[/bold cyan]")
                    add_to_tree(sub_branch, val)
                
                # Add specific techniques (leaf nodes)
                if '_techniques' in data:
                    for m in sorted(data['_techniques'], key=lambda x: x.name):
                        leaf_name = m.name.split('.')[-1]
                        difficulty_color = "green" if m.difficulty.value == "beginner" else "yellow" if m.difficulty.value == "intermediate" else "red"
                        
                        # Technqiue header
                        tech_node = branch.add(
                            f"[bold white]⚔️  {m.display_name}[/bold white] "
                            f"[dim]({m.name})[/dim] "
                            f"[[{difficulty_color}]{m.difficulty.value.upper()}[/{difficulty_color}]]"
                        )
                        
                        # Detailed Description
                        if m.description:
                            tech_node.add(f"[italic dim]{m.description}[/italic dim]")
                        
                        if m.owasp_mapping:
                            tech_node.add(f"[dim]OWASP: [bold white]{m.owasp_mapping}[/bold white][/dim]")

            add_to_tree(tree, hierarchy)
            console.print(tree)
            console.print("\nType [bold cyan]use <canonical_name>[/bold cyan] to load (e.g., [italic]use injection.direct.basic[/italic]).\n")
        
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
        self._set_prompt()
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
