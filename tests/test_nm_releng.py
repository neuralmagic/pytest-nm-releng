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
    assert isinstance(actual, str)
    assert actual.startswith("results")
