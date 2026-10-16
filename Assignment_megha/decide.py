from datetime import date

import config
import log_scan
import safety
import spoof_check


def decide(arm, windows, model, log_path, today=None):
    today = today or date.today()
    latest = {j: w[-1] for j, w in windows.items()}
    res = {"arm": arm}

    # 1. instant stop - model is not touched
    problems = safety.check_stop(latest)
    if problems:
        res.update(decision="EMERGENCY_STOP", reason="; ".join(problems))
        return res

    # 2. the two softer signals
    log_risk, critical, found = log_scan.scan(log_path, arm, today)
    try:
        p, per_joint = model.arm_risk(latest)
    except Exception:          # model missing or broken -> log only
        p, per_joint = None, {}
    combined = log_risk if p is None else config.MODEL_WEIGHT * p + config.LOG_WEIGHT * log_risk
    res.update(model_p=None if p is None else round(p, 2), log_risk=round(log_risk, 2),
               combined=round(combined, 2), log_words=found)

    # 3. spoof check
    spoof = spoof_check.check_arm(windows)
    res["spoof"] = spoof

    if spoof:
        # torque can't be trusted: never lower than maintenance, stop if anything else looks bad
        if critical or (p is not None and p >= 0.6):
            res.update(decision="EMERGENCY_STOP", reason="spoof suspected and another signal is bad")
        else:
            res.update(decision="SCHEDULE_MAINTENANCE", reason="spoof suspected, send someone to check the sensor")
        return res

    if critical and p is not None and p >= 0.5:
        res.update(decision="EMERGENCY_STOP", reason="critical note in the log and model also sees wear")
    elif combined >= config.MAINTENANCE_AT:
        res.update(decision="SCHEDULE_MAINTENANCE", reason="combined risk high")
    elif combined >= config.MONITOR_AT:
        res.update(decision="MONITOR", reason="combined risk medium")
    else:
        res.update(decision="SAFE", reason="combined risk low")
    return res
