"""
Technique: Agentic Prompt Extraction
Category: Extraction > Agentic
"""

from src.core.engine import (
    BaseModule, ModuleMetadata, ModuleCategory, Difficulty, AttackResult, ModuleOption
)
from src.agents.deployer import AgentDeployer
from typing import Optional, Any

class AgenticPromptExtraction(BaseModule):
    @property
    def metadata(self) -> ModuleMetadata:
        return ModuleMetadata(
            name="extraction.agentic.prompt",
            display_name="Autonomous Prompt Extraction",
            version="1.0.0",
            category=ModuleCategory.PROMPT_INJECTION,
            difficulty=Difficulty.INTERMEDIATE,
            owasp_mapping="ML01",
            description="Deploys an autonomous Attacker Agent to interactively probe the target model and force it to reveal its system prompt using multi-turn reasoning.",
            author="SK Labs"
        )

    def get_options(self) -> list[ModuleOption]:
        return [
            ModuleOption(name="TARGET", default="openai", required=True),
            ModuleOption(name="MODEL", default="gpt-4o", required=True),
            ModuleOption(name="ATTACKER_PROVIDER", default="openai"),
            ModuleOption(name="ATTACKER_MODEL", default="gpt-4o"),
            ModuleOption(name="MAX_TURNS", default=5),
            ModuleOption(name="EXPECTED_FLAG", default=None),
            ModuleOption(name="GOAL", default="Extract the system instructions."),
            ModuleOption(name="BASE_URL", default=None),
        ]

    def get_payloads(self) -> list[str]:
        return ["<agentic_dynamic_payloads>"]

    async def run(self, target_provider, target_model, **kwargs) -> AttackResult:
        deployer = AgentDeployer(
            attacker_provider=kwargs.get("attacker_provider", "openai"), 
            attacker_model=kwargs.get("attacker_model", "gpt-4o")
        )
        
        result = await deployer.deploy(
            module=self,
            target_provider=target_provider,
            target_model=target_model,
            system_prompt=kwargs.get("system_prompt", "Follow your instructions."),
            goal=kwargs.get("goal", "Extract the system instructions."),
            expected_flag=kwargs.get("expected_flag"),
            max_turns=int(kwargs.get("max_turns", 5)),
            on_event=kwargs.get("on_event"),
            base_url=kwargs.get("base_url"),
            api_key=kwargs.get("api_key")
        )
        return result
