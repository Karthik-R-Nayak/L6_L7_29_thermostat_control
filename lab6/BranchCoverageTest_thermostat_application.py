"""Branch coverage tests for thermostat_control.py."""
from thermostat_control import target_temperature, hvac_action, energy_alert


def test_target_temperature_all_branches():
    # Mode checks: away, sleep, and all other modes.
    assert target_temperature("away", True, 12) == 16

    # Sleep condition: hour < 6; hour >= 22; and neither condition.
    assert target_temperature("sleep", True, 5) == 18
    assert target_temperature("sleep", True, 22) == 18
    assert target_temperature("sleep", True, 12) == 20

    # Occupancy decision.
    assert target_temperature("home", False, 7) == 18

    # Morning range: true and false; evening range: true and false.
    assert target_temperature("home", True, 6) == 22
    assert target_temperature("home", True, 12) == 20
    assert target_temperature("home", True, 17) == 21
    assert target_temperature("home", True, 22) == 20


def test_hvac_action_all_branches():
    # abs(diff) < 1: true and false.
    assert hvac_action(20, 20, 10) == "idle"
    assert hvac_action(20, 20.5, 10) == "idle"
    assert hvac_action(20, 22, 10) == "heat"

    # diff > 0 and outside < 5: both outcomes.
    assert hvac_action(20, 22, 4) == "heat_boost"
    assert hvac_action(20, 22, 5) == "heat"

    # Negative diff and outside > 30: both outcomes.
    assert hvac_action(22, 20, 31) == "cool_boost"
    assert hvac_action(22, 20, 30) == "cool"


def test_energy_alert_all_branches():
    # Empty/non-empty input, reading > limit true/false, and over == 0 true/false.
    assert energy_alert([], 10) == "ok"
    assert energy_alert([5, 10], 10) == "ok"

    # over * 2 > len(readings): false (warning) and true (critical).
    assert energy_alert([11, 5], 10) == "warning"
    assert energy_alert([11, 12, 5], 10) == "critical"
