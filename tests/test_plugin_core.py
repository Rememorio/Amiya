from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import types
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _install_astrbot_stubs() -> None:
    astrbot_module = types.ModuleType("astrbot")
    api_module = types.ModuleType("astrbot.api")
    event_module = types.ModuleType("astrbot.api.event")
    star_module = types.ModuleType("astrbot.api.star")

    class _Logger:
        def info(self, message: str) -> None:
            del message

    class _Filter:
        @staticmethod
        def regex(regex: str, **kwargs):
            def decorator(func):
                func.__amiya_test_regex__ = regex
                func.__amiya_test_filter_kwargs__ = kwargs
                return func

            return decorator

    class _Star:
        def __init__(self, context, config=None) -> None:
            self.context = context
            self.config = config or {}

    api_module.logger = _Logger()
    event_module.AstrMessageEvent = object
    event_module.filter = _Filter()
    star_module.Context = object
    star_module.Star = _Star

    sys.modules["astrbot"] = astrbot_module
    sys.modules["astrbot.api"] = api_module
    sys.modules["astrbot.api.event"] = event_module
    sys.modules["astrbot.api.star"] = star_module


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class _FakeEvent:
    def __init__(self, sender_name: str = "chat user", message_str: str = "") -> None:
        self._sender_name = sender_name
        self.message_str = message_str
        self.stopped = False

    def get_message_str(self) -> str:
        return self.message_str

    def get_sender_name(self) -> str:
        return self._sender_name

    def is_private_chat(self) -> bool:
        return False

    def stop_event(self) -> None:
        self.stopped = True


class PluginCoreTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _install_astrbot_stubs()
        cls.plugin_module = _load_module("amiya_main_test", ROOT / "main.py")
        cls.package_module = _load_module("amiya_package_test", ROOT / "scripts" / "package.py")

    def _plugin(self, config: dict | None = None):
        return self.plugin_module.AmiyaCodexChat(object(), config or {})

    def test_handler_regex_leaves_slash_commands_to_astrbot(self) -> None:
        regex = re.compile(self.plugin_module.HANDLER_REGEX)
        self.assertIsNone(regex.search("/help"))
        self.assertIsNone(regex.search("   /reset"))
        self.assertIsNotNone(regex.search("兔兔 状态"))
        self.assertIsNotNone(regex.search("ordinary chat"))

    def test_configured_prefixes_are_runtime_effective(self) -> None:
        plugin = self._plugin({"command_prefixes": "兔兔,Amiya,艾雅法拉,Eyjafjalla"})

        self.assertEqual(plugin._strip_known_prefix("兔兔状态"), ("状态", True))
        self.assertEqual(plugin._strip_known_prefix("amiya status"), ("status", True))
        self.assertEqual(plugin._strip_known_prefix("艾雅法拉你好"), ("你好", True))
        self.assertEqual(plugin._strip_known_prefix("Eyjafjalla 你好"), ("你好", True))
        self.assertEqual(plugin._strip_known_prefix("AmiyaBot status"), ("AmiyaBot status", False))
        self.assertEqual(plugin._strip_known_prefix("ordinary chat"), ("ordinary chat", False))

    async def test_unmatched_messages_continue_pipeline(self) -> None:
        plugin = self._plugin({"command_prefixes": "兔兔"})
        event = _FakeEvent(message_str="ordinary chat")

        results = []
        async for result in plugin.on_prefixed_message(event):
            results.append(result)

        self.assertFalse(event.stopped)
        self.assertEqual(results, [])

    def test_soul_file_can_select_eyjafjalla(self) -> None:
        plugin = self._plugin({"soul_file": "SOUL-Eyjafjalla.md"})
        soul, state = plugin._resolve_soul()

        self.assertIn("艾雅法拉", soul)
        self.assertIn("SOUL-Eyjafjalla.md", state)

    def test_reply_and_sender_sanitization(self) -> None:
        plugin = self._plugin()
        self.assertEqual(plugin._sanitize_reply("see /tmp/project/file.py"), "see <local path>")

        prompt = plugin._format_prompt(_FakeEvent("Alice\n/tmp/project/file.py"), "hello")
        self.assertIn("Sender: Alice <local path>", prompt)
        self.assertNotIn("/tmp/project", prompt)

    def test_package_includes_all_bundled_soul_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "plugin.zip"
            self.package_module.build(target)
            with zipfile.ZipFile(target) as archive:
                names = set(archive.namelist())

        self.assertIn("SOUL-Amiya.md", names)
        self.assertIn("SOUL-Eyjafjalla.md", names)


if __name__ == "__main__":
    unittest.main()
