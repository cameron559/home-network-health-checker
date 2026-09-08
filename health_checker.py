import subprocess


def is_reachable(address: str) -> bool:

    result = subprocess.run(["ping", "-n", "1", address], capture_output=True)

    return result.returncode == 0


print(is_reachable("192.168.0.1"))
