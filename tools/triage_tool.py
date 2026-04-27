def compute_news2(respiratory_rate, spo2, on_oxygen,
                  systolic_bp, heart_rate, temperature, consciousness):
    score = 0
    if respiratory_rate <= 8: score += 3
    elif respiratory_rate <= 11: score += 1
    elif respiratory_rate <= 20: score += 0
    elif respiratory_rate <= 24: score += 2
    else: score += 3
    if spo2 <= 91: score += 3
    elif spo2 <= 93: score += 2
    elif spo2 <= 95: score += 1
    if on_oxygen: score += 2
    if systolic_bp <= 90: score += 3
    elif systolic_bp <= 100: score += 2
    elif systolic_bp <= 110: score += 1
    elif systolic_bp >= 220: score += 3
    if heart_rate <= 40: score += 3
    elif heart_rate <= 50: score += 1
    elif heart_rate <= 90: score += 0
    elif heart_rate <= 110: score += 1
    elif heart_rate <= 130: score += 2
    else: score += 3
    if temperature <= 35.0: score += 3
    elif temperature <= 36.0: score += 1
    elif temperature <= 38.0: score += 0
    elif temperature <= 39.0: score += 1
    else: score += 2
    if consciousness.lower() != "alert": score += 3
    return score


def triage_clinical_note(
    patient_name: str,
    age: int,
    gender: str,
    chief_complaint: str,
    respiratory_rate: int,
    spo2: int,
    on_oxygen: bool,
    systolic_bp: int,
    heart_rate: int,
    temperature: float,
    consciousness: str
) -> dict:
    """
    Perform clinical triage. Computes NEWS2 score, severity,
    care recommendation, and bias audit.

    Args:
        patient_name: Patient name
        age: Patient age in years
        gender: Patient gender
        chief_complaint: Main presenting complaint
        respiratory_rate: Breaths per minute
        spo2: Oxygen saturation percentage
        on_oxygen: Whether patient is on supplemental oxygen
        systolic_bp: Systolic blood pressure in mmHg
        heart_rate: Heart rate in beats per minute
        temperature: Body temperature in Celsius
        consciousness: Alert, Verbal, Pain, or Unresponsive

    Returns:
        dict with full triage assessment
    """
    news2 = compute_news2(
        respiratory_rate, spo2, on_oxygen,
        systolic_bp, heart_rate, temperature, consciousness
    )

    if news2 <= 4:
        severity = "LOW"
        recommendation = "Monitor in waiting area. Reassess in 60 minutes."
    elif news2 <= 6:
        severity = "MEDIUM"
        recommendation = "Prioritise assessment. Notify senior nurse. Reassess in 30 minutes."
    elif news2 <= 8:
        severity = "HIGH"
        recommendation = "Urgent medical review required. Alert on-call doctor immediately."
    else:
        severity = "CRITICAL"
        recommendation = "EMERGENCY: Immediate resuscitation team activation required."

    bias_flags = []
    if age > 75 and severity == "LOW":
        bias_flags.append("Elderly patient with low score - verify no under-reporting of symptoms.")
    if gender.lower() == "female" and "chest" in chief_complaint.lower():
        bias_flags.append("Female cardiac presentation - literature shows under-triage risk. Manual review recommended.")

    bias_status = "REVIEW REQUIRED" if bias_flags else "FAIR"
    if not bias_flags:
        bias_flags.append("No demographic bias indicators detected.")

    return {
        "patient": patient_name,
        "age": age,
        "gender": gender,
        "chief_complaint": chief_complaint,
        "vitals": {
            "respiratory_rate": respiratory_rate,
            "spo2": spo2,
            "on_oxygen": on_oxygen,
            "systolic_bp": systolic_bp,
            "heart_rate": heart_rate,
            "temperature": temperature,
            "consciousness": consciousness
        },
        "news2_score": news2,
        "severity": severity,
        "recommendation": recommendation,
        "bias_audit": {
            "status": bias_status,
            "flags": bias_flags
        }
    }