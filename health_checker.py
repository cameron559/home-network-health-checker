import subprocess
import json
from datetime import datetime


def is_reachable(address: str) -> bool:
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", address], capture_output=True
        )

        return result.returncode == 0

    except OSError:
        return False


def log_health_check(name: str, address: str, status: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("health_checks.log", "a") as file:
        file.write(f"{timestamp} | {name} | {address} | {status}\n")


def log_summary(
    reachable: int, unreachable: int, total: int, percentage: float
) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("health_checks.log", "a") as file:
        file.write(
            f"{timestamp} | Summary | "
            f"Reachable: {reachable} | "
            f"Unreachable: {unreachable} | "
            f"Total: {total} | "
            f"Reachable percentage: {percentage:.1f}%\n"
        )


def get_unreachable_hosts(hosts: dict) -> list:
    return [host for host, status in hosts.items() if not status]


def get_reachable_hosts(hosts: dict) -> list:
    return [host for host, status in hosts.items() if status]


def get_status_counts(hosts: dict) -> dict:
    reachable_count = sum(hosts.values())
    unreachable_count = len(hosts) - reachable_count
    return {"reachable": reachable_count, "unreachable": unreachable_count}


def get_health_percentage(hosts: dict) -> float:
    if not hosts:
        return 0.0
    reachable_hosts = sum(hosts.values())
    return round(reachable_hosts / len(hosts) * 100, 1)


def get_health_status(hosts: dict) -> str:
    health_percentage = get_health_percentage(hosts)

    if health_percentage >= 80:
        return "Healthy"

    if health_percentage >= 50:
        return "Degraded"

    return "Critical"


def has_failures(hosts: dict) -> bool:
    return not all(hosts.values())


def format_health_summary(hosts: dict) -> str:
    health_status = get_health_status(hosts)
    status_counts = get_status_counts(hosts)
    availability = get_health_percentage(hosts)

    return (
        f"Health: {health_status} | "
        f"Reachable: {status_counts['reachable']} | "
        f"Unreachable: {status_counts['unreachable']} | "
        f"Availability: {availability}%"
    )


def load_hosts() -> dict:
    try:
        with open("config.json", "r") as file:
            config = json.load(file)

        hosts = config["hosts"]

        if not isinstance(hosts, dict):
            print("Error: hosts must be a dictionary.")
            raise SystemExit(1)

    except FileNotFoundError:
        print("Error: config.json was not found.")
        raise SystemExit(1)

    except json.JSONDecodeError:
        print("Error: config.json contains invalid JSON.")
        raise SystemExit(1)

    except KeyError:
        print("Error: config.json is missing the hosts section.")
        raise SystemExit(1)

    if not hosts:
        print("No hosts configured.")
        raise SystemExit(1)

    return hosts


def main() -> None:
    hosts = load_hosts()
    host_statuses = {}

    for name, address in hosts.items():
        reachable = is_reachable(address)
        status = "reachable" if reachable else "unreachable"

        host_statuses[name] = reachable

        print(f"{name} ({address}) is {status}")
        log_health_check(name, address, status)

    status_counts = get_status_counts(host_statuses)

    reachable_percentage = get_health_percentage(host_statuses)

    log_summary(
        status_counts["reachable"],
        status_counts["unreachable"],
        len(host_statuses),
        reachable_percentage,
    )

    print(format_health_summary(host_statuses))
    unreachable_hosts = get_unreachable_hosts(host_statuses)
    reachable_hosts = get_reachable_hosts(host_statuses)

    if unreachable_hosts:
        print(f"Unreachable hosts: {', '.join(unreachable_hosts)}")

    if reachable_hosts:
        print(f"Reachable hosts: {', '.join(reachable_hosts)}")

    if has_failures(host_statuses):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
