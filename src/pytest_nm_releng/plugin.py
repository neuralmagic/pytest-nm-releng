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
from datetime import datetime, timezone
from pathlib import Path


def get_utc_timestamp() -> float:
    return datetime.now(timezone.utc).timestamp()


def generate_junit_flags() -> list[str]:
    if not (junitxml_base_dir := os.getenv("PDRN_JUNIT_BASE")):
        return []

    junitxml_file = Path(junitxml_base_dir) / f"{get_utc_timestamp()}.xml"

    if prefix := os.getenv("PDRN_JUNIT_PREFIX"):
        junitxml_file = junitxml_file.with_name(f"{prefix}{junitxml_file.name}")

    return [f"--junit-xml={junitxml_file.as_posix()}"]


def generate_coverage_flags() -> list[str]:
    if not (cc_package_name := os.getenv("PDRN_COV_NAME")):
        return []

    return [
        f"--cov={cc_package_name}",
        "--cov-append",
        "--cov-report=html:coverage-html",
        "--cov-report=json:coverage.json",
    ]


def pytest_load_initial_conftests(early_config, args: list[str], parser):
    new_args: list[str] = []
    new_args.extend(generate_junit_flags())
    new_args.extend(generate_coverage_flags())
    args[:] = [*args, *new_args]
