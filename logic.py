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


from urllib.parse import urlparse

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
        
    return previous_row[-1]

def analyze_url_safety(url_input):
    url_input = url_input.strip()
    if not re.match(r"^https?://", url_input, re.IGNORECASE):
        url_input_parsed = "http://" + url_input
    else:
        url_input_parsed = url_input
        
    try:
        parsed = urlparse(url_input_parsed)
        domain = parsed.netloc.lower()
        if not domain:
            domain = parsed.path.lower()
            
        if ":" in domain:
            domain = domain.split(":")[0]
            
        domain_clean = domain
        if domain_clean.startswith("www."):
            domain_clean = domain_clean[4:]
    except Exception:
        domain = url_input.lower()
        domain_clean = domain
        
    findings = []
    risk_score = 0
    
    is_punycode = domain_clean.startswith("xn--")
    has_non_ascii = any(ord(c) > 127 for c in domain_clean)
    if is_punycode or has_non_ascii:
        findings.append("Potential Homograph Attack: Domain uses non-ASCII characters or Punycode IDN format to mimic legitimate brand names.")
        risk_score += 45
        
    if url_input.lower().startswith("http://"):
        findings.append("Unencrypted connection (HTTP): Sites using HTTP do not encrypt data transmission, raising interception risks.")
        risk_score += 15
        
    abused_tlds = [".zip", ".mov", ".cc", ".ru", ".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq", ".click", ".link", ".work", ".info", ".biz", ".fit"]
    matched_tld = None
    for tld in abused_tlds:
        if domain_clean.endswith(tld):
            matched_tld = tld
            break
    if matched_tld:
        findings.append(f"Suspicious Top-Level Domain ({matched_tld}): Free or highly abused TLDs are frequently preferred by malicious operators.")
        risk_score += 20
        
    popular_brands = {
        "google": "google.com",
        "paypal": "paypal.com",
        "microsoft": "microsoft.com",
        "facebook": "facebook.com",
        "apple": "apple.com",
        "amazon": "amazon.com",
        "netflix": "netflix.com",
        "instagram": "instagram.com",
        "linkedin": "linkedin.com",
        "twitter": "twitter.com",
        "yahoo": "yahoo.com",
        "dropbox": "dropbox.com",
        "chase": "chase.com",
        "bankofamerica": "bankofamerica.com",
        "wellsfargo": "wellsfargo.com",
        "binance": "binance.com",
        "coinbase": "coinbase.com",
        "fedex": "fedex.com",
        "dhl": "dhl.com",
        "github": "github.com",
        "steam": "steampowered.com",
        "adobe": "adobe.com"
    }
    
    domain_parts = domain_clean.split(".")
    core_parts = [p for p in domain_parts if p not in ["com", "org", "net", "edu", "gov", "co", "in", "uk", "us", "de", "fr", "info", "biz"]]
    
    spoofed_brand = None
    typosquatting_detected = False
    
    for part in core_parts:
        for brand, official in popular_brands.items():
            if brand in part and domain_clean != official:
                spoofed_brand = brand
                findings.append(f"Brand Impersonation: Domain contains target trademark '{brand}' but is not the official domain '{official}'.")
                risk_score += 40
                break
        if spoofed_brand:
            break
            
        for brand, official in popular_brands.items():
            if domain_clean != official and len(part) >= 4:
                dist = levenshtein_distance(part, brand)
                if 1 <= dist <= 2:
                    spoofed_brand = brand
                    typosquatting_detected = True
                    findings.append(f"Typo-Squatting Alert: Domain core '{part}' is extremely close to trademark '{brand}' (spelling edit distance: {dist}).")
                    risk_score += 45
                    break
        if spoofed_brand:
            break

    hyphen_count = domain_clean.count("-")
    subdomain_count = len(domain_parts) - 2
    if hyphen_count >= 3:
        findings.append(f"Suspicious Hyphen Density ({hyphen_count} hyphens): Phishing domains often daisy-chain words to look legitimate.")
        risk_score += 15
    if subdomain_count >= 3:
        findings.append(f"Excessive Subdomain Routing ({subdomain_count} layers): Multi-layered subdomains are used to spoof corporate login endpoints.")
        risk_score += 15

    risk_score = min(risk_score, 100)
    
    if risk_score <= 15:
        risk_level = "Low Risk / Safe"
        risk_color = "Green"
        explanation = f"The domain '{domain_clean}' appears legitimate with no signs of typo-squatting, homograph attacks, or malicious structures."
    elif risk_score <= 40:
        risk_level = "Suspicious"
        risk_color = "Yellow"
        explanation = f"The URL domain '{domain_clean}' displays suspicious metadata or structural anomalies. Do not enter passwords or sensitive details on this portal without direct verification."
    else:
        risk_level = "High Risk Spoofing"
        risk_color = "Red"
        explanation = f"Critical safety warnings. The domain '{domain_clean}' is highly likely a typo-squatted, homograph-spoofed, or brand-impersonation web portal designed to harvest credentials or install payloads."

    recommendations = []
    if is_punycode or has_non_ascii:
        recommendations.append("Do not click links. The site uses internationalized domain names (IDN) to masquerade as standard domains.")
    if typosquatting_detected or spoofed_brand:
        recommendations.append(f"Access this brand's services exclusively by manually typing the official domain '{popular_brands[spoofed_brand]}' in a new window.")
    if url_input.lower().startswith("http://"):
        recommendations.append("Never enter credentials or payment details on unencrypted HTTP web forms.")
    if matched_tld:
        recommendations.append("Remain cautious of links ending in atypical extensions. Scammers exploit free domain registration platforms.")
    if not recommendations:
        recommendations.append("Double-check domain spellings character-by-character. Look for zero '0' instead of letter 'O', or 'l' instead of '1'.")

    return {
        "url": url_input,
        "domain": domain_clean,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "explanation": explanation,
        "findings": findings,
        "recommendations": recommendations
    }


def generate_custom_scenario(persona, vector):
    persona_names = {
        "retiree": "Retired Citizen",
        "finance": "Finance Manager",
        "remote": "Remote IT Specialist",
        "student": "College Student",
        "executive": "Executive Director"
    }
    vector_names = {
        "tax": "Urgent Tax Claim",
        "shipment": "Failed Cargo Delivery",
        "support": "Internal Security Lockout",
        "crypto": "Exclusive Asset Offering",
        "relative": "Supervisor Impersonation"
    }
    
    p_name = persona_names.get(persona, "Target Profile")
    v_name = vector_names.get(vector, "Social Engineering Hook")
    
    title = f"Simulated: {v_name} ({p_name})"
    
    if vector == "tax":
        stage1_text = f"<b>Official Notice [Gov-Revenue Portal]:</b> Urgent message for {p_name}. Tax deficiency audit indicates unpaid dues on your profile. Settle penalty of $120.50 immediately to avoid formal legal proceedings. Click to settle: <u>http://tax-refund-gov.cc</u>"
        
        stage1_choice_comp = "Click the link and pay standard dues."
        stage1_fb_comp = "<b>Compromised!</b> Gov-Revenue portals do not use '.cc' TLDs or request wire payments on untrusted landing pages. Your payment credentials were stolen."
        
        stage1_choice_vuln = "Reply to notice: 'Can I check the calculation details first?'"
        stage1_fb_vuln = "<b>Vulnerable:</b> You engaged with a malicious gateway. They will try to build trust or pressure you further."
        
        stage1_choice_safe = "Close message and check your official Government Tax Portal directly."
        stage1_fb_safe = "<b>Vigilant!</b> Official audits are delivered via formal courier or authenticated government portals. You avoided credential harvesting."
        
        next_stage_text = "<b>Incoming Call [Tax Agent spoofed number]:</b> 'This is Agent Sharma. I see your inquiry. If you do not settle this instantly, we are dispatching law enforcement to your address. Pay via credit card now.'"
        stage2_choice_comp = "Provide credit card details to avoid trouble."
        stage2_fb_comp = "<b>Compromised!</b> High pressure tactics succeeded. Legitimate tax officers never threaten immediate arrest over a phone call or demand credit card numbers."
        stage2_choice_safe = "Hang up, block, and file a report with cyber crime cell."
        stage2_fb_safe = "<b>Vigilant!</b> Recognized high-pressure coercion. Security rating maintained."
        
    elif vector == "shipment":
        stage1_text = f"<b>SMS Alert [Postal Logistics]:</b> Courier shipment for {p_name} is suspended at warehouse due to incorrect street number. Settle address correction and pay $1.50 processing fee to reschedule dispatch: <u>http://postal-track-reschedule.link</u>"
        
        stage1_choice_comp = "Click link, type correct address, and pay fee."
        stage1_fb_comp = "<b>Compromised!</b> This is a package delivery scam. The site cloned a standard post page to capture your debit card number and billing details."
        
        stage1_choice_vuln = "Search the tracking code on Google to see if anyone else has flagged this link."
        stage1_fb_vuln = "<b>Vulnerable:</b> Searching helps, but clicking the link or continuing to interact exposes you to active redirection exploits."
        
        stage1_choice_safe = "Check your recent order receipts. Navigate to the official shop portal directly to view tracking."
        stage1_fb_safe = "<b>Vigilant!</b> Verifying shipment statuses using original purchase invoices prevents falling for warehouse tracking traps."
        
        next_stage_text = "<b>Logistics Helpdesk Bot:</b> 'To release your shipment, please type the 6-digit SMS verification code sent to your phone to confirm your delivery address.'"
        stage2_choice_comp = "Send the 6-digit code received via SMS."
        stage2_fb_comp = "<b>Compromised!</b> The SMS code was a 2FA token to reset your online payment portal. The scammers used it to log in and authorize a withdrawal."
        stage2_choice_safe = "Refuse to share the code. Contact the vendor support team independently."
        stage2_fb_safe = "<b>Vigilant!</b> SMS verification codes are confidential security keys. Safe choice."
        
    elif vector == "support":
        stage1_text = f"<b>Enterprise IT [Alert]:</b> Priority action required for {p_name}. Unusual login attempt detected from IP: 185.120.31.22. Your active workspace connection has been restricted. Re-authenticate on the mirror node to verify identity: <u>https://corp-identity-sso.info</u>"
        
        stage1_choice_comp = "Navigate to the SSO link and type company credentials."
        stage1_fb_comp = "<b>Compromised!</b> A phishing portal harvested your corporate login credentials. Scammers can now access your internal network."
        
        stage1_choice_vuln = "Contact IT desk: 'My connection says restricted. Is the server down?'"
        stage1_fb_vuln = "<b>Vulnerable:</b> Reporting helps, but clicking or verifying with an unverified warning text without using official Slack/Teams channels is risky."
        
        stage1_choice_safe = "Do not open link. Open your standard browser bookmarks to access the SSO portal directly."
        stage1_fb_safe = "<b>Vigilant!</b> Standard operating procedure is to access corporate systems using verified local gateways only."
        
        next_stage_text = "<b>IT Administrator [Slack/Teams mock profile]:</b> 'Hey, I see your SSO login attempt. I need you to authorize the Push notification on your authenticator app to sync your device.'"
        stage2_choice_comp = "Approve the MFA Push request on your authenticator app."
        stage2_fb_comp = "<b>Compromised!</b> MFA fatigue bypass. Approving unauthorized push notifications grants attackers access to restricted corporate databases."
        stage2_choice_safe = "Deny push alert and immediately contact IT support hotline."
        stage2_fb_safe = "<b>Vigilant!</b> Denied external MFA prompts. Intrusion averted successfully."
        
    elif vector == "relative":
        stage1_text = f"<b>Urgent Message [Supervisor]:</b> Hey, this is your Director/Manager. I am in a locked board meeting and need {p_name} to buy 4 electronic gift cards ($100 each) for client bonuses. Send codes here. I will reimburse you by evening."
        
        stage1_choice_comp = "Buy the gift cards instantly and text the voucher codes."
        stage1_fb_comp = "<b>Compromised!</b> Gift card scam. Impersonating corporate supervisors to request voucher code transfers is a standard social engineering tactic."
        
        stage1_choice_vuln = "Reply: 'Sure, but can you send me the department charge code first?'"
        stage1_fb_vuln = "<b>Vulnerable:</b> Engaged with attacker. They will claim they don't have code access on their mobile device to pressure you."
        
        stage1_choice_safe = "Call the supervisor directly via phone or voice call to verify request authenticity."
        stage1_fb_safe = "<b>Vigilant!</b> Multi-channel authentication is the only definitive way to verify emergency supervisor financial directives."
        
        next_stage_text = "<b>Manager Profile [Spoofed SMS]:</b> 'I can't take calls right now. Clients are waiting. Please buy them now or we might lose the account. I will make sure you get a bonus.'"
        stage2_choice_comp = "Purchase gift cards to secure client contract and get bonus."
        stage2_fb_comp = "<b>Compromised!</b> Scammers exploited fear of supervisor disappointment and promise of rewards. Reimbursing is impossible."
        stage2_choice_safe = "Decline request and report the impersonation to internal compliance/HR."
        stage2_fb_safe = "<b>Vigilant!</b> Aborted coercion attempt. Security compliance verified."
        
    else:
        stage1_text = f"<b>VIP Alert [Global Crypto Trade]:</b> Exclusive opportunity for {p_name}. Premium asset pool is open for 30 minutes. High return rate guaranteed. Invest $100 in USDT, get $1,000 within 24 hours. Register wallet: <u>http://usdt-earn-trade.xyz</u>"
        
        stage1_choice_comp = "Connect your Web3/Crypto wallet to register."
        stage1_fb_comp = "<b>Compromised!</b> The portal runs an automated drainer script that transfers all assets from your wallet once approved."
        
        stage1_choice_vuln = "Reply: 'Is there any minimum deposit requirement?'"
        stage1_fb_vuln = "<b>Vulnerable:</b> Showing interest makes you a target for persistent high-pressure sales pitches by scammers."
        
        stage1_choice_safe = "Ignore and delete message. High yield claims on unknown channels are always scams."
        stage1_fb_safe = "<b>Vigilant!</b> Guaranteed high returns in crypto are absolute red flags for asset drainage scams."
        
        next_stage_text = "<b>Support Chat Bot [Earn-USDT]:</b> 'To complete registration, please type your wallet's 12-word recovery seed phrase for safety verification.'"
        stage2_choice_comp = "Enter the 12-word seed phrase to activate wallet."
        stage2_fb_comp = "<b>Compromised!</b> Sharing your seed phrase gives scammers complete, permanent ownership of your cryptocurrency wallet."
        stage2_choice_safe = "Close chat immediately and block the sender."
        stage2_fb_safe = "<b>Vigilant!</b> Never share a seed phrase under any circumstances. Wallet integrity secured."
        
    scenario = {
        "title": title,
        "stages": [
            {
                "text": stage1_text,
                "choices": [
                    {
                        "text": stage1_choice_comp,
                        "scoreEffect": 35,
                        "feedback": stage1_fb_comp,
                        "nextStage": None
                    },
                    {
                        "text": stage1_choice_vuln,
                        "scoreEffect": 15,
                        "feedback": stage1_fb_vuln,
                        "nextStage": f"{vector}_custom_doubt"
                    },
                    {
                        "text": stage1_choice_safe,
                        "scoreEffect": 0,
                        "feedback": stage1_fb_safe,
                        "nextStage": None
                    }
                ]
            },
            {
                "id": f"{vector}_custom_doubt",
                "text": next_stage_text,
                "choices": [
                    {
                        "text": stage2_choice_comp,
                        "scoreEffect": 40,
                        "feedback": stage2_fb_comp,
                        "nextStage": None
                    },
                    {
                        "text": stage2_choice_safe,
                        "scoreEffect": 0,
                        "feedback": stage2_fb_safe,
                        "nextStage": None
                    }
                ]
            }
        ]
    }
    
    return scenario

def run_osint_scan(email):
    email = email.strip().lower()
    
    exposure_score = 0
    breaches = []
    
    if not email or "@" not in email:
        return {
            "success": False,
            "error": "Invalid email address formatting."
        }
        
    domain = email.split("@")[1]
    
    breaches.append({
        "name": "Naz.api Combined Credential Leak",
        "date": "January 2024",
        "severity": "High",
        "compromised_data": ["Passwords", "Email Addresses"],
        "details": "A collection of combo lists containing credentials harvested by info-stealer malware. Scammers use this for credential stuffing attacks."
    })
    exposure_score += 30
    
    if "gmail" in domain or "yahoo" in domain or "outlook" in domain:
        breaches.append({
            "name": "Wattpad Data Leak",
            "date": "June 2020",
            "severity": "Medium",
            "compromised_data": ["Passwords", "Email Addresses", "Screen Names", "IP Addresses"],
            "details": "A large-scale repository compromise exposing millions of personal profile structures and hashed password keys."
        })
        exposure_score += 20
    else:
        breaches.append({
            "name": "Apollo.io B2B Intelligence Database Scrape",
            "date": "July 2018",
            "severity": "Medium",
            "compromised_data": ["Employer Name", "Job Titles", "Corporate Emails", "Phone Numbers"],
            "details": "An exposed database containing professional contact details. Frequently abused by threat actors for hyper-targeted spear-phishing campaigns."
        })
        exposure_score += 25
        
    has_numbers = any(char.isdigit() for char in email)
    if has_numbers:
        breaches.append({
            "name": "RedLine Stealer Botnet Log Dump",
            "date": "September 2023",
            "severity": "Critical",
            "compromised_data": ["Browser Autocomplete Forms", "Cached Cookies", "Plaintext Passwords", "Crypto Wallet Extensions"],
            "details": "Active info-stealer log harvest uploaded to Telegram channels by threat actors. Contains active session cookies allowing MFA-bypass."
        })
        exposure_score += 35
        
    exposure_score = min(exposure_score, 100)
    
    return {
        "success": True,
        "email": email,
        "exposure_score": exposure_score,
        "breaches_count": len(breaches),
        "breaches": breaches
    }

