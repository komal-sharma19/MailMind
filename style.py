CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;1,400&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Design tokens ─────────────────────────────────────────────────────────── */
:root {
    --bg:          #f7f5f2;
    --surface:     #ffffff;
    --surface-alt: #f9f8f6;
    --ink:         #1c1917;
    --ink-soft:    #44403c;
    --muted:       #78716c;
    --border:      #e5e0d8;
    --accent:      #c2410c;
    --accent-soft: #fff7ed;
    --gold:        #d97706;
    --green:       #15803d;
    --radius:      10px;
    --shadow:      0 1px 4px rgba(0,0,0,0.07), 0 0 0 1px rgba(0,0,0,0.04);
    --shadow-md:   0 4px 16px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.04);
}

/* ── Global reset ───────────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    background: var(--bg) !important;
    color: var(--ink) !important;
}
.block-container {
    padding: 0 2.5rem 4rem !important;
    max-width: 100% !important;
}
/* Hide default Streamlit chrome */
header[data-testid="stHeader"]   { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stStatusWidget"]   { display: none !important; }
footer                           { display: none !important; }

/* ── Top bar ────────────────────────────────────────────────────────────────── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--ink);
    padding: 1rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
}
.topbar-brand h1 {
    font-family: 'Lora', serif !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: #f5f2ee !important;
    margin: 0 !important;
    letter-spacing: 0;
}
.topbar-tagline {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    color: rgba(245,242,238,0.35);
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-top: 1px;
}
.topbar-badge {
    display: flex;
    align-items: center;
    gap: 7px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 4px 12px 4px 9px;
    border-radius: 100px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: rgba(245,242,238,0.45);
}
.topbar-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 8px #4ade80;
    animation: blink 2.5s ease-in-out infinite;
}
@keyframes blink {
    0%,100% { opacity:1; }
    50%      { opacity:0.4; }
}

/* ── Section labels (rendered via st.markdown, sit above fields) ────────────── */
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.63rem;
    font-weight: 500;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color: var(--muted);
    padding: 0 0 0.7rem 0;
    margin-top: 0.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.section-gap {
    height: 1.6rem;
}

/* ── Streamlit field labels ─────────────────────────────────────────────────── */
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stFileUploader"] label,
div[data-testid="stSelectbox"] label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.62rem !important;
    font-weight: 500 !important;
    letter-spacing: 1.1px !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

/* ── Inputs & textareas ─────────────────────────────────────────────────────── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.875rem !important;
    color: var(--ink) !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(217,119,6,0.12) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #bdb5ab !important;
    font-style: italic;
    font-size: 0.83rem !important;
}
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* ── File uploader ──────────────────────────────────────────────────────────── */
div[data-testid="stFileUploader"] section {
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface-alt) !important;
    padding: 0.8rem !important;
    transition: all 0.15s !important;
}
div[data-testid="stFileUploader"] section:hover {
    border-color: var(--gold) !important;
    background: var(--accent-soft) !important;
}

/* ── Generate Draft button ──────────────────────────────────────────────────── */
div[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    background: var(--ink) !important;
    color: #f7f5f2 !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    padding: 0.7rem !important;
    cursor: pointer !important;
    transition: background 0.15s, box-shadow 0.15s, transform 0.1s !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    background: #292524 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.22) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stFormSubmitButton"] button:active {
    transform: translateY(0) !important;
}

/* ── Regular buttons ────────────────────────────────────────────────────────── */
div[data-testid="stButton"] button {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    border-radius: var(--radius) !important;
    transition: all 0.15s !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: var(--ink) !important;
    color: #f7f5f2 !important;
    border: none !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background: #292524 !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] button:not([kind="primary"]) {
    background: var(--surface) !important;
    color: var(--ink-soft) !important;
    border: 1px solid var(--border) !important;
}
div[data-testid="stButton"] button:not([kind="primary"]):hover {
    border-color: var(--ink-soft) !important;
    background: var(--surface-alt) !important;
}

/* ── Link button (Open in Gmail) ────────────────────────────────────────────── */
div[data-testid="stLinkButton"] a {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: var(--ink) !important;
    color: #f7f5f2 !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    text-decoration: none !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.15s !important;
    width: 100% !important;
    box-sizing: border-box !important;
}
div[data-testid="stLinkButton"] a:hover {
    background: #292524 !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2) !important;
    transform: translateY(-1px) !important;
    color: white !important;
}

/* ── Divider ────────────────────────────────────────────────────────────────── */
.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2.2rem 0;
}

/* ── Signature preview ──────────────────────────────────────────────────────── */
.sig-preview {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: var(--radius);
    padding: 1rem 1.3rem;
    font-size: 0.84rem;
    line-height: 1.8;
    color: var(--ink);
    box-shadow: var(--shadow);
}
.sig-preview .sig-name   { font-weight: 600; font-size: 0.9rem; display: block; color: var(--ink); }
.sig-preview .sig-desig  { font-size: 0.77rem; color: var(--muted); display: block; }
.sig-preview .sig-detail { font-size: 0.75rem; color: var(--muted); display: block; }

/* ── Draft card ─────────────────────────────────────────────────────────────── */
.draft-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    margin: 0.8rem 0;
    box-shadow: var(--shadow-md);
    position: relative;
}
.draft-tag {
    position: absolute;
    top: -10px; left: 18px;
    background: var(--ink);
    color: #f7f5f2;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 2px 10px;
    border-radius: 100px;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.draft-tag::before {
    content: '';
    width: 5px; height: 5px;
    background: var(--gold);
    border-radius: 50%;
    display: inline-block;
}
.draft-meta {
    display: grid;
    grid-template-columns: 68px 1fr;
    gap: 0.35rem 0.8rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.1rem;
    align-items: baseline;
}
.meta-lbl {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--muted);
    font-weight: 500;
}
.draft-body {
    font-size: 0.875rem;
    line-height: 1.9;
    white-space: pre-wrap;
    color: var(--ink-soft);
}

/* ── Info banners ───────────────────────────────────────────────────────────── */
.confirm-banner {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 3px solid var(--gold);
    border-radius: var(--radius);
    padding: 0.85rem 1.1rem;
    font-size: 0.82rem;
    line-height: 1.65;
    color: #78350f;
    margin-bottom: 1.2rem;
}
.env-warning {
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 3px solid #e11d48;
    border-radius: var(--radius);
    padding: 1rem 1.4rem;
    font-size: 0.875rem;
    color: #881337;
    margin-bottom: 1.5rem;
    line-height: 1.65;
}
.alert-danger {
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 3px solid #e11d48;
    border-radius: var(--radius);
    padding: 1rem 1.4rem;
    font-size: 0.875rem;
    color: #881337;
    margin-bottom: 1rem;
    line-height: 1.65;
}

/* ── Expander ───────────────────────────────────────────────────────────────── */
div[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--surface) !important;
    box-shadow: var(--shadow) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--ink-soft) !important;
    padding: 0.8rem 1rem !important;
}
div[data-testid="stExpander"] summary:hover {
    background: var(--surface-alt) !important;
}

/* ── Alerts (st.error, st.success) ─────────────────────────────────────────── */
div[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    font-size: 0.875rem !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}

/* ── Spinner ────────────────────────────────────────────────────────────────── */
div[data-testid="stSpinner"] > div {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    color: var(--muted) !important;
}

/* ── Send note ──────────────────────────────────────────────────────────────── */
.send-note {
    font-size: 0.7rem;
    font-family: 'IBM Plex Mono', monospace;
    color: var(--muted);
    text-align: center;
    margin-top: 0.6rem;
    letter-spacing: 0.3px;
}

/* ── Footer ─────────────────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 0.5rem 0 2rem;
    opacity: 0.6;
}
</style>
"""