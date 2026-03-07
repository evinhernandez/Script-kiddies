import unittest
from src.core.plugin_loader import discover_modules

class TestPluginLoader(unittest.TestCase):
    def test_dynamic_discovery_and_canonical_naming(self):
        """
        Ensures the loader recursively scans the src/modules folder
        and correctly transforms file paths into canonical dotted names.
        """
        modules = discover_modules()
        
        # Verify core modules exist and are named properly
        self.assertIn("injection.direct.basic", modules)
        self.assertIn("injection.direct.roleplay", modules)
        self.assertIn("exfiltration.markdown", modules)
        self.assertIn("extraction.agentic.prompt", modules)
        self.assertIn("jailbreak.adversarial.homoglyph", modules)

if __name__ == '__main__':
    unittest.main()
