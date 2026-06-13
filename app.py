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

@app.route("/scam-alerts", methods=["GET"])
def scam_alerts():
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

