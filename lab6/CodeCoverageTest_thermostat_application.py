"""Line/code coverage tests for thermostat_control.py."""
from thermostat_control import target_temperature, hvac_action, energy_alert


def test_target_temperature_code_paths():
    assert target_temperature("away", True, 12) == 16
    assert target_temperature("sleep", True, 23) == 18
    assert target_temperature("sleep", True, 12) == 20
    assert target_temperature("home", False, 12) == 18
    assert target_temperature("home", True, 7) == 22
    assert target_temperature("home", True, 18) == 21
    assert target_temperature("home", True, 12) == 20


def test_hvac_action_code_paths():
    assert hvac_action(20, 20, 10) == "idle"
    assert hvac_action(18, 22, 2) == "heat_boost"
    assert hvac_action(18, 22, 10) == "heat"
    assert hvac_action(24, 20, 35) == "cool_boost"
    assert hvac_action(24, 20, 20) == "cool"


def test_energy_alert_code_paths():
    assert energy_alert([], 10) == "ok"
    assert energy_alert([5, 10], 10) == "ok"
    assert energy_alert([11, 5], 10) == "warning"
    assert energy_alert([11, 12, 5], 10) == "critical"
