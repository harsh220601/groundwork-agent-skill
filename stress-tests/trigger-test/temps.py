"""Daily temperature stats for the greenhouse dashboard."""


def average(readings):
    """Mean of the readings."""
    return sum(readings) / len(readings)


def spread(readings):
    """Difference between the hottest and coldest reading."""
    return max(readings) - min(readings)


if __name__ == "__main__":
    day = [21.5, 22.4, 23.1, 22.9]
    print("avg:", average(day))
    print("spread:", spread(day))
