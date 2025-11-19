from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from fpdf import FPDF
from datetime import datetime

app = Flask(__name__)

# ----------------------------------------
# FOLDER SETUP
# ----------------------------------------
VIDEO_1_5_DIR = "uploads/videos_1_5"
VIDEO_6_18_DIR = "uploads/videos_6_18"
PROJECT_DIR = "uploads/projects"
CERT_DIR = "uploads/certificates"

os.makedirs(VIDEO_1_5_DIR, exist_ok=True)
os.makedirs(VIDEO_6_18_DIR, exist_ok=True)
os.makedirs(PROJECT_DIR, exist_ok=True)
os.makedirs(CERT_DIR, exist_ok=True)

# ----------------------------------------
# HOME PAGE
# ----------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ----------------------------------------
# AGE GROUP PAGES
# ----------------------------------------
@app.route("/age/<group>")
def age_page(group):
    if group == "1-5":
        return render_template("age_1_5.html")
    elif group == "6-18":
        return render_template("age_6_18.html")
    elif group == "19-25":
        return render_template("age_19_25.html")
    else:
        return "Invalid age group"

# ----------------------------------------
# ANIMATED VIDEOS PAGE (AGE 1–5 UPLOADS)
# ----------------------------------------
@app.route("/animated-videos")
def animated_videos():
    videos = os.listdir(VIDEO_1_5_DIR)
    return render_template("animated_videos.html", videos=videos)

# ----------------------------------------
# UPLOAD VIDEO — AGE 1–5
# ----------------------------------------
@app.route("/videos/upload/1-5", methods=["GET", "POST"])
def upload_video_1_5():
    if request.method == "GET":
        return render_template("upload_video_1_5.html")

    file = request.files["video"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(VIDEO_1_5_DIR, filename))

    return "Uploaded for Age 1–5<br><br><a href='/age/1-5'>Back</a>"

# Serve video (Age 1–5)
@app.route("/videos/1-5/<filename>")
def serve_video_1_5(filename):
    return send_from_directory(VIDEO_1_5_DIR, filename)

# ----------------------------------------
# UPLOAD VIDEO — AGE 6–18
# ----------------------------------------
@app.route("/videos/upload/6-18", methods=["GET", "POST"])
def upload_video_6_18():
    if request.method == "GET":
        return render_template("upload_video_6_18.html")

    file = request.files["video"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(VIDEO_6_18_DIR, filename))

    return "Uploaded for Age 6–18<br><br><a href='/age/6-18'>Back</a>"

# Serve video (Age 6–18)
@app.route("/videos/6-18/<filename>")
def serve_video_6_18(filename):
    return send_from_directory(VIDEO_6_18_DIR, filename)

# ----------------------------------------
# SEE UPLOADED VIDEOS — AGE 6–18
# ----------------------------------------
@app.route("/videos/list/6-18")
def list_videos_6_18():
    videos = os.listdir(VIDEO_6_18_DIR)
    return render_template("list_video_6_18.html", videos=videos)

# ----------------------------------------
# KIT PAGE
# ----------------------------------------
@app.route("/kit")
def kit_page():
    return render_template("kit.html")

# ----------------------------------------
# DAY-TO-DAY PROBLEM STATEMENTS PAGE
# ----------------------------------------
@app.route("/problems")
def problems_page():
    return render_template("day_to_day.html")

# ----------------------------------------
# PROJECT UPLOAD (AGE 19–25) + CERTIFICATE
# ----------------------------------------
@app.route("/project/upload", methods=["POST"])
def upload_project():
    name = request.form.get("name")
    file = request.files.get("project")

    if not name or not file:
        return "Name or project missing"

    filename = secure_filename(file.filename)
    file.save(os.path.join(PROJECT_DIR, filename))

    # Generate certificate
    cert_filename = name.replace(" ", "_") + "_certificate.pdf"
    cert_path = os.path.join(CERT_DIR, cert_filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=22)
    pdf.cell(200, 20, txt="Certificate of Project Submission", ln=1, align="C")

    pdf.set_font("Arial", size=16)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Awarded to: {name}", ln=1, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="For successfully submitting the project.", ln=1, align="C")
    pdf.ln(20)

    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%d-%m-%Y')}", ln=1, align="C")

    pdf.output(cert_path)

    return f"""
    Project uploaded successfully!<br><br>
    <a href='/cert/{cert_filename}'><button>Download Certificate</button></a><br><br>
    <a href='/age/19-25'><button>Back</button></a>
    """

# Serve certificate
@app.route("/cert/<filename>")
def send_cert(filename):
    return send_from_directory(CERT_DIR, filename)

# ----------------------------------------
# RUN APP
# ----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)