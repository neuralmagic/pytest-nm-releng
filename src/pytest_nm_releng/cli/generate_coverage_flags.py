import argparse
from pathlib import Path

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

    print(f"Coverage flags written to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate pytest coverage flags.")
    parser.add_argument(
        "--package",
        required=True,
        help="Name of the package to cover"
    )
    parser.add_argument(
        "--output-file",
        default=".coverage_flags.sh",
        help="Output file to write the export command"
    )
    args = parser.parse_args()

    generate_coverage_flags(args.package, args.output_file)