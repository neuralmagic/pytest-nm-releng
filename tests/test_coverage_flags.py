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

import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pytest_nm_releng.cli import generate_coverage_flags


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
            "generate_coverage_flags",
            "--package",
            package_name,
            "--output-file",
            str(output_path),
        ]

        with patch.object(sys, "argv", test_args):
            generate_coverage_flags.main()

        assert output_path.exists()

        content = output_path.read_text()
        assert expected_flag in content
