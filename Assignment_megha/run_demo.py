import os
import random
from datetime import date

from decide import decide
from wear_model import WearModel

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "data", "maintenance_notes.txt")
random.seed(5)


def window(torque, temp, vib, drift=(0, 0, 0), n=6, noise=True):
    """makes n samples ending at (torque,temp,vib); drift = total change over the window"""
    out = []
    for i in range(n):
        f = (i - (n - 1)) / (n - 1)          # -1 ... 0
        r = (lambda s: random.gauss(0, s)) if noise else (lambda s: 0)
        out.append((round(torque + drift[0] * f + r(1.0), 1),
                    round(temp + drift[1] * f + r(0.4), 1),
                    round(vib + drift[2] * f + r(0.08), 2)))
    return out


def arm(sh, el, wr, **kw):
    return {"shoulder": window(*sh, **kw), "elbow": window(*el, **kw), "wrist": window(*wr, **kw)}


if __name__ == "__main__":
    model = WearModel()
    print(f"model cross-val accuracy: {model.cv_score:.2f}\n")
    today = date(2026, 10, 16)

    cases = [
        ("ARM-12", "normal arm, only harmless notes", arm((92, 56, 2.2), (60, 54, 2.1), (27, 50, 1.9))),
        ("ARM-13", "slightly warm joints + rattle/jerky notes", arm((100, 60, 3.2), (66, 60, 3.3), (31, 58, 3.1))),
        ("ARM-13", "same arm a week later, sensors clearly worse", arm((106, 68, 4.9), (72, 68, 5.0), (32, 62, 3.8))),
        ("ARM-14", "wear in the sensors and a burning smell in the log", arm((108, 70, 5.4), (75, 72, 6.0), (33, 62, 4.0))),
        ("ARM-15", "wrist vibration too high", arm((92, 56, 2.2), (60, 54, 2.1), (27, 52, 12.8))),
        ("ARM-16", "elbow torque replayed as a flat number", arm((92, 56, 2.2), (60, 60, 3.4), (27, 50, 1.9))),
    ]
    # ARM-16: overwrite elbow torque with a frozen value while temp/vib keep moving
    cases[-1][2]["elbow"] = [(60.0, 58 + i * 0.6, 2.6 + i * 0.12) for i in range(6)]

    for arm_id, label, w in cases:
        r = decide(arm_id, w, model, LOG, today)
        print(f"{arm_id}: {label}")
        print(f"   -> {r['decision']}  ({r['reason']})")
        if "combined" in r:
            print(f"      model={r['model_p']} log={r['log_risk']} combined={r['combined']} words={r['log_words']} spoof={r['spoof']}")
