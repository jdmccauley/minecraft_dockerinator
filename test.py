# The purpose of this script is to run tests and get coverage.

# Native libraries
import subprocess
import os

def main():
    """
    Runs pytest through coverage, and outputs the test results alongside test
    coverage. The output is saved to coverage.json for linter support.
    """
    # Run pytest through coverage.
    subprocess.run(
        "coverage run -m pytest"
    )
    # Generate coverage report.
    subprocess.run(
        "coverage report -m"
    )
    # Save coverage report to json.
    subprocess.run(
        "coverage json --pretty-print"
    )