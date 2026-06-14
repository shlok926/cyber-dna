<p align="center">
  <img src="static/logo.png" width="180" height="180" alt="ChetnaScan AI Logo" style="border-radius: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.3);">
</p>

<h1 align="center">🛡️ ChetnaScan AI</h1>
<p align="center"><b>Adaptive Human Cybersecurity Assessment Command & Risk Scanner</b></p>

<p align="center">
  <i>Empowering users through cognitive cybersecurity awareness, real-time social engineering simulations, NLP threat scanning, and downloadable security audits.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask Framework">
  <img src="https://img.shields.io/badge/UI-HTML5%20%2F%20CSS3%20%2F%20JS-orange?style=flat-square&logo=html5&logoColor=white" alt="UI Stack">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Platform-Windows%20%2F%20macOS%20%2F%20Linux-lightgrey?style=flat-square" alt="Platforms">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License">
</p>

<p align="center">
  <a href="https://chetnascan-ai.vercel.app/" target="_blank">
    <img src="https://img.shields.io/badge/🚀_LAUNCH_LIVE_DEMO-ChetnaScan_AI-000000?style=for-the-badge&logo=vercel&logoColor=white" alt="Launch Live App">
  </a>
</p>

<p align="center">
  <a href="https://chetnascan-ai.vercel.app/" target="_blank">🌐 Live App</a> •
  <a href="#-key-features">✨ Features</a> •
  <a href="#-tech-stack">💻 Tech Stack</a> •
  <a href="#%EF%B8%8F-installation--setup">🚀 Installation</a> •
  <a href="#-project-architecture">📦 Architecture</a> •
  <a href="#-usage-guide">📖 Usage Guide</a> •
  <a href="#-future-scope">🌱 Future Roadmap</a>
</p>

---

## 🎯 Key Features at a Glance

| 🧠 Cognitive Profiling | 🛡️ Real-Time Simulator | 🔍 Threat Vector Scan | 📊 Live SOC Command |
| :--- | :--- | :--- | :--- |
| Behavior-based cyber risk scoring across multi-threat vectors. | Interactive real-time chat simulations of social engineering attacks. | Heuristic NLP scanning of suspicious texts & URLs. | Dashboard monitoring vigilance levels & unlocking badges. |

---

## 📋 Table of Contents

- [✨ Core Capabilities](#-core-capabilities)
- [💻 Tech Stack](#-tech-stack)
- [🚀 Installation & Setup](#%EF%B8%8F-installation--setup)
- [📦 Project Architecture](#-project-architecture)
- [📖 Usage Guide](#-usage-guide)
- [🛡️ Security Disclaimer](#%EF%B8%8F-security-disclaimer)
- [🌱 Future Scope](#-future-scope)
- [🤝 Contributing & Feedback](#-contributing--feedback)
- [⭐ Show Your Support](#-show-your-support)
- [👤 Author & Contact](#-author--contact)

---

## ✨ Core Capabilities

### 1. Human Vulnerability Assessment (Chetna Profiler)
* **Vulnerability Indexing**: Evaluates safety behavior across general cyber hygiene and specific incident scenarios.
* **Risk Categorization**: Automatically categorizes profile safety levels into **Low**, **Medium**, or **High** using a weighted scoring model.
* **PDF Audit Generation**: Leverages `ReportLab` to compile dynamic, formatted security reports complete with custom score breakdowns, remediation bullet points, and timestamped authenticity badges.

### 2. Threat Vector Scanner (Phishing & URL Parser)
* **Suspicious Text Analyzer**: Utilizes rule-based Natural Language Processing to detect high-urgency keywords, financial demands, coercive phrases, and other social engineering markers.
* **Spoof Link Inspector**: Evaluates input URLs for typo-squatting, structural anomalies, target domain spoofing, and malicious referral strings.

### 3. Interactive Social Engineering Simulator
* **Interactive Attack Scenarios**: Puts the user directly in simulated chat interface sessions (e.g. Bank OTP Verification Scam, Megamillions Prize Scam, Relative Crisis Scam).
* **Reflex & Stress Profiler**: Measures user decisions and conversation paths dynamically, logging vulnerability indicators if the user shares sensitive codes or gives in to high-stress social engineering traps.

### 4. Security Operations Center (SOC) Command Center
* **Vigilance Shield Status**: A reactive UI display that transitions from "Unassessed" to "Fortified" or "Breached" based on test and simulation outcomes.
* **Tactical Badges**: Dynamic achievement unlock system reward badges such as *Geneticist*, *Social Engineer Deflector*, and *ChetnaScan AI Sentinel* for verified behavior benchmarks.
* **Real-time Alert Center**: Slides out to present active vulnerability notifications and remediation checklists requiring user attention.

---

## 💻 Tech Stack

* **Frontend**: HTML5, Vanilla CSS3 (Custom styling with futuristic glassmorphism theme, CSS Variables, and micro-animations), Vanilla JavaScript (ES6+).
* **Backend**: Python (Flask micro-framework).
* **Document Engine**: ReportLab (Dynamic PDF design & rendering).
* **Security & Testing**: Built-in credential checks, OSINT simulation APIs.

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.10 or higher installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/shlok926/chetnascan-ai.git
cd chetnascan-ai
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Server
```bash
python app.py
```
*The web server will spin up locally at `http://127.0.0.1:5000/`.*

---

## 📦 Project Architecture

```structure
ChetnaScan_AI_Hackathon/
├── app.py                   # Main Flask application, routes, and PDF rendering engine
├── logic.py                 # Core analysis algorithms, simulator scenario loaders, and NLP logic
├── requirements.txt         # Project dependencies
├── Procfile                 # Production WSGI process deployment mapping
├── static/
│   ├── style.css            # Dark mode glassmorphism UI stylesheet
│   └── logo.png             # ChetnaScan AI branding logo image
├── templates/
│   └── index.html           # Single-page dashboard dashboard layout and JS logic
└── README.md                # Project documentation
```

---

## 📖 Usage Guide

1. **Conduct a Behavior Profile**: Select a target checklist, answer the weighted questions, and click **Generate ChetnaScan AI Profile** to get your score.
2. **Download Security Audits**: After completing the test or simulator, click the download button to export a detailed, professional PDF assessment report.
3. **Analyze Links & Messages**: Switch to the **Message Scanner** tab to instantly paste suspicious texts or inspect URLs for spoofing indicators.
4. **Train in Active Simulations**: Navigate to the **Attack Simulator**, choose a scam persona, start the chat session, and test if you can outsmart the simulated attacker.
5. **Monitor Your Score in the SOC**: View your vigilance shield status, alerts, and unlocked tactical badges on the **Security Center** dashboard.

---

## 🛡️ Security Disclaimer

This software is provided for educational and cybersecurity awareness purposes only. The assessment metrics, NLP scores, and simulator runs are heuristic evaluations of user-provided inputs and should not be used as a substitute for professional security audits, enterprise threat assessments, or compliance certifications.

---

## 🌱 Future Scope

- [ ] AI/NLP-based deep semantic threat understanding.
- [ ] User accounts database with historical safety graphs.
- [ ] Direct credential monitoring & active API integration with HaveIBeenPwned.
- [ ] Mobile-native application wrappers (PWA support).

---

## 🤝 Contributing & Feedback

Contributions, suggestions, and feedback are highly welcome!

* **Got suggestions or feature requests?** Feel free to open a new [Issue](https://github.com/shlok926/chetnascan-ai/issues) or share your ideas.
* **Want to contribute?** Feel free to fork this repository, make your changes, and submit a Pull Request.

---

## ⭐ Show Your Support

<p align="center"><b>Love this tool? Help us grow:</b></p>

```text
✨ Star the repository  (GitHub Star Button)
🐛 Report bugs          (GitHub Issues)
💡 Suggest features     (GitHub Discussions)
📢 Share with others    (LinkedIn/Twitter)
🤝 Contribute code      (Pull Requests)
```

---

## 👤 Author & Contact

<p align="center">
  <b>👨‍💻 Shlok Thorat</b>
</p>

<p align="center"><i>Let's connect on LinkedIn, collaborate, and build amazing things together!</i></p>

<p align="center">
  <a href="mailto:shlokthorat29075@gmail.com">
    <img src="https://img.shields.io/badge/Email-shlokthorat29075%40gmail.com-d14836?style=flat-square&logo=gmail&logoColor=white" alt="Email">
  </a>
  <a href="https://github.com/shlok926">
    <img src="https://img.shields.io/badge/GitHub-%40shlok926-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub">
  </a>
  <a href="https://www.linkedin.com/in/shlok-thorat-39916a405">
    <img src="https://img.shields.io/badge/LinkedIn-shlok--thorat--39916a405-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
</p>

---

<p align="center">
  Made with ❤️ for cyber security awareness • <a href="#-chetnascan-ai">Back to Top</a>
</p>
