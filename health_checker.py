import subprocess
import json
from datetime import datetime

try:
    with open("config.json", "r") as file:
        config = json.load(file)

    addresses = config["hosts"]

    if not isinstance(addresses, dict):
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


if not addresses:
    print("No hosts configured.")
    raise SystemExit(1)

reachable_addresses = 0

for name, address in addresses.items():
    reachable = is_reachable(address)
    status = "reachable" if reachable else "unreachable"

    print(f"{name} ({address}) is {status}")
    log_health_check(name, address, status)

    if reachable:
        reachable_addresses += 1

unreachable_addresses = len(addresses) - reachable_addresses
reachable_percentage = (reachable_addresses / len(addresses)) * 100

if not unreachable_addresses:
    overall_status = "HEALTHY"
else:
    overall_status = "DEGRADED"


def get_unreachable_hosts(hosts: dict) -> list:
    unreachable_hosts = []
    for host, status in hosts.items():
        if not status:
            unreachable_hosts.append(host)
    return unreachable_hosts


def get_reachable_hosts(hosts: dict) -> list:
    reachable_hosts = []
    for host, status in hosts.items():
        if status:
            reachable_hosts.append(host)
    return reachable_hosts


def get_status_counts(hosts: dict) -> dict:
    reachable_count = 0
    unreachable_count = 0
    for status in hosts.values():
        if not status:
            unreachable_count += 1
        else:
            reachable_count += 1
    return {"reachable": reachable_count, "unreachable": unreachable_count}


def get_health_percentage(hosts: dict) -> float:
    reachable_hosts = 0
    if not hosts:
        return 0.0
    for status in hosts.values():
        if status:
            reachable_hosts += 1
    return round(reachable_hosts / len(hosts) * 100, 1)


def get_health_status(hosts: dict) -> str:
    health_percentage = get_health_percentage(hosts)
    if health_percentage >= 80:
        return "Healthy"
    elif 50 <= health_percentage <= 79.9:
        return "Degraded"
    else:
        return "Critical"


def has_failures(hosts: dict) -> bool:
    for status in hosts.values():
        if not status:
            return True
    return False


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


print("Summary:")
print(f"Reachable: {reachable_addresses}")
print(f"Unreachable: {unreachable_addresses}")
print(f"Total: {len(addresses)}")
print(f"Reachable percentage: {reachable_percentage:.1f}%")
print(f"Overall status: {overall_status}")

log_summary(
    reachable_addresses, unreachable_addresses, len(addresses), reachable_percentage
)

if unreachable_addresses > 0:
    raise SystemExit(1)
