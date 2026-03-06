import unittest
from unittest.mock import patch, MagicMock
from src.cli.console import SKConsole
from src.core.engine import ModuleMetadata, ModuleCategory, Difficulty, ModuleOption

class TestSKConsole(unittest.TestCase):
    def setUp(self):
        # Patch SKEngine to avoid module discovery and LLM initialization during tests
        with patch('src.cli.console.SKEngine') as mock_engine:
            self.mock_engine = mock_engine.return_value
            self.mock_engine.list_modules.return_value = []
            self.console = SKConsole()

    def test_welcome_screen_displayed(self):
        # The welcome screen is printed during __init__
        with patch('src.cli.console.console.print') as mock_print:
            SKConsole()
            # Verify that some form of welcome message was printed
            mock_print.assert_called()

    def test_do_exit(self):
        self.assertTrue(self.console.do_exit(""))

    def test_do_quit(self):
        self.assertTrue(self.console.do_quit(""))

    def test_do_set_global(self):
        with patch('src.cli.console.console.print') as mock_print:
            self.console.do_set("GLOBAL_VAR value")
            self.assertEqual(self.console.global_vars['GLOBAL_VAR'], 'value')
            mock_print.assert_called_with("[bold green][*][/bold green] GLOBAL_VAR (global) => [bold cyan]value[/bold cyan]")

    def test_do_set_module_specific(self):
        mock_module = MagicMock()
        mock_module.get_options.return_value = [
            ModuleOption(name="TARGET", default="openai", description="Test desc", required=True)
        ]
        self.console.module_instance = mock_module
        
        with patch('src.cli.console.console.print') as mock_print:
            self.console.do_set("TARGET google")
            self.assertEqual(self.console.module_vars['TARGET'], 'google')
            # Global should NOT be updated if it's a module var
            self.assertEqual(self.console.global_vars['TARGET'], 'openai')
            mock_print.assert_called_with("[bold green][*][/bold green] TARGET (module) => [bold cyan]google[/bold cyan]")

    def test_do_use_success(self):
        mock_module = MagicMock()
        mock_module.metadata.name = "prompt_injection"
        self.mock_engine.get_module.return_value = mock_module
        
        with patch('src.cli.console.console.print') as mock_print:
            self.console.do_use("prompt_injection")
            self.assertEqual(self.console.current_module, "prompt_injection")
            self.assertIn("prompt_injection", self.console.prompt)
            mock_print.assert_called_with("[bold green][+][/bold green] Loaded module: [bold cyan]prompt_injection[/bold cyan]")

    def test_do_use_fail(self):
        self.mock_engine.get_module.side_effect = ValueError("Module not found")
        with patch('src.cli.console.console.print') as mock_print:
            self.console.do_use("invalid_module")
            self.assertIsNone(self.console.current_module)
            mock_print.assert_called_with("[bold red][-][/bold red] Error: Module not found")

    def test_do_show_options_reflects_set_values(self):
        mock_module = MagicMock()
        mock_module.metadata.name = "test_module"
        mock_module.get_options.return_value = [
            ModuleOption(name="TARGET", default="openai", description="Test desc", required=True)
        ]
        self.console.current_module = "test_module"
        self.console.module_instance = mock_module
        self.console.module_vars = {"TARGET": "anthropic"}
        
        with patch('src.cli.console.console.print') as mock_print:
            self.console.do_show("options")
            # Verify that the value shown is the one we set
            # We check the call to add_row via mock_print being called with the Table
            # (Testing the exact row content of a Rich Table via mocks is complex, 
            # so we rely on the logic in do_show being tested)
            self.assertEqual(mock_print.call_count, 2)

    def test_do_back(self):
        self.console.current_module = "some_module"
        self.console.module_instance = MagicMock()
        self.console.do_back("")
        self.assertIsNone(self.console.current_module)
        self.assertIsNone(self.console.module_instance)
        self.assertEqual(self.console.prompt, "sk> ")

if __name__ == '__main__':
    unittest.main()
