import csv
import math
import os
import random

from config import RATED

_HERE = os.path.dirname(os.path.abspath(__file__))


def _features(joint, torque, temp, vib):
    return [torque / RATED[joint], temp, vib]


def _sigmoid(z):
    z = max(-30.0, min(30.0, z))
    return 1.0 / (1.0 + math.exp(-z))


class _Logistic:
    """logistic regression trained by plain gradient descent (no libraries)"""

    def fit(self, X, y, steps=3000, lr=0.1):
        n = len(X)
        cols = len(X[0])
        self.mean = [sum(r[c] for r in X) / n for c in range(cols)]
        self.std = [math.sqrt(sum((r[c] - self.mean[c]) ** 2 for r in X) / n) or 1.0 for c in range(cols)]
        Z = [self._scale(r) for r in X]
        self.w = [0.0] * cols
        self.b = 0.0
        for _ in range(steps):
            gw = [0.0] * cols
            gb = 0.0
            for z, t in zip(Z, y):
                err = _sigmoid(sum(w * v for w, v in zip(self.w, z)) + self.b) - t
                for c in range(cols):
                    gw[c] += err * z[c]
                gb += err
            self.w = [w - lr * g / n for w, g in zip(self.w, gw)]
            self.b -= lr * gb / n
        return self

    def _scale(self, row):
        return [(v - m) / s for v, m, s in zip(row, self.mean, self.std)]

    def prob(self, row):
        z = self._scale(row)
        return _sigmoid(sum(w * v for w, v in zip(self.w, z)) + self.b)


class WearModel:
    def __init__(self):
        X, y = [], []
        with open(os.path.join(_HERE, "data", "joint_history.csv")) as f:
            for r in csv.DictReader(f):
                X.append(_features(r["joint"], float(r["torque_nm"]), float(r["temp_c"]), float(r["vib_mms"])))
                y.append(int(r["worn"]))

        # 5-fold cross validation, done by hand
        idx = list(range(len(X)))
        random.Random(1).shuffle(idx)
        folds = [idx[i::5] for i in range(5)]
        scores = []
        for k in range(5):
            test = set(folds[k])
            tr = [i for i in idx if i not in test]
            m = _Logistic().fit([X[i] for i in tr], [y[i] for i in tr], steps=1000)
            ok = sum((m.prob(X[i]) >= 0.5) == (y[i] == 1) for i in folds[k])
            scores.append(ok / len(folds[k]))
        self.cv_score = sum(scores) / 5

        self.model = _Logistic().fit(X, y)

    def arm_risk(self, latest):
        """worst joint decides the arm's wear probability"""
        probs = {}
        for joint, (t, temp, vib) in latest.items():
            probs[joint] = self.model.prob(_features(joint, t, temp, vib))
        return max(probs.values()), probs
