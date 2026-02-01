"""
SK Framework — Plugin Loader
Dynamically discovers and imports all attack modules.
Modules are auto-discovered from src/modules/ subdirectories.
Each module directory must have an __init__.py that exports a BaseModule subclass.
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Any

from src.utils.logger import get_logger

log = get_logger("plugin_loader")

MODULES_DIR = Path(__file__).resolve().parents[1] / "modules"


def discover_modules() -> dict[str, Any]:
    """
    Scan src/modules/ for all subdirectories containing attack modules.
    Each valid module directory must:
        - Have an __init__.py
        - Export a class that extends BaseModule
        - That class must have a `metadata` property

    Returns:
        dict mapping module name -> module class
    """
    from src.core.engine import BaseModule  # Import here to avoid circular

    discovered: dict[str, Any] = {}

    if not MODULES_DIR.exists():
        log.warning("modules_dir_missing", path=str(MODULES_DIR))
        return discovered

    # Iterate over subdirectories in src/modules/
    for item in sorted(MODULES_DIR.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith("_"):
            continue  # Skip __pycache__ etc.

        init_file = item / "__init__.py"
        if not init_file.exists():
            continue

        module_path = f"src.modules.{item.name}"

        try:
            mod = importlib.import_module(module_path)

            # Find the BaseModule subclass in the module
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseModule)
                    and attr is not BaseModule
                ):
                    # Instantiate to grab metadata for the name
                    instance = attr()
                    name = instance.metadata.name
                    discovered[name] = attr
                    log.info("module_discovered", name=name, path=module_path)
                    break  # One module class per directory

        except Exception as e:
            log.error("module_load_failed", path=module_path, error=str(e))

    return discovered
