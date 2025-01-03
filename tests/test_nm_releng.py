from importlib.metadata import version

import pytest


def test_plugin_loaded(pytester: pytest.Pytester):
    """Verify the plugin is loaded by pytest"""

    plugin_version = version("pytest-nm-releng")

    pytester.makepyfile("""
        def test_pass():
            pass
    """)

    result = pytester.runpytest()
    result.stdout.fnmatch_lines([f"plugins:*nm-releng-{plugin_version}*"])
