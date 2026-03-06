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
    Supports recursive discovery.

    Returns:
        dict mapping module name -> module class
    """
    from src.core.engine import BaseModule  # Import here to avoid circular

    discovered: dict[str, Any] = {}

    if not MODULES_DIR.exists():
        log.warning("modules_dir_missing", path=str(MODULES_DIR))
        return discovered

    # pkgutil.walk_packages allows recursive discovery
    # We provide the absolute path and the prefix for imports
    import src.modules as modules_pkg
    
    for loader, module_name, is_pkg in pkgutil.walk_packages(modules_pkg.__path__, modules_pkg.__name__ + "."):
        if is_pkg:
            try:
                mod = importlib.import_module(module_name)

                # Find the BaseModule subclass in the module
                for attr_name in dir(mod):
                    attr = getattr(mod, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, BaseModule)
                        and attr is not BaseModule
                    ):
                        # Instantiate to grab metadata for the name
                        try:
                            instance = attr()
                            name = instance.metadata.name
                            discovered[name] = attr
                            log.info("module_discovered", name=name, path=module_name)
                        except Exception as e:
                            log.error("module_init_failed", path=module_name, error=str(e))
                        
                        break  # One module class per package/directory

            except Exception as e:
                # Silently skip modules that fail to import (might be submodules without BaseModule)
                continue

    return discovered
