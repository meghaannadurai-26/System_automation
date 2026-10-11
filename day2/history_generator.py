import csv
import random
from pathlib import Path


MACHINE_COUNT = 255
OUTPUT_FILE = Path(__file__).with_name("machine_data.csv")


def get_machine_state(
    temperature: float,
    pressure: float,
    vibration: float,
    rpm: int,
    current: float,
) -> str:
    """Classify a machine using example limits; adjust these for your equipment."""
    if (
        temperature >= 90
        or pressure >= 10
        or vibration >= 8
        or current >= 45
    ):
        return "CRITICAL"

    if (
        temperature >= 80
        or pressure >= 9
        or vibration >= 5
        or current >= 40
        or rpm == 0
    ):
        return "WARNING"

    return "RUNNING"


def generate_machine_reading(machine_id: int) -> dict[str, object]:
    """Create one example sensor reading for a machine."""
    temperature = round(random.uniform(55, 95), 1)
    pressure = round(random.uniform(4, 10), 2)
    vibration = round(random.uniform(0.2, 10), 2)
    rpm = random.randint(0, 3000)
    current = round(random.uniform(10, 50), 2)

    return {
        "machine_id": machine_id,
        "temperature_c": temperature,
        "pressure_bar": pressure,
        "vibration_mm_s": vibration,
        "rpm": rpm,
        "current_a": current,
        "state": get_machine_state(temperature, pressure, vibration, rpm, current),
    }


def main() -> None:
    readings = [
        generate_machine_reading(machine_id)
        for machine_id in range(1, MACHINE_COUNT + 1)
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=readings[0].keys())
        writer.writeheader()
        writer.writerows(readings)

    print(f"Generated {len(readings)} machine readings: {OUTPUT_FILE}")
    for reading in readings[:5]:
        print(reading)


if __name__ == "__main__":
    main()
