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
Google DNS (8.8.8.8)
```
