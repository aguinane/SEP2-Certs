import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from sep2cert.cli import app


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_version(runner):
    result = runner.invoke(app, ["--version"])
    assert "sep2cert version:" in result.stdout
    assert result.exit_code == 0


def test_cli_get_lfdi(runner):
    file_name = "example-certs/example-ABC-cert.pem"
    result = runner.invoke(app, ["info", file_name])
    expected_lfdi = "CA6A-EDC0-3021-4C70-B798-89EF-B8E5-D8CD-244D-CDAA"
    assert f"The LFDI is: {expected_lfdi}" in result.stdout
    expected_sfdi = "543-360-849-954"
    assert f"The SFDI is: {expected_sfdi}" in result.stdout
    assert result.exit_code == 0


def test_cli_create_serca(runner):
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(app, ["create-serca", "--output-dir", tmpdir])
        assert result.exit_code == 0

        exp_file = Path(tmpdir) / "serca.pem"
        assert exp_file.exists()


def test_cli_create_full_chain(runner):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a SERCA certificate
        result = runner.invoke(app, ["create-serca", "--output-dir", tmpdir])
        assert result.exit_code == 0

        serca_key = Path(tmpdir) / "serca.key"
        serca_cert = Path(tmpdir) / "serca.pem"
        assert serca_key.exists()
        assert serca_cert.exists()

        # Create a MICA key and CSR
        mica_key = Path(tmpdir) / "mica.key"
        result = runner.invoke(app, ["create-key", str(mica_key)])
        assert result.exit_code == 0
        assert mica_key.exists()

        mica_csr = Path(tmpdir) / "mica.csr"
        result = runner.invoke(
            app,
            [
                "create-csr",
                str(mica_key),
                "--org-name",
                "Example Org",
                "--country-name",
                "AU",
                "--common-name",
                "IEEE 2030.5 MICA",
                "--serial-no",
                "1",
            ],
        )
        assert result.exit_code == 0
        assert mica_csr.exists()

        # Create a MICA certificate signed by the SERCA
        result = runner.invoke(
            app, ["create-mica", str(mica_csr), str(serca_cert), str(serca_key)]
        )
        mica_cert = Path(tmpdir) / "mica.pem"
        assert result.exit_code == 0
        assert mica_cert.exists()
