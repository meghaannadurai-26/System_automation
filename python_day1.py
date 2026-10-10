"""
DAY 1 · HANDS-ON — Build Your Rule Engine
23IF02 System Automation

Work through the TODOs in order. Each one matches a step on the
"Hands-on · Build Your Rule Engine" slide. Run this file after each
step to see your progress:

    python hands_on_starter.py

Need the answer? See hands_on_solution.py — but try it yourself first.
"""

import random
import time

LOG_FILE = "day1_log.txt"


# ---------------------------------------------------------------------------
# STEP 1 — Generate simulated sensor data
# ---------------------------------------------------------------------------
def generate_sensor_data():
    """Return a dict with at least 'temperature', 'pressure', 'vibration'."""
    # TODO: fill in realistic random values, e.g. temperature 50-95 (deg C)
    return {
        "temperature": random.randint(50, 95),   # TODO
        "pressure": random.randint(1, 10),      # TODO
        "vibration": random.randint(1, 10),     # TODO
        "current": random.randint(5, 20)        # TODO
    }
   
RULES = [
    {
        "name": "LOW_PRESSURE",
        "priority": 0,
        "condition": lambda r: r["pressure"] < 3,
        "action": "CHECK_SUPPLY"
    },
    {
        "name": "HIGH_TEMP",
        "priority": 1,
        "condition": lambda r: r["temperature"] > 80,
        "action": "STOP_MACHINE"
    },
    {
        "name": "HIGH_VIBRATION",
        "priority": 2,
        "condition": lambda r: r["vibration"] > 7,
        "action": "INSPECT_MACHINE"
    },
    {
        "name": "HIGH_PRESSURE",
        "priority": 3,
        "condition": lambda r: r["pressure"] > 8,
        "action": "REDUCE_PRESSURE"
    },
    {
        "name": "HIGH_CURRENT",
        "priority": 4,
        "condition": lambda r: r["current"] > 15,
        "action": "CHECK_MOTOR"
    }
]


# ---------------------------------------------------------------------------
# STEP 3 — Detect machine state from the rules
def evaluate_rules(reading, rules):
 

    sorted_rules = sorted(rules, key=lambda rule: rule["priority"])

  
    for rule in sorted_rules:
        if rule["condition"](reading):
            return rule["name"], rule["action"]

    
    return "NO_RULE_FIRED", "CONTINUE_NORMAL"
# ---------------------------------------------------------------------------
# STEP 4 — Trigger an action when a rule fires
# ---------------------------------------------------------------------------
def take_action(action):
    """Return a message describing what happens for an action."""

    if action == "STOP_MACHINE":
        return "Machine stopped due to high temperature!"

    elif action == "REDUCE_PRESSURE":
        return "High pressure detected. Reduce the pressure!"

    elif action == "INSPECT_MACHINE":
        return "High vibration detected. Inspect the machine!"

    elif action == "CHECK_SUPPLY":
        return "Pressure is too low. Check the supply line!"

    elif action == "CONTINUE_NORMAL":
        return "All parameters normal. Machine continues running."

    else:
        return f"No handler available for action: {action}" 
# ---------------------------------------------------------------------------
# STEP 5 — Log every decision made
# ---------------------------------------------------------------------------
def log_decision(reading, rule_name, action):
    """Append one line to LOG_FILE with the reading, rule fired, and action."""
    
    with open(LOG_FILE, "a") as f:
        f.write(f"Reading: {reading}, Rule: {rule_name}, Action: {action}\n")
        



# ---------------------------------------------------------------------------
# STEP 6 — Add a second sensor to the system
# TODO: add e.g. "current" to generate_sensor_data(), then use it in a rule
# ---------------------------------------------------------------------------


def main():
    for tick in range(1, 11):
        reading = generate_sensor_data()
        rule_name, action = evaluate_rules(reading, RULES)
        outcome = take_action(action)

        print(f"[Tick {tick:02d}] SENSE -> {reading}")
        print(f"           THINK -> {rule_name}")
        print(f"           ACT   -> {outcome}\n")

        log_decision(reading, rule_name, action)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
