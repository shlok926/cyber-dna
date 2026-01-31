from flask import Flask, render_template, request, jsonify, send_file
from logic import analyze_responses
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
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

@app.route("/download-report", methods=["POST"])
def download_report():
    data = request.json

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ===== TITLE =====
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, height - 50, "Cyber DNA – Security Risk Report")
    pdf.line(50, height - 55, width - 50, height - 55)

    # ===== SUMMARY =====
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 90, "Overall Risk Level:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(230, height - 90, data["risk_level"])

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, height - 115, "Risk Score:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(230, height - 115, f"{data['total_score']} / 31")

    # ===== WEAK AREAS =====
    y = height - 160
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Identified Weak Areas")
    pdf.line(50, y - 3, 250, y - 3)

    y -= 25
    pdf.setFont("Helvetica-Bold", 11)

    if data["weak_areas"]:
        for area in data["weak_areas"]:
            pdf.drawString(60, y, f"• {area}")
            y -= 18
    else:
        pdf.setFont("Helvetica", 11)
        pdf.drawString(60, y, "• No major weak areas detected")

    # ===== RECOMMENDATIONS =====
    y -= 30
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Security Recommendations")
    pdf.line(50, y - 3, 300, y - 3)

    y -= 25
    for tip in data["recommendations"]:
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(60, y, "✔")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(80, y, tip)
        y -= 18

    # ===== FOOTER =====
    pdf.setFont("Helvetica-Oblique", 9)
    pdf.drawString(50, 40, "Generated for cyber awareness purposes only.")
    pdf.drawRightString(
        width - 50, 40,
        f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M')}"
    )

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name="Cyber_DNA_Report.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run()
