# the instant stop check. plain if-statements only, nothing from the model is imported here
import math

from config import RATED, STOP_TEMP, STOP_TORQUE_FACTOR, STOP_VIB


def check_stop(latest):
    """latest = {joint: (torque, temp, vib)}. returns list of problems (empty = fine)."""
    problems = []
    for joint, values in latest.items():
        torque, temp, vib = values
        for name, v in (("torque", torque), ("temp", temp), ("vib", vib)):
            # a missing or nonsense number is treated like a danger too
            if v is None or (isinstance(v, float) and math.isnan(v)) or v < 0:
                problems.append(f"{joint} {name} invalid ({v})")
        if problems:
            continue
        if torque > RATED[joint] * STOP_TORQUE_FACTOR:
            problems.append(f"{joint} torque {torque} Nm over {RATED[joint] * STOP_TORQUE_FACTOR:.0f}")
        if temp > STOP_TEMP:
            problems.append(f"{joint} temp {temp} C over {STOP_TEMP}")
        if vib > STOP_VIB:
            problems.append(f"{joint} vibration {vib} mm/s over {STOP_VIB}")
    return problems
