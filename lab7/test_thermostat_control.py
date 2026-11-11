import math

import pytest
from hypothesis import given, strategies as st

from thermostat_control import parse_setpoint, average_temperature, schedule_slot


finite_floats = st.floats(
    allow_nan=False,
    allow_infinity=False,
    min_value=-1_000_000,
    max_value=1_000_000,
)


@given(value=finite_floats, unit=st.sampled_from(["C", "F", "c", "f"]))
def test_parse_setpoint_valid_values_are_rounded(value, unit):
    result = parse_setpoint(f"{value}{unit}")
    expected = value if unit.upper() == "C" else (value - 32) * (5 / 9)
    assert result == round(expected, 1)
    assert math.isfinite(result)


@given(text=st.text())
def test_parse_setpoint_arbitrary_text_has_controlled_result(text):
    try:
        result = parse_setpoint(text)
    except ValueError:
        return
    assert math.isfinite(result)


@pytest.mark.parametrize("value", [None, 21.5, True])
def test_parse_setpoint_rejects_non_strings(value):
    with pytest.raises(TypeError):
        parse_setpoint(value)


@pytest.mark.parametrize("text", ["", "21", "C", "abcC", "nanC", "infF", "20K"])
def test_parse_setpoint_rejects_malformed_values(text):
    with pytest.raises(ValueError):
        parse_setpoint(text)


@given(readings=st.lists(finite_floats, min_size=1, max_size=30))
def test_average_temperature_matches_mean(readings):
    readings_csv = ",".join(str(reading) for reading in readings)
    result = average_temperature(readings_csv)
    assert math.isclose(result, sum(readings) / len(readings), rel_tol=1e-12)


def test_average_temperature_handles_large_finite_readings():
    result = average_temperature(
        "1.7976931348623157e308,1.7976931348623157e308"
    )
    assert math.isfinite(result)
    assert result == 1.7976931348623157e308


def test_average_temperature_preserves_small_subnormal_readings():
    assert average_temperature("5e-324,5e-324") == 5e-324


@given(text=st.text())
def test_average_temperature_arbitrary_text_has_controlled_result(text):
    try:
        result = average_temperature(text)
    except ValueError:
        return
    assert math.isfinite(result)


@pytest.mark.parametrize("value", [None, 20, True])
def test_average_temperature_rejects_non_strings(value):
    with pytest.raises(TypeError):
        average_temperature(value)


@pytest.mark.parametrize(
    "text",
    ["", " ", ",", "20,", ",20", "20,,21", "one,2", "nan", "inf"],
)
def test_average_temperature_rejects_malformed_values(text):
    with pytest.raises(ValueError):
        average_temperature(text)


@given(
    hour=st.integers(min_value=0, max_value=23),
    minute=st.integers(min_value=0, max_value=59),
)
def test_schedule_slot_valid_times_are_classified(hour, minute):
    time_text = f"{hour:02d}:{minute:02d}"
    expected = f"night {minute:02d}" if hour < 6 else f"day {minute}"
    assert schedule_slot(time_text) == expected


@given(text=st.text())
def test_schedule_slot_arbitrary_text_has_controlled_result(text):
    try:
        result = schedule_slot(text)
    except ValueError:
        return
    assert result.startswith(("night ", "day "))


@pytest.mark.parametrize("value", [None, 730, True])
def test_schedule_slot_rejects_non_strings(value):
    with pytest.raises(TypeError):
        schedule_slot(value)


@pytest.mark.parametrize(
    "text",
    ["", "7:30", "07:3", "07-30", "24:00", "12:60", "-1:00", "ab:cd", " 07:30"],
)
def test_schedule_slot_rejects_malformed_times(text):
    with pytest.raises(ValueError):
        schedule_slot(text)
