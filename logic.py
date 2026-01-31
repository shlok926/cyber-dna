def analyze_responses(data):
    score_map = {"A": 1, "B": 3, "C": 5}

    total_score = 0
    weak_areas = []
    recommendations = []

    questions = {
        "q1": ("Clicking Unknown Links", "Avoid clicking links from unknown senders."),
        "q2": ("OTP Sharing", "Never share OTPs or verification codes."),
        "q3": ("Public Wi-Fi Usage", "Avoid banking on public Wi-Fi."),
        "q4": ("Password Reuse", "Use unique passwords for every platform."),
        "q5": ("Urgent Warning Reaction", "Always verify urgent security alerts."),
        "q6": ("App Permissions", "Review app permissions carefully."),
        "q7": ("Two-Factor Authentication", "Enable 2FA wherever possible.")
    }

    for q, (area, tip) in questions.items():
        if q in data:
            val = score_map.get(data[q], 0)
            total_score += val
            if val >= 4:
                weak_areas.append(area)
                recommendations.append(tip)

    if total_score <= 12:
        risk_level = "Low Risk"
        risk_color = "Green"
    elif total_score <= 22:
        risk_level = "Medium Risk"
        risk_color = "Yellow"
    else:
        risk_level = "High Risk"
        risk_color = "Red"

    return {
        "total_score": total_score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "weak_areas": weak_areas,
        "recommendations": recommendations
    }
