import subprocess
import json
from datetime import datetime

try:
    with open("config.json", "r") as file:
        config = json.load(file)

    addresses = config["hosts"]

except FileNotFoundError:
    print("Error: config.json was not found.")
    raise SystemExit

except json.JSONDecodeError:
    print("Error: config.json contains invalid JSON.")
    raise SystemExit

except KeyError:
    print("Error: config.json is missing the hosts section.")
    raise SystemExit


def is_reachable(address: str) -> bool:
    try:
        result = subprocess.run(["ping", "-n", "1", address], capture_output=True)

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
    raise SystemExit

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

print("Summary:")
print(f"Reachable: {reachable_addresses}")
print(f"Unreachable: {unreachable_addresses}")
print(f"Total: {len(addresses)}")
print(f"Reachable percentage: {reachable_percentage:.1f}%")

log_summary(
    reachable_addresses, unreachable_addresses, len(addresses), reachable_percentage
)
