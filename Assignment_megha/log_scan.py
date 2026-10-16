import math
import re
from datetime import datetime

from config import LOG_HALF_LIFE_DAYS

CRITICAL = re.compile(r"smell(s)? like burning|burning smell|burnt|smoke|sparks|crack(ed|ing)|loose (bolt|mount)|oil leak")
MEDIUM = re.compile(r"grind(ing)?|whin(e|ing)|backlash|jerky|overheat(ing|ed)?|runs? hot|leak(ing)?")
LOW = re.compile(r"noise|noisy|vibrat(ion|ing)|rough|sticky|rattle(s)?|warm")
NEGATORS = re.compile(r"\b(no|not|without|isn't|didn't|nothing)\b")
LINE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s+(ARM-\d+)\s+-\s+(.*)$")

LEVELS = [(CRITICAL, 1.0, "critical"), (MEDIUM, 0.5, "medium"), (LOW, 0.2, "low")]


def _clauses(text):
    # split on punctuation and "but" so that "no leak, jerky motion" is handled per part
    return [c.strip() for c in re.split(r"[.,;]| but ", text.lower()) if c.strip()]


def scan(path, arm, today):
    """returns (risk 0..1, has_critical, list of matched words)"""
    total = 0.0
    critical = False
    found = []
    with open(path) as f:
        for line in f:
            m = LINE.match(line.strip())
            if not m or m.group(2) != arm:
                continue
            age = (today - datetime.strptime(m.group(1), "%Y-%m-%d").date()).days
            fade = 0.5 ** (age / LOG_HALF_LIFE_DAYS)
            for clause in _clauses(m.group(3)):
                for pattern, weight, level in LEVELS:
                    hit = pattern.search(clause)
                    if not hit:
                        continue
                    if NEGATORS.search(clause[:hit.start()]):
                        continue
                    total += weight * fade
                    found.append(hit.group(0))
                    if level == "critical" and age <= 14:
                        critical = True
                    break   # one level per clause is enough
    return 1 - math.exp(-total), critical, found
