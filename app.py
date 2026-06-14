from flask import Flask, render_template, request, jsonify, send_file
from logic import analyze_responses, analyze_text_phishing, analyze_url_safety, generate_custom_scenario, run_osint_scan
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    result = analyze_responses(data)
    return jsonify(result)

@app.route("/analyze-text", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "")
    result = analyze_text_phishing(text)
    return jsonify(result)

@app.route("/analyze-url", methods=["POST"])
def analyze_url():
    data = request.json
    url = data.get("url", "")
    result = analyze_url_safety(url)
    return jsonify(result)

@app.route("/generate-scenario", methods=["POST"])
def generate_scenario():
    data = request.json
    persona = data.get("persona", "retiree")
    vector = data.get("vector", "tax")
    result = generate_custom_scenario(persona, vector)
    return jsonify(result)

@app.route("/osint-scan", methods=["POST"])
def osint_scan():
    data = request.json
    email = data.get("email", "")
    result = run_osint_scan(email)
    return jsonify(result)


@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.json

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Calculation of Vigilance Rating
    total_score = data.get("total_score", 7)
    vigilance_pct = 100 - int(((total_score - 7) / 28) * 100)
    vigilance_pct = max(0, min(100, vigilance_pct))

    # Color definitions
    risk_color = data.get("risk_color", "Green").lower()
    if risk_color == "red":
        color_hex = "#ef4444"
        text_color_hex = "#ef4444"
    elif risk_color == "yellow":
        color_hex = "#f59e0b"
        text_color_hex = "#d97706"
    else:
        color_hex = "#10b981"
        text_color_hex = "#059669"

    # ===== 1. HEADER BANNER =====
    pdf.setFillColor(HexColor("#0f172a")) # Slate 900
    pdf.rect(0, height - 90, width, 90, fill=1, stroke=0)

    # Title and Subtitle
    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(40, height - 42, "CYBER DNA")
    
    pdf.setFillColor(HexColor("#38bdf8")) # Light blue
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(40, height - 62, "PERSONAL CYBER HYGIENE & VULNERABILITY AUDIT")

    # Header Metadata (Right Aligned)
    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawRightString(width - 40, height - 38, f"DATE: {datetime.now().strftime('%d %b %Y').upper()}")
    pdf.setFillColor(HexColor("#94a3b8"))
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(width - 40, height - 52, f"AUDIT ID: CDNA-{datetime.now().strftime('%m%d%H%M')}")
    pdf.drawRightString(width - 40, height - 66, "STATUS: OFFICIAL AUDIT")

    # ===== 2. AUDIT STATUS CARD =====
    card_y = height - 200
    card_h = 85
    card_w = width - 80
    
    pdf.setFillColor(HexColor("#f8fafc"))
    pdf.setStrokeColor(HexColor("#e2e8f0"))
    pdf.setLineWidth(1)
    pdf.rect(40, card_y, card_w, card_h, fill=1, stroke=1)

    # Left Column: Vigilance Index
    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(60, card_y + 60, "VIGILANCE SAFETY INDEX")
    
    pdf.setFillColor(HexColor(text_color_hex))
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(60, card_y + 35, f"{vigilance_pct}%")

    # Draw progress bar background
    bar_x, bar_y, bar_w, bar_h = 60, card_y + 18, 130, 8
    pdf.setFillColor(HexColor("#e2e8f0"))
    pdf.rect(bar_x, bar_y, bar_w, bar_h, fill=1, stroke=0)
    
    # Draw progress bar fill
    fill_w = bar_w * (vigilance_pct / 100)
    if fill_w > 0:
        pdf.setFillColor(HexColor(color_hex))
        pdf.rect(bar_x, bar_y, fill_w, bar_h, fill=1, stroke=0)

    # Vertical Divider Line
    pdf.setStrokeColor(HexColor("#cbd5e1"))
    pdf.line(220, card_y + 12, 220, card_y + card_h - 12)

    # Right Column: Details
    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(240, card_y + 60, "RISK PROFILE LEVEL:")
    pdf.setFillColor(HexColor(text_color_hex))
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(370, card_y + 60, data["risk_level"].upper())

    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(240, card_y + 40, "METRIC EVALUATION SCORE:")
    pdf.setFillColor(HexColor("#1e293b"))
    pdf.setFont("Helvetica", 10)
    pdf.drawString(370, card_y + 40, f"{data['total_score']} / 35")

    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(240, card_y + 20, "THREAT CATEGORY ASSESSED:")
    pdf.setFillColor(HexColor("#1e293b"))
    pdf.setFont("Helvetica", 9)
    # Get threat category if present, or general
    threat_cat = data.get("threat_category", "General Cyber Risk Check")
    pdf.drawString(370, card_y + 20, str(threat_cat).upper())

    # ===== 3. WEAK AREAS SECTION =====
    y = card_y - 35
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(40, y, "1. IDENTIFIED BEHAVIORAL VULNERABILITIES")
    
    # Accent line
    pdf.setStrokeColor(HexColor("#cbd5e1"))
    pdf.setLineWidth(1)
    pdf.line(40, y - 5, width - 40, y - 5)

    y -= 25
    if data.get("weak_areas"):
        for area in data["weak_areas"]:
            # Draw warning bullet
            pdf.setFillColor(HexColor("#f43f5e")) # Rose 500
            pdf.circle(55, y + 4, 3, fill=1, stroke=0)
            
            # Print item text
            pdf.setFillColor(HexColor("#334155"))
            pdf.setFont("Helvetica-Bold", 9.5)
            pdf.drawString(70, y, area)
            y -= 18
    else:
        pdf.setFillColor(HexColor("#10b981")) # Emerald 500
        pdf.circle(55, y + 4, 3, fill=1, stroke=0)
        
        pdf.setFillColor(HexColor("#475569"))
        pdf.setFont("Helvetica", 9.5)
        pdf.drawString(70, y, "No critical behavioral risks detected in this assessment cycle.")
        y -= 18

    # ===== 4. RECOMMENDATIONS SECTION =====
    y -= 15
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(40, y, "2. RECOMMENDATIONS & INCIDENT PREVENTION PROTOCOLS")
    
    pdf.setStrokeColor(HexColor("#cbd5e1"))
    pdf.line(40, y - 5, width - 40, y - 5)

    y -= 25
    for tip in data["recommendations"]:
        # Draw checkmark bullet
        pdf.setFillColor(HexColor("#10b981")) # Emerald 500
        pdf.circle(55, y + 4, 3, fill=1, stroke=0)
        
        # Print recommendation text
        pdf.setFillColor(HexColor("#334155"))
        pdf.setFont("Helvetica", 9.5)
        pdf.drawString(70, y, tip)
        y -= 18

    # ===== 5. FOOTER & DISCLAIMER =====
    pdf.setStrokeColor(HexColor("#e2e8f0"))
    pdf.setLineWidth(1)
    pdf.line(40, 55, width - 40, 55)

    pdf.setFillColor(HexColor("#64748b"))
    pdf.setFont("Helvetica-Oblique", 7.5)
    disclaimer = "Disclaimer: This assessment is for cyber security awareness purposes only and does not constitute technical penetration testing."
    pdf.drawString(40, 42, disclaimer)
    
    pdf.setFont("Helvetica", 7.5)
    pdf.drawRightString(width - 40, 42, "Generated by Cyber DNA Core Engine")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="Cyber_DNA_Report.pdf",
        mimetype="application/pdf"
    )

@app.route("/download-comprehensive-report", methods=["POST"])
def download_comprehensive_report():
    data = request.json
    history = data.get("history", [])
    osint_result = data.get("osint_result")
    protection_index = int(data.get("protection_index", 100))
    shield_status = data.get("shield_status", "UNASSESSED").upper()
    shield_desc = data.get("shield_desc", "")
    badges = data.get("badges", [])

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Color configuration based on status
    if shield_status in ["FORTIFIED", "SAFE"]:
        color_hex = "#10b981" # Emerald
        bg_card_hex = "#ecfdf5"
    elif shield_status in ["VIGILANT", "WARNING"]:
        color_hex = "#f59e0b" # Amber
        bg_card_hex = "#fffbeb"
    else:
        color_hex = "#ef4444" # Red
        bg_card_hex = "#fef2f2"

    # ==========================================
    # PAGE 1: EXECUTIVE SECURITY BRIEFING
    # ==========================================
    
    # 1. Slate Top Header Banner
    pdf.setFillColor(HexColor("#0f172a")) # Dark Slate
    pdf.rect(0, height - 100, width, 100, fill=1, stroke=0)

    # Title & Subtitle
    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(40, height - 45, "CYBER DNA")
    
    pdf.setFillColor(HexColor("#38bdf8")) # Sky Blue
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(40, height - 68, "EXECUTIVE CYBER RISK AUDIT & INTEGRATED SECURITY REPORT")

    # Header Metadata
    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawRightString(width - 40, height - 40, f"DATE: {datetime.now().strftime('%d %b %Y').upper()}")
    pdf.setFillColor(HexColor("#94a3b8"))
    pdf.setFont("Helvetica", 8.5)
    pdf.drawRightString(width - 40, height - 55, f"REPORT ID: CDNA-EXEC-{datetime.now().strftime('%m%d%H%M')}")
    pdf.drawRightString(width - 40, height - 70, "CLASSIFICATION: CONFIDENTIAL PERSONAL AUDIT")

    # Decorative Cyan Line under header
    pdf.setFillColor(HexColor("#0ea5e9"))
    pdf.rect(0, height - 103, width, 3, fill=1, stroke=0)

    # 2. Main Executive Summary Card
    card_y = height - 230
    card_h = 100
    card_w = width - 80
    
    pdf.setFillColor(HexColor(bg_card_hex))
    pdf.setStrokeColor(HexColor("#cbd5e1"))
    pdf.setLineWidth(1)
    pdf.rect(40, card_y, card_w, card_h, fill=1, stroke=1)

    # Draw left border accent highlight
    pdf.setFillColor(HexColor(color_hex))
    pdf.rect(40, card_y, 5, card_h, fill=1, stroke=0)

    # Overall Vigilance Index Label
    pdf.setFillColor(HexColor("#334155"))
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(65, card_y + 75, "INTEGRATED VIGILANCE SHIELD INDEX")

    # Large Percentage & Status
    pdf.setFillColor(HexColor(color_hex))
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(65, card_y + 42, f"{protection_index}%")
    
    pdf.setFillColor(HexColor("#1e293b"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(65, card_y + 22, f"POSTURE STATUS: {shield_status}")

    # Vertical Divider Line
    pdf.setStrokeColor(HexColor("#cbd5e1"))
    pdf.line(260, card_y + 12, 260, card_y + card_h - 12)

    # Summary Details (Right side of card)
    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(280, card_y + 75, "AUDIT METRICS & FINDINGS OVERVIEW:")

    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(HexColor("#334155"))
    num_tests = len(history)
    pdf.drawString(280, card_y + 55, f"• Assessments Completed: {num_tests} run(s)")
    
    badge_count = len(badges)
    pdf.drawString(280, card_y + 38, f"• Badges Unlocked: {badge_count} tactical badges")
    
    has_osint = "YES (Critical Leak Assessment)" if osint_result else "NO (Baseline Assessment)"
    pdf.drawString(280, card_y + 21, f"• Dark Web Scan Performed: {has_osint}")

    # 3. Badges Section
    badge_y = card_y - 35
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, badge_y, "1. UNLOCKED TACTICAL SECURITY BADGES")
    pdf.setStrokeColor(HexColor("#e2e8f0"))
    pdf.line(40, badge_y - 6, width - 40, badge_y - 6)

    # Draw badges
    y_pos = badge_y - 45
    if badges:
        col_w = (width - 80) / 2
        for idx, badge in enumerate(badges):
            col = idx % 2
            row = idx // 2
            bx = 40 + col * col_w
            by = y_pos - row * 40
            
            # Badge card container
            pdf.setFillColor(HexColor("#f8fafc"))
            pdf.setStrokeColor(HexColor("#e2e8f0"))
            pdf.rect(bx, by, col_w - 10, 32, fill=1, stroke=1)
            
            # Icon Dot
            pdf.setFillColor(HexColor("#0284c7"))
            pdf.circle(bx + 15, by + 16, 4, fill=1, stroke=0)
            
            # Title
            pdf.setFillColor(HexColor("#1e293b"))
            pdf.setFont("Helvetica-Bold", 8.5)
            pdf.drawString(bx + 28, by + 18, badge.get("title", ""))
            
            # Desc
            pdf.setFillColor(HexColor("#64748b"))
            pdf.setFont("Helvetica", 7.5)
            pdf.drawString(bx + 28, by + 7, badge.get("desc", ""))
        
        # Calculate new y position based on badge rows
        y_pos -= (((len(badges) + 1) // 2) * 40)
    else:
        pdf.setFillColor(HexColor("#475569"))
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.drawString(55, y_pos + 15, "No tactical badges unlocked. Complete behavioral profiles to earn recognition.")
        y_pos -= 20

    # 4. History Logs Section (Table)
    log_y = y_pos - 15
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, log_y, "2. SECURITY ASSESSMENT HISTORY LOGS")
    pdf.setStrokeColor(HexColor("#e2e8f0"))
    pdf.line(40, log_y - 6, width - 40, log_y - 6)

    # Draw Table Header
    th_y = log_y - 25
    pdf.setFillColor(HexColor("#f1f5f9"))
    pdf.rect(40, th_y - 4, width - 80, 18, fill=1, stroke=0)
    
    pdf.setFillColor(HexColor("#475569"))
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(50, th_y, "TIMESTAMP")
    pdf.drawString(180, th_y, "ASSESSMENT TYPE / THREAT CHECK")
    pdf.drawString(380, th_y, "SCORE")
    pdf.drawString(460, th_y, "RISK LEVEL")

    # Draw Table Rows (up to 6 records to fit page 1)
    tr_y = th_y - 20
    if history:
        for idx, entry in enumerate(history[:6]):
            # Alternate row background
            if idx % 2 == 1:
                pdf.setFillColor(HexColor("#f8fafc"))
                pdf.rect(40, tr_y - 4, width - 80, 16, fill=1, stroke=0)
                
            pdf.setFillColor(HexColor("#334155"))
            pdf.setFont("Helvetica", 8.5)
            pdf.drawString(50, tr_y, entry.get("timestamp", ""))
            pdf.drawString(180, tr_y, entry.get("type", ""))
            pdf.drawString(380, tr_y, entry.get("score", ""))
            
            # Risk color matching
            lvl_color = entry.get("color", "green").lower()
            if lvl_color == "red":
                pdf.setFillColor(HexColor("#ef4444"))
            elif lvl_color == "yellow":
                pdf.setFillColor(HexColor("#d97706"))
            else:
                pdf.setFillColor(HexColor("#10b981"))
                
            pdf.setFont("Helvetica-Bold", 8.5)
            pdf.drawString(460, tr_y, entry.get("level", "SAFE"))
            tr_y -= 18
    else:
        pdf.setFillColor(HexColor("#64748b"))
        pdf.setFont("Helvetica-Oblique", 9)
        pdf.drawString(50, tr_y - 5, "No history logs found in assessment databases.")
        tr_y -= 20

    # Page Footer
    pdf.setStrokeColor(HexColor("#cbd5e1"))
    pdf.line(40, 50, width - 40, 50)
    pdf.setFillColor(HexColor("#64748b"))
    pdf.setFont("Helvetica", 7.5)
    pdf.drawString(40, 38, "Cyber DNA Integrated Core Report - Confidential")
    pdf.drawRightString(width - 40, 38, "Page 1 of 2")

    # ==========================================
    # PAGE 2: OSINT EXPOSURE & TACTICAL MITIGATION
    # ==========================================
    pdf.showPage()

    # Smaller top header banner for Page 2
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.rect(0, height - 60, width, 60, fill=1, stroke=0)
    pdf.setFillColor(HexColor("#ffffff"))
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, height - 35, "CYBER DNA - INTEGRATED AUDIT REPORT")
    pdf.setFillColor(HexColor("#38bdf8"))
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawRightString(width - 40, height - 35, "SECTION II: OSINT LEAK DATA & SPECIFIC REMEDIATIONS")

    # 1. OSINT Exposure Data
    osint_y = height - 100
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, osint_y, "3. SIMULATED OSINT DARK WEB DATA EXPOSURE")
    pdf.setStrokeColor(HexColor("#e2e8f0"))
    pdf.line(40, osint_y - 6, width - 40, osint_y - 6)

    oy = osint_y - 25
    if osint_result:
        email_addr = osint_result.get("email", "")
        exp_index = int(osint_result.get("exposure_index", 0))
        breaches = osint_result.get("breaches", [])
        
        pdf.setFillColor(HexColor("#1e293b"))
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(40, oy, f"Target Scanned Identity: ")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(160, oy, email_addr)
        
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(380, oy, "Exposure Rating:")
        
        if exp_index >= 70:
            pdf.setFillColor(HexColor("#ef4444")) # Critical Red
            rating_txt = f"{exp_index}/100 (CRITICAL RISK)"
        elif exp_index >= 40:
            pdf.setFillColor(HexColor("#d97706")) # Medium Amber
            rating_txt = f"{exp_index}/100 (MEDIUM RISK)"
        else:
            pdf.setFillColor(HexColor("#10b981")) # Low Emerald
            rating_txt = f"{exp_index}/100 (LOW RISK)"
            
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(470, oy, rating_txt)
        
        oy -= 25
        pdf.setFillColor(HexColor("#475569"))
        pdf.setFont("Helvetica-Bold", 9)
        pdf.drawString(40, oy, f"Identified Data Breaches & Leaks ({len(breaches)} found):")
        oy -= 15

        for b in breaches[:4]: # Limit to 4 to fit clean page height
            # Draw leak summary card
            pdf.setFillColor(HexColor("#f8fafc"))
            pdf.setStrokeColor(HexColor("#cbd5e1"))
            pdf.rect(40, oy - 50, width - 80, 54, fill=1, stroke=1)
            
            # Left accent bar based on leak risk
            pdf.setFillColor(HexColor("#f43f5e"))
            pdf.rect(40, oy - 50, 4, 54, fill=1, stroke=0)
            
            # Title
            pdf.setFillColor(HexColor("#0f172a"))
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(55, oy - 4, b.get("name", ""))
            
            # Date
            pdf.setFillColor(HexColor("#64748b"))
            pdf.setFont("Helvetica", 7.5)
            pdf.drawRightString(width - 55, oy - 4, f"LEAK DATE: {b.get('date', '').upper()}")
            
            # Compromised parameters
            comp_data = ", ".join(b.get("compromised_data", []))
            pdf.setFillColor(HexColor("#b91c1c"))
            pdf.setFont("Helvetica-Bold", 8)
            pdf.drawString(55, oy - 16, f"COMPROMISED DATA: {comp_data}")
            
            # Description
            desc_text = b.get("details", "")
            # Wrap description into 2 lines if long
            pdf.setFillColor(HexColor("#475569"))
            pdf.setFont("Helvetica", 8)
            if len(desc_text) > 110:
                pdf.drawString(55, oy - 28, desc_text[:110])
                pdf.drawString(55, oy - 38, desc_text[110:220] + "...")
            else:
                pdf.drawString(55, oy - 28, desc_text)
                
            oy -= 64
    else:
        # Placeholder if OSINT not run
        pdf.setFillColor(HexColor("#f8fafc"))
        pdf.setStrokeColor(HexColor("#e2e8f0"))
        pdf.rect(40, oy - 45, width - 80, 50, fill=1, stroke=1)
        
        pdf.setFillColor(HexColor("#0284c7"))
        pdf.circle(60, oy - 20, 4, fill=1, stroke=0)
        
        pdf.setFillColor(HexColor("#334155"))
        pdf.setFont("Helvetica-Bold", 9.5)
        pdf.drawString(75, oy - 17, "No External Dark Web Credential Scans Run")
        pdf.setFillColor(HexColor("#64748b"))
        pdf.setFont("Helvetica", 8.5)
        pdf.drawString(75, oy - 32, "Verify your exposure index by performing an OSINT Leak Scan in the Security Operations Center (SOC).")
        oy -= 65

    # 2. Recommendations Section
    rec_y = oy - 10
    pdf.setFillColor(HexColor("#0f172a"))
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, rec_y, "4. TACTICAL MITIGATION GUIDANCE & RECOMMENDATIONS")
    pdf.setStrokeColor(HexColor("#e2e8f0"))
    pdf.line(40, rec_y - 6, width - 40, rec_y - 6)

    # Compile custom recommendations list
    recs = []
    # If OSINT leaks exist
    if osint_result and osint_result.get("breaches"):
        recs.append("A data breach contains your credentials. Change passwords on all shared accounts immediately.")
        recs.append("Implement Multi-Factor Authentication (MFA/2FA) on your email provider and corporate platforms.")
    
    # If behavioral scores are low
    has_unsafe = False
    for item in history:
        if "vulnerable" in item.get("level", "").lower() or "medium" in item.get("level", "").lower():
            has_unsafe = True
            break
            
    if has_unsafe or not history:
        recs.append("Verify email attachments or sender domains prior to logging into credential forms.")
        recs.append("Never share One-Time Passwords (OTPs) or authorization prompt tokens over phone or text.")
        recs.append("Establish out-of-band communication lines to verify identity when receiving money transfer requests.")
    else:
        recs.append("Maintain routine simulation practices on emerging threat vectors (like AI voice clones).")
        recs.append("Review connected applications permissions in your email and social accounts annually.")
        
    recs.append("Conduct a security profile evaluation at least once a quarter to update your Cyber DNA Shield.")

    # Render recommendations
    ry = rec_y - 25
    for r in recs[:5]:
        pdf.setFillColor(HexColor("#10b981")) # Green bullet
        pdf.circle(50, ry + 3, 2.5, fill=1, stroke=0)
        
        pdf.setFillColor(HexColor("#334155"))
        pdf.setFont("Helvetica", 9)
        pdf.drawString(65, ry, r)
        ry -= 18

    # Page Footer
    pdf.setStrokeColor(HexColor("#cbd5e1"))
    pdf.line(40, 50, width - 40, 50)
    
    pdf.setFillColor(HexColor("#64748b"))
    pdf.setFont("Helvetica-Oblique", 7.5)
    disclaimer = "Disclaimer: This comprehensive audit is based on local assessments and simulated exposures. Use it for organizational awareness."
    pdf.drawString(40, 38, disclaimer)
    
    pdf.setFont("Helvetica", 7.5)
    pdf.drawRightString(width - 40, 38, "Page 2 of 2")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="Cyber_DNA_Comprehensive_Audit.pdf",
        mimetype="application/pdf"
    )

@app.route("/scam-alerts", methods=["GET"])
def scam_alerts():
    import urllib.request
    import xml.etree.ElementTree as ET
    import re
    
    url = "https://www.cisa.gov/cybersecurity-advisories/all.xml"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    alerts = []
    try:
        with urllib.request.urlopen(req, timeout=4) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        items = root.findall(".//item")
        
        for idx, item in enumerate(items[:3]):
            title = item.find("title").text if item.find("title") is not None else "Active Security Advisory"
            link = item.find("link").text if item.find("link") is not None else "#"
            pub_date = item.find("pubDate").text if item.find("pubDate") is not None else "Trending Today"
            description = item.find("description").text if item.find("description") is not None else ""
            
            # Basic HTML tag strip and cleanup
            if description:
                description = re.sub('<[^<]+?>', '', description)
                description = description.replace("&nbsp;", " ").strip()
                if len(description) > 170:
                    description = description[:167] + "..."
            else:
                description = "CISA has released a trending cyber alert. Review specific advisory references for organizational threat mitigations."
            
            # Format CISA date cleanly
            clean_date = pub_date.split(" +")[0] if " +" in pub_date else pub_date
            clean_date = clean_date.split(" -")[0] if " -" in clean_date else clean_date
            if len(clean_date) > 16:
                clean_date = clean_date[:16]

            alerts.append({
                "id": idx + 1,
                "title": title,
                "type": "CISA Advisory Bulletin",
                "date": clean_date,
                "risk": "Critical Risk" if idx == 0 else "High Risk",
                "color": "red" if idx == 0 else "yellow",
                "description": description,
                "advisory": f"Review active CVE patches and apply security updates outlined in official advisory. Details: {link}"
            })
            
    except Exception as e:
        print("CISA Live RSS Feed fetch failed. Falling back to local threat alerts. Error:", e)

    # Fallback to rich local alerts if CISA fetch fails or yields empty list
    if not alerts:
        alerts = [
            {
                "id": 1,
                "title": "Smishing: USPS Courier Address Rescheduling",
                "type": "Package Delivery Scam",
                "date": "Trending Today",
                "risk": "High Risk",
                "color": "red",
                "description": "SMS alerts claiming package delivery is held at transit hub due to missing street numbers. Redirects to clone postal portals requesting address edits and minor processing fees.",
                "advisory": "Never click SMS links for delivery rescheduling. Check status directly on the official postal tracker using your original invoice tracking number."
            },
            {
                "id": 2,
                "title": "Vishing: AI Voice Cloning Urgent Impersonation",
                "type": "Voice Spoofing Scam",
                "date": "Active Threat",
                "risk": "Critical Risk",
                "color": "red",
                "description": "Scammers are using voice samples from social media reels/videos to clone relatives' voices. They call crying or in distress claiming they are in jail or had an accident and require urgent wire transfers.",
                "advisory": "Set up a secret safety passcode with your close family members. Always call the relative back on their known official contact number to verify."
            },
            {
                "id": 3,
                "title": "Phishing: Fake Electricity Bill Disconnection Alerts",
                "type": "Utility Fraud Scam",
                "date": "Highly Trending",
                "risk": "High Risk",
                "color": "yellow",
                "description": "WhatsApp messages or robocalls warning that electricity will be disconnected within 2 hours due to unpaid dues, prompting you to call a fake helpline number.",
                "advisory": "Utility providers do not contact users via personal WhatsApp numbers or request direct UPI payments to unofficial phone numbers."
            }
        ]
    return jsonify(alerts)

if __name__ == "__main__":
    app.run()

