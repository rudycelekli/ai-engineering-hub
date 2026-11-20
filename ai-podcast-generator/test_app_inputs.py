import os
import runpy
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch


class _StopApp(Exception):
    pass


class _UI(ModuleType):
    def __init__(self, values):
        super().__init__("streamlit")
        self.values = values
        self.errors = []
        self.sidebar = self

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def __getattr__(self, name):
        return lambda *args, **kwargs: self

    def text_input(self, label, **kwargs):
        return self.values[label]

    def button(self, *args, **kwargs):
        return True

    def error(self, message):
        self.errors.append(message)

    def stop(self):
        raise _StopApp


class TestRequiredAppInputs(unittest.TestCase):
    def run_app(self, values):
        ui = _UI(values)
        calls = []

        class Scraper:
            def __init__(self):
                calls.append(dict(os.environ))

            def scrape(self, url):
                calls.append(url)
                raise RuntimeError("synthetic stop before any provider call")

        modules = {
            "streamlit": ui,
            "scraper": SimpleNamespace(WebScraper=Scraper),
            "script_generator": SimpleNamespace(ScriptGenerator=object),
            "tts_converter": SimpleNamespace(TTSConverter=object),
            "pydub": SimpleNamespace(AudioSegment=object),
        }
        with patch.dict(sys.modules, modules), patch.dict(os.environ, {}, clear=True):
            try:
                runpy.run_path(str(Path(__file__).with_name("app.py")), run_name="__main__")
            except _StopApp:
                pass
            environment = dict(os.environ)
        return ui.errors, calls, environment

    def test_whitespace_only_required_input_stops_before_client_creation(self):
        values = {
            "Minimax API Key": "synthetic-minimax",
            "Firecrawl API Key": "synthetic-firecrawl",
            "OpenRouter API Key": "synthetic-openrouter",
            "Article URL": "https://example.invalid/article",
        }
        for field in values:
            with self.subTest(field=field):
                errors, calls, environment = self.run_app({**values, field: " \t\n "})
                self.assertEqual(errors, ["❌ Please fill in all API keys and provide a URL"])
                self.assertEqual(calls, [])
                self.assertEqual(environment, {})

    def test_padded_values_are_normalized_before_environment_and_client_use(self):
        errors, calls, environment = self.run_app({
            "Minimax API Key": " synthetic-minimax \n",
            "Firecrawl API Key": "\t synthetic-firecrawl ",
            "OpenRouter API Key": " synthetic-openrouter ",
            "Article URL": " https://example.invalid/article \n",
        })
        expected = {
            "MINIMAX_API_KEY": "synthetic-minimax",
            "FIRECRAWL_API_KEY": "synthetic-firecrawl",
            "OPENROUTER_API_KEY": "synthetic-openrouter",
        }
        self.assertEqual(environment, expected)
        self.assertEqual(calls, [expected, "https://example.invalid/article"])
        self.assertEqual(errors, ["❌ Scraping failed: synthetic stop before any provider call"])


if __name__ == "__main__":
    unittest.main()
