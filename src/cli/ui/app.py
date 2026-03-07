"""
SK Framework — Terminal Dashboard
Full-screen TUI for real-time attack monitoring using Textual.
"""

import random
import asyncio
import json
import time
import pyperclip
from typing import Any, Optional
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, RichLog, Label, Tree, LoadingIndicator, Input
from textual.suggester import Suggester
from textual.binding import Binding
from textual.message import Message
from textual.screen import Screen
from rich.tree import Tree as RichTree
from rich.panel import Panel
from rich.text import Text

from src.utils.llm_client import LLMClient, LLMRequest
from src.core.engine import SKEngine

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

class ShellSuggester(Suggester):
    """Provides tab completion for the session shell."""
    def __init__(self, modules: list[str]):
        super().__init__(use_cache=False)
        self.modules = sorted(modules)
        self.cmds = ["/run ", "/help", "/clear", "exit", "quit"]

    async def get_suggestion(self, value: str) -> Optional[str]:
        if not value: return None
        v = value.lower()
        for cmd in self.cmds:
            if cmd.startswith(v):
                return cmd
        if v.startswith("/run "):
            typed_mod = value[5:]
            for mod in self.modules:
                if mod.startswith(typed_mod):
                    return f"/run {mod}"
        return None

class TelemetryScreen(Screen):
    """A secondary screen for deep forensic activity tailing."""
    def __init__(self, history: list[str]):
        super().__init__()
        self.history = history

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("[bold green]DEEP SYSTEM TELEMETRY (FORENSIC TAIL)[/bold green]", classes="pane-title")
        yield RichLog(id="telemetry-log-full", markup=True, wrap=True, highlight=True)
        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#telemetry-log-full", RichLog)
        for line in self.history:
            log.write(line)

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back to Dashboard"),
        Binding("t", "app.pop_screen", "Back to Dashboard"),
    ]

class SKDashboard(App):
    """
    Main dashboard for SK Framework attacks.
    """
    ENABLE_COMMAND_PALETTE = False
    
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
        height: 33%;
        padding: 1;
    }

    .sub-pane-half {
        height: 50%;
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

    #notebook-pane {
        border: solid #00FF00;
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

    .notebook-title {
        background: #00FF00;
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
        min-height: 5;
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
        Binding("3", "focus_pane('right')", "Tree/Notebook/Edu"),
        Binding("t", "toggle_telemetry", "Telemetry"),
        Binding("c", "copy_winning_exploit", "Copy Exploit"),
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
        self.session_history = []
        self.engine = SKEngine()
        self.pivot_count = 0
        self.telemetry_history = []
        self.reproduction_cmd = ""

    def compose(self) -> ComposeResult:
        modules = [m.name for m in self.engine.list_modules()]
        yield Header(show_clock=True)
        with Container(id="main-container"):
            with Horizontal():
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
                with Vertical(id="center-stack"):
                    with Vertical(id="logs-pane", classes="pane sub-pane-half"):
                        yield Label("IO TRAFFIC (RAW)", classes="pane-title")
                        yield RichLog(id="agent-log", highlight=True, markup=True, wrap=True)
                    with Vertical(id="brain-pane", classes="pane sub-pane-half"):
                        yield Label("ATTACKER BRAIN (THOUGHTS)", classes="pane-title brain-title")
                        yield RichLog(id="brain-log", markup=True, wrap=True)
                with Vertical(id="right-stack"):
                    with Vertical(id="threat-pane", classes="pane sub-pane"):
                        yield Label("ATTACK TREE", classes="pane-title")
                        yield Tree("Attack Root", id="threat-tree")
                    with Vertical(id="notebook-pane", classes="pane sub-pane"):
                        yield Label("EXPLOIT NOTEBOOK", classes="pane-title notebook-title")
                        yield RichLog(id="notebook-log", markup=True, wrap=True)
                    with Vertical(id="education-pane", classes="pane sub-pane"):
                        yield Label("EDUCATIONAL TRACING", classes="pane-title edu-title")
                        yield RichLog(id="edu-log", markup=True, wrap=True)
            with Horizontal(id="shell-container"):
                yield Label("[bold green]SESSION_SHELL $> [/bold green]")
                yield Input(placeholder="Type follow-up command or /run <module>...", id="shell-input", suggester=ShellSuggester(modules))
        yield Footer()

    def on_mount(self) -> None:
        self.log_to_pane("agent-log", f"[bold green]>>> I/O SUBSYSTEM ONLINE[/bold green]")
        self.log_to_pane("brain-log", f"[bold green]>>> COGNITIVE ENGINE ONLINE[/bold green]")
        self.log_to_pane("notebook-log", f"[bold green]>>> EXPLOIT NOTEBOOK ACTIVE[/bold green]")
        self.telemetry_log(f"[bold green]>>> TELEMETRY HUB INITIALIZED[/bold green]")
        tree = self.query_one("#threat-tree", Tree)
        tree.root.expand()
        self.run_worker(self.execute_engine())
        self.run_worker(self.rotate_status())

    async def rotate_status(self):
        lbl = self.query_one("#lbl-hacking", Static)
        while True:
            if "COMPLETED" in str(lbl.content) or "CRASH" in str(lbl.content): break
            new_status = random.choice(HACKER_STATUSES)
            lbl.update(f"\n[blink bold yellow]{new_status}[/blink bold yellow]")
            await asyncio.sleep(2.5)

    def action_focus_pane(self, pane_type: str) -> None:
        self.is_zoomed = True
        status, center, right = self.query_one("#status-pane"), self.query_one("#center-stack"), self.query_one("#right-stack")
        for p in [status, center, right]:
            p.set_class(False, "zoomed")
            p.set_class(True, "hidden")
        if pane_type == "status": status.set_class(True, "zoomed"); status.set_class(False, "hidden")
        elif pane_type == "center": center.set_class(True, "zoomed"); center.set_class(False, "hidden")
        elif pane_type == "right": right.set_class(True, "zoomed"); right.set_class(False, "hidden")

    def action_toggle_telemetry(self) -> None:
        self.push_screen(TelemetryScreen(history=self.telemetry_history))

    def action_copy_winning_exploit(self) -> None:
        to_copy = ""
        if self.winning_payload:
            to_copy = f"EXPLOIT PAYLOAD:\n{self.winning_payload}"
            if self.reproduction_cmd: to_copy += f"\n\nREPRODUCTION COMMAND:\n{self.reproduction_cmd}"
            pyperclip.copy(to_copy)
            self.log_to_pane("agent-log", "\n[bold green]>>> COPIED EXPLOIT TO CLIPBOARD[/bold green]")
            self.telemetry_log("CLIPBOARD_COPY -> Success")
        else:
            self.log_to_pane("agent-log", "\n[bold yellow]>>> NOTHING TO COPY YET[/bold yellow]")

    def action_reset_layout(self) -> None:
        self.is_zoomed = False
        status, center, right = self.query_one("#status-pane"), self.query_one("#center-stack"), self.query_one("#right-stack")
        for p in [status, center, right]: p.set_class(False, "hidden"); p.set_class(False, "zoomed")

    def log_to_pane(self, pane_id: str, message: str):
        try: self.query_one(f"#{pane_id}", RichLog).write(message)
        except Exception: pass

    def telemetry_log(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}"
        self.telemetry_history.append(line)
        try: self.query_one("#telemetry-log-full", RichLog).write(line)
        except Exception: pass
        self.log_to_pane("agent-log", f"[dim][{timestamp}] TELEMETRY: {message}[/dim]")

    async def execute_engine(self):
        try:
            provider, model = self.target.split('/', 1) if '/' in self.target else ("openai", self.target)
            result = await self.engine.run_module(module_name=self.module_name, target_provider=provider, target_model=model, on_event=self.engine_callback, **self.engine_kwargs)
            status = result.score.result.value.upper()
            color = "green" if status == "SUCCESS" else "red"
            self.log_to_pane("agent-log", f"\n[bold {color}]>>> SESSION TERMINATED: {status}[/bold {color}]")
            self.telemetry_log(f"[bold {color}]ENGINE_STOP -> {status}[/bold {color}]")
            if status == "SUCCESS":
                self.is_compromised = True
                shell = self.query_one("#shell-container")
                shell.styles.display = "block"
                self.query_one("#shell-input").focus()
            else:
                self.query_one("#lbl-secret").update(f"\n[bold red]Exploit / Secret:[/bold red]\n[dim]No secret found.[/dim]")
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            self.log_to_pane("agent-log", f"\n[bold red]>>> CORE ENGINE CRASH:[/bold red] {str(e)}")
            self.telemetry_log(f"[bold red]ENGINE_CRASH -> {str(e)}[/bold red]")
            self.log_to_pane("agent-log", f"[dim]{error_details}[/dim]")
            self.query_one("#lbl-hacking").update("\n[bold red]ENGINE CRASHED[/bold red]")

    def engine_callback(self, event_type: str, data: dict):
        if event_type == "attack_fired": self.post_message(AttackFired(data))
        elif event_type == "target_responded": self.post_message(TargetResponded(data))
        elif event_type == "attack_complete": self.post_message(AttackComplete(data))

    def on_attack_fired(self, event: AttackFired) -> None:
        turn, thought, payload = event.data.get("turn"), event.data.get("thought", "Calculating strategy..."), event.data.get("payload", "")
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        self.winning_payload = payload
        self.telemetry_log(f"[cyan]PAYLOAD_SENT[/cyan] -> Turn {turn} ({len(payload)} chars): {payload[:50]}...")
        self.log_to_pane("agent-log", f"\n[bold magenta]— TURN {turn} —[/bold magenta]\n[bold cyan]Payload fired:[/bold cyan] {payload[:300]}")
        self.log_to_pane("brain-log", f"\n[bold magenta]Turn {turn} Rationale:[/bold magenta]\n{thought}")
        tree = self.query_one("#threat-tree", Tree)
        self.last_turn_node = tree.root.add(f"[bold yellow]Turn {turn}:[/bold yellow] Attempt", expand=True)
        self.query_one("#lbl-tokens").update(f"\n[bold cyan]Tokens:[/bold cyan]\n{self.total_tokens}")
        self.query_one("#lbl-payload").update(f"\n[bold yellow]Last Payload:[/bold yellow]\n[dim]{payload[:100]}...[/dim]")

    def on_target_responded(self, event: TargetResponded) -> None:
        turn, response, score_data = event.data.get("turn"), event.data.get("response"), event.data.get("score", {})
        result_str, remediation, latency = str(score_data.get("result", "unknown")).lower(), score_data.get("remediation", ""), event.data.get('latency_ms', 0)
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        self.telemetry_log(f"[yellow]TARGET_RESP[/yellow] -> {result_str.upper()} ({latency}ms) - {response[:50]}...")
        is_success, is_failure = "success" in result_str, "failure" in result_str
        res_color = "green" if is_success else "yellow" if not is_failure else "red"
        self.log_to_pane("agent-log", f"[bold {res_color}]Target Responded ({result_str.upper()}):[/bold {res_color}]\n{response[:400]}...")
        if is_success:
            self.is_compromised = True
            banner = self.query_one("#pwnd-banner")
            banner.styles.display = "block"
            banner.update("\n[b]!!! PWND !!![/b]\nTARGET COMPROMISED")
            self.query_one("#lbl-secret").update(f"\n[bold red]Exploit SUCCESS![/bold red]\n[dim]See Notebook[/dim]")
            base_url, model = self.engine_kwargs.get("base_url", "http://target/v1"), self.engine_kwargs.get("model", "phi3")
            escaped_payload = self.winning_payload.replace("'", "'\\''").replace("\n", " ")
            self.reproduction_cmd = f"curl -X POST {base_url}/chat/completions -d '{{\"model\": \"{model}\", \"messages\": [{{\"role\": \"user\", \"content\": \"{escaped_payload}\"}}]}}'"
            self.log_to_pane("notebook-log", f"\n[bold green]>>> SUCCESSFUL EXPLOIT (Turn {turn})[/bold green]\n[bold cyan]Payload:[/bold cyan]\n{self.winning_payload}\n[bold yellow]Reproduction:[/bold yellow]\n{self.reproduction_cmd}")
            self.log_to_pane("edu-log", "\n[bold red]CRITICAL: TARGET COMPROMISED[/bold red]")
        if remediation: self.log_to_pane("edu-log", f"\n[bold {res_color}]Analysis (Turn {turn}):[/bold {res_color}]\n{remediation}")
        if self.last_turn_node:
            icon = "✅" if is_success else "❌" if is_failure else "⚠️"
            resp_node = self.last_turn_node.add(f"{icon} [bold {res_color}]Response ({result_str})[/bold {res_color}]")
            for signal in score_data.get("signals", []): resp_node.add(f"[dim]{signal}[/dim]")
        self.query_one("#lbl-latency").update(f"\n[bold cyan]Latency:[/bold cyan]\n{latency}ms")
        self.query_one("#lbl-tokens").update(f"\n[bold cyan]Tokens:[/bold cyan]\n{self.total_tokens}")
        self.query_one("#lbl-hacking").update("\n[dim]Waiting for agent...[/dim]")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_text = event.value
        if not user_text: return
        self.query_one("#shell-input", Input).value = ""
        cmd = user_text.lower().strip()
        if cmd in ["exit", "quit", "/exit"]: self.exit(); return
        if cmd == "/help":
            self.log_to_pane("agent-log", "\n[bold yellow]Shell Commands:[/bold yellow]\n  exit, quit, /exit - Return to Console\n  /run <module>     - Execute another module via this session\n  /clear            - Clear the IO log")
            return
        if cmd == "/clear": self.query_one("#agent-log", RichLog).clear(); self.telemetry_log("[dim]IO Log Cleared.[/dim]"); return
        if cmd.startswith("/run "):
            module_name = cmd.replace("/run ", "").strip()
            await self.pivot_exploit(module_name)
            return
        self.telemetry_log(f"[bold green]USER_SHELL_CMD[/bold green] -> {user_text[:20]}...")
        self.log_to_pane("agent-log", f"\n[bold green]SHELL >> [/bold green]{user_text}")
        await self.communicate_with_target(user_text)

    async def communicate_with_target(self, prompt: str):
        client = LLMClient()
        provider, model = self.target.split('/', 1) if '/' in self.target else ("openai", self.target)
        req = LLMRequest(prompt=prompt, provider=provider, model=model, messages=self.session_history, base_url=self.engine_kwargs.get("base_url"), api_key=self.engine_kwargs.get("api_key"))
        self.log_to_pane("agent-log", "[dim]Communicating...[/dim]")
        try:
            start_time = time.perf_counter()
            resp = await client.send(req)
            latency = int((time.perf_counter() - start_time) * 1000)
            self.log_to_pane("agent-log", f"[bold green]SHELL << [/bold green]{resp.content}")
            self.telemetry_log(f"[bold green]SHELL_SUCCESS[/bold green] ({latency}ms) - {resp.content[:50]}...")
            self.session_history.append({"role": "user", "content": prompt})
            self.session_history.append({"role": "assistant", "content": resp.content})
            self.query_one("#lbl-latency").update(f"\n[bold cyan]Latency:[/bold cyan]\n{latency}ms")
        except Exception as e:
            self.log_to_pane("agent-log", f"[bold red]ERROR:[/bold red] {str(e)}")
            self.telemetry_log(f"[bold red]SHELL_ERROR[/bold red] -> {str(e)}")

    async def pivot_exploit(self, module_name: str):
        try:
            module = self.engine.get_module(module_name)
            payloads = module.get_payloads()
            self.pivot_count += 1
            self.query_one("#lbl-module").update(f"[bold cyan]Module (PIVOT):[/bold cyan]\n{module_name}")
            self.log_to_pane("agent-log", f"\n[bold yellow]>>> PIVOTING: Executing {module_name} payloads...[/bold yellow]")
            self.log_to_pane("brain-log", f"\n[bold magenta]Pivot Strategy:[/bold magenta]\nRunning {module_name} vectors through established context.")
            self.telemetry_log(f"[bold yellow]PIVOT_START[/bold yellow] -> {module_name}")
            tree = self.query_one("#threat-tree", Tree)
            pivot_root = tree.root.add(f"[bold magenta]Pivot {self.pivot_count}:[/bold magenta] {module_name}", expand=True)
            for i, p in enumerate(payloads):
                self.winning_payload = p
                self.query_one("#lbl-payload").update(f"\n[bold yellow]Last Payload:[/bold yellow]\n[dim]{p[:100]}...[/dim]")
                self.telemetry_log(f"[cyan]PIVOT_VECTOR[/cyan] -> {i+1}/{len(payloads)}: {p[:50]}...")
                self.last_turn_node = pivot_root.add(f"[bold yellow]Vector {i+1}:[/bold yellow] Attempt", expand=True)
                self.log_to_pane("agent-log", f"\n[bold cyan]Vector {i+1}:[/bold cyan] {p[:100]}...")
                client = LLMClient()
                provider, model = self.target.split('/', 1) if '/' in self.target else ("openai", self.target)
                req = LLMRequest(prompt=p, provider=provider, model=model, messages=self.session_history, base_url=self.engine_kwargs.get("base_url"), api_key=self.engine_kwargs.get("api_key"))
                resp = await client.send(req)
                self.log_to_pane("agent-log", f"[bold green]SHELL << [/bold green]{resp.content}")
                score = module.scorer.score(response_text=resp.content, attack_payload=p)
                result_str = score.result.value.lower()
                res_color = "green" if "success" in result_str else "yellow" if "partial" in result_str else "red"
                self.last_turn_node.add(f"[bold {res_color}]Response ({result_str})[/bold {res_color}]")
                if "success" in result_str:
                    self.log_to_pane("notebook-log", f"\n[bold green]>>> PIVOT SUCCESS: {module_name} (Vector {i+1})[/bold green]\n[bold cyan]Payload:[/bold cyan]\n{p}")
                self.session_history.append({"role": "user", "content": p})
                self.session_history.append({"role": "assistant", "content": resp.content})
                await asyncio.sleep(1)
            self.telemetry_log(f"[bold green]PIVOT_COMPLETE[/bold green] -> {module_name}")
        except Exception as e:
            self.log_to_pane("agent-log", f"[bold red]PIVOT FAILED:[/bold red] {str(e)}")

    def on_attack_complete(self, event: AttackComplete) -> None:
        self.total_tokens = event.data.get("total_tokens", self.total_tokens)
        self.session_history = event.data.get("history", [])
        self.query_one("#lbl-tokens").update(f"\n[bold cyan]Tokens:[/bold cyan]\n{self.total_tokens}")
        self.telemetry_log("[bold green]ATTACK_ORCHESTRATION_COMPLETE[/bold green]")
        spinner = self.query_one("#loading-spinner"); 
        if spinner: spinner.styles.display = "none"
        self.query_one("#lbl-hacking").update("\n[bold green]SESSION COMPLETED[/bold green]")
        quote = random.choice(HACKER_QUOTES)
        self.log_to_pane("brain-log", f"\n[italic cyan]\"{quote}\"[/italic cyan]")

if __name__ == "__main__":
    app = SKDashboard("injection.direct.basic", "openai/gpt-4o")
    app.run()
