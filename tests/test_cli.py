"""Tests for CLI."""

import re

from typer.testing import CliRunner

from dhis2_era5land.cli import app

runner = CliRunner()


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def test_cli_help() -> None:
    """Test that CLI shows help with --help."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Import ERA5-Land climate data into DHIS2" in result.stdout


def test_cli_no_args_shows_help() -> None:
    """Test that CLI shows help by default when no args."""
    result = runner.invoke(app, [])
    # no_args_is_help returns exit code 0 for typer
    assert "Import ERA5-Land climate data into DHIS2" in result.stdout


def test_cli_run_help() -> None:
    """Test that run command shows help."""
    result = runner.invoke(app, ["run", "--help"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert "Run the ERA5-Land to DHIS2 import" in output
    assert "--start-date" in output
    assert "--dry-run" in output


def test_cli_serve_help() -> None:
    """Test that serve command shows help."""
    result = runner.invoke(app, ["serve", "--help"])
    assert result.exit_code == 0
    output = strip_ansi(result.stdout)
    assert "Start the API server" in output
    assert "--host" in output
    assert "--port" in output
