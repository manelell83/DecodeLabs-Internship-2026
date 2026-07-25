"""Tests for CommandRunner error handling, using cross-platform commands (not PowerShell)."""

import sys

import pytest

from app.services.audit.command_runner import CommandError, CommandRunner


def test_run_shell_returns_stdout_on_success():
    runner = CommandRunner()
    output = runner.run_shell([sys.executable, "-c", "print('hello')"])
    assert output == "hello"


def test_run_shell_raises_on_nonzero_exit():
    runner = CommandRunner()
    with pytest.raises(CommandError):
        runner.run_shell([sys.executable, "-c", "import sys; sys.exit(1)"])


def test_run_shell_raises_on_missing_command():
    runner = CommandRunner()
    with pytest.raises(CommandError):
        runner.run_shell(["this-command-does-not-exist-anywhere"])


def test_run_shell_raises_on_timeout():
    runner = CommandRunner(timeout_seconds=1)
    with pytest.raises(CommandError):
        runner.run_shell([sys.executable, "-c", "import time; time.sleep(5)"])
