import os
from pathlib import Path

def generate_coverage_env(cc_package_name: str = None):
    if not cc_package_name:
        cc_package_name = os.getenv("NMRE_COV_NAME")
    
    if not cc_package_name:
        print("NMRE_COV_NAME not set. Cannot write coverage flags.")
        return

    coverage_flags = (
        f"--cov={cc_package_name} "
        "--cov-append "
        "--cov-report=term "
        "--cov-report=json "
        "--cov-report=html:coverage-html"
    )

    project_root = Path.cwd()
    coverage_env_path = project_root / ".coverage_env.sh"

    with open(coverage_env_path, "w") as f:
        f.write(f'export PYTEST_ADDOPTS="{coverage_flags}"\n')

    print(f"Coverage flags written to: {coverage_env_path}")