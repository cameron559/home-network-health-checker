import socket
from unittest.mock import patch

from health_checker import (
    get_status_counts,
    get_health_percentage,
    get_health_status,
    has_failures,
    get_reachable_hosts,
    get_unreachable_hosts,
    resolve_hostname,
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
