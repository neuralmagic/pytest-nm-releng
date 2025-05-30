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

from typing import Callable

import pytest
import os
import toml
from pathlib import Path

from .lib import generate_junit_flags


def pytest_load_initial_conftests(early_config, args: list[str], parser):
    new_args: list[str] = []
    new_args.extend(generate_junit_flags())
    new_args.extend(generate_coverage_flags())
    args[:] = [*args, *new_args]
    print(f"[plugin] Injected CLI args: {' '.join(new_args)}")
    

# Hook to add custom CLI options
def pytest_addoption(parser: pytest.Parser, pluginmanager):
    parser.addoption(
        "--testcase-property",
        dest="testcase_property",
        nargs="*",
        help="property to add to all test cases (can pass multiple separated values)",
    )
    parser.addoption(
        "--testsuite-property",
        dest="testsuite_property",
        nargs="*",
        help="property to add to test suite (can pass multiple separated values)",
    )
    
# use pytest hook to add properties to testcase
def pytest_collection_modifyitems(
    session: pytest.Session, config: pytest.Config, items: list[pytest.Item]
):
    if not (properties := config.getoption("testcase_property")):
        return
    for item in items:
        for property in properties:
            name, val = property.split("=", maxsplit=1)
            item.user_properties.append((name, val))


# use fixture to add properties to testsuite
@pytest.fixture(autouse=True, scope="session")
def add_testsuite_property(
    request: pytest.FixtureRequest,
    record_testsuite_property: Callable[[str, object], None],
):
    if not (suite_properties := request.config.getoption("testsuite_property")):
        return
    for property in suite_properties:
        name, value = property.split("=", maxsplit=1)
        record_testsuite_property(name, value)    

# Find project root by walking up to locate pyproject.toml
def find_project_root(filename="pyproject.toml") -> Path:
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        candidate = parent / filename
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"{filename} not found in any parent directory of {current}"
    )

def generate_coverage_flags() -> list[str]:
    cc_package_name = os.getenv("NMRE_COV_NAME")
    if not cc_package_name:
        print("[plugin] NMRE_COV_NAME not set.")
        return []

    flags = [
        f"--cov={cc_package_name}",
        "--cov-append",
        "--cov-report=term",
        "--cov-report=json",
        "--cov-report=html:coverage-html",
    ]

    print(f"[plugin] Coverage flags to ensure: {' '.join(flags)}")

    # Load pyproject.toml
    pyproject_path = find_project_root()
    data = toml.load(pyproject_path)

    # Navigate or create the necessary structure
    tool = data.setdefault("tool", {})
    pytest = tool.setdefault("pytest", {})
    ini_options = pytest.setdefault("ini_options", {})

    old_addopts = ini_options.get("addopts", "")
    old_flags = old_addopts.split() if isinstance(old_addopts, str) else []

    # Only add flags if any are missing
    if all(flag in old_flags for flag in flags):
        print("[plugin] All coverage flags already present. Skipping update.")
    else:
        updated_flags = list(dict.fromkeys(old_flags + flags))
        ini_options["addopts"] = " ".join(updated_flags)

        with pyproject_path.open("w", encoding="utf-8") as f:
            toml.dump(data, f)

        print("[plugin] Added coverage flags to pyproject.toml.")


    return flags



