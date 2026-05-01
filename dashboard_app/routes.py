import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
from flask import jsonify, render_template, request

load_dotenv()

MAIL_USER = os.environ.get("MAIL_USER", "").strip()
MAIL_PASS = os.environ.get("MAIL_PASS", "").strip()


def send_contact_email(name: str, user_email: str, message: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"New Quick Message from {name} ({user_email})"
    msg["From"] = MAIL_USER
    msg["To"] = MAIL_USER

    body = (
        f"New contact message received:\n\n"
        f"Name:    {name}\n"
        f"Email:   {user_email}\n"
        f"Message: {message}\n"
    )
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(MAIL_USER, MAIL_PASS)
        smtp.sendmail(MAIL_USER, MAIL_USER, msg.as_string())


def send_audit_email(user_email: str, tools: str, problem: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"New Free Data Audit Request from {user_email}"
    msg["From"] = MAIL_USER
    msg["To"] = MAIL_USER

    body = (
        f"New audit request received:\n\n"
        f"Email:   {user_email}\n"
        f"Tools:   {tools}\n"
        f"Problem: {problem}\n"
    )
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(MAIL_USER, MAIL_PASS)
        smtp.sendmail(MAIL_USER, MAIL_USER, msg.as_string())


def register_routes(server):
    @server.route("/")
    def home():
        return render_template("index.html")

    @server.route("/dashboard-service")
    def dashboard_service():
        return render_template("dashboard-section.html")

    @server.route("/data-analysis")
    def data_analysis():
        return render_template("data-analysis.html")

    @server.route("/automation")
    def automation():
        return render_template("automation-section.html")

    @server.route("/marketing-portfolio")
    def marketing_portfolio():
        return render_template("marketing-portfolio.html")

    @server.route("/sales-portfolio")
    def sales_portfolio():
        return render_template("sales-portfolio.html")

    @server.route("/underperforming-campaigns")
    def underperforming_campaigns():
        return render_template("underperforming-campaigns.html")

    @server.route("/reallocation-plan")
    def reallocation_plan():
        return render_template("reallocation-plan.html")

    @server.route("/submit-audit", methods=["POST"])
    def submit_audit():
        data = request.get_json(silent=True) or {}
        user_email = data.get("email", "").strip()
        tools = data.get("tools", "").strip()
        problem = data.get("problem", "").strip()

        if not user_email or not tools or not problem:
            return jsonify({"ok": False, "error": "Missing fields"}), 400

        try:
            send_audit_email(user_email, tools, problem)
            return jsonify({"ok": True})
        except Exception as exc:
            server.logger.error("Email send failed: %s", exc)
            return jsonify({"ok": False, "error": "Failed to send email"}), 500

    @server.route("/submit-contact", methods=["POST"])
    def submit_contact():
        data = request.get_json(silent=True) or {}
        name = data.get("name", "").strip()
        user_email = data.get("email", "").strip()
        message = data.get("message", "").strip()

        if not name or not user_email or not message:
            return jsonify({"ok": False, "error": "Missing fields"}), 400

        try:
            send_contact_email(name, user_email, message)
            return jsonify({"ok": True})
        except Exception as exc:
            server.logger.error("Contact email send failed: %s", exc)
            return jsonify({"ok": False, "error": "Failed to send email"}), 500

    @server.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @server.errorhandler(500)
    def internal_server_error(error):
        return render_template("500.html"), 500
