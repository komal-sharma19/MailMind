"""
helpers.py — MailMind
All helper functions: email logic, LLM utilities, and HTML component builders.
"""

import re
import smtplib
import urllib.parse
from email.message import EmailMessage


# ─────────────────────────────────────────────────────────────────────────────
# Email & LLM utilities
# ─────────────────────────────────────────────────────────────────────────────

def build_signature(name: str, designation: str, company: str, contact: str) -> str:
    parts = ["Best regards,", name or ""]
    if designation: parts.append(designation)
    if company:     parts.append(company)
    if contact:     parts.append(f"{contact}")
    return "\n".join(p for p in parts if p)


def extract_subject_and_body(raw: str):
    subject, body = "No Subject", raw.strip()
    m = re.search(r"^Subject:\s*(.+)$", raw, re.MULTILINE | re.IGNORECASE)
    if m:
        subject = m.group(1).strip()
        body = re.sub(r"^\n+", "", raw[m.end():].strip())
    return subject, body


def strip_auto_signoff(body: str) -> str:
    pattern = r"\n+(best regards?|warm regards?|sincerely|regards?|thanks?|thank you)[^\n]*\n.*$"
    body = re.sub(pattern, "", body, flags=re.IGNORECASE | re.DOTALL)
    return body.rstrip()


def send_email(sender: str, app_password: str, recipient: str,
               subject: str, body: str, uploaded_file=None) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = recipient
    msg.set_content(body)
    if uploaded_file:
        file_data = uploaded_file.read()
        msg.add_attachment(file_data, maintype="application",
                           subtype="octet-stream", filename=uploaded_file.name)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)


def build_gmail_url(recipient: str, subject: str, body: str) -> str:
    return (
        "https://mail.google.com/mail/?view=cm&fs=1"
        f"&to={urllib.parse.quote(recipient)}"
        f"&su={urllib.parse.quote(subject)}"
        f"&body={urllib.parse.quote(body)}"
    )


# ─────────────────────────────────────────────────────────────────────────────
# HTML component builders
# ─────────────────────────────────────────────────────────────────────────────

def html_header() -> str:
    return """
    <div class="mail-header">
        <h1>✉ MailMind</h1>
        <div class="tagline">AI-Powered Email Composer · Groq</div>
    </div>
    """


def html_signature_preview(name: str, designation: str, company: str, contact: str) -> str:
    lines = [f"<span class='sig-name'>{name}</span>"]
    if designation: lines.append(f"<span class='sig-desig'>{designation}</span>")
    if company:     lines.append(f"<span class='sig-detail'>{company}</span>")
    if contact:     lines.append(f"<span class='sig-detail'>{contact}</span>")
    return f"""
    <div style="font-size:0.75rem;color:var(--muted);letter-spacing:1px;text-transform:uppercase;margin:0.8rem 0 0.3rem;">
        Signature Preview
    </div>
    <div class="sig-preview">
        Best regards,<br>{"<br>".join(lines)}
    </div>
    """


def html_draft_card(sender: str, recipient: str, subject: str, body: str) -> str:
    body_safe = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <div class="draft-card">
        <div class="draft-tag">AI Draft · Groq</div>
        <div class="draft-meta">
            <span class="meta-lbl">From</span><span>{sender}</span>
            <span class="meta-lbl">To</span><span>{recipient}</span>
            <span class="meta-lbl">Subject</span><span><strong>{subject}</strong></span>
        </div>
        <div class="draft-body">{body_safe}</div>
    </div>
    """


def html_attachment_banner() -> str:
    return """
    <div style="background:#fff3cd;border:1px solid #ffeeba;border-left:5px solid #e67e22;
        padding:14px 16px;border-radius:6px;font-size:0.88rem;margin-bottom:12px;
        color:#7a5c00;line-height:1.6;">
        ⚠️ <strong>Attachment Detected</strong><br><br>
        You have added a file to this email.<br>
        <strong>This email will be sent directly when you click "Send Email".</strong><br><br>
        👉 If you want to review the email in Gmail first, please remove the attachment.
    </div>
    """


def html_review_banner() -> str:
    return """
    <div style="background:#e8f5e9;border:1px solid #c8e6c9;border-left:5px solid #2ecc71;
        padding:14px 16px;border-radius:6px;font-size:0.88rem;margin-bottom:12px;
        color:#1b5e20;line-height:1.6;">
        ✅ <strong>Review Mode</strong><br><br>
        No attachment added.<br>
        Clicking <strong>"Open in Gmail Compose"</strong> will allow you to review before sending.
    </div>
    """


def html_confirm_banner() -> str:
    return """
    <div class="confirm-banner">
        ⚠️ Review your draft above. Clicking <strong>"Open in Gmail Compose"</strong> opens Gmail
        with everything pre-filled. Nothing is sent until <em>you</em> click Send inside Gmail.
    </div>
    """

def contains_sensitive_data(text):
    patterns = [
        r"(upi\s*pin\s*[:\-]?\s*\d{4})",
        r"(otp\s*[:\-]?\s*\d{6})",
        r"(cvv\s*[:\-]?\s*\d{3})",
        r"(card\s*number\s*[:\-]?\s*\d{12,16})",
        r"(account\s*number\s*[:\-]?\s*\d+)",
        r"(ifsc\s*[:\-]?\s*[A-Z]{4}0[A-Z0-9]{6})",
        r"password\s*[:\-]?\s*\S+",
    ]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def html_apppass_guide() -> str:
    return """
    <div style="background:#f8f9fa;border:1px solid #ddd;border-left:4px solid #e8a838;
        padding:12px 16px;border-radius:6px;font-size:0.85rem;margin-top:8px;">
        <strong>🔐 How to get App Password:</strong><br><br>
        1️⃣ Go to your Google Account<br>
        2️⃣ Open <strong>Security</strong> settings<br>
        3️⃣ Turn ON <strong>2-Step Verification</strong><br>
        4️⃣ Search for <strong>App Passwords</strong><br>
        5️⃣ Generate a password for "Mail"<br>
        6️⃣ Paste that password here
    </div>
    """


def html_env_warning() -> str:
    return """
    <div class="env-warning">
        🔑 <strong>Groq API key not found.</strong><br>
        Add <code>GROQ_API_KEY=gsk_...</code> to your <code>.env</code> file and restart.
    </div>
    """