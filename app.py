"""
app.py — MailMind
AI-Powered Email Composer using Groq + LLaMA 3.3.

File structure:
  app.py      → Main Streamlit app (layout + logic)
  helpers.py  → Email utilities + HTML component builders
  style.py    → All CSS (CUSTOM_CSS string)
"""

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

from style import CUSTOM_CSS
from helpers import (
    build_signature,
    extract_subject_and_body,
    strip_auto_signoff,
    send_email,
    build_gmail_url,
    html_signature_preview,
    html_draft_card,
    html_attachment_banner,
    html_review_banner,
    html_confirm_banner,
    html_apppass_guide,
    html_env_warning,
    contains_sensitive_data,
)

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="MailMind · AI Email Composer",
    page_icon="✉️",
    layout="wide",                      # ← WIDE layout for full screen
)
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Top bar ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-brand">
        <div>
            <h1>✉ MailMind</h1>
            <div class="topbar-tagline">AI-Powered Email Composer · Groq + LLaMA 3.3</div>
        </div>
    </div>
    <div class="topbar-badge">
        <span class="topbar-dot"></span>
        Groq · Live
    </div>
</div>
""", unsafe_allow_html=True)

# ── API key guard ─────────────────────────────────────────────────────────────
if not GROQ_API_KEY:
    st.markdown(html_env_warning(), unsafe_allow_html=True)
    st.stop()

# ── Session state defaults ────────────────────────────────────────────────────
for k, v in {
    "draft_subject": "", "draft_body": "",
    "show_confirmation": False,
    "sender": "", "recipient": "",
    "sig_name": "", "sig_designation": "",
    "sig_contact": "", "sig_company": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# FORM  — two columns: left = config + signature, right = prompt + actions
# ─────────────────────────────────────────────────────────────────────────────
with st.form("email_form"):
    left, right = st.columns([1, 1], gap="large")

    # ── LEFT: Email config + Signature ──────────────────────────────────────
    with left:
        st.markdown('<div class="config-box"><p class="box-title">⚙️ &nbsp;Email Configuration</p>', unsafe_allow_html=True)
        sender = st.text_input("Your Email (From)", placeholder="you@gmail.com",
                               value=st.session_state.sender)
        recipient = st.text_input("Recipient Email (To)", placeholder="them@gmail.com",
                                  value=st.session_state.recipient)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="signature-box"><p class="box-title">✍️ &nbsp;Sender Signature</p>', unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1:
            sig_name    = st.text_input("Full Name",       placeholder="e.g. Rahul Sharma",        value=st.session_state.sig_name)
            sig_contact = st.text_input("Contact / Phone", placeholder="e.g. +91 98765 43210",     value=st.session_state.sig_contact)
        with s2:
            sig_designation = st.text_input("Designation", placeholder="e.g. Software Engineer",   value=st.session_state.sig_designation)
            sig_company     = st.text_input("Company",     placeholder="e.g. Aspire Technologies", value=st.session_state.sig_company)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT: Prompt + file + submit ────────────────────────────────────────
    with right:
        st.markdown('<div class="prompt-box"><p class="box-title">💬 &nbsp;What email do you want to send?</p>', unsafe_allow_html=True)
        prompt = st.text_area(
            "Email request",
            placeholder='e.g. "Send mail to HR requesting a half-day leave tomorrow for a personal appointment"',
            height=180,
            label_visibility="collapsed",
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="config-box"><p class="box-title">📎 &nbsp;Attachment (optional)</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Attach a file", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button(
            "✦  Generate Draft",
            type="primary",
            use_container_width=True,
        )

# ── Live signature preview ────────────────────────────────────────────────────
if any([sig_name, sig_designation, sig_contact, sig_company]):
    _, preview_col, _ = st.columns([1, 2, 1])
    with preview_col:
        st.markdown(
            html_signature_preview(sig_name, sig_designation, sig_company, sig_contact),
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────────────
# Generate draft
# ─────────────────────────────────────────────────────────────────────────────
if submitted:
    if not sender or not recipient:
        st.error("⚠️ Please fill in both From and To email addresses.")
    elif not prompt.strip():
        st.error("⚠️ Please describe the email you want to send.")      
    elif contains_sensitive_data(prompt):
        st.markdown("""
        <div style="
            background:#fff0f0;
            border:1px solid #e74c3c;
            border-left:5px solid #c0392b;
            padding:14px 16px;
            border-radius:6px;
            font-size:0.9rem;
            color:#922b21;
            line-height:1.6;
        ">
        🚫 <strong>Sensitive Information Detected</strong><br><br>

        Your request contains personal or confidential data (like password, bank details, or PIN).<br><br>

        🔒 For your security, this information will NOT be sent to the AI.<br><br>

        👉 Please remove sensitive details and try again.
        </div>
        """, unsafe_allow_html=True)
    
    else:
        with st.spinner("✍️ Composing your email via Groq…"):
            try:
                signature = build_signature(sig_name, sig_designation, sig_company, sig_contact)

                client = Groq(api_key=GROQ_API_KEY)
                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    max_tokens=1000,
                    messages=[
                        {"role": "system", "content": (
                        "You are a professional email writer with strict security rules.\n\n"
                        
                        "🚫 NEVER process or include any sensitive or personal information such as:\n"
                        "- Passwords or login credentials\n"
                        "- Bank account details or IFSC codes\n"
                        "- Credit/Debit card numbers or CVV\n"
                        "- UPI IDs or UPI PINs\n"
                        "- OTPs or verification codes\n"
                        "- Phone numbers or private contact details\n\n"
                        
                        "If the user request contains any such sensitive data:\n"
                        "- DO NOT generate the email\n"
                        "- DO NOT repeat the sensitive information\n"
                        "- Respond with a warning asking the user to remove confidential data\n\n"
                        
                        "Otherwise:\n"
                        "- Write a professional, concise email\n"
                        "- Respond ONLY with the email\n"
                        "- Start with: Subject: <subject line>\n"
                        "- Do NOT include any sign-off"
                    )},
                        {"role": "user", "content": (
                            f"From: {sender}\nTo: {recipient}\nRequest: {prompt}\n\n"
                            "Format strictly:\nSubject: <subject line>\n\n"
                            "<email body starting with Dear/Hi — stop before any sign-off>"
                        )},
                    ],
                )
                raw = resp.choices[0].message.content
                subject, body = extract_subject_and_body(raw)
                body = strip_auto_signoff(body)

                if signature:
                    body = body + "\n\n" + signature

                st.session_state.update({
                    "draft_subject":     subject,
                    "draft_body":        body,
                    "sender":            sender,
                    "recipient":         recipient,
                    "sig_name":          sig_name,
                    "sig_designation":   sig_designation,
                    "sig_contact":       sig_contact,
                    "sig_company":       sig_company,
                    "show_confirmation": True,
                })
            except Exception as e:
                err = str(e)
                if any(x in err.lower() for x in ["401", "invalid_api_key", "authentication"]):
                    st.error("❌ Invalid Groq API key in .env. Please check and restart.")
                else:
                    st.error(f"❌ Error: {err}")

# ─────────────────────────────────────────────────────────────────────────────
# Draft display + send controls
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.show_confirmation:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    draft_col, actions_col = st.columns([3, 2], gap="large")

    with draft_col:
        if uploaded_file:
            st.markdown(html_attachment_banner(), unsafe_allow_html=True)
        else:
            st.markdown(html_review_banner(), unsafe_allow_html=True)

        st.markdown(
            html_draft_card(
                st.session_state.sender,
                st.session_state.recipient,
                st.session_state.draft_subject,
                st.session_state.draft_body,
            ),
            unsafe_allow_html=True,
        )

        with st.expander("✏️ Edit draft before sending"):
            edited_subject = st.text_input("Subject", value=st.session_state.draft_subject, key="edit_subj")
            edited_body    = st.text_area("Body",    value=st.session_state.draft_body,    height=260, key="edit_body")
            if st.button("💾 Save edits"):
                st.session_state.draft_subject = edited_subject
                st.session_state.draft_body    = edited_body
                st.rerun()

    with actions_col:
        st.markdown(html_confirm_banner(), unsafe_allow_html=True)

        if uploaded_file:
            app_password = st.text_input("🔐 App Password", type="password")
            st.markdown(html_apppass_guide(), unsafe_allow_html=True)

            if st.button("📤 Send Email with Attachment", use_container_width=True, type="primary"):
                if not app_password:
                    st.error("⚠️ Please enter your App Password")
                else:
                    try:
                        send_email(
                            sender        = st.session_state.sender,
                            app_password  = app_password,
                            recipient     = st.session_state.recipient,
                            subject       = st.session_state.draft_subject,
                            body          = st.session_state.draft_body,
                            uploaded_file = uploaded_file,
                        )
                        st.success("✅ Email sent successfully with attachment!")
                    except Exception as e:
                        st.error(f"❌ Failed to send email: {e}")
        else:
            gmail_url = build_gmail_url(
                st.session_state.recipient,
                st.session_state.draft_subject,
                st.session_state.draft_body,
            )
            st.link_button(
                "📬 Open in Gmail Compose →",
                url=gmail_url,
                use_container_width=True,
                type="primary",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🗑  Discard Draft", use_container_width=True):
            st.session_state.show_confirmation = False
            st.session_state.draft_subject = ""
            st.session_state.draft_body    = ""
            st.rerun()

        st.markdown(
            '<div style="font-size:0.72rem;color:var(--muted);margin-top:0.6rem;text-align:center;">'
            "Gmail opens in a new tab · pre-filled · you decide when to send"
            "</div>",
            unsafe_allow_html=True,
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="footer">MailMind · Powered by Groq + LLaMA 3.3 · Keys stay local</div>', unsafe_allow_html=True)