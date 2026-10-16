# builds data/joint_history.csv
# one row = one joint at one moment. worn=1 means that joint later failed / needed a repair
import csv
import os
import random

from config import JOINTS, RATED

random.seed(2026)


def sample(joint, worn):
    wear = random.uniform(0.3, 1.0) if worn else 0.0
    ratio = random.gauss(0.60, 0.10) + 0.15 * wear
    temp = 40 + 25 * ratio + random.gauss(0, 2.5) + 14 * wear
    vib = 1.0 + 2.0 * ratio + abs(random.gauss(0, 0.4)) + 4.5 * wear
    return {
        "joint": joint,
        "torque_nm": round(ratio * RATED[joint], 1),
        "temp_c": round(temp, 1),
        "vib_mms": round(vib, 2),
        "worn": int(worn),
    }


rows = []
for j in JOINTS:
    for _ in range(25):
        rows.append(sample(j, False))
    for _ in range(25):
        rows.append(sample(j, True))
random.shuffle(rows)

os.makedirs("data", exist_ok=True)
with open("data/joint_history.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows written")
