import pytest


def test_plugin_loaded(pytester: pytest.Pytester):
    """Verify the plugin is loaded by pytest"""

    pytester.makepyfile("""
        def test_pass():
            pass
    """)

    result = pytester.runpytest()
    result.stdout.fnmatch_lines(["plugins:*nm-releng-*"])
