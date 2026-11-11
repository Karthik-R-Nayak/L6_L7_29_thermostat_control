import math


def parse_setpoint(text):
    if not isinstance(text, str):
        raise TypeError("setpoint must be a string")

    text = text.strip()
    if len(text) < 2 or text[-1].upper() not in {"C", "F"}:
        raise ValueError("setpoint must be a number followed by C or F")

    try:
        value = float(text[:-1].strip())
    except ValueError as exc:
        raise ValueError("setpoint must contain a valid number") from exc

    if not math.isfinite(value):
        raise ValueError("setpoint must be finite")
    if text[-1].upper() == "F":
        value = (value - 32) * (5 / 9)
    return round(value, 1)


def average_temperature(readings_csv):
    if not isinstance(readings_csv, str):
        raise TypeError("readings_csv must be a string")

    readings = readings_csv.split(",")
    if not readings or any(not reading.strip() for reading in readings):
        raise ValueError("readings_csv must contain comma-separated numbers")

    try:
        values = [float(reading.strip()) for reading in readings]
    except ValueError as exc:
        raise ValueError("readings_csv must contain only valid numbers") from exc

    if any(not math.isfinite(value) for value in values):
        raise ValueError("readings must be finite")

    scale = max(abs(value) for value in values)
    if scale == 0:
        return 0.0
    return (math.fsum(value / scale for value in values) / len(values)) * scale


def schedule_slot(time_text):
    if not isinstance(time_text, str):
        raise TypeError("time_text must be a string in HH:MM format")

    if (
        len(time_text) != 5
        or time_text[2] != ":"
        or not all("0" <= digit <= "9" for digit in time_text[:2] + time_text[3:])
    ):
        raise ValueError("time_text must be in HH:MM format")

    hour, minute = time_text.split(":")
    hour = int(hour)
    minute_value = int(minute)
    if hour > 23 or minute_value > 59:
        raise ValueError("time_text must be a valid time from 00:00 to 23:59")

    if hour < 6:
        return "night " + minute
    return "day " + str(minute_value)


def main():
    print("==== Running parse_setpoint ====")
    user_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    result = parse_setpoint(user_input)
    print("Setpoint in Celsius:", result)

    print("\n==== Running average_temperature ====")
    user_input = input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): ")
    result = average_temperature(user_input)
    print("Average Temperature:", result)

    print("\n==== Running schedule_slot ====")
    user_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    result = schedule_slot(user_input)
    print("Schedule Slot:", result)


if __name__ == "__main__":
    main()
