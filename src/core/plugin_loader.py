"""
SK Framework — Plugin Loader
Dynamically discovers and imports all attack modules.
Modules are auto-discovered from src/modules/ recursively.
The module's canonical name is derived from its file path relative to src/modules/.
"""

import importlib
import pkgutil
import os
from pathlib import Path
from typing import Any

from src.utils.logger import get_logger

log = get_logger("plugin_loader")

MODULES_DIR = Path(__file__).resolve().parents[1] / "modules"


def discover_modules() -> dict[str, Any]:
    """
    Scan src/modules/ for all .py files containing attack modules.
    Supports deep recursive discovery.

    Returns:
        dict mapping dotted module name -> module class
    """
    from src.core.engine import BaseModule

    discovered: dict[str, Any] = {}

    if not MODULES_DIR.exists():
        log.warning("modules_dir_missing", path=str(MODULES_DIR))
        return discovered

    # pkgutil.walk_packages allows recursive discovery of packages AND modules
    import src.modules as modules_pkg
    
    for loader, module_full_name, is_pkg in pkgutil.walk_packages(modules_pkg.__path__, modules_pkg.__name__ + "."):
        # We only want actual module files, not directory packages themselves
        if not is_pkg:
            try:
                mod = importlib.import_module(module_full_name)

                # Find the BaseModule subclass in the module
                for attr_name in dir(mod):
                    attr = getattr(mod, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, BaseModule)
                        and attr is not BaseModule
                    ):
                        # Canonical name is derived from the module path relative to 'src.modules'
                        # e.g. 'src.modules.injection.direct.basic' -> 'injection.direct.basic'
                        canonical_name = module_full_name.replace("src.modules.", "")
                        
                        discovered[canonical_name] = attr
                        log.info("module_discovered", name=canonical_name, path=module_full_name)
                        
                        break  # Usually one primary module per file

            except Exception as e:
                log.error("module_load_failed", path=module_full_name, error=str(e))
                continue

    return discovered
