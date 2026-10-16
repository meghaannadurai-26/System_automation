# looks at the last few torque samples of each joint over time.
# a real torque signal is noisy and moves smoothly; a faked one often doesn't.
from config import DROP_FRACTION, FLAT_RANGE, JUMP_FRACTION, RATED


def check_window(joint, window):
    """window = list of (torque, temp, vib), oldest first. returns list of reasons."""
    torques = [w[0] for w in window]
    temps = [w[1] for w in window]
    vibs = [w[2] for w in window]
    why = []

    # 1. frozen / replayed value
    if max(torques) - min(torques) < FLAT_RANGE and (max(vibs) - min(vibs) > 0.15 or max(temps) - min(temps) > 0.5):
        why.append(f"{joint}: torque frozen while other sensors still move")

    # 2. impossible jump between two samples
    limit = JUMP_FRACTION * RATED[joint]
    for a, b in zip(torques, torques[1:]):
        if abs(b - a) > limit:
            why.append(f"{joint}: torque jumped {abs(b - a):.0f} Nm in one step")
            break

    # 3. torque going down while temperature and vibration go up (hides a problem)
    if (torques[0] - torques[-1] > DROP_FRACTION * RATED[joint]
            and temps[-1] - temps[0] > 1.0 and vibs[-1] - vibs[0] > 0.3):
        why.append(f"{joint}: torque falling while temp and vibration rise")
    return why


def check_arm(windows):
    out = []
    for joint, w in windows.items():
        out += check_window(joint, w)
    return out
