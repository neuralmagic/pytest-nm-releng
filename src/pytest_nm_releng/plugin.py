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


def generate_coverage_flags() -> list[str]:
    cc_package_name = os.getenv("NMRE_COV_NAME")
    if not cc_package_name:
        return []

    flags = [
        f"--cov={cc_package_name}",
        "--cov-append",
        "--cov-report=term",
        "--cov-report=html:coverage-html",
        "--cov-report=json:coverage.json",
    ]

    print(f"Coverage flags generated from plugin: {' '.join(flags)}")
    return flags

    