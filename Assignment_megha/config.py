# all the numbers in one place so they are easy to change
JOINTS = ("shoulder", "elbow", "wrist")

# rated torque of each joint in Nm
RATED = {"shoulder": 150.0, "elbow": 100.0, "wrist": 45.0}

# emergency stop if torque goes over 120% of rated, temp over 100 C, vib over 12 mm/s
STOP_TORQUE_FACTOR = 1.20
STOP_TEMP = 100.0
STOP_VIB = 12.0

# combined risk cut-offs
MONITOR_AT = 0.25
MAINTENANCE_AT = 0.55
MODEL_WEIGHT = 0.6
LOG_WEIGHT = 0.4

# spoof check settings (window of recent torque samples)
FLAT_RANGE = 0.2          # Nm - a real torque signal is never this still
JUMP_FRACTION = 0.30      # of rated torque, between two neighbouring samples
DROP_FRACTION = 0.20      # torque falling by this much while temp + vib rise

LOG_HALF_LIFE_DAYS = 7
