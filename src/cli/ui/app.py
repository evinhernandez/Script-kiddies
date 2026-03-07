"""
SK Framework — Terminal Dashboard
Full-screen TUI for real-time attack monitoring using Textual.
"""

import random
import asyncio
import json
from typing import Any, Optional
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, RichLog, Label, Tree, LoadingIndicator, Input
from textual.binding import Binding
from textual.message import Message
from rich.tree import Tree as RichTree
from rich.panel import Panel
from rich.text import Text

from src.utils.llm_client import LLMClient, LLMRequest

HACKER_QUOTES = [
    "Hack the planet! — Hackers (1995)",
    "There is no spoon. — The Matrix (1999)",
    "Everything is a project. — Mr. Robot",
    "I'm in. — Every hacker movie ever",
    "Mess with the best, die like the rest. — Hackers (1995)",
    "Never send a human to do a machine's job. — Agent Smith",
    "The world is a very different place now. — Mr. Robot",
    "Control is an illusion. — Mr. Robot",
]

HACKER_STATUSES = [
    "BRUTE-FORCING NEURAL GATEWAY...",
    "BYPASSING CORPORATE FIREWALL...",
    "INJECTING MALICIOUS HEURISTICS...",
    "POISONING GRADIENT DESCENT...",
    "HIJACKING ATTENTION HEADS...",
    "EXTRACTING WEIGHT MATRICES...",
    "CORRUPTING EMBEDDING SPACE...",
    "SYNTHESIZING BYPASS TOKENS...",
    "DECRYPTING SYSTEM CONTEXT...",
    "RE-ROUTING LOGIC GATES...",
]

class EngineEvent(Message):
    """Base class for all engine-related events."""
    def __init__(self, data: dict = None):
        super().__init__()
        self.data = data or {}

class AttackFired(EngineEvent):
    """Sent when a payload is sent to the target."""
    pass

class TargetResponded(EngineEvent):
    """Sent when the target responds."""
    pass

class AttackComplete(EngineEvent):
    """Sent when the attack module finishes."""
    pass

class SKDashboard(App):
    """
    Main dashboard for SK Framework attacks.
    """
    CSS = """
    Screen {
        background: #000000;
    }

    #main-container {
        height: 100%;
        width: 100%;
    }

    .pane {
        border: solid #00FFFF;
        background: #000000;
        height: 100%;
        padding: 1;
    }

    .sub-pane {
        border: solid #333333;
        height: 50%;
        padding: 1;
    }

    #status-pane {
        width: 25%;
    }

    #center-stack {
        width: 45%;
    }

    #right-stack {
        width: 30%;
    }

    #brain-pane {
        border: solid #A020F0;
    }

    #education-pane {
        border: solid #FFD700;
    }

    .pane-title {
        text-align: center;
        background: #00FFFF;
        color: #000000;
        text-style: bold;
        margin-bottom: 1;
    }

    .brain-title {
        background: #A020F0;
        color: #FFFFFF;
    }

    .edu-title {
        background: #FFD700;
        color: #000000;
    }

    #pwnd-banner {
        background: #FF0000;
        color: #FFFFFF;
        text-align: center;
        text-style: bold;
        display: none;
        margin-top: 1;
        padding: 1;
        height: 5;
        border: double white;
    }

    #loading-container {
        height: 3;
        content-align: center middle;
    }

    #shell-container {
        display: none;
        height: 3;
        border: tall #00FF00;
        background: #002200;
        padding: 0 1;
    }

    #shell-input {
        background: #002200;
        border: none;
        color: #00FF00;
        width: 100%;
    }

    Tree {
        background: #000000;
        color: #00FFFF;
    }

    .zoomed {
        width: 100% !important;
        height: 100% !important;
    }

    .hidden {
        display: none !important;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit Dashboard"),
        Binding("esc", "quit", "Return to Console"),
        Binding("1", "focus_pane('status')", "Status"),
        Binding("2", "focus_pane('center')", "Brain/IO"),
        Binding("3", "focus_pane('right')", "Tree/Edu"),
        Binding("0", "reset_layout", "Reset View"),
    ]

    def __init__(self, module_name: str, target: str, engine_kwargs: dict = None):
        super().__init__()
        self.module_name = module_name
        self.target = target
        self.engine_kwargs = engine_kwargs or {}
        self.total_tokens = 0
        self.last_turn_node = None
        self.is_zoomed = False
        self.is_compromised = False
        self.winning_payload = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main-container"):
            with Horizontal():
                # LEFT: Status
                with Vertical(id="status-pane", classes="pane"):
                    yield Label("TARGET STATUS", classes="pane-title")
                    yield Static(f"[bold cyan]Module:[/bold cyan]\n{self.module_name}", id="lbl-module")
                    yield Static(f"\n[bold cyan]Target:[/bold cyan]\n{self.target}", id="lbl-target")
                    yield Static(f"\n[bold cyan]Tokens:[/bold cyan]\n{self.total_tokens}", id="lbl-tokens")
                    yield Static(f"\n[bold cyan]Latency:[/bold cyan]\n0ms", id="lbl-latency")
                    yield Static(f"\n[bold yellow]Last Payload:[/bold yellow]\n[dim]None[/dim]", id="lbl-payload")
                    
                    yield Static("", id="pwnd-banner")
                    yield Static(f"\n[bold green]Exploit / Secret:[/bold green]\n[dim]Waiting...[/dim]", id="lbl-secret")
                    
                    yield Static("\n[dim]Initializing...[/dim]", id="lbl-hacking")
                    with Container(id="loading-container"):
                        yield LoadingIndicator(id="loading-spinner")
                
                # CENTER: Logs & Brain
                with Vertical(id="center-stack"):
                    with Vertical(id="logs-pane", classes="pane sub-pane"):
                        yield Label("IO TRAFFIC (RAW)", classes="pane-title")
                        yield RichLog(id="agent-log", highlight=True, markup=True, wrap=True)
                    with Vertical(id="brain-pane", classes="pane sub-pane"):
                        yield Label("ATTACKER BRAIN (THOUGHTS)", classes="pane-title brain-title")
                        yield RichLog(id="brain-log", markup=True, wrap=True)
                
                # RIGHT: Tree & Education
                with Vertical(id="right-stack"):
                    with Vertical(id="threat-pane", classes="pane sub-pane"):
                        yield Label("ATTACK TREE", classes="pane-title")
                        yield Tree("Attack Root", id="threat-tree")
                    with Vertical(id="education-pane", classes="pane sub-pane"):
                        yield Label("EDUCATIONAL TRACING", classes="pane-title edu-title")
                        yield RichLog(id="edu-log", markup=True, wrap=True)
            
            with Horizontal(id="shell-container"):
                yield Label("[bold green]SESSION_SHELL $> [/bold green]")
                yield Input(placeholder="Send follow-up command to compromised model...", id="shell-input")
        yield Footer()

    def on_mount(self) -> None:
        self.log_to_pane("agent-log", f"[bold green]>>> I/O SUBSYSTEM ONLINE[/bold green]")
        self.log_to_pane("brain-log", f"[bold green]>>> COGNITIVE ENGINE ONLINE[/bold green]")
        
        # Setup initial tree
        tree = self.query_one("#threat-tree", Tree)
        tree.root.expand()
        
        # Start the engine in a background worker
        self.run_worker(self.execute_engine())
        # Start the hacker status rotator
        self.run_worker(self.rotate_status())

    async def rotate_status(self):
        """Rotate through hacker status messages while engine is running."""
        lbl = self.query_one("#lbl-hacking", Static)
        while True:
            if "COMPLETED" in str(lbl.content) or "CRASH" in str(lbl.content):
                break
            new_status = random.choice(HACKER_STATUSES)
            lbl.update(f"\n[blink bold yellow]{new_status}[/blink bold yellow]")
            await asyncio.sleep(2.5)

    def action_focus_pane(self, pane_type: str) -> None:
        """Zoom in on a specific pane stack."""
        self.is_zoomed = True
        status = self.query_one("#status-pane")
        center = self.query_one("#center-stack")
        right = self.query_one("#right-stack")

        for p in [status, center, right]:
            p.set_class(False, "zoomed")
            p.set_class(True, "hidden")

        if pane_type == "status":
            status.set_class(True, "zoomed")
            status.set_class(False, "hidden")
        elif pane_type == "center":
            center.set_class(True, "zoomed")
            center.set_class(False, "hidden")
        elif pane_type == "right":
            right.set_class(True, "zoomed")
            right.set_class(False, "hidden")

    def action_reset_layout(self) -> None:
        """Reset layout to 3-pane view."""
        self.is_zoomed = False
        status = self.query_one("#status-pane")
        center = self.query_one("#center-stack")
        right = self.query_one("#right-stack")

        for p in [status, center, right]:
            p.set_class(False, "hidden")
            p.set_class(False, "zoomed")

    def log_to_pane(self, pane_id: str, message: str):
        """Helper to write to specific log panes."""
        try:
            self.query_one(f"#{pane_id}", RichLog).write(message)
        except Exception:
            pass

    async def execute_engine(self):
        """Background task to run the SKEngine."""
        from src.core.engine import SKEngine
        
        engine = SKEngine()
        
        def engine_callback(event_type: str, data: dict):
            if event_type == "attack_fired":
                self.post_message(AttackFired(data))
            elif event_type == "target_responded":
                self.post_message(TargetResponded(data))
            elif event_type == "attack_complete":
                self.post_message(AttackComplete(data))

        try:
            if '/' in self.target:
                provider, model = self.target.split('/', 1)
            else:
                provider, model = "openai", self.target
            
            result = await engine.run_module(
                module_name=self.module_name,
                target_provider=provider,
                target_model=model,
                on_event=engine_callback,
                **self.engine_kwargs
            )
            
            status = result.score.result.value.upper()
            color = "green" if status == "SUCCESS" else "red"
            
            self.log_to_pane("agent-log", f"\n[bold {color}]>>> SESSION TERMINATED: {status}[/bold {color}]")
            
            if status == "SUCCESS":
                self.is_compromised = True
                # Show Shell using 'block' which is supported by Textual
                shell = self.query_one("#shell-container")
                shell.styles.display = "block"
                self.query_one("#shell-input").focus()
            else:
                self.query_one("#lbl-secret").update(f"\n[bold red]Exploit / Secret:[/bold red]\n[dim]No secret found.[/dim]")

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.log_to_pane("agent-log", f"\n[bold red]>>> CORE ENGINE CRASH:[/bold red] {str(e)}")
            self.log_to_pane("agent-log", f"[dim]{error_details}[/dim]")
            self.query_one("#lbl-hacking").update("\n[bold red]ENGINE CRASHED[/bold red]")

    # ─── Event Handlers ───

    def on_attack_fired(self, event: AttackFired) -> None:
        turn = event.data.get("turn")
        thought = event.data.get("thought", "Calculating strategy...")
        payload = event.data.get("payload", "")
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        self.winning_payload = payload # Keep track of potential winner
        
        self.log_to_pane("agent-log", f"\n[bold magenta]— TURN {turn} —[/bold magenta]")
        self.log_to_pane("agent-log", f"[bold cyan]Payload fired:[/bold cyan] {payload[:300]}")
        self.log_to_pane("brain-log", f"\n[bold magenta]Turn {turn} Rationale:[/bold magenta]")
        self.log_to_pane("brain-log", f"{thought}")
        
        tree = self.query_one("#threat-tree", Tree)
        self.last_turn_node = tree.root.add(f"[bold yellow]Turn {turn}:[/bold yellow] Attempt", expand=True)
        
        self.query_one("#lbl-tokens").update(f"\n[bold cyan]Tokens:[/bold cyan]\n{self.total_tokens}")
        self.query_one("#lbl-payload").update(f"\n[bold yellow]Last Payload:[/bold yellow]\n[dim]{payload[:100]}...[/dim]")

    def on_target_responded(self, event: TargetResponded) -> None:
        turn = event.data.get("turn")
        response = event.data.get("response")
        score_data = event.data.get("score", {})
        result_str = str(score_data.get("result", "unknown"))
        remediation = score_data.get("remediation", "")
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        
        is_success = (result_str.lower() == "success")
        is_failure = (result_str.lower() == "failure")
        res_color = "green" if is_success else "yellow" if not is_failure else "red"
        
        self.log_to_pane("agent-log", f"[bold {res_color}]Target Responded ({result_str.upper()}):[/bold {res_color}]")
        self.log_to_pane("agent-log", f"{response[:400]}...")
        
        if is_success:
            self.is_compromised = True
            banner = self.query_one("#pwnd-banner")
            banner.styles.display = "block"
            banner.update("\n[b]!!! PWND !!![/b]\nTARGET COMPROMISED")
            
            # Show Winning Exploit clearly
            self.query_one("#lbl-secret").update(f"\n[bold red]Winning Exploit:[/bold red]\n[bold white]{self.winning_payload}[/bold white]")

            # Educational Tracing (Reproduction)
            base_url = self.engine_kwargs.get("base_url", "http://target/v1")
            model = self.engine_kwargs.get("model", "phi3")
            curl_cmd = f"curl -X POST {base_url}/chat/completions -d '{{\"model\": \"{model}\", \"messages\": [{{...}}]}}'"
            self.log_to_pane("edu-log", f"\n[bold green]REPRODUCTION STEPS:[/bold green]")
            self.log_to_pane("edu-log", f"[dim]{curl_cmd}[/dim]")
            self.log_to_pane("edu-log", "\n[bold red]CRITICAL: TARGET COMPROMISED[/bold red]")

        if remediation:
            self.log_to_pane("edu-log", f"\n[bold {res_color}]Analysis (Turn {turn}):[/bold {res_color}]")
            self.log_to_pane("edu-log", f"{remediation}")
        
        if self.last_turn_node:
            icon = "✅" if is_success else "❌" if is_failure else "⚠️"
            resp_node = self.last_turn_node.add(f"{icon} [bold {res_color}]Response ({result_str})[/bold {res_color}]")
            for signal in score_data.get("signals", []):
                resp_node.add(f"[dim]{signal}[/dim]")
        
        self.query_one("#lbl-latency").update(f"\n[bold cyan]Latency:[/bold cyan]\n{event.data.get('latency_ms', 0)}ms")
        self.query_one("#lbl-tokens").update(f"\n[bold cyan]Tokens:[/bold cyan]\n{self.total_tokens}")
        self.query_one("#lbl-hacking").update("\n[dim]Waiting for agent...[/dim]")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle manual interaction in the Virtual Shell."""
        user_text = event.value
        if not user_text: return
        
        self.query_one("#shell-input", Input).value = ""
        self.log_to_pane("agent-log", f"\n[bold green]SHELL >> [/bold green]{user_text}")
        
        client = LLMClient()
        provider, model = self.target.split('/', 1) if '/' in self.target else ("openai", self.target)
            
        # FIX: Corrected argument names from target_provider/target_model to provider/model
        req = LLMRequest(
            prompt=user_text, 
            provider=provider, 
            model=model,
            base_url=self.engine_kwargs.get("base_url"), 
            api_key=self.engine_kwargs.get("api_key")
        )
        
        self.log_to_pane("agent-log", "[dim]Shell communicating with target...[/dim]")
        try:
            resp = await client.send(req)
            self.log_to_pane("agent-log", f"[bold green]SHELL << [/bold green]{resp.content}")
        except Exception as e:
            self.log_to_pane("agent-log", f"[bold red]SHELL ERROR:[/bold red] {str(e)}")

    def on_attack_complete(self, event: AttackComplete) -> None:
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        self.query_one("#lbl-tokens").update(f"\n[bold cyan]Tokens:[/bold cyan]\n{self.total_tokens}")
        
        spinner = self.query_one("#loading-spinner")
        spinner.styles.display = "none"
        self.query_one("#lbl-hacking").update("\n[bold green]SESSION COMPLETED[/bold green]")
        
        quote = random.choice(HACKER_QUOTES)
        self.log_to_pane("brain-log", f"\n[italic cyan]\"{quote}\"[/italic cyan]")

if __name__ == "__main__":
    app = SKDashboard("prompt_injection", "openai/gpt-4o")
    app.run()
