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

import os
import re
from typing import Union

import pytest

from pytest_nm_releng.plugin import generate_coverage_flags, generate_junit_flags

EnvVarValue = Union[str, None]


def _setenv(
    monkeypatch: pytest.MonkeyPatch, name: str, value: Union[str, None]
) -> None:
    if value is None:
        monkeypatch.delenv(name, raising=False)
    else:
        monkeypatch.setenv(name, value)


@pytest.mark.parametrize(
    "env_cov_name",
    [
        pytest.param("vllm", id="value:vllm"),
        pytest.param("", id="empty"),
        pytest.param(None, id="unset"),
    ],
)
def test_generate_coverage_flags_set(
    monkeypatch: pytest.MonkeyPatch, env_cov_name: EnvVarValue
):
    _setenv(monkeypatch, "NMRE_COV_NAME", env_cov_name)

    if env_cov_name in (None, ""):
        expected_flags = []
    else:
        expected_flags = [
            f"--cov={env_cov_name}",
            "--cov-append",
            "--cov-report=html:coverage-html",
            "--cov-report=json:coverage.json",
        ]

    result = generate_coverage_flags()
    assert result == expected_flags


@pytest.mark.parametrize(
    ("env_junit_base", "env_junit_prefix"),
    [
        pytest.param("test-results", "run-", id="base-with-prefix"),
        pytest.param("test-results", "", id="base-with-empty-prefix"),
        pytest.param("test-results", None, id="base-with-unset-prefix"),
        pytest.param("", "run-", id="empty-base-with-prefix"),
        pytest.param("", "", id="empty-base-with-empty-prefix"),
        pytest.param("", None, id="empty-base-with-unset-prefix"),
        pytest.param(None, "run-", id="unset-base-with-prefix"),
        pytest.param(None, "", id="unset-base-with-empty-prefix"),
        pytest.param(None, None, id="unset-base-with-unset-prefix"),
    ],
)
def test_generate_junit_flags(
    monkeypatch: pytest.MonkeyPatch,
    env_junit_base: EnvVarValue,
    env_junit_prefix: EnvVarValue,
):
    _setenv(monkeypatch, "NMRE_JUNIT_BASE", env_junit_base)
    _setenv(monkeypatch, "NMRE_JUNIT_PREFIX", env_junit_prefix)

    result = generate_junit_flags()

    if env_junit_base in (None, ""):
        assert result == []
        return

    # basic assertions
    assert len(result) == 1
    flag = result[0]
    assert flag.startswith("--junit-xml")
    assert flag.endswith(".xml")

    # assertions about flag value structure
    value = flag[12:]
    assert os.sep in value

    # assertions about flag value contents
    fpath, fname = value.rsplit(os.sep, 1)
    assert fpath == env_junit_base

    pattern = r"\d{10,}\.\d+\.xml"
    if env_junit_prefix not in (None, ""):
        pattern = f"{env_junit_prefix}{pattern}"

    pattern = re.compile(pattern)
    assert pattern.fullmatch(fname)
