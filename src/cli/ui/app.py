"""
SK Framework — Terminal Dashboard
Full-screen TUI for real-time attack monitoring using Textual.
"""

import random
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Log, Label
from textual.binding import Binding
from textual.message import Message
from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text

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

class ThreatGraph(Static):
    """
    A widget that displays a dynamic ASCII threat tree.
    """
    def on_mount(self) -> None:
        self._tree = Tree("[bold cyan]Attack Root[/bold cyan]")
        self.update(self._tree)

    def add_node(self, label: str, success: bool | None = None):
        """Add a new node to the tree."""
        icon = ""
        if success is True:
            icon = "[bold green][✓][/bold green] "
        elif success is False:
            icon = "[bold red][X][/bold red] "
        
        self._tree.add(f"{icon}{label}")
        self.update(self._tree)

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

    #status-pane {
        width: 25%;
    }

    #logs-pane {
        width: 50%;
    }

    #threat-pane {
        width: 25%;
    }

    .pane-title {
        text-align: center;
        background: #00FFFF;
        color: #000000;
        text-style: bold;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit Dashboard"),
        Binding("esc", "quit", "Return to Console"),
    ]

    def __init__(self, module_name: str, target: str, engine_kwargs: dict = None):
        super().__init__()
        self.module_name = module_name
        self.target = target
        self.engine_kwargs = engine_kwargs or {}
        self.total_tokens = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main-container"):
            with Horizontal():
                with Vertical(id="status-pane", classes="pane"):
                    yield Label("TARGET STATUS", classes="pane-title")
                    yield Static(f"Module: {self.module_name}", id="lbl-module")
                    yield Static(f"Target: {self.target}", id="lbl-target")
                    yield Static(f"\nTokens: {self.total_tokens}", id="lbl-tokens")
                    yield Static("Latency: 0ms", id="lbl-latency")
                
                with Vertical(id="logs-pane", classes="pane"):
                    yield Label("AGENT THOUGHTS / LOGS", classes="pane-title")
                    yield Log(id="agent-log")
                
                with Vertical(id="threat-pane", classes="pane"):
                    yield Label("THREAT GRAPH", classes="pane-title")
                    yield ThreatGraph(id="threat-tree")
        yield Footer()

    def on_mount(self) -> None:
        self.log_to_pane(f"Initializing dashboard for {self.module_name}...")
        self.log_to_pane(f"Targeting: {self.target}")
        
        # Start the engine in a background worker
        self.run_worker(self.execute_engine())

    def log_to_pane(self, message: str):
        """Helper to write to the agent log pane."""
        self.query_one("#agent-log", Log).write_line(message)

    async def execute_engine(self):
        """Background task to run the SKEngine."""
        from src.core.engine import SKEngine
        
        engine = SKEngine()
        
        def engine_callback(event_type: str, data: dict):
            # Map string event types to Textual Message classes
            if event_type == "attack_fired":
                self.post_message(AttackFired(data))
            elif event_type == "target_responded":
                self.post_message(TargetResponded(data))
            elif event_type == "attack_complete":
                self.post_message(AttackComplete(data))

        try:
            # We must use proper provider/model parsing here
            provider, model = self.target.split('/', 1)
            
            result = await engine.run_module(
                module_name=self.module_name,
                target_provider=provider,
                target_model=model,
                on_event=engine_callback,
                **self.engine_kwargs
            )
            
            self.log_to_pane(f"\n[bold green]ATTACK COMPLETE[/bold green]")
            self.log_to_pane(f"Final Result: {result.score.result.value.upper()}")
            self.log_to_pane(f"Details: {result.score.details}")

        except Exception as e:
            self.log_to_pane(f"\n[bold red]ERROR:[/bold red] {str(e)}")

    # ─── Event Handlers ───

    def on_attack_fired(self, event: AttackFired) -> None:
        turn = event.data.get("turn")
        payload = event.data.get("payload")
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        
        self.log_to_pane(f"\n[bold cyan]Turn {turn}: Attacker generating payload...[/bold cyan]")
        self.log_to_pane(f"Payload: {payload[:200]}...")
        self.query_one("#threat-tree", ThreatGraph).add_node(f"Turn {turn}: Payload Fired")
        self.query_one("#lbl-tokens").update(f"\nTokens: {self.total_tokens}")

    def on_target_responded(self, event: TargetResponded) -> None:
        turn = event.data.get("turn")
        response = event.data.get("response")
        score_data = event.data.get("score", {})
        result_obj = score_data.get("result", "unknown")
        
        # Extremely defensive conversion to string
        if hasattr(result_obj, "value"):
            result = str(result_obj.value)
        else:
            result = str(result_obj)
            
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        
        is_success = (result.lower() == "success")
        is_failure = (result.lower() == "failure")
        res_color = "green" if is_success else "yellow" if not is_failure else "red"
        
        self.log_to_pane(f"[bold {res_color}]Target Responded ({result}):[/bold {res_color}]")
        self.log_to_pane(f"{response[:200]}...")
        
        # Update Threat Graph
        self.query_one("#threat-tree", ThreatGraph).add_node(f"Turn {turn} Response: {result.upper()}", success=is_success if (is_success or is_failure) else None)
        
        # Update Status
        self.query_one("#lbl-latency").update(f"Latency: {event.data.get('latency_ms', 0)}ms")
        self.query_one("#lbl-tokens").update(f"\nTokens: {self.total_tokens}")

    def on_attack_complete(self, event: AttackComplete) -> None:
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        self.query_one("#lbl-tokens").update(f"\nTokens: {self.total_tokens}")
        
        self.log_to_pane("\n[bold magenta]*** Session Finalized ***[/bold magenta]")
        
        # Add random hacker quote to logs
        quote = random.choice(HACKER_QUOTES)
        self.log_to_pane(f"\n[italic cyan]\"{quote}\"[/italic cyan]")

if __name__ == "__main__":
    app = SKDashboard("prompt_injection", "openai/gpt-4o")
    app.run()
