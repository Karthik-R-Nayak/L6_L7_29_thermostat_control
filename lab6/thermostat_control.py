import math
from numbers import Real


def _validate_hour(hour):
    if isinstance(hour, bool) or not isinstance(hour, int):
        raise TypeError("hour must be an integer between 0 and 23")
    if not 0 <= hour <= 23:
        raise ValueError("hour must be between 0 and 23")


def _validate_numeric(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a finite real number")
    if not math.isfinite(float(value)):
        raise ValueError(f"{name} must be finite")


def target_temperature(mode, occupied, hour):
    if not isinstance(mode, str):
        raise TypeError("mode must be a string")

    normalized_mode = mode.lower()
    if normalized_mode not in {"away", "sleep", "home"}:
        raise ValueError("mode must be 'away', 'sleep', or 'home'")

    if not isinstance(occupied, bool):
        raise TypeError("occupied must be a boolean")

    _validate_hour(hour)

    if normalized_mode == "away":
        return 16
    if normalized_mode == "sleep":
        if hour < 6 or hour >= 22:
            return 18
        return 20
    if not occupied:
        return 18
    if 6 <= hour < 9:
        return 22
    if 17 <= hour < 22:
        return 21
    return 20


def hvac_action(current, target, outside):
    _validate_numeric(current, "current")
    _validate_numeric(target, "target")
    _validate_numeric(outside, "outside")

    diff = target - current
    if abs(diff) < 1:
        return "idle"
    if diff > 0:
        if outside < 5:
            return "heat_boost"
        return "heat"
    if outside > 30:
        return "cool_boost"
    return "cool"


def energy_alert(readings, limit):
    if readings is None:
        raise TypeError("readings must be an iterable of numeric values")
    if isinstance(readings, (str, bytes)):
        raise TypeError("readings must be an iterable of numeric values")

    try:
        read_list = list(readings)
    except TypeError as exc:
        raise TypeError("readings must be an iterable of numeric values") from exc

    _validate_numeric(limit, "limit")

    over = 0
    for reading in read_list:
        _validate_numeric(reading, "reading")
        if reading > limit:
            over += 1

    if not read_list:
        return "ok"
    if over == 0:
        return "ok"
    if over * 2 > len(read_list):
        return "critical"
    return "warning"
