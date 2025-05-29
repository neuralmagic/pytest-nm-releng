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


# add CLI options to pass properties for test cases/suites
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


def pytest_configure(config):
    """
    Pytest hook that runs during pytest startup.
    It checks for the NMRE_COV_NAME environment variable and injects code coverage flags
    into the pyproject.toml file of the calling project.
    """
    package_name = os.getenv("NMRE_COV_NAME")
    if not package_name:
        return  

    addopts_value = f"--cov={package_name} --cov-append --cov-report=term --cov-report=html --cov-report=json"

    pyproject_path = Path.cwd() / "pyproject.toml"
    if not pyproject_path.exists():
        print(f"pyproject.toml not found in {Path.cwd()}")
        return

    with pyproject_path.open("r") as f:
        data = toml.load(f)

    tool = data.setdefault("tool", {})
    pytest_config = tool.setdefault("pytest", {})
    ini_options = pytest_config.setdefault("ini_options", {})

    # Only update if different
    if ini_options.get("addopts") != addopts_value:
        ini_options["addopts"] = addopts_value
        with pyproject_path.open("w") as f:
            toml.dump(data, f)
        print(f"Updated code coverage addopts in {pyproject_path}")
    else:
        print(f"Coverage addopts already set in {pyproject_path}")

    