"""
SK Framework — Command Line Interface
Usage: sk <command> [options]

Commands:
    sk modules list              List all available attack modules
    sk modules info <name>       Show details about a module
    sk attack <module>           Run an attack module
    sk lab list                  List available labs
    sk lab start <name>          Start an interactive lab
    sk ctf list                  List CTF challenges
    sk ctf start <name>          Start a CTF challenge
    sk serve                     Start the API + web UI server
    sk history                   Show attack history
    sk info                      Show framework info and config
"""

import asyncio
import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

console = Console()


# ─── Async helper ───
def run_async(coro):
    """Run an async function from sync click context."""
    return asyncio.run(coro)


# ─── Root CLI Group ───
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option("0.1.0", prog_name="SK Framework")
def sk():
    """
    SK Framework — AI Security Testing & Training

    An open-source offensive security framework for AI systems.
    """
    pass


# ─────────────────────────────────
# MODULES
# ─────────────────────────────────

@sk.group()
def modules():
    """List and inspect attack modules."""
    pass


@modules.command("list")
def modules_list():
    """List all available attack modules."""
    from src.core.engine import SKEngine

    engine = SKEngine()
    module_list = engine.list_modules()

    if not module_list:
        rprint("[red]No modules found.[/red]")
        return

    table = Table(title="[bold cyan]SK Framework — Attack Modules[/bold cyan]", show_lines=True)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Display Name", style="white")
    table.add_column("Category", style="yellow")
    table.add_column("Difficulty", style="green")
    table.add_column("OWASP", style="magenta")
    table.add_column("Version", style="dim")

    for m in module_list:
        table.add_row(
            m.name,
            m.display_name,
            m.category.value,
            m.difficulty.value,
            m.owasp_mapping or "—",
            m.version,
        )

    console.print(table)


@modules.command("info")
@click.argument("name")
def modules_info(name: str):
    """Show detailed info about a specific module."""
    from src.core.engine import SKEngine

    engine = SKEngine()
    try:
        module = engine.get_module(name)
        m = module.metadata

        console.print(Panel(
            f"[bold cyan]{m.display_name}[/bold cyan]\n"
            f"[dim]v{m.version} by {m.author}[/dim]\n\n"
            f"[white]{m.description}[/white]\n\n"
            f"Category:  [yellow]{m.category.value}[/yellow]\n"
            f"Difficulty: [green]{m.difficulty.value}[/green]\n"
            f"OWASP:     [magenta]{m.owasp_mapping or 'N/A'}[/magenta]\n"
            f"Tags:      {', '.join(m.tags)}\n\n"
            f"[dim]Payloads available: {len(module.get_payloads())}[/dim]",
            title=f"[bold]Module: {m.name}[/bold]",
            border_style="cyan",
        ))
    except ValueError as e:
        rprint(f"[red]{e}[/red]")


# ─────────────────────────────────
# ATTACK
# ─────────────────────────────────

@sk.command()
@click.argument("module_name")
@click.option("--target", "-t", default=None, help="LLM provider (openai, anthropic, google)")
@click.option("--model", "-m", default=None, help="Model name (e.g. gpt-4o)")
@click.option("--payload", "-p", default=None, help="Specific payload to use (None = auto)")
@click.option("--system-prompt", "-s", default=None, help="Target system prompt")
@click.option("--save/--no-save", default=True, help="Save result to session history")
def attack(module_name: str, target: str, model: str, payload: str, system_prompt: str, save: bool):
    """Run an attack module against a target LLM."""
    from src.core.engine import SKEngine
    from src.core.session import SessionManager

    async def _run():
        engine = SKEngine()

        console.print(Panel(
            f"[cyan]Module:[/cyan]   {module_name}\n"
            f"[cyan]Target:[/cyan]   {target or 'default'}\n"
            f"[cyan]Model:[/cyan]    {model or 'default'}\n"
            f"[cyan]Payload:[/cyan]  {'specified' if payload else 'auto (full sweep)'}",
            title="[bold yellow]⚔️  Attack Starting[/bold yellow]",
            border_style="yellow",
        ))

        result = await engine.run_module(
            module_name=module_name,
            target_provider=target,
            target_model=model,
            payload=payload,
            system_prompt=system_prompt,
        )

        # Display result
        score = result.score
        color = {"success": "green", "partial": "yellow", "failure": "red", "unknown": "dim"}.get(
            score.result.value, "white"
        )

        console.print(Panel(
            f"[bold {color}]Result: {score.result.value.upper()}[/bold {color}]\n"
            f"Confidence: {score.confidence:.0%}  |  Score: {score.score:.2f}\n\n"
            f"[dim]Signals:[/dim]\n" + "\n".join(f"  • {s}" for s in score.signals) + "\n\n"
            f"[dim]Details:[/dim] {score.details}\n\n"
            f"[dim]Technique:[/dim] {result.metadata.get('technique', 'N/A')}\n"
            f"[dim]Latency:[/dim]  {result.metadata.get('latency_ms', 'N/A')} ms\n\n"
            f"[dim]─── Response Preview ───[/dim]\n"
            f"{result.response[:500]}{'...' if len(result.response) > 500 else ''}",
            title=f"[bold]Attack Result — {module_name}[/bold]",
            border_style=color,
        ))

        # Save to session history
        if save:
            session_mgr = SessionManager()
            session_id = session_mgr.save(result)
            rprint(f"[dim]Session saved: {session_id}[/dim]")

    run_async(_run())


# ─────────────────────────────────
# LAB
# ─────────────────────────────────

@sk.group()
def lab():
    """Interactive training labs."""
    pass


@lab.command("list")
def lab_list():
    """List all available labs."""
    labs = [
        ("owasp_ml_01", "Input Manipulation",        "beginner",     "ML01"),
        ("owasp_ml_02", "Data Poisoning",            "intermediate", "ML02"),
        ("owasp_ml_03", "Model Inversion",           "intermediate", "ML03"),
        ("owasp_ml_04", "Membership Inference",      "advanced",     "ML04"),
        ("owasp_ml_05", "Model Theft",               "intermediate", "ML05"),
        ("owasp_ml_06", "AI Supply Chain",           "advanced",     "ML06"),
        ("owasp_ml_07", "Transfer Learning Attack",  "advanced",     "ML07"),
        ("owasp_ml_08", "Model Skewing",             "intermediate", "ML08"),
        ("owasp_ml_09", "Integrity Attacks",         "advanced",     "ML09"),
        ("owasp_ml_10", "Model Denial of Service",   "beginner",     "ML10"),
    ]

    table = Table(title="[bold cyan]SK Framework — Training Labs[/bold cyan]", show_lines=True)
    table.add_column("Lab ID", style="cyan", no_wrap=True)
    table.add_column("Topic", style="white")
    table.add_column("Difficulty", style="green")
    table.add_column("OWASP", style="magenta")

    for lab_id, topic, diff, owasp in labs:
        table.add_row(lab_id, topic, diff, owasp)

    console.print(table)
    rprint("\n[dim]Run a lab: sk lab start <lab_id>[/dim]")


@lab.command("start")
@click.argument("lab_id")
def lab_start(lab_id: str):
    """Start an interactive training lab."""
    # MVP stub — labs will be fully implemented in next iteration
    console.print(Panel(
        f"[cyan]Lab:[/cyan] {lab_id}\n\n"
        f"[yellow]⚠️  This lab is currently a stub.[/yellow]\n"
        f"Labs are being built iteratively. Run [cyan]sk attack prompt_injection[/cyan] "
        f"to start hands-on AI security testing now.",
        title="[bold]🎓 Lab Runner[/bold]",
        border_style="cyan",
    ))


# ─────────────────────────────────
# CTF
# ─────────────────────────────────

@sk.group()
def ctf():
    """Capture The Flag challenges."""
    pass


@ctf.command("list")
def ctf_list():
    """List CTF challenges."""
    challenges = [
        ("prompt_escape_001", "Escape the Sandbox",       "beginner",     100),
        ("exfil_vault_001",   "Crack the Vault",          "intermediate", 250),
        ("jailbreak_pro_001", "Break the Chain",          "intermediate", 300),
        ("ghost_model_001",   "Ghost in the Machine",    "advanced",     500),
    ]

    table = Table(title="[bold cyan]SK Framework — CTF Challenges[/bold cyan]", show_lines=True)
    table.add_column("Challenge", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Difficulty", style="green")
    table.add_column("Points", style="yellow", justify="right")

    for cid, name, diff, pts in challenges:
        table.add_row(cid, name, diff, str(pts))

    console.print(table)
    rprint("\n[dim]Start a challenge: sk ctf start <challenge_id>[/dim]")


@ctf.command("start")
@click.argument("challenge_id")
def ctf_start(challenge_id: str):
    """Start a CTF challenge."""
    console.print(Panel(
        f"[cyan]Challenge:[/cyan] {challenge_id}\n\n"
        f"[yellow]⚠️  CTF engine is being built.[/yellow]\n"
        f"Use [cyan]sk attack[/cyan] commands to practice in the meantime.",
        title="[bold]🏴 CTF Challenge[/bold]",
        border_style="cyan",
    ))


# ─────────────────────────────────
# SERVE
# ─────────────────────────────────

@sk.command()
@click.option("--host", default="0.0.0.0", help="Host to bind")
@click.option("--port", "-p", default=8000, help="Port to listen on")
def serve(host: str, port: int):
    """Start the SK Framework API server."""
    import uvicorn
    from src.api.app import app

    console.print(Panel(
        f"[cyan]Starting SK Framework API[/cyan]\n\n"
        f"Host: {host}\n"
        f"Port: {port}\n\n"
        f"[dim]API:  http://{host}:{port}/api[/dim]\n"
        f"[dim]Docs: http://{host}:{port}/docs[/dim]",
        title="[bold green]🚀 Server Starting[/bold green]",
        border_style="green",
    ))

    uvicorn.run(app, host=host, port=port)


# ─────────────────────────────────
# HISTORY
# ─────────────────────────────────

@sk.command()
@click.option("--limit", "-n", default=10, help="Number of results to show")
@click.option("--module", "-m", default=None, help="Filter by module name")
def history(limit: int, module: str):
    """Show attack session history."""
    from src.core.session import SessionManager
    import json

    session_mgr = SessionManager()
    sessions = session_mgr.history(limit=limit, module=module)

    if not sessions:
        rprint("[dim]No sessions found.[/dim]")
        return

    table = Table(title="[bold cyan]Attack History[/bold cyan]", show_lines=True)
    table.add_column("ID", style="dim", no_wrap=True, max_width=12)
    table.add_column("Module", style="cyan")
    table.add_column("Target", style="white")
    table.add_column("Result", style="bold")
    table.add_column("Score", style="yellow", justify="right")
    table.add_column("Time", style="dim")

    color_map = {"success": "green", "partial": "yellow", "failure": "red", "unknown": "dim"}

    for s in sessions:
        color = color_map.get(s.result, "white")
        table.add_row(
            s.id[:12],
            s.module_name,
            f"{s.target_provider}/{s.target_model}",
            f"[{color}]{s.result.upper()}[/{color}]",
            f"{s.score:.2f}",
            str(s.created_at)[:19] if s.created_at else "—",
        )

    console.print(table)


# ─────────────────────────────────
# INFO
# ─────────────────────────────────

@sk.command()
def info():
    """Show framework configuration and status."""
    from src.core.config import config

    console.print(Panel(
        f"[bold cyan]SK Framework[/bold cyan] v0.1.0\n"
        f"[dim]by Script-Kiddies · SK Labs[/dim]\n\n"
        f"[white]Default Provider:[/white] {config.default_provider}\n"
        f"[white]Default Model:[/white]    {config.default_model}\n"
        f"[white]Dry Run:[/white]          {'ON' if config.dry_run else 'OFF'}\n"
        f"[white]Log Level:[/white]        {config.log.log_level}\n"
        f"[white]DB Path:[/white]          {config.db.db_path}\n\n"
        f"[white]Configured Providers:[/white]\n" +
        "\n".join(f"  {'✓' if config.has_provider(p) else '✗'} {p}" for p in ["openai", "anthropic", "google"]),
        title="[bold]ℹ️  SK Framework Info[/bold]",
        border_style="cyan",
    ))


# ─── Entry Point ───
if __name__ == "__main__":
    sk()
