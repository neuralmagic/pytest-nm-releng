# Copyright (c) 2025 - present / Redhat, Inc. All Rights Reserved.
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

import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pytest_nm_releng.cli.generate_coverage_flags import generate_coverage_flags, main


@pytest.mark.parametrize(
    "package_name, expected_flag",
    [
        ("vllm", "--cov=vllm"),
        ("my_lib", "--cov=my_lib"),
    ],
)
def test_generate_coverage_flags_to_file(package_name, expected_flag):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "coverage-flags.sh"

        test_args = [
            "nmre-generate-coverage-flags",
            "--package",
            package_name,
            "--output-file",
            str(output_path),
        ]

        with patch.object(sys, "argv", test_args):
            main()

        assert output_path.exists(), "Coverage flags output file was not created."

        content = output_path.read_text()
        assert (
            expected_flag in content
        ), f"Expected flag '{expected_flag}' not found in:\n{content}"
        assert (
            "${PYTEST_ADDOPTS:-}" in content
        ), "Expected '${PYTEST_ADDOPTS:-}' to be present in:\n{content}"


@pytest.mark.parametrize(
    "package_name, expected_flag",
    [
        ("vllm", "--cov=vllm"),
        ("custom_lib", "--cov=custom_lib"),
    ],
)
def test_generate_coverage_flags_function(package_name, expected_flag):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "cov-flags.sh"

        generate_coverage_flags(package=package_name, output_file=str(output_path))

        assert output_path.exists()

        content = output_path.read_text()
        assert expected_flag in content
        assert "--cov-append" in content
        assert "--cov-report=html:coverage-html" in content
        assert "${PYTEST_ADDOPTS:-}" in content


@pytest.mark.parametrize(
    "package_name, expected_flag",
    [
        ("vllm", "--cov=vllm"),
    ],
)
def test_nmre_generate_coverage_flags_e2e(package_name, expected_flag):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = Path(tmpdir) / "coverage-env.sh"

        result = subprocess.run(
            [
                "nmre-generate-coverage-flags",
                "--package",
                package_name,
                "--output-file",
                str(output_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"CLI failed with stderr:\n{result.stderr}"
        assert output_file.exists(), "Output file was not created"

        content = output_file.read_text()
        assert expected_flag in content, f"Missing expected flag: {expected_flag}"
        assert "--cov-append" in content
        assert "--cov-report=json" in content
        assert "${PYTEST_ADDOPTS:-}" in content
