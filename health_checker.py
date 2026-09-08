import subprocess

addresses = ["192.168.0.1", "8.8.8.8", "192.0.2.1"]


def is_reachable(address: str) -> bool:

    result = subprocess.run(["ping", "-n", "1", address], capture_output=True)

    return result.returncode == 0


reachable_addresses = 0

for address in addresses:
    if is_reachable(address):
        print(f"{address} is reachable.")
        reachable_addresses += 1
    else:
        print(f"{address} is unreachable.")

print(f"Summary: {reachable_addresses}/{len(addresses)} hosts reachable.")
