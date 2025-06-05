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

import argparse


def generate_coverage_flags(package: str, output_file: str = ".coverage_env.sh"):
    coverage_flags = (
        f"--cov={package} "
        "--cov-append "
        "--cov-report=term "
        "--cov-report=json "
        "--cov-report=html:coverage-html"
    )

    with open(output_file, "w") as f:
        f.write(f'export PYTEST_ADDOPTS="{coverage_flags}"\n')

    print(f"Coverage flags written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Generate pytest coverage flags.")
    parser.add_argument("--package", required=True, help="Name of the package to cover")
    parser.add_argument(
        "--output-file",
        default=".coverage_flags.sh",
        help="Output file to write the export command",
    )
    args = parser.parse_args()

    generate_coverage_flags(args.package, args.output_file)
