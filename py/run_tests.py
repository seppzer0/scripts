"""
Script to run tests according to configuration in pyproject.toml.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Literal
from subprocess import CompletedProcess

ROOTPATH: Path = Path(__file__).absolute().parents[3]
INTERPRETER: str = "python" if sys.platform.startswith("win") else "python3"


class Tester:
    """Single class for all types of tests."""

    @staticmethod
    def _launch_cmd(cmd: str) -> CompletedProcess:
        """Launch specified command."""
        return subprocess.run(cmd, shell=True, check=True)

    @staticmethod
    def _step_message(tool: str, step: Literal["start", "finish"]) -> str:
        """Return message of test's start or finish."""
        print(f'\n=== {tool.capitalize()} checks: {"Start" if step == "start" else "Finish"} ===')

    def pyright_check(self) -> None:
        """Run static typing checks with Pyright."""
        tool = "pyright"

        self._step_message(tool, "start")
        self._launch_cmd(f"{INTERPRETER} -m pyright")
        self._step_message(tool, "finish")

    def pytest_check(self) -> None:
        """Run unit tests with Pytest and coverage checks."""
        tool = "pytest"

        # for internal imports to be recognized
        os.environ["PYTHONPATH"] = str(ROOTPATH)

        self._step_message(tool, "start")
        self._launch_cmd(f"{INTERPRETER} -m pytest -vv tests/ --cov")
        self._step_message(tool, "finish")

    def bandit_check(self) -> None:
        """Run SAST with Bandit."""
        tool = "bandit"

        self._step_message(tool, "start")
        fmts = {"json", "html"}
        for fmt in fmts:
            self._launch_cmd(f"{INTERPRETER} -m bandit -r -f {fmt} {ROOTPATH} -o report.{fmt}")
        self._step_message(tool, "finish")

    def ruff_check(self) -> None:
        """Run linting with Ruff."""
        tool = "ruff"

        self._step_message(tool, "start")
        self._launch_cmd(f"{INTERPRETER} -m ruff check")
        self._step_message(tool, "finish")


def main() -> None:
    os.chdir(ROOTPATH)
    t = Tester()
    t.pyright_check()
    t.pytest_check()
    t.ruff_check()
    #t.bandit_check()


if __name__ == "__main__":
    main()
