# Health Checker

A simple Python command-line health checker that monitors configured hosts using ICMP ping, reports their reachability, calculates an overall health status, and logs the results.

This project was built to practise Python fundamentals, networking concepts, configuration handling, logging, error handling, refactoring, Git/GitHub workflow, and automated testing.

## Features

- Loads host names and IP addresses from a JSON configuration file
- Checks whether each host is reachable using `ping`
- Displays individual host status
- Calculates overall availability percentage
- Categorises overall health as:
  - `Healthy`
  - `Degraded`
  - `Critical`

- Lists reachable and unreachable hosts
- Logs individual checks and summary results
- Handles missing or invalid configuration files
- Returns a non-zero exit code when hosts are unreachable
- Includes automated tests using `pytest`

## Requirements

- Python 3
- `pytest` for running the automated tests
- A system with the `ping` command available

The current implementation uses Windows ping arguments.

## Configuration

Hosts are configured in `config.json`.

Example:

```json
{
  "hosts": {
    "Router": "192.168.0.1",
    "Google DNS": "8.8.8.8",
    "Test Host": "192.0.2.1"
  }
}
```

Each entry contains:

- A descriptive host name
- The IP address or hostname to check

## Running the Project

From the project directory, run:

```bash
python health_checker.py
```

Example output:

```text
Router (192.168.0.1) is reachable
Google DNS (8.8.8.8) is reachable
Test Host (192.0.2.1) is unreachable
Health: Degraded | Reachable: 2 | Unreachable: 1 | Availability: 66.7%
Unreachable hosts: Test Host
Reachable hosts: Router, Google DNS
```

When all configured hosts are reachable, output may look like:

```text
Router (192.168.0.1) is reachable
Google DNS (8.8.8.8) is reachable
Cloudflare DNS (1.1.1.1) is reachable
Health: Healthy | Reachable: 3 | Unreachable: 0 | Availability: 100.0%
Reachable hosts: Router, Google DNS, Cloudflare DNS
```

## Health Status

The overall health status is calculated from the percentage of reachable hosts.

| Availability | Status   |
| ------------ | -------- |
| 80–100%      | Healthy  |
| 50–79.9%     | Degraded |
| Below 50%    | Critical |

## Logging

Health check results are written to:

```text
health_checks.log
```

Each host check contains a timestamp, host name, address, and status.

Example:

```text
2026-09-17 13:15:00 | Router | 192.168.0.1 | reachable
```

A summary is also logged after each run.

The generated log file is excluded from Git using `.gitignore`.

## Testing

The project includes automated tests for the health calculation and host-status helper functions.

Run the test suite with:

```bash
python -m pytest
```

The tests currently cover areas including:

- Reachable and unreachable host counts
- Availability percentage
- Healthy status
- Degraded status
- Critical status
- Empty host collections
- Failure detection
- Reachable host lists
- Unreachable host lists

## Project Structure

```text
health-checker/
├── health_checker.py
├── config.json
├── test_health_checker.py
├── README.md
└── .gitignore
```

`health_checks.log`, Python cache files, pytest cache files, and the virtual environment are excluded from version control.

## What I Learned

Building this project helped me practise:

- Python functions and return values
- Dictionaries, lists, loops, and conditionals
- List comprehensions
- Boolean values and truthiness
- Reading and validating JSON configuration
- Handling exceptions
- Running operating-system commands with `subprocess`
- Working with exit codes
- Logging program results
- Refactoring duplicated logic
- Separating program logic into reusable functions
- Using a `main()` entry point
- Writing automated tests with `pytest`
- Using Git branches, commits, and pull requests

## Future Improvements

Possible future improvements include:

- Cross-platform support for Windows, Linux, and macOS ping commands
- Configurable timeouts and retry counts
- Command-line arguments
- More detailed logging
- Notifications when hosts become unavailable
- Historical availability reporting

## Status

Health Checker v1.0 — complete.
