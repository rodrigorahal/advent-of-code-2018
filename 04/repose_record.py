import fileinput
from collections import defaultdict


def parse():
    lines = [line for line in fileinput.input()]

    readings = []
    for line in lines:
        content = line.strip().split("]")
        date, time = content[0][1:].split()
        year, month, day = tuple(map(int, date.split("-")))
        hours, minutes = tuple(map(int, time.split(":")))

        if "wakes" in content[1]:
            record = "wake"
            readings.append(((year, month, day), (hours, minutes), record))
        elif "asleep" in content[1]:
            record = "sleep"
            readings.append(((year, month, day), (hours, minutes), record))
        else:
            guard = int(content[1].strip().split()[1][1:])
            readings.append(((year, month, day), (hours, minutes), guard))
    return readings


def count(readings):
    guard = None
    sleep_by_guard = defaultdict(int)
    start = None
    for (year, month, day), (hours, minutes), item in readings:
        if isinstance(item, int):
            guard = item
        elif item == "sleep":
            start = (hours, minutes)
        elif item == "wake":
            fell_sleep_hours, fell_sleep_minutes = start
            if hours == fell_sleep_hours:
                sleep_by_guard[guard] += minutes - fell_sleep_minutes
            else:
                sleep_by_guard += minutes + 60 - fell_sleep_minutes
    return sleep_by_guard


def common(readings):
    guard = None
    sleep_by_minute_by_guard = defaultdict(lambda: defaultdict(int))
    start = None
    for (year, month, day), (hours, minutes), item in readings:
        if isinstance(item, int):
            guard = item
        elif item == "sleep":
            start = (hours, minutes)
        elif item == "wake":
            fell_sleep_hours, fell_sleep_minutes = start
            if hours == fell_sleep_hours:
                for m in range(fell_sleep_minutes, minutes):
                    sleep_by_minute_by_guard[guard][m] += 1
            else:
                for m in range(minutes):
                    sleep_by_minute_by_guard[guard][m] += 1
    return sleep_by_minute_by_guard


def most_asleep(readings):
    sleep_by_guard = count(readings)
    _, guard = max([(v, k) for k, v in sleep_by_guard.items()])
    sleep_by_minute_by_guard = common(readings)
    _, minutes = max([(v, k) for k, v in sleep_by_minute_by_guard[guard].items()])
    return guard, minutes


def display(reading):
    (year, month, day), (hours, minutes), item = reading
    timestamp = f"[{year}-{month:02}-{day:02} {hours:02}:{minutes:02}]"
    if item == "wake":
        msg = "wakes up"
    elif item == "sleep":
        msg = "falls asleep"
    else:
        msg = f"Guard #{item} begins shift"
    print(f"{timestamp} {msg}")


def most_frequent(readings):
    sleep_by_minute_by_guard = common(readings)
    minutes_frequency_by_guard = frequent(sleep_by_minute_by_guard)
    (frequency, minutes), guard = max(
        [(v, k) for k, v in minutes_frequency_by_guard.items()]
    )
    return guard, minutes


def frequent(sleep_by_minute_by_guard):
    minutes_frequency_by_guard = dict()
    for guard in sleep_by_minute_by_guard:
        frequency, minutes = max(
            [(v, k) for k, v in sleep_by_minute_by_guard[guard].items()]
        )
        minutes_frequency_by_guard[guard] = (frequency, minutes)
    return minutes_frequency_by_guard


def main():
    readings = parse()
    readings = sorted(readings)
    guard, minutes = most_asleep(readings)
    print(f"Part 1: {guard} x {minutes} = {guard * minutes}")
    guard, minutes = most_frequent(readings)
    print(f"Part 2: {guard} x {minutes} = {guard * minutes}")


if __name__ == "__main__":
    main()
