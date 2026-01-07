"""Tests for CLI."""

from typer.testing import CliRunner

from dhis2_era5land.cli import app

runner = CliRunner(mix_stderr=False, color=False)


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
    assert "Run the ERA5-Land to DHIS2 import" in result.stdout
    assert "--start-date" in result.stdout
    assert "--dry-run" in result.stdout


def test_cli_serve_help() -> None:
    """Test that serve command shows help."""
    result = runner.invoke(app, ["serve", "--help"])
    assert result.exit_code == 0
    assert "Start the API server" in result.stdout
    assert "--host" in result.stdout
    assert "--port" in result.stdout
