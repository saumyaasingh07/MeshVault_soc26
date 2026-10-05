"""
Unit tests for MeshVault CLI with Typer framework, shell auto-completion, and UX error handling.
"""

import pytest
from typer.testing import CliRunner
from cli.__main__ import app, complete_interface, complete_alias

runner = CliRunner()


def test_cli_split_command_success():
    result = runner.invoke(
        app, ["split", "--threshold", "3", "--shares", "5", "--interface", "eth0"]
    )
    assert result.exit_code == 0
    assert "MeshVault Command Line Interface" in result.output
    assert "Command selected: split" in result.output
    assert "Threshold (K): 3, Shares (N): 5" in result.output
    assert "Interface: eth0" in result.output


def test_cli_recover_command_success():
    result = runner.invoke(app, ["recover", "-k", "3", "-p", "5050"])
    assert result.exit_code == 0
    assert "MeshVault Command Line Interface" in result.output
    assert "Command selected: recover" in result.output
    assert "Threshold (K): 3, Port: 5050" in result.output


def test_cli_completion_bash():
    result = runner.invoke(app, ["completion", "bash"])
    assert result.exit_code == 0
    assert "# MeshVault Bash Completion" in result.output
    assert "complete -F _meshvault_completion meshvault" in result.output


def test_cli_completion_zsh():
    result = runner.invoke(app, ["completion", "zsh"])
    assert result.exit_code == 0
    assert "#compdef meshvault" in result.output
    assert "# MeshVault Zsh Completion" in result.output


def test_cli_completion_fish():
    result = runner.invoke(app, ["completion", "fish"])
    assert result.exit_code == 0
    assert "# MeshVault Fish Completion" in result.output


def test_cli_completion_powershell():
    result = runner.invoke(app, ["completion", "powershell"])
    assert result.exit_code == 0
    assert "# MeshVault PowerShell Completion" in result.output


def test_cli_completion_invalid_shell():
    result = runner.invoke(app, ["completion", "unsupported_shell"])
    assert result.exit_code != 0
    assert "Unsupported shell" in result.output


def test_complete_interface_helper():
    matches = complete_interface("eth")
    assert "eth0" in matches
    assert "wlan0" not in matches


def test_complete_alias_helper():
    matches = complete_alias("")
    assert isinstance(matches, list)
