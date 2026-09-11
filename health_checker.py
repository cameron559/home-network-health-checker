import subprocess
from datetime import datetime

addresses = ["192.168.0.1", "8.8.8.8", "192.0.2.1"]


def is_reachable(address: str) -> bool:

    result = subprocess.run(["ping", "-n", "1", address], capture_output=True)

    return result.returncode == 0


reachable_addresses = 0


def log_health_check(address: str, status: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("health_checks.log", "a") as file:
        file.write(f"{timestamp} | {address} | {status}\n")


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


for address in addresses:
    reachable = is_reachable(address)
    status = "reachable" if reachable else "unreachable"

    print(f"{address} is {status}.")
    log_health_check(address, status)

    if reachable:
        reachable_addresses += 1

unreachable_addresses = len(addresses) - reachable_addresses
reachable_percentage = (reachable_addresses / len(addresses)) * 100


log_summary(
    reachable_addresses, unreachable_addresses, len(addresses), reachable_percentage
)
