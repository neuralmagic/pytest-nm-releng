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

from pytest_nm_releng.plugin import generate_junit_flags
from tests.utils import setenv

EnvVarValue = Union[str, None]

SUFFIX_PATTERN_MAP = {
    "timestamp": r"\d{10,}\.\d+\.xml",
    "uuid4": r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\.xml",
    "uuid7": r"[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\.xml",
}
DEFAULT_SUFFIX_PATTERN = SUFFIX_PATTERN_MAP["timestamp"]


@pytest.mark.parametrize(
    ("env_junit_base", "env_junit_prefix", "env_junit_suffix"),
    [
        # base path present
        pytest.param("test-results", "run-", "", id="base-with-prefix"),
        pytest.param("test-results", "", "", id="base-with-empty-prefix"),
        pytest.param("test-results", None, "", id="base-with-unset-prefix"),
        # base path empty
        pytest.param("", "run-", "", id="empty-base-with-prefix"),
        pytest.param("", "", "", id="empty-base-with-empty-prefix"),
        pytest.param("", None, "", id="empty-base-with-unset-prefix"),
        # base path unset
        pytest.param(None, "run-", "", id="unset-base-with-prefix"),
        pytest.param(None, "", "", id="unset-base-with-empty-prefix"),
        pytest.param(None, None, "", id="unset-base-with-unset-prefix"),
        # suffix empty/unset
        pytest.param("test-results", "", None, id="unset-suffix-type"),
        pytest.param("test-results", "", "", id="empty-suffix-type"),
        # suffix type variants
        pytest.param("test-results", "", "timestamp", id="suffix-timestamp"),
        pytest.param("test-results", "", "uuid4", id="suffix-uuid4"),
        pytest.param("test-results", "", "uuid7", id="suffix-uuid7"),
    ],
)
def test_generate_junit_flags(
    monkeypatch: pytest.MonkeyPatch,
    env_junit_base: EnvVarValue,
    env_junit_prefix: EnvVarValue,
    env_junit_suffix: EnvVarValue,
):
    setenv(monkeypatch, "NMRE_JUNIT_BASE", env_junit_base)
    setenv(monkeypatch, "NMRE_JUNIT_PREFIX", env_junit_prefix)
    setenv(monkeypatch, "NMRE_JUNIT_SUFFIX_TYPE", env_junit_suffix)

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

    pattern = SUFFIX_PATTERN_MAP.get(str(env_junit_suffix), DEFAULT_SUFFIX_PATTERN)
    if env_junit_prefix not in (None, ""):
        pattern = f"{env_junit_prefix}{pattern}"

    pattern = re.compile(pattern)
    assert pattern.fullmatch(fname)
