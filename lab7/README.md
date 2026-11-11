# L6_L7_29 — Smart Thermostat Controller

Lab 7: Fuzz Testing

## About

A small Python module that reads temperature setpoints, averages sensor readings, and labels schedule slots. The functions validate malformed values and are tested with Hypothesis.

## Files

| File | Description |
|------|-------------|
| `thermostat_control.py` | The validated application code |
| `test_thermostat_control.py` | Unit and Hypothesis property-based tests |

## Run

From this directory, install the test dependencies and run the tests:

```powershell
python -m pip install hypothesis pytest
python -m pytest -q
```

Run the interactive application with:

```powershell
python thermostat_control.py
```
