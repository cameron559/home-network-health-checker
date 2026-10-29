import json
import socket
from unittest.mock import patch

import pytest

from health_checker import (
    get_status_counts,
    get_health_percentage,
    get_health_status,
    has_failures,
    get_reachable_hosts,
    get_unreachable_hosts,
    resolve_hostname,
    load_hosts,
)


def test_get_status_counts():
    hosts = {
        "Router": True,
        "Google DNS": True,
        "Test Host": False,
    }

    result = get_status_counts(hosts)

    assert result["reachable"] == 2
    assert result["unreachable"] == 1


def test_get_health_percentage():
    hosts = {
        "Router": True,
        "Google DNS": True,
        "Test Host": False,
    }

    result = get_health_percentage(hosts)

    assert result == 66.7


def test_get_health_status():
    hosts = {
        "Router": True,
        "Google DNS": True,
        "Test Host": False,
    }

    result = get_health_status(hosts)

    assert result == "Degraded"


def test_has_failures():
    hosts = {
        "Router": True,
        "Google DNS": True,
        "Test Host": False,
    }

    result = has_failures(hosts)

    assert result is True


def test_get_health_percentage_empty_hosts():
    hosts = {}

    result = get_health_percentage(hosts)

    assert result == 0.0


def test_get_health_status_healthy():
    hosts = {
        "Router": True,
        "Google DNS": True,
        "Cloudflare DNS": True,
    }

    assert get_health_status(hosts) == "Healthy"


def test_get_health_status_critical():
    hosts = {
        "Router": False,
        "Google DNS": False,
        "Cloudflare DNS": True,
    }

    assert get_health_status(hosts) == "Critical"


def test_get_reachable_hosts():
    hosts = {
        "Router": True,
        "Google DNS": True,
        "Test Host": False,
    }

    result = get_reachable_hosts(hosts)

    assert result == ["Router", "Google DNS"]


def test_get_unreachable_hosts():
    hosts = {
        "Router": True,
        "Google DNS": True,
        "Test Host": False,
    }

    result = get_unreachable_hosts(hosts)

    assert result == ["Test Host"]


def test_resolve_hostname_success():
    with patch("health_checker.socket.gethostbyname") as mock_gethostbyname:
        mock_gethostbyname.return_value = "93.184.216.34"

        result = resolve_hostname("example.com")

        assert result == "93.184.216.34"


def test_resolve_hostname_failure():
    with patch("health_checker.socket.gethostbyname") as mock_gethostbyname:
        mock_gethostbyname.side_effect = socket.gaierror

        result = resolve_hostname("example.com")

        assert result is None


@pytest.mark.parametrize(
    "config, message",
    [
        ([], "must contain a JSON object"),
        (None, "must contain a JSON object"),
        ("text", "must contain a JSON object"),
        (123, "must contain a JSON object"),
        (True, "must contain a JSON object"),
        ({}, "missing the hosts section"),
        ({"hosts": []}, "hosts must be a dictionary"),
        ({"hosts": None}, "hosts must be a dictionary"),
        ({"hosts": "router"}, "hosts must be a dictionary"),
        ({"hosts": 123}, "hosts must be a dictionary"),
        ({"hosts": True}, "hosts must be a dictionary"),
        ({"hosts": {}}, "No hosts configured"),
    ],
)
def test_load_hosts_invalid_structure(config, message, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config.json").write_text(json.dumps(config), encoding="utf-8")

    with pytest.raises(SystemExit) as error:
        load_hosts()

    assert error.value.code == 1
    assert message in capsys.readouterr().out


@pytest.mark.parametrize("address", [None, 123, True, [], {}, "", " \t\n"])
def test_load_hosts_invalid_address(address, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    config = {"hosts": {"Valid": "192.168.0.1", "Invalid": address}}
    (tmp_path / "config.json").write_text(json.dumps(config), encoding="utf-8")

    with pytest.raises(SystemExit) as error:
        load_hosts()

    assert error.value.code == 1
    output = capsys.readouterr().out
    assert "host 'Invalid'" in output
    assert "nonempty string containing non-whitespace characters" in output


def test_load_hosts_valid_configuration(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    hosts = {"Router": "192.168.0.1", "DNS": "example.com", "Padded": " example.com "}
    (tmp_path / "config.json").write_text(json.dumps({"hosts": hosts}), encoding="utf-8")

    assert load_hosts() == hosts


def test_load_hosts_invalid_json(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config.json").write_text('{"hosts":', encoding="utf-8")

    with pytest.raises(SystemExit) as error:
        load_hosts()

    assert error.value.code == 1
    assert "contains invalid JSON" in capsys.readouterr().out
