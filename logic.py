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


import re

def analyze_text_phishing(text):
    text_lower = text.lower()
    
    # Categories of indicators
    urgency_keywords = ["urgent", "immediate", "suspended", "blocked", "closed", "legal action", "unauthorized", "verify now", "within 24 hours", "action required", "compromised", "restrict"]
    financial_keywords = ["bank", "account", "prize", "won", "lottery", "gift card", "reward", "crypto", "refund", "bitcoin", "loan", "tax", "inheritance", "cash", "payment", "money"]
    credential_keywords = ["password", "otp", "pin", "ssn", "social security", "card details", "credentials", "login details", "verification code"]
    greeting_keywords = ["dear customer", "dear user", "valued customer", "dear friend", "customer support"]

    detected_urgency = [word for word in urgency_keywords if word in text_lower]
    detected_financial = [word for word in financial_keywords if word in text_lower]
    detected_credentials = [word for word in credential_keywords if word in text_lower]
    detected_greetings = [word for word in greeting_keywords if word in text_lower]
    
    # Check for URLs
    url_pattern = r"https?://[^\s]+|www\.[^\s]+"
    urls = re.findall(url_pattern, text_lower)
    
    # Calculate score
    score = 0
    if detected_urgency:
        score += min(len(detected_urgency) * 15, 30)
    if detected_financial:
        score += min(len(detected_financial) * 10, 25)
    if detected_credentials:
        score += min(len(detected_credentials) * 20, 35)
    if detected_greetings:
        score += 15
    if urls:
        score += 25
        
    # Cap score at 100
    score = min(score, 100)
    
    # Determine risk level
    if score <= 20:
        risk_level = "Low Risk / Safe"
        risk_color = "Green"
        explanation = "This message seems safe, with no obvious signs of phishing. However, always remain vigilant and avoid sharing sensitive data."
    elif score <= 50:
        risk_level = "Suspicious"
        risk_color = "Yellow"
        explanation = "This message exhibits some suspicious characteristics, such as requesting generic actions or mentioning financial terms. Proceed with caution."
    else:
        risk_level = "High Risk Phishing"
        risk_color = "Red"
        explanation = "This message shows strong indicators of a phishing or social engineering scam. It uses urgency, requests credentials, or directs you to external links."

    # Generate tips
    tips = []
    if detected_urgency:
        tips.append("Do not rush. Scammers use urgency to prevent you from thinking clearly.")
    if detected_credentials:
        tips.append("Never share passwords, PINs, or OTPs. Legitimate organizations will never ask for them.")
    if urls:
        tips.append("Avoid clicking on links in suspicious messages. Manually type the official website address in your browser.")
    if detected_greetings:
        tips.append("Be cautious of generic greetings like 'Dear customer'. Legitimate emails usually address you by your real name.")
    if detected_financial:
        tips.append("Verify financial requests through an official, independent contact number for the bank or sender.")
        
    if not tips:
        tips.append("Always double check the sender's email address or phone number for subtle spelling errors.")

    return {
        "phishing_score": score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "indicators_detected": {
            "urgency": detected_urgency,
            "financial": detected_financial,
            "credentials": detected_credentials,
            "greetings": detected_greetings,
            "links": urls
        },
        "explanation": explanation,
        "tips": tips
    }

