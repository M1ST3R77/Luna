from datetime import datetime
import os
import subprocess
import sys
import io
import coverage
import unittest
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "docs", "reports", "test_reports")
COVERAGE_DIR = os.path.join(PROJECT_ROOT, "docs", "reports", "coverage")
FUNCTIONAL_DIR = os.path.join(PROJECT_ROOT, "tests", "functional")
UNITAIRES_DIR = os.path.join(PROJECT_ROOT, "tests", "unitaires")

def run_functional_tests(functional_dir, debug_output):
    """Runs functional tests located in the given directory.

    :param str functional_dir: Path to the functional test directory.
    :param bool debug_output: If True, enables debug output.
    :return: A dictionary containing test results summary.
    """
    results = {"success": 0, "fail": 0, "crash": 0, "details": []}

    for root, _, files in os.walk(functional_dir):
        for file in files:
            if file == "return_tester.py":
                continue
            if file.endswith(".py") and file != "__init__.py":
                test_path = os.path.join(root, file)
                try:
                    result = subprocess.run(
                        ["python", test_path, "-d" if debug_output else ""],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if debug_output:
                        print(result.stdout, end="")
                        print(result.stderr)

                    if result.returncode == 0:
                        results["success"] += 1
                        results["details"].append(f"[SUCCESS] {test_path} : {result.stdout.splitlines()[-1]}")
                    else:
                        results["fail"] += 1
                        results["details"].append(f"[FAIL] {test_path} : {result.stderr.splitlines()[-1]}")
                except Exception as e:
                    results["crash"] += 1
                    results["details"].append(f"[CRASH] {test_path} : {str(e)}")
    return results

def run_unit_tests(unit_dir, debug_output):
    """Runs unit tests and generates coverage report.

    :param str unit_dir: Path to the unit test directory.
    :param bool debug_output: If True, enables debug output.
    :return: A dictionary containing test results summary.
    """
    results = {"success": 0, "fail": 0, "crash": 0, "details": []}
    cov = coverage.Coverage()
    cov.start()
    loader = unittest.TestLoader()
    suite = loader.discover(unit_dir)

    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, verbosity=2)
    result = runner.run(suite)

    if debug_output:
        print(buffer.getvalue(), end="")

    results["success"] = result.testsRun - len(result.failures) - len(result.errors)
    results["fail"] = len(result.failures)
    results["crash"] = len(result.errors)

    for line in buffer.getvalue().splitlines():
        if "ok" in line:
            test_name = line.split(" ... ")[0]
            results["details"].append(f"[SUCCESS] {test_name}")
        elif "FAIL" in line:
            test_name = line.split(" ... ")[0]
            results["details"].append(f"[FAIL] {test_name}")
    
    cov.stop()
    cov.save()
    if os.path.exists(COVERAGE_DIR):
        shutil.rmtree(COVERAGE_DIR)
    os.makedirs(COVERAGE_DIR, exist_ok=True)
    cov.html_report(directory=COVERAGE_DIR)
    if os.path.exists(os.path.join(PROJECT_ROOT, ".coverage")):
        os.remove(os.path.join(PROJECT_ROOT, ".coverage"))
    print(f"Coverage html saved to {COVERAGE_DIR}")
    return results

def save_report(results_functional, results_unitaires):
    """Saves the test results to a report file.

    :param dict results_functional: Results dictionary from functional tests.
    :param dict results_unitaires: Results dictionary from unit tests.
    """
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
    report_path = os.path.join(REPORTS_DIR, f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(report_path, "w", encoding='utf-8') as report_file:
        report_file.write("=== Functional Test Report ===\n")
        report_file.write(f"Success: {results_functional['success']}\n")
        report_file.write(f"Fail: {results_functional['fail']}\n")
        report_file.write(f"Crash: {results_functional['crash']}\n")
        report_file.write("\nDetails:\n")
        report_file.write("\n".join(results_functional["details"]))
        report_file.write("\n\n")

        report_file.write("=== Unit Test Report ===\n")
        report_file.write(f"Success: {results_unitaires['success']}\n")
        report_file.write(f"Fail: {results_unitaires['fail']}\n")
        report_file.write(f"Crash: {results_unitaires['crash']}\n")
        report_file.write("\nDetails:\n")
        report_file.write("\n".join(results_unitaires["details"]))
        report_file.write("\n")
    print(f"Report saved to {report_path}")

def main():
    """
    Main function that executes the functional and unit tests, and saves reports.
    """
    debug_output = "-d" in sys.argv
    if not os.path.exists(FUNCTIONAL_DIR):
        print(f"Error: Directory '{FUNCTIONAL_DIR}' does not exist.")
        sys.exit(1)
    if not os.path.exists(UNITAIRES_DIR):
        print(f"Error: Directory '{UNITAIRES_DIR}' does not exist.")
        sys.exit(1)

    results_functional = run_functional_tests(FUNCTIONAL_DIR, debug_output)
    results_unitaires = run_unit_tests(UNITAIRES_DIR, debug_output)

    save_report(results_functional, results_unitaires)

    if (results_functional["fail"] + results_functional["crash"] +
            results_unitaires["fail"] + results_unitaires["crash"]) == 0:
        sys.exit(0)
    else:
        sys.exit(84)

if __name__ == "__main__":
    main()