import math

import pytest
from hypothesis import given, strategies as st

from thermostat_control import energy_alert, hvac_action, target_temperature


VALID_MODES = ["away", "sleep", "home"]


# Example test cases.
def test_away_mode():
    assert target_temperature("away", True, 12) == 16


def test_no_readings():
    assert energy_alert([], 10) == "ok"


# Functional coverage tests.
def test_sleep_and_home_temperature_paths():
    assert target_temperature("sleep", True, 5) == 18
    assert target_temperature("sleep", True, 12) == 20
    assert target_temperature("home", False, 7) == 18
    assert target_temperature("home", True, 8) == 22
    assert target_temperature("home", True, 18) == 21
    assert target_temperature("home", True, 23) == 20


def test_hvac_action_paths():
    assert hvac_action(20, 20, 10) == "idle"
    assert hvac_action(20, 22, 4) == "heat_boost"
    assert hvac_action(20, 22, 10) == "heat"
    assert hvac_action(22, 20, 31) == "cool_boost"
    assert hvac_action(22, 20, 10) == "cool"


def test_energy_alert_paths():
    assert energy_alert([11, 5], 10) == "warning"
    assert energy_alert([11, 12, 5], 10) == "critical"
    assert energy_alert([5, 10], 10) == "ok"


# Hypothesis fuzz tests for valid and invalid input handling.
@given(
    mode=st.sampled_from(VALID_MODES),
    occupied=st.booleans(),
    hour=st.integers(min_value=0, max_value=23),
)
def test_target_temperature_valid_inputs_are_stable(mode, occupied, hour):
    result = target_temperature(mode, occupied, hour)
    assert isinstance(result, int)
    assert result in {16, 18, 20, 21, 22}


@given(mode=st.text().filter(lambda value: value not in VALID_MODES))
def test_target_temperature_invalid_mode_raises(mode):
    with pytest.raises(ValueError):
        target_temperature(mode, True, 12)


@given(hour=st.one_of(st.integers().filter(lambda value: value < 0 or value > 23), st.floats(allow_nan=False, allow_infinity=False, width=32).filter(lambda value: not value.is_integer())))
def test_target_temperature_invalid_hour_raises(hour):
    with pytest.raises((TypeError, ValueError)):
        target_temperature("home", True, hour)


@given(
    current=st.floats(allow_nan=False, allow_infinity=False, width=32),
    target=st.floats(allow_nan=False, allow_infinity=False, width=32),
    outside=st.floats(allow_nan=False, allow_infinity=False, width=32),
)
def test_hvac_action_valid_inputs_return_known_states(current, target, outside):
    result = hvac_action(current, target, outside)
    assert result in {"idle", "heat_boost", "heat", "cool_boost", "cool"}


@given(current=st.one_of(st.none(), st.text(), st.booleans(), st.floats(allow_nan=True, allow_infinity=True).filter(lambda value: not math.isfinite(float(value)))))
def test_hvac_action_rejects_invalid_numbers(current):
    with pytest.raises((TypeError, ValueError)):
        hvac_action(current, 20, 10)


@given(
    readings=st.lists(
        st.floats(allow_nan=False, allow_infinity=False, width=32),
        max_size=20,
    ),
    limit=st.floats(allow_nan=False, allow_infinity=False, width=32),
)
def test_energy_alert_valid_inputs_return_status(readings, limit):
    result = energy_alert(readings, limit)
    assert result in {"ok", "warning", "critical"}


@given(readings=st.one_of(st.none(), st.text(), st.lists(st.none(), min_size=1), st.lists(st.text(), min_size=1)))
def test_energy_alert_rejects_bad_input(readings):
    with pytest.raises((TypeError, ValueError)):
        energy_alert(readings, 10)
