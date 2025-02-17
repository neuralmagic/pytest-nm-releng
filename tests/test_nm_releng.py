# Copyright (c) 2025 - present / Neuralmagic, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from importlib.metadata import PackageNotFoundError, version

import pytest

try:
    version("pytest-cov")
    _pytest_cov_installed = True
except PackageNotFoundError:
    _pytest_cov_installed = False


def test_plugin_loaded(pytester: pytest.Pytester):
    """Verify the plugin is loaded by pytest"""

    plugin_version = version("pytest-nm-releng")

    pytester.makepyfile("""
        def test_pass():
            pass
    """)

    result = pytester.runpytest()
    result.stdout.fnmatch_lines([f"plugins:*nm-releng-{plugin_version}*"])


def test_plugin_adds_junit_args(
    pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
):
    """Verify the plugin adds the expected junit args"""

    monkeypatch.setenv("NMRE_JUNIT_BASE", "results")

    cf = pytester.parseconfigure()
    actual = cf.getoption("--junit-xml", None)
    assert actual is not None
    assert actual.startswith("results")


def test_plugin_adds_full_junit_args(
    pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
):
    """Verify the plugin adds the expected junit args"""

    monkeypatch.setenv("NMRE_JUNIT_FULL", "1")

    cf = pytester.parseconfigure()
    actual = cf.getoption("-o", None)
    assert actual is not None
    assert actual == ["junit_logging=all", "junit_log_passing_tests=True"]


@pytest.mark.skipif(not _pytest_cov_installed, reason="pytest-cov is required")
def test_plugin_adds_coverage_args(
    pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
):
    """Verify the plugin adds the expected coverage args"""

    monkeypatch.setenv("NMRE_COV_NAME", "vllm")

    cf = pytester.parseconfigure()

    assert "vllm" in cf.getoption("--cov", None)
    assert cf.getoption("--cov-append") is True


@pytest.mark.skipif(not _pytest_cov_installed, reason="pytest-cov is required")
def test_plugin_adds_all_args(
    pytester: pytest.Pytester, monkeypatch: pytest.MonkeyPatch
):
    """Verify the plugin adds the expected coverage args"""

    monkeypatch.setenv("NMRE_JUNIT_BASE", "results")
    monkeypatch.setenv("NMRE_JUNIT_FULL", "1")
    monkeypatch.setenv("NMRE_COV_NAME", "vllm")

    cf = pytester.parseconfigure()

    assert cf.getoption("--junit-xml", "").startswith("results")
    assert "vllm" in cf.getoption("--cov", [])
    assert cf.getoption("-o", None) == [
        "junit_logging=all",
        "junit_log_passing_tests=True",
    ]
    assert cf.getoption("--cov-append") is True
