import streamlit as st
import fitz
import re
import pandas as pd
import sqlite3
import json
import hashlib
import hmac
import secrets
import os
import textwrap
import io
import zipfile
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="DevHandover AI",
    page_icon="📘",
    layout="wide"
)
# ==========================================================
# 1A. DARK PRODUCT UI THEME AND NAVIGATION
# ==========================================================
st.markdown("""
<style>
:root { --dha-bg:#0b1220; --dha-panel:#111c2e; --dha-panel2:#17243a; --dha-border:#263852; --dha-text:#e7eef8; --dha-muted:#9fb0c7; --dha-accent:#2dd4bf; --dha-accent2:#38bdf8; }
.stApp { background: radial-gradient(circle at 85% 0%, #14243a 0%, #0b1220 42%, #080e19 100%); color:var(--dha-text); }
[data-testid="stHeader"] { background:rgba(8,14,25,.82); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#101b2d 0%,#0b1423 100%); border-right:1px solid var(--dha-border); }
[data-testid="stSidebar"] a { color:#c8d7e9 !important; text-decoration:none; }
[data-testid="stSidebar"] a:hover { color:var(--dha-accent) !important; }
.block-container { padding-top:1.8rem; padding-bottom:3rem; max-width:1450px; }
h1,h2,h3 { color:#f2f7ff !important; letter-spacing:-.025em; }
h2 { padding-top:.35rem; }
p, label, .stMarkdown { color:var(--dha-text); }
[data-testid="stMetric"] { background:linear-gradient(145deg,#17263d,#101b2c); border:1px solid #2a3d58; border-radius:15px; padding:15px 17px; box-shadow:0 8px 24px rgba(0,0,0,.16); }
[data-testid="stMetricLabel"] { color:#9fb0c7 !important; }
[data-testid="stMetricValue"] { color:#f4fbff !important; }
.stButton>button, .stDownloadButton>button, button[kind="primary"] { border:1px solid rgba(45,212,191,.42); border-radius:10px; background:linear-gradient(100deg,#0f766e,#0e7490); color:white; font-weight:650; transition:all .18s ease; }
.stButton>button:hover, .stDownloadButton>button:hover { border-color:#5eead4; color:white; transform:translateY(-1px); }
input, textarea, [data-baseweb="select"] > div { background-color:#142238 !important; border-color:#314762 !important; border-radius:9px !important; }
[data-testid="stExpander"] { background:#111e31; border:1px solid #263a55; border-radius:12px; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid #263a55; border-radius:10px; overflow:hidden; }
hr { border-color:#263852 !important; }
.dha-hero { background:linear-gradient(115deg,rgba(20,49,69,.98),rgba(16,35,57,.98) 58%,rgba(15,73,75,.88)); border:1px solid #2b5265; border-radius:20px; padding:25px 28px; margin:8px 0 20px 0; box-shadow:0 14px 38px rgba(0,0,0,.22); }
.dha-eyebrow { color:#5eead4; font-size:12px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; margin-bottom:8px; }
.dha-title { color:#f4fbff; font-size:34px; line-height:1.15; font-weight:800; letter-spacing:-.04em; }
.dha-subtitle { color:#b9cde0; font-size:15px; margin-top:9px; max-width:850px; }
.dha-pill { display:inline-block; border:1px solid #347c79; background:rgba(13,148,136,.15); color:#99f6e4; border-radius:999px; padding:5px 11px; font-size:12px; font-weight:700; margin-top:15px; }
.dha-nav-title { color:#5eead4; font-size:11px; font-weight:800; letter-spacing:.15em; text-transform:uppercase; margin:8px 0 10px 0; }
.dha-nav a { display:block; padding:8px 10px; margin:3px 0; border-radius:8px; color:#c5d4e6 !important; background:rgba(255,255,255,.025); font-size:13px; }
.dha-nav a:hover { background:rgba(45,212,191,.12); color:#99f6e4 !important; }
.dha-section-note { color:#9fb0c7; font-size:13px; }

/* ======================================================
   ACCESSIBILITY + READABILITY OVERRIDES
   Preserve the existing navy / teal product identity.
   ====================================================== */
:root {
  color-scheme: dark;
  --dha-text: #f4f7fb;
  --dha-muted: #c0ccda;
  --dha-border: #40536d;
  --dha-focus: #7dd3fc;
}
html { scroll-behavior: smooth; }
body, .stApp, [data-testid="stAppViewContainer"] {
  color: #f4f7fb !important;
  font-size: 16px;
}
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
[data-testid="stCaptionContainer"], [data-testid="stText"],
[data-testid="stWidgetLabel"], label, .stRadio, .stCheckbox,
[data-testid="stExpander"] summary {
  color: #eaf1f8 !important;
}
.stMarkdown p, .stMarkdown li { line-height: 1.65; }
[data-testid="stCaptionContainer"] { color: #c0ccda !important; }
h1 { font-size: clamp(1.8rem, 3vw, 2.35rem) !important; line-height: 1.2 !important; }
h2 { font-size: clamp(1.4rem, 2.4vw, 1.8rem) !important; line-height: 1.3 !important; }
h3 { font-size: 1.2rem !important; line-height: 1.35 !important; }
.dha-title { font-size: clamp(1.9rem, 3.5vw, 2.45rem) !important; line-height: 1.2 !important; }
.dha-subtitle { color: #d5e2ef !important; line-height: 1.6 !important; }
.dha-section-note { color: #c0ccda !important; font-size: 14px !important; line-height: 1.5; }
/* Inputs: readable value, label, placeholder and clear focus state. */
input, textarea, [data-baseweb="select"] > div,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
  color: #f8fafc !important;
  background-color: #172840 !important;
  border-color: #536985 !important;
  font-size: 16px !important;
}
input::placeholder, textarea::placeholder { color: #bdc9d8 !important; opacity: 1 !important; }
[data-baseweb="select"] *, [data-testid="stSelectbox"] *,
[data-testid="stMultiSelect"] * { color: #f4f7fb !important; }
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
  color: #f4f7fb !important; font-weight: 650 !important; font-size: 15px !important;
}
input:focus, textarea:focus, [data-baseweb="select"]:focus-within,
button:focus-visible, a:focus-visible {
  outline: 3px solid var(--dha-focus) !important;
  outline-offset: 2px !important;
  border-color: var(--dha-focus) !important;
}
/* Buttons are larger and easier to distinguish. */
.stButton > button, .stDownloadButton > button,
[data-testid="stFormSubmitButton"] button {
  min-height: 44px;
  padding: 0.55rem 1rem;
  font-size: 15px !important;
  font-weight: 700 !important;
  border: 1px solid #5eead4 !important;
  background: #0f766e !important;
  color: #ffffff !important;
}
.stButton > button:hover, .stDownloadButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
  background: #115e59 !important; border-color: #99f6e4 !important;
}
/* Sidebar navigation and user identity. */
[data-testid="stSidebar"] { border-right: 1px solid #40536d !important; }
[data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] span {
  color: #eaf1f8 !important;
}
.dha-nav a { font-size: 14px !important; padding: 10px 12px !important; margin: 4px 0 !important; color: #eaf1f8 !important; }
.dha-nav a:hover { background: rgba(45,212,191,.2) !important; color: #ffffff !important; }
/* Cards, metrics, tables and expandable sections. */
[data-testid="stMetric"] { background: #172840 !important; border-color: #40536d !important; }
[data-testid="stMetricLabel"] { color: #c0ccda !important; }
[data-testid="stMetricValue"] { color: #ffffff !important; }
[data-testid="stExpander"] { background: #14243a !important; border-color: #40536d !important; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border-color: #40536d !important; }
[data-testid="stDataFrame"] *, [data-testid="stTable"] * { color: #f4f7fb; }
hr { border-color: #40536d !important; }
/* Status messages should remain legible against the dark background. */
[data-testid="stAlert"] { border-radius: 10px; }
[data-testid="stAlert"] p { color: inherit !important; }
/* Avoid cramped controls on narrow screens. */
@media (max-width: 768px) {
  .block-container { padding: 1rem 1rem 2rem 1rem !important; }
  .dha-hero { padding: 20px !important; border-radius: 14px !important; }
  .dha-title { font-size: 1.8rem !important; }
  .stButton > button, .stDownloadButton > button { width: 100%; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { scroll-behavior: auto !important; transition: none !important; }
}


/* Theme-aware Light Mode overrides. Streamlit applies data-theme to the
   document/app root; these rules override the dark-only accessibility CSS. */
html[data-theme="light"], body[data-theme="light"],
[data-testid="stAppViewContainer"][data-theme="light"] {
  color-scheme: light !important;
}
html[data-theme="light"] .stApp,
body[data-theme="light"] .stApp,
[data-testid="stAppViewContainer"][data-theme="light"] {
  background: #f5f7fb !important;
  color: #172033 !important;
}
html[data-theme="light"] [data-testid="stHeader"],
body[data-theme="light"] [data-testid="stHeader"] {
  background: rgba(255,255,255,.96) !important;
}
html[data-theme="light"] [data-testid="stSidebar"],
body[data-theme="light"] [data-testid="stSidebar"] {
  background: #ffffff !important;
  border-right: 1px solid #d7deea !important;
}
html[data-theme="light"] h1, html[data-theme="light"] h2,
html[data-theme="light"] h3, html[data-theme="light"] p,
html[data-theme="light"] .stMarkdown,
html[data-theme="light"] .stMarkdown p,
html[data-theme="light"] .stMarkdown li,
html[data-theme="light"] [data-testid="stText"],
html[data-theme="light"] [data-testid="stWidgetLabel"],
html[data-theme="light"] label,
body[data-theme="light"] h1, body[data-theme="light"] h2,
body[data-theme="light"] h3, body[data-theme="light"] p,
body[data-theme="light"] .stMarkdown,
body[data-theme="light"] .stMarkdown p,
body[data-theme="light"] .stMarkdown li,
body[data-theme="light"] [data-testid="stText"],
body[data-theme="light"] [data-testid="stWidgetLabel"],
body[data-theme="light"] label {
  color: #172033 !important;
}
html[data-theme="light"] [data-testid="stCaptionContainer"],
body[data-theme="light"] [data-testid="stCaptionContainer"] {
  color: #526174 !important;
}
html[data-theme="light"] input,
html[data-theme="light"] textarea,
html[data-theme="light"] [data-baseweb="select"] > div,
body[data-theme="light"] input,
body[data-theme="light"] textarea,
body[data-theme="light"] [data-baseweb="select"] > div {
  color: #172033 !important;
  background: #ffffff !important;
  border-color: #aebbd0 !important;
}
html[data-theme="light"] input::placeholder,
html[data-theme="light"] textarea::placeholder,
body[data-theme="light"] input::placeholder,
body[data-theme="light"] textarea::placeholder {
  color: #65748a !important;
  opacity: 1 !important;
}
html[data-theme="light"] [data-baseweb="select"] *,
html[data-theme="light"] [data-testid="stSelectbox"] *,
html[data-theme="light"] [data-testid="stMultiSelect"] *,
body[data-theme="light"] [data-baseweb="select"] *,
body[data-theme="light"] [data-testid="stSelectbox"] *,
body[data-theme="light"] [data-testid="stMultiSelect"] * {
  color: #172033 !important;
}
/* BaseWeb dropdown menu and options */
html[data-theme="light"] [data-baseweb="popover"],
html[data-theme="light"] [role="listbox"],
html[data-theme="light"] [role="option"],
body[data-theme="light"] [data-baseweb="popover"],
body[data-theme="light"] [role="listbox"],
body[data-theme="light"] [role="option"] {
  background: #ffffff !important;
  color: #172033 !important;
}
html[data-theme="light"] [data-testid="stMetric"],
body[data-theme="light"] [data-testid="stMetric"] {
  background: #ffffff !important;
  border: 1px solid #d7deea !important;
}
html[data-theme="light"] [data-testid="stMetricLabel"],
html[data-theme="light"] [data-testid="stMetricValue"],
body[data-theme="light"] [data-testid="stMetricLabel"],
body[data-theme="light"] [data-testid="stMetricValue"] {
  color: #172033 !important;
}
html[data-theme="light"] [data-testid="stExpander"],
body[data-theme="light"] [data-testid="stExpander"] {
  background: #ffffff !important;
  border-color: #d7deea !important;
}
html[data-theme="light"] [data-testid="stDataFrame"],
html[data-theme="light"] [data-testid="stDataEditor"],
html[data-theme="light"] [data-testid="stTable"],
body[data-theme="light"] [data-testid="stDataFrame"],
body[data-theme="light"] [data-testid="stDataEditor"],
body[data-theme="light"] [data-testid="stTable"] {
  background: #ffffff !important;
  border-color: #d7deea !important;
  color: #172033 !important;
  --gdg-bg-cell: #ffffff;
  --gdg-bg-cell-medium: #f3f6fa;
  --gdg-bg-header: #eef2f7;
  --gdg-bg-header-hovered: #e3eaf3;
  --gdg-text-dark: #172033;
  --gdg-text-medium: #344256;
  --gdg-text-light: #526174;
  --gdg-border-color: #d7deea;
  --gdg-accent-color: #0f766e;
}
html[data-theme="light"] [data-testid="stDataFrame"] *,
html[data-theme="light"] [data-testid="stTable"] *,
body[data-theme="light"] [data-testid="stDataFrame"] *,
body[data-theme="light"] [data-testid="stTable"] * {
  color: #172033 !important;
}
html[data-theme="light"] .dha-hero,
body[data-theme="light"] .dha-hero {
  background: linear-gradient(115deg,#e7f0f7,#edf5fb 58%,#e2f5f1) !important;
  border-color: #c5d8e4 !important;
}
html[data-theme="light"] .dha-eyebrow,
html[data-theme="light"] .dha-title,
html[data-theme="light"] .dha-subtitle,
html[data-theme="light"] .dha-pill,
body[data-theme="light"] .dha-eyebrow,
body[data-theme="light"] .dha-title,
body[data-theme="light"] .dha-subtitle,
body[data-theme="light"] .dha-pill {
  color: #173047 !important;
}
html[data-theme="light"] .dha-nav a,
html[data-theme="light"] [data-testid="stSidebar"] *,
body[data-theme="light"] .dha-nav a,
body[data-theme="light"] [data-testid="stSidebar"] * {
  color: #243449 !important;
}
html[data-theme="light"] .dha-nav a,
body[data-theme="light"] .dha-nav a { background: #f1f5f9 !important; }
html[data-theme="light"] hr, body[data-theme="light"] hr {
  border-color: #d7deea !important;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div class='dha-nav-title'>DEVHANDOVER AI</div>", unsafe_allow_html=True)
    st.markdown("**Workspace navigation**")
    st.markdown("""
    <div class="dha-nav">
      <a href="#workspace">01 · Workspace</a>
      <a href="#documentation">02 · Documentation</a>
      <a href="#knowledge-assistant">03 · Knowledge assistant</a>
      <a href="#knowledge-gaps">04 · Knowledge gaps</a>
      <a href="#knowledge-interview">05 · AI interview</a>
      <a href="#evidence-verification">06 · Evidence verification</a>
      <a href="#knowledge-map">07 · Knowledge map</a>
      <a href="#expertise-map">08 · Expertise map</a>
      <a href="#checkpoint-tracker">09 · Checkpoints</a>
      <a href="#continuity-risk">10 · Continuity risk</a>
      <a href="#readiness">11 · Successor readiness</a>
      <a href="#project-history">12 · Project history</a>
      <a href="#handover-package">13 · Handover package</a>
      <a href="#successor-workspace">14 · Successor workspace</a>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Knowledge continuity · Risk visibility · Confident handovers")
# ==========================================================
# 2. SQLITE DATABASE SETUP
# ==========================================================
DB_NAME = "devhandover.db"
def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# ==========================================================
# 2B. BACKUP AND RESTORE UTILITIES
# ==========================================================
BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)
BACKUP_INTERVAL_DAYS = 30


def build_backup_archive():
    """Create a consistent ZIP backup using SQLite's online backup API."""
    if not Path(DB_NAME).exists():
        raise FileNotFoundError("The project database does not exist yet.")

    with tempfile.TemporaryDirectory() as temp_dir:
        snapshot_path = Path(temp_dir) / "devhandover.db"
        source_connection = sqlite3.connect(DB_NAME)
        destination_connection = sqlite3.connect(str(snapshot_path))
        try:
            source_connection.backup(destination_connection)
        finally:
            destination_connection.close()
            source_connection.close()

        integrity_connection = sqlite3.connect(str(snapshot_path))
        integrity_result = integrity_connection.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]
        integrity_connection.close()
        if integrity_result != "ok":
            raise sqlite3.DatabaseError("Database integrity check failed.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"devhandover_backup_{timestamp}.zip"
        metadata = {
            "application": "DevHandover AI",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "database_file": "devhandover.db",
            "backup_contents": "SQLite database including users, workspaces, extracted PDF text/pages, interviews, risks, readiness and handover records.",
            "format_version": 1
        }
        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(snapshot_path, arcname="devhandover.db")
            archive.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
        return backup_name, archive_buffer.getvalue()


def save_automatic_backup():
    """Create a local automatic backup if none exists or 30 days have passed."""
    existing_backups = sorted(BACKUP_DIR.glob("devhandover_backup_*.zip"))
    if existing_backups:
        latest_backup = max(existing_backups, key=lambda item: item.stat().st_mtime)
        last_backup_time = datetime.fromtimestamp(latest_backup.stat().st_mtime)
        if datetime.now() - last_backup_time < timedelta(days=BACKUP_INTERVAL_DAYS):
            return False, latest_backup.name

    backup_name, backup_bytes = build_backup_archive()
    backup_path = BACKUP_DIR / backup_name
    backup_path.write_bytes(backup_bytes)
    return True, backup_name


def validate_backup_archive(backup_bytes):
    """Validate ZIP structure, required database, integrity and app tables."""
    with zipfile.ZipFile(io.BytesIO(backup_bytes), "r") as archive:
        names = set(archive.namelist())
        if "devhandover.db" not in names or "backup_metadata.json" not in names:
            raise ValueError("This is not a valid DevHandover AI backup ZIP.")
        metadata = json.loads(archive.read("backup_metadata.json").decode("utf-8"))
        if metadata.get("application") != "DevHandover AI":
            raise ValueError("The backup does not belong to DevHandover AI.")
        database_bytes = archive.read("devhandover.db")

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        temp_file.write(database_bytes)

    try:
        check_connection = sqlite3.connect(str(temp_path))
        integrity = check_connection.execute("PRAGMA integrity_check").fetchone()[0]
        tables = {row[0] for row in check_connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()}
        check_connection.close()
        required_tables = {"users", "workspaces", "documents"}
        if integrity != "ok" or not required_tables.issubset(tables):
            raise ValueError("The backup database is damaged or incomplete.")
        return temp_path
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def restore_backup_archive(backup_bytes):
    """Create a safety copy, then atomically replace the active database."""
    validated_database = validate_backup_archive(backup_bytes)
    try:
        safety_name, safety_bytes = build_backup_archive()
        safety_path = BACKUP_DIR / f"before_restore_{safety_name}"
        safety_path.write_bytes(safety_bytes)
        os.replace(str(validated_database), DB_NAME)
        return safety_path.name
    finally:
        validated_database.unlink(missing_ok=True)

def create_knowledge_interview(workspace_id, topic, interviewee):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO knowledge_interviews (
            workspace_id, topic, interviewee, status, created_at
        ) VALUES (?, ?, ?, 'In Progress', ?)
    """, (workspace_id, topic, interviewee, datetime.now().isoformat()))
    interview_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return interview_id


def save_interview_response(
    interview_id, question, answer, completeness,
    follow_up_question, structured_note
):
    connection = get_connection()
    connection.execute("""
        INSERT INTO interview_responses (
            interview_id, question, answer, completeness,
            follow_up_question, structured_note, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        interview_id, question, answer, completeness,
        follow_up_question, structured_note, datetime.now().isoformat()
    ))
    connection.commit()
    connection.close()


def get_interview_display_number(workspace_id, interview_id):
    """Return a workspace-local interview number without changing database IDs."""
    connection = get_connection()
    number = connection.execute("""
        SELECT COUNT(*)
        FROM knowledge_interviews
        WHERE workspace_id = ? AND id <= ?
    """, (workspace_id, interview_id)).fetchone()[0]
    connection.close()
    return number


def get_interview_history(workspace_id):
    connection = get_connection()
    rows = connection.execute("""
        SELECT ki.id, ki.topic, ki.interviewee, ki.status, ki.created_at,
               ir.question, ir.answer, ir.completeness,
               ir.follow_up_question, ir.structured_note, ir.created_at
        FROM knowledge_interviews ki
        LEFT JOIN interview_responses ir ON ki.id = ir.interview_id
        WHERE ki.workspace_id = ?
        ORDER BY ki.id DESC, ir.id ASC
    """, (workspace_id,)).fetchall()
    connection.close()
    return rows


def get_knowledge_gaps(workspace_id):
    """Return AI-detected knowledge gaps for one workspace."""
    connection = get_connection()
    rows = connection.execute("""
        SELECT id, knowledge_area, gap_description, severity, status,
               follow_up_question, source_question, created_at
        FROM knowledge_gaps
        WHERE workspace_id = ?
        ORDER BY
            CASE severity
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                ELSE 4
            END,
            id DESC
    """, (workspace_id,)).fetchall()
    connection.close()
    return rows


def save_knowledge_gap(
    workspace_id, interview_id, knowledge_area, gap_description,
    severity, follow_up_question, source_question, source_answer
):
    """Persist a gap found during an interview without changing interview history."""
    connection = get_connection()
    now = datetime.now().isoformat()
    connection.execute("""
        INSERT INTO knowledge_gaps (
            workspace_id, interview_id, knowledge_area, gap_description,
            severity, status, follow_up_question, source_question,
            source_answer, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, 'Open', ?, ?, ?, ?, ?)
    """, (
        workspace_id, interview_id, knowledge_area, gap_description,
        severity, follow_up_question, source_question, source_answer, now, now
    ))
    connection.commit()
    connection.close()


def update_knowledge_gap_status(gap_id, workspace_id, status):
    """Update only the selected gap belonging to the active workspace."""
    connection = get_connection()
    connection.execute("""
        UPDATE knowledge_gaps
        SET status = ?, updated_at = ?
        WHERE id = ? AND workspace_id = ?
    """, (status, datetime.now().isoformat(), gap_id, workspace_id))
    connection.commit()
    connection.close()


def save_evidence_verification_results(workspace_id, results):
    """Persist a complete evidence-verification run for the active workspace."""
    connection = get_connection()
    connection.execute("""
        INSERT INTO evidence_verification_runs (workspace_id, results_json, verified_at)
        VALUES (?, ?, ?)
    """, (workspace_id, json.dumps(results, ensure_ascii=False), datetime.now().isoformat()))
    connection.commit()
    connection.close()


def get_latest_evidence_verification(workspace_id):
    """Load the latest saved evidence-verification run for one workspace."""
    connection = get_connection()
    row = connection.execute("""
        SELECT results_json, verified_at
        FROM evidence_verification_runs
        WHERE workspace_id = ?
        ORDER BY id DESC LIMIT 1
    """, (workspace_id,)).fetchone()
    connection.close()
    if not row:
        return [], None
    try:
        results = json.loads(row[0] or "[]")
        if not isinstance(results, list):
            results = []
    except (TypeError, json.JSONDecodeError):
        results = []
    return results, row[1]


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE COLLATE NOCASE,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Successor',
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workspaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            outgoing_employee TEXT NOT NULL,
            successor TEXT NOT NULL,
            deadline TEXT,
            created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER,
            filename TEXT,
            document_hash TEXT,
            extracted_text TEXT,
            pages_json TEXT,
            created_at TEXT,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)
    # Migrate older databases whose document_hash was globally UNIQUE.
    # A PDF hash must be unique only inside its workspace, not across all workspaces.
    document_table_sql = cursor.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='documents'"
    ).fetchone()[0]
    if document_table_sql and 'document_hash TEXT UNIQUE' in document_table_sql:
        cursor.execute("ALTER TABLE documents RENAME TO documents_old_global_hash")
        cursor.execute("""
            CREATE TABLE documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workspace_id INTEGER,
                filename TEXT,
                document_hash TEXT,
                extracted_text TEXT,
                pages_json TEXT,
                created_at TEXT,
                FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
            )
        """)
        cursor.execute("""
            INSERT INTO documents (id, workspace_id, filename, document_hash,
                                  extracted_text, pages_json, created_at)
            SELECT id, workspace_id, filename, document_hash,
                   extracted_text, pages_json, created_at
            FROM documents_old_global_hash
        """)
        cursor.execute("DROP TABLE documents_old_global_hash")
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_documents_workspace_hash
        ON documents(workspace_id, document_hash)
    """)
    # Additive semantic index: existing document and workspace records remain untouched.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS semantic_chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            document_hash TEXT NOT NULL,
            document_name TEXT NOT NULL,
            page_number INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            chunk_text TEXT NOT NULL,
            embedding_json TEXT NOT NULL,
            embedding_model TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(workspace_id, document_hash, page_number, chunk_index, embedding_model),
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risk_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER,
            risk_data TEXT,
            average_risk REAL,
            created_at TEXT,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readiness_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER,
            readiness_score INTEGER,
            completed_activities INTEGER,
            technical_notes TEXT,
            pending_tasks TEXT,
            manager_name TEXT,
            approved INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            interviewee TEXT,
            status TEXT DEFAULT 'In Progress',
            created_at TEXT,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            completeness TEXT,
            follow_up_question TEXT,
            structured_note TEXT,
            created_at TEXT,
            FOREIGN KEY(interview_id) REFERENCES knowledge_interviews(id)
        )
    """)
    # Additive AI knowledge-gap records; existing interview and gap data remain untouched.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_gaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            interview_id INTEGER,
            knowledge_area TEXT NOT NULL,
            gap_description TEXT NOT NULL,
            severity TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'Open',
            follow_up_question TEXT,
            source_question TEXT,
            source_answer TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id),
            FOREIGN KEY(interview_id) REFERENCES knowledge_interviews(id)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_knowledge_gaps_workspace_status
        ON knowledge_gaps(workspace_id, status, severity)
    """)
    # Additive storage for evidence-verification runs used by the unified dashboard.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence_verification_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            results_json TEXT NOT NULL,
            verified_at TEXT NOT NULL,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_evidence_runs_workspace
        ON evidence_verification_runs(workspace_id, id)
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS successor_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            successor_name TEXT,
            question TEXT NOT NULL,
            answer TEXT,
            source_pages TEXT,
            source_types TEXT,
            created_at TEXT,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS domain_expertise (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            knowledge_area TEXT NOT NULL,
            team_member TEXT,
            expertise_level TEXT,
            is_primary TEXT,
            backup_member TEXT,
            evidence_notes TEXT,
            updated_at TEXT,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS handover_checkpoints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            workspace_id INTEGER NOT NULL,
            checkpoint TEXT NOT NULL,
            description TEXT,
            owner TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'Planned',
            evidence_notes TEXT,
            updated_at TEXT,
            FOREIGN KEY(workspace_id) REFERENCES workspaces(id)
        )
    """)
    connection.commit()
    connection.close()

def hash_user_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 310000
    ).hex()
    return digest, salt

def register_user(username, email, password, role):
    password_hash, salt = hash_user_password(password)
    connection = get_connection()
    try:
        connection.execute("""
            INSERT INTO users (username, email, password_hash, password_salt, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username.strip(), email.strip().lower(), password_hash, salt,
              role, datetime.now().isoformat()))
        connection.commit()
        return True, "Account created. You can now sign in."
    except sqlite3.IntegrityError:
        return False, "That username or email is already registered."
    finally:
        connection.close()

def authenticate_user(username_or_email, password):
    connection = get_connection()
    user = connection.execute("""
        SELECT id, username, email, password_hash, password_salt, role
        FROM users WHERE username = ? COLLATE NOCASE OR email = ? COLLATE NOCASE
    """, (username_or_email.strip(), username_or_email.strip())).fetchone()
    connection.close()
    if not user:
        return None
    candidate, _ = hash_user_password(password, user[4])
    if hmac.compare_digest(candidate, user[3]):
        return {"id": user[0], "username": user[1], "email": user[2], "role": user[5]}
    return None

def get_user_count():
    connection = get_connection()
    count = connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    connection.close()
    return count

def get_domain_expertise(workspace_id):
    connection = get_connection()
    rows = connection.execute("""
        SELECT knowledge_area, team_member, expertise_level, is_primary,
               backup_member, evidence_notes
        FROM domain_expertise WHERE workspace_id = ?
        ORDER BY id
    """, (workspace_id,)).fetchall()
    connection.close()
    columns = ["Knowledge Area", "Team Member", "Expertise Level",
               "Role", "Backup Member", "Evidence / Notes"]
    return pd.DataFrame(rows, columns=columns)


def save_domain_expertise(workspace_id, dataframe):
    connection = get_connection()
    connection.execute("DELETE FROM domain_expertise WHERE workspace_id = ?", (workspace_id,))
    for _, row in dataframe.iterrows():
        area = str(row.get("Knowledge Area", "")).strip()
        member = str(row.get("Team Member", "")).strip()
        if not area or area.lower() == "nan":
            continue
        def clean(value):
            value = str(value).strip()
            return "" if value.lower() in ("nan", "none") else value
        connection.execute("""
            INSERT INTO domain_expertise (workspace_id, knowledge_area, team_member,
                expertise_level, is_primary, backup_member, evidence_notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (workspace_id, area, clean(row.get("Team Member", "")),
              clean(row.get("Expertise Level", "Not assessed")),
              clean(row.get("Role", "Contributor")),
              clean(row.get("Backup Member", "")),
              clean(row.get("Evidence / Notes", "")), datetime.now().isoformat()))
    connection.commit()
    connection.close()


def get_handover_checkpoints(workspace_id):
    connection = get_connection()
    rows = connection.execute("""
        SELECT checkpoint, description, owner, due_date, status, evidence_notes
        FROM handover_checkpoints WHERE workspace_id = ? ORDER BY id
    """, (workspace_id,)).fetchall()
    connection.close()
    return pd.DataFrame(rows, columns=[
        "Checkpoint", "Description", "Owner", "Due Date", "Status", "Evidence / Notes"
    ])


def save_handover_checkpoints(workspace_id, dataframe):
    connection = get_connection()
    connection.execute("DELETE FROM handover_checkpoints WHERE workspace_id = ?", (workspace_id,))
    for _, row in dataframe.iterrows():
        checkpoint = str(row.get("Checkpoint", "")).strip()
        if not checkpoint or checkpoint.lower() == "nan":
            continue
        def clean_checkpoint(value):
            value = str(value).strip()
            return "" if value.lower() in ("nan", "none", "nat") else value
        connection.execute("""
            INSERT INTO handover_checkpoints
            (workspace_id, checkpoint, description, owner, due_date, status, evidence_notes, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            workspace_id, checkpoint,
            clean_checkpoint(row.get("Description", "")),
            clean_checkpoint(row.get("Owner", "")),
            clean_checkpoint(row.get("Due Date", "")),
            clean_checkpoint(row.get("Status", "Planned")) or "Planned",
            clean_checkpoint(row.get("Evidence / Notes", "")),
            datetime.now().isoformat()
        ))
    connection.commit()
    connection.close()


def save_workspace(project, outgoing, successor, deadline):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO workspaces (
            project_name,
            outgoing_employee,
            successor,
            deadline,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        project,
        outgoing,
        successor,
        str(deadline),
        datetime.now().isoformat()
    ))
    workspace_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return workspace_id
def get_workspace(workspace_id):
    connection = get_connection()
    result = connection.execute("""
        SELECT id, project_name, outgoing_employee,
               successor, deadline
        FROM workspaces
        WHERE id = ?
    """, (workspace_id,)).fetchone()
    connection.close()
    return result
def get_latest_workspace():
    connection = get_connection()
    result = connection.execute("""
        SELECT id, project_name, outgoing_employee,
               successor, deadline
        FROM workspaces
        ORDER BY id DESC
        LIMIT 1
    """).fetchone()
    connection.close()
    return result


def get_all_workspaces():
    """Return workspaces newest first for the workspace manager."""
    connection = get_connection()
    rows = connection.execute("""
        SELECT id, project_name, outgoing_employee, successor, deadline
        FROM workspaces
        ORDER BY id DESC
    """).fetchall()
    connection.close()
    return rows


def delete_workspace_and_related_data(workspace_id):
    """Delete one workspace and all records owned by it in one transaction."""
    connection = get_connection()
    try:
        cursor = connection.cursor()

        # interview_responses belongs to interviews, so remove it first.
        cursor.execute("""
            DELETE FROM interview_responses
            WHERE interview_id IN (
                SELECT id FROM knowledge_interviews WHERE workspace_id = ?
            )
        """, (workspace_id,))

        # Remove all workspace-scoped records from the current app schema.
        for table_name in (
            "documents",
            "semantic_chunks",
            "risk_assessments",
            "readiness_assessments",
            "successor_questions",
            "domain_expertise",
            "handover_checkpoints",
            "knowledge_interviews",
        ):
            cursor.execute(
                f"DELETE FROM {table_name} WHERE workspace_id = ?",
                (workspace_id,)
            )

        cursor.execute("DELETE FROM workspaces WHERE id = ?", (workspace_id,))
        deleted = cursor.rowcount

        # Reset the workspace ID sequence only when every workspace is gone.
        # This lets the next fresh workspace start at ID 1 without risking
        # collisions with workspaces that still exist.
        remaining_workspaces = cursor.execute(
            "SELECT COUNT(*) FROM workspaces"
        ).fetchone()[0]
        if remaining_workspaces == 0:
            cursor.execute(
                "DELETE FROM sqlite_sequence WHERE name = 'workspaces'"
            )

        connection.commit()
        return deleted > 0
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
def save_document(workspace_id, filename, document_hash,
                  extracted_text, pages):
    connection = get_connection()
    cursor = connection.execute("""
        INSERT OR IGNORE INTO documents (
            workspace_id,
            filename,
            document_hash,
            extracted_text,
            pages_json,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        workspace_id,
        filename,
        document_hash,
        extracted_text,
        json.dumps(pages),
        datetime.now().isoformat()
    ))
    inserted = cursor.rowcount == 1
    connection.commit()
    connection.close()
    return inserted
def get_latest_document(workspace_id):
    """Load all saved PDFs for a workspace while preserving each source name/page."""
    connection = get_connection()
    rows = connection.execute("""
        SELECT document_hash, filename, extracted_text, pages_json
        FROM documents
        WHERE workspace_id = ?
        ORDER BY id ASC
    """, (workspace_id,)).fetchall()
    connection.close()

    if not rows:
        return None

    all_pages = []
    all_text = []
    document_hashes = []
    for document_hash, filename, extracted_text, pages_json in rows:
        document_hashes.append(document_hash)
        if extracted_text:
            all_text.append(f"--- DOCUMENT: {filename or 'Uploaded PDF'} ---\n{extracted_text}")
        try:
            document_pages = json.loads(pages_json or "[]")
        except (TypeError, json.JSONDecodeError):
            document_pages = []
        for page_item in document_pages:
            page_with_source = dict(page_item)
            page_with_source.setdefault("document_name", filename or "Uploaded PDF")
            all_pages.append(page_with_source)

    return {
        "document_hash": document_hashes[-1],
        "document_hashes": document_hashes,
        "extracted_text": "\n\n".join(all_text),
        "pages": all_pages
    }


def activate_workspace_in_session(workspace_id):
    """Load a selected workspace and its saved document into the current session."""
    selected_workspace = get_workspace(workspace_id)
    if not selected_workspace:
        return False

    # Remove state belonging to the previously active workspace so that
    # assessments, interview answers, and generated outputs cannot leak across workspaces.
    workspace_state_keys = [
        "pages", "extracted_text", "document_hash", "document_hashes", "risk_results",
        "gemini_last_question", "gemini_last_answer", "gemini_last_sources",
        "readiness_score", "readiness_data", "readiness_assessment_id",
        "readiness_approved", "active_interview_id", "interview_pending_question",
        "interview_structured_notes", "last_interview_evaluation",
        "interview_topic_active", "handover_package_pdf",
        "successor_workspace_question", "project_pdf"
    ]
    for state_key in workspace_state_keys:
        st.session_state.pop(state_key, None)

    st.session_state["workspace_id"] = selected_workspace[0]
    st.session_state["workspace"] = {
        "project": selected_workspace[1],
        "outgoing": selected_workspace[2],
        "successor": selected_workspace[3],
        "deadline": selected_workspace[4]
    }

    saved_document = get_latest_document(selected_workspace[0])
    if saved_document:
        st.session_state["pages"] = saved_document["pages"]
        st.session_state["extracted_text"] = saved_document["extracted_text"]
        st.session_state["document_hash"] = saved_document["document_hash"]
        st.session_state["document_hashes"] = saved_document.get("document_hashes", [saved_document["document_hash"]])
    return True


def save_risk_assessment(workspace_id, risk_data):
    connection = get_connection()
    average_risk = float(
        risk_data["Risk Score"].mean()
    )
    connection.execute("""
        INSERT INTO risk_assessments (
            workspace_id,
            risk_data,
            average_risk,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """, (
        workspace_id,
        risk_data.to_json(orient="records"),
        average_risk,
        datetime.now().isoformat()
    ))
    connection.commit()
    connection.close()
def save_readiness_assessment(
    workspace_id,
    score,
    completed,
    technical_notes,
    pending_tasks
):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO readiness_assessments (
            workspace_id,
            readiness_score,
            completed_activities,
            technical_notes,
            pending_tasks,
            manager_name,
            approved,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        workspace_id,
        score,
        completed,
        technical_notes,
        pending_tasks,
        None,
        0,
        datetime.now().isoformat()
    ))
    assessment_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return assessment_id
def approve_readiness(assessment_id, manager_name):
    connection = get_connection()
    connection.execute("""
        UPDATE readiness_assessments
        SET manager_name = ?, approved = 1
        WHERE id = ?
    """, (
        manager_name,
        assessment_id
    ))
    connection.commit()
    connection.close()
def get_saved_history(workspace_id):
    connection = get_connection()
    risks = pd.read_sql_query("""
        SELECT id, average_risk, created_at
        FROM risk_assessments
        WHERE workspace_id = ?
        ORDER BY id DESC
    """, connection, params=(workspace_id,))
    readiness = pd.read_sql_query("""
        SELECT id, readiness_score, completed_activities,
               manager_name, approved, created_at
        FROM readiness_assessments
        WHERE workspace_id = ?
        ORDER BY id DESC
    """, connection, params=(workspace_id,))
    documents = pd.read_sql_query("""
        SELECT id, filename, created_at
        FROM documents
        WHERE workspace_id = ?
        ORDER BY id DESC
    """, connection, params=(workspace_id,))
    connection.close()
    return risks, readiness, documents
initialize_database()

# Run the 30-day backup check whenever the app starts. The archive is stored locally.
try:
    automatic_backup_created, automatic_backup_name = save_automatic_backup()
except Exception as backup_error:
    automatic_backup_created = False
    automatic_backup_name = None
    st.warning(f"Automatic backup could not be completed: {backup_error}")

# ==========================================================
# 2A. USER AUTHENTICATION GATE
# ==========================================================
if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None

if not st.session_state["authenticated_user"]:
    st.markdown("""
    <div class="dha-hero">
      <div class="dha-eyebrow">Secure project knowledge workspace</div>
      <div class="dha-title">Welcome to DevHandover AI</div>
      <div class="dha-subtitle">Sign in to manage project knowledge, handovers and continuity risks.</div>
    </div>
    """, unsafe_allow_html=True)
    login_tab, register_tab = st.tabs(["Sign in", "Create account"])
    with login_tab:
        with st.form("dha_login_form"):
            login_identity = st.text_input("Username or email")
            login_password = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Sign in", type="primary", use_container_width=True)
        if login_submit:
            user = authenticate_user(login_identity, login_password)
            if user:
                st.session_state["authenticated_user"] = user
                st.success("Signed in successfully.")
                st.rerun()
            else:
                st.error("Incorrect username/email or password.")
    with register_tab:
        if get_user_count() == 0:
            st.info("The first registered account becomes the Admin account.")
        else:
            st.caption("New accounts can register as Outgoing Staff or Successor. Admin access is reserved for the first account.")
        with st.form("dha_register_form"):
            new_username = st.text_input("Choose a username", key="dha_new_username")
            new_email = st.text_input("Email address", key="dha_new_email")
            new_password = st.text_input("Create password", type="password", key="dha_new_password")
            confirm_password = st.text_input("Confirm password", type="password")
            if get_user_count() == 0:
                new_role = "Admin"
                st.text_input("Account role", value="Admin", disabled=True)
            else:
                new_role = st.selectbox("Account role", ["Outgoing Staff", "Successor"])
            register_submit = st.form_submit_button("Create account", type="primary", use_container_width=True)
        if register_submit:
            if not new_username.strip() or not new_email.strip() or not new_password:
                st.error("Please complete all fields.")
            elif "@" not in new_email or "." not in new_email.split("@")[-1]:
                st.error("Enter a valid email address.")
            elif len(new_password) < 8:
                st.error("Use a password with at least 8 characters.")
            elif new_password != confirm_password:
                st.error("The passwords do not match.")
            else:
                ok, message = register_user(new_username, new_email, new_password, new_role)
                if ok:
                    st.success(message)
                else:
                    st.error(message)
    st.stop()

# Authenticated user controls
with st.sidebar:
    signed_in_user = st.session_state["authenticated_user"]
    st.markdown(f"**Signed in:** {signed_in_user['username']}")
    st.caption(f"Role: {signed_in_user['role']}")
    if st.button("Log out", use_container_width=True):
        st.session_state["authenticated_user"] = None
        st.rerun()

# ==========================================================
# 2C. BACKUP AND RESTORE CENTER
# ==========================================================
st.markdown("<div id='backup-center'></div>", unsafe_allow_html=True)
with st.expander("🛡️ Backup & Restore Center", expanded=False):
    st.subheader("Protect your DevHandover AI data")
    st.write(
        "Automatic backups are checked when the app starts. A new local backup "
        "is created if no backup exists or the latest one is at least 30 days old."
    )
    if automatic_backup_created:
        st.success(f"Automatic backup created: {automatic_backup_name}")
    elif automatic_backup_name:
        st.caption(f"Latest automatic backup: {automatic_backup_name}")
    else:
        st.caption("No automatic backup has been created yet.")

    backup_col, restore_col = st.columns(2)
    with backup_col:
        st.markdown("**Manual backup**")
        if st.button("Create backup now", key="create_manual_backup", type="primary"):
            try:
                manual_backup_name, manual_backup_bytes = build_backup_archive()
                st.session_state["manual_backup_name"] = manual_backup_name
                st.session_state["manual_backup_bytes"] = manual_backup_bytes
                st.success("Backup is ready to download.")
            except Exception as backup_error:
                st.error(f"Could not create backup: {backup_error}")
        if st.session_state.get("manual_backup_bytes"):
            st.download_button(
                "Download backup ZIP",
                data=st.session_state["manual_backup_bytes"],
                file_name=st.session_state["manual_backup_name"],
                mime="application/zip",
                key="download_manual_backup"
            )

    with restore_col:
        st.markdown("**Restore from backup**")
        restore_file = st.file_uploader(
            "Choose a DevHandover AI backup ZIP",
            type=["zip"],
            key="restore_backup_upload"
        )
        confirm_restore = st.checkbox(
            "I understand that restoring replaces the current database.",
            key="confirm_backup_restore"
        )
        if st.button(
            "Restore selected backup",
            key="restore_backup_button",
            disabled=(restore_file is None or not confirm_restore)
        ):
            try:
                safety_copy_name = restore_backup_archive(restore_file.getvalue())
                for state_key in (
                    "workspace_id", "workspace", "pages", "extracted_text",
                    "document_hash", "manual_backup_bytes", "manual_backup_name"
                ):
                    st.session_state.pop(state_key, None)
                st.success(
                    "Backup restored successfully. A safety copy of the previous "
                    f"database was saved as {safety_copy_name}."
                )
                st.rerun()
            except Exception as restore_error:
                st.error(f"Restore failed: {restore_error}")

    st.info(
        "The backup contains the SQLite database, including extracted PDF text "
        "and page records. The original uploaded PDF file itself is not currently "
        "stored by this app, so it cannot be included unless you upload it again. "
        "Keep downloaded backups in a secure location because they include account "
        "and project information."
    )

# ==========================================================
# 3. RESTORE LATEST WORKSPACE
# ==========================================================
if "workspace_id" not in st.session_state:
    latest = get_latest_workspace()
    if latest:
        st.session_state["workspace_id"] = latest[0]
        st.session_state["workspace"] = {
            "project": latest[1],
            "outgoing": latest[2],
            "successor": latest[3],
            "deadline": latest[4]
        }

        saved_document = get_latest_document(latest[0])
        if saved_document:
            st.session_state["pages"] = saved_document["pages"]
            st.session_state["extracted_text"] = saved_document["extracted_text"]
            st.session_state["document_hash"] = saved_document["document_hash"]
def current_workspace_id():
    return st.session_state.get("workspace_id")

# Compact dashboard header and live workspace indicators.
active_workspace_for_ui = st.session_state.get("workspace", {})
active_project_for_ui = active_workspace_for_ui.get("project", "No workspace selected")
active_status_for_ui = "WORKSPACE ACTIVE" if current_workspace_id() is not None else "SETUP REQUIRED"
st.markdown(f"""
<div class="dha-hero">
  <div class="dha-eyebrow">AI-powered knowledge continuity platform</div>
  <div class="dha-title">DevHandover AI</div>
  <div class="dha-subtitle">Protect critical project knowledge, uncover continuity risks, and guide a structured transfer from outgoing employees to successors.</div>
  <div class="dha-pill">● {active_status_for_ui} &nbsp; · &nbsp; {active_project_for_ui}</div>
</div>
""", unsafe_allow_html=True)

# Workspace summary metrics are read-only and do not alter stored records.
if current_workspace_id() is not None:
    dashboard_connection = get_connection()
    dashboard_counts = {}
    for table_name, label in [
        ("documents", "documents"),
        ("knowledge_interviews", "interviews"),
        ("handover_checkpoints", "checkpoints"),
        ("successor_questions", "successor questions")
    ]:
        try:
            dashboard_counts[label] = dashboard_connection.execute(
                f"SELECT COUNT(*) FROM {table_name} WHERE workspace_id = ?",
                (current_workspace_id(),)
            ).fetchone()[0]
        except sqlite3.OperationalError:
            dashboard_counts[label] = 0
    dashboard_connection.close()
    metric_columns = st.columns(4)
    metric_columns[0].metric("Documents", dashboard_counts["documents"])
    metric_columns[1].metric("Knowledge interviews", dashboard_counts["interviews"])
    metric_columns[2].metric("Handover checkpoints", dashboard_counts["checkpoints"])
    metric_columns[3].metric("Successor questions", dashboard_counts["successor questions"])
else:
    st.info("Create a handover workspace to activate your project dashboard and tools.")

st.divider()
# ==========================================================
# 4. HANDOVER WORKSPACE
# ==========================================================
st.markdown("<div id='workspace'></div>", unsafe_allow_html=True)
st.header("1. Handover Workspace")
with st.form("workspace_form"):
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input("Project Name")
        outgoing_employee = st.text_input("Outgoing Employee")
    with col2:
        successor = st.text_input("Successor / New Employee")
        handover_deadline = st.date_input("Handover Deadline")
    create_workspace = st.form_submit_button("Create Workspace")
if create_workspace:
    if (
        project_name.strip()
        and outgoing_employee.strip()
        and successor.strip()
    ):
        workspace_id = save_workspace(
            project_name,
            outgoing_employee,
            successor,
            handover_deadline
        )
        st.session_state["workspace_id"] = workspace_id
        st.session_state["workspace"] = {
            "project": project_name,
            "outgoing": outgoing_employee,
            "successor": successor,
            "deadline": str(handover_deadline)
        }
        # Clear old document and assessment state for the new workspace.
        for key in [
            "pages",
            "extracted_text",
            "document_hash",
            "risk_results",
            "gemini_last_question",
            "gemini_last_answer",
            "gemini_last_sources",
            "readiness_score",
            "readiness_data",
            "readiness_assessment_id",
            "readiness_approved",
            "active_interview_id",
            "interview_pending_question",
            "interview_structured_notes",
            "last_interview_evaluation",
            "interview_topic_active"
        ]:
            st.session_state.pop(key, None)
        st.success(
            f"Workspace created and saved in SQLite! ID: {workspace_id}"
        )
    else:
        st.warning("Please fill in all workspace fields.")
if "workspace" in st.session_state:
    workspace = st.session_state["workspace"]
    st.success(
        f"Active Workspace ID: {current_workspace_id()}"
    )
    st.info(
        f"**Project:** {workspace['project']}  \n"
        f"**Outgoing Employee:** {workspace['outgoing']}  \n"
        f"**Successor:** {workspace['successor']}  \n"
        f"**Deadline:** {workspace['deadline']}"
    )
else:
    st.info("Create a workspace to begin.")

# Workspace deletion is deliberately separated from workspace creation.
with st.expander("Manage existing workspaces", expanded=False):
    available_workspaces = get_all_workspaces()
    if not available_workspaces:
        st.caption("There are no saved workspaces to manage.")
    else:
        workspace_labels = {
            row[0]: f"{row[1]} · {row[2]} → {row[3]} (ID: {row[0]})"
            for row in available_workspaces
        }

        st.markdown("#### Switch Active Workspace")
        active_id = current_workspace_id()
        switch_options = list(workspace_labels.keys())
        default_switch_index = (
            switch_options.index(active_id) if active_id in switch_options else 0
        )
        selected_switch_id = st.selectbox(
            "Choose the workspace you want to open",
            options=switch_options,
            index=default_switch_index,
            format_func=lambda workspace_id: workspace_labels[workspace_id],
            key="workspace_switch_select"
        )
        if active_id in workspace_labels:
            st.caption(f"Currently active: {workspace_labels[active_id]}")
        if st.button(
            "Switch to selected workspace",
            type="primary",
            key="switch_workspace_button",
            disabled=(selected_switch_id == active_id)
        ):
            try:
                if activate_workspace_in_session(selected_switch_id):
                    st.success("Active workspace changed. Its saved document and project data are loaded.")
                    st.rerun()
                else:
                    st.error("The selected workspace could not be found. Refresh and try again.")
            except Exception as switch_error:
                st.error(f"Could not switch workspace: {switch_error}")

        st.divider()
        st.markdown("#### Delete a Workspace")
        selected_delete_id = st.selectbox(
            "Select a workspace",
            options=list(workspace_labels.keys()),
            format_func=lambda workspace_id: workspace_labels[workspace_id],
            key="workspace_delete_select"
        )
        st.warning(
            "Deleting a workspace permanently removes its uploaded-document "
            "records, interviews and answers, risk/readiness assessments, "
            "expertise records, checkpoints, and successor Q&A history. "
            "This action cannot be undone."
        )
        confirm_workspace_delete = st.checkbox(
            "I understand that this workspace and its related records will be permanently deleted.",
            key="confirm_workspace_delete"
        )
        if st.button(
            "Delete selected workspace",
            type="secondary",
            disabled=not confirm_workspace_delete,
            key="delete_workspace_button"
        ):
            try:
                deleted = delete_workspace_and_related_data(selected_delete_id)
                if deleted:
                    # Clear all state that may contain data from the deleted workspace.
                    workspace_state_keys = [
                        "workspace_id", "workspace", "pages", "extracted_text",
                        "document_hash", "risk_results", "gemini_last_question",
                        "gemini_last_answer", "gemini_last_sources",
                        "readiness_score", "readiness_data",
                        "readiness_assessment_id", "readiness_approved",
                        "active_interview_id", "interview_pending_question",
                        "interview_structured_notes", "last_interview_evaluation",
                        "interview_topic_active", "handover_package_pdf",
                        "successor_workspace_question"
                    ]
                    for state_key in workspace_state_keys:
                        st.session_state.pop(state_key, None)

                    # Restore the newest remaining workspace, if one exists.
                    remaining_workspace = get_latest_workspace()
                    if remaining_workspace:
                        st.session_state["workspace_id"] = remaining_workspace[0]
                        st.session_state["workspace"] = {
                            "project": remaining_workspace[1],
                            "outgoing": remaining_workspace[2],
                            "successor": remaining_workspace[3],
                            "deadline": remaining_workspace[4]
                        }
                        saved_document = get_latest_document(remaining_workspace[0])
                        if saved_document:
                            st.session_state["pages"] = saved_document["pages"]
                            st.session_state["extracted_text"] = saved_document["extracted_text"]
                            st.session_state["document_hash"] = saved_document["document_hash"]

                    st.success("Workspace and its related records were deleted.")
                    st.rerun()
                else:
                    st.error("The selected workspace could not be found.")
            except Exception as error:
                st.error("Workspace deletion failed. No partial deletion was saved.")
                st.caption(f"Technical details: {error}")

st.divider()
# ==========================================================
# 5. PDF UPLOAD AND EXTRACTION
# ==========================================================
st.markdown("<div id='documentation'></div>", unsafe_allow_html=True)
st.header("2. Project Documentation Upload")
uploaded_files = st.file_uploader(
    "Upload Project Documentation (PDFs)",
    type=["pdf"],
    accept_multiple_files=True,
    key="project_pdf",
    disabled=current_workspace_id() is None,
    help="Upload one or more project PDFs. Create or restore a workspace first."
)
if uploaded_files:
    # Always read saved hashes for the active workspace from SQLite.
    # Session state can contain hashes from a previously selected workspace.
    document_connection = get_connection()
    saved_hash_rows = document_connection.execute(
        "SELECT document_hash FROM documents WHERE workspace_id = ?",
        (current_workspace_id(),)
    ).fetchall()
    document_connection.close()
    processed_hashes = {row[0] for row in saved_hash_rows if row[0]}
    newly_processed = 0
    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.getvalue()
        document_hash = hashlib.sha256(file_bytes).hexdigest()
        if document_hash in processed_hashes:
            continue
        try:
            pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
            document_pages = []
            for page_number, page in enumerate(pdf_document, start=1):
                document_pages.append({
                    "page": page_number,
                    "document_name": uploaded_file.name,
                    "text": page.get_text()
                })
            pdf_document.close()
            document_text = "\n\n".join(
                f"--- Page {page['page']} ---\n{page['text']}"
                for page in document_pages
            )
            if document_text.strip():
                was_saved = save_document(
                    current_workspace_id(), uploaded_file.name,
                    document_hash, document_text, document_pages
                )
                if was_saved:
                    processed_hashes.add(document_hash)
                    newly_processed += 1
            else:
                st.warning(f"No selectable text found in {uploaded_file.name}. OCR is not included.")
        except Exception as error:
            st.error(f"PDF processing error for {uploaded_file.name}: {error}")

    saved_documents = get_latest_document(current_workspace_id())
    if saved_documents:
        st.session_state["pages"] = saved_documents["pages"]
        st.session_state["extracted_text"] = saved_documents["extracted_text"]
        st.session_state["document_hash"] = saved_documents["document_hash"]
        st.session_state["document_hashes"] = saved_documents["document_hashes"]
    if newly_processed:
        st.success(f"Successfully processed {newly_processed} new PDF(s).")
    elif saved_documents:
        st.info("These PDFs are already saved in this workspace.")

pages = st.session_state.get("pages", [])
extracted_text = st.session_state.get("extracted_text", "")
if extracted_text.strip():
    col1, col2, col3 = st.columns(3)
    col1.metric("Documents", len(st.session_state.get("document_hashes", [])))
    col2.metric("Total Pages", len(pages))
    col3.metric("Extracted Characters", len(extracted_text))
    with st.expander("View Extracted Text"):
        st.text(extracted_text[:20000])
    st.download_button(
        "Download Extracted Text", extracted_text,
        file_name="project_documentation.txt", mime="text/plain"
    )
else:
    st.info("Upload one or more text-based PDFs to begin. Scanned PDFs require OCR, which is not included yet.")
pages = st.session_state.get("pages", [])
extracted_text = st.session_state.get("extracted_text", "")

st.divider()
# ==========================================================
# 6. GEMINI-POWERED PROJECT KNOWLEDGE ASSISTANT
# ==========================================================
st.markdown("<div id='knowledge-assistant'></div>", unsafe_allow_html=True)
st.header("3. Gemini Project Knowledge Assistant")
st.write(
    "Ask questions in natural language. Semantic search retrieves relevant "
    "passages across all uploaded project PDFs and Gemini cites the source document and page."
)

st.caption("The app uses Gemini embeddings for semantic retrieval, with the existing keyword search as a fallback. Scanned PDFs need OCR.")
def get_gemini_client():
    """Create a Gemini client using the API key stored in .env."""
    from dotenv import load_dotenv
    from google import genai
    from google.genai import types
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None, None
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(timeout=120000)
    )
    return client, types
def normalize_words(text):
    """
    Convert text into searchable words.
    Important: use a real word-boundary regex (\\b).
    """
    text = (text or "").lower()
    words = re.findall(r"\b[a-z0-9]+\b", text)
    stop_words = {
        "what", "where", "when", "which", "who", "why", "how",
        "the", "is", "are", "was", "were", "in", "on", "at",
        "to", "of", "for", "and", "a", "an", "does", "do",
        "can", "could", "this", "that", "about", "with", "from",
        "it", "our", "their", "please", "tell", "me", "explain",
        "describe", "give", "show", "project"
    }
    return [word for word in words if word not in stop_words]


def expand_query_terms(question):
    """
    Add common alternatives so natural-language questions can match
    headings and terminology used in project documentation.
    """
    aliases = {
        "architecture": {
            "architecture", "architectural", "system design", "design",
            "components", "modules", "workflow", "data flow",
            "system flow", "structure", "high level design"
        },
        "technology": {
            "technology", "technologies", "tech stack", "technology stack",
            "framework", "language", "tools", "platform", "libraries"
        },
        "setup": {
            "setup", "installation", "install", "configure", "configuration",
            "getting started", "run", "running", "environment", "requirements"
        },
        "database": {
            "database", "storage", "sqlite", "postgres", "postgresql",
            "data storage", "tables", "schema"
        },
        "troubleshooting": {
            "troubleshooting", "debugging", "errors", "issues", "problems",
            "fix", "failure", "exception"
        },
        "roles": {
            "roles", "responsibilities", "team", "owner", "ownership",
            "primary owner", "backup owner", "team members"
        },
        "risk": {
            "risk", "risks", "limitations", "known issues", "dependencies",
            "single point of failure", "knowledge loss"
        },
        "decision": {
            "decision", "decisions", "technical decisions", "tradeoffs",
            "design choices", "rationale"
        },
    }

    question_lower = (question or "").lower()
    query_terms = set(normalize_words(question))

    for concept, terms in aliases.items():
        if concept in query_terms or any(term in question_lower for term in terms):
            for term in terms:
                query_terms.update(normalize_words(term))

    return query_terms


def retrieve_relevant_pages(question, document_pages, max_pages=8):
    """
    Retrieve likely source pages using normalized word matching,
    phrase matching, and a safe fallback.

    A fallback is intentional: a zero keyword score should not prevent
    Gemini from checking the document. Gemini is instructed to say when
    the supplied excerpts do not contain the answer.
    """
    if not question or not document_pages:
        return []

    query_terms = expand_query_terms(question)
    question_lower = question.lower()
    scored_pages = []

    for item in document_pages:
        page_text = item.get("text", "") or ""
        page_lower = page_text.lower()
        page_words = set(normalize_words(page_text))

        overlap = query_terms.intersection(page_words)
        score = len(overlap)

        # Give extra weight to exact question phrases and useful headings.
        for phrase in [
            "project architecture", "system architecture", "system design",
            "architecture", "data flow", "technology stack",
            "installation", "troubleshooting", "team responsibilities",
            "technical decisions", "risks and limitations"
        ]:
            if phrase in question_lower and phrase in page_lower:
                score += 5
            elif phrase in question_lower and any(
                word in page_lower for word in phrase.split()
            ):
                score += 1

        # Slightly prefer pages with a meaningful amount of extracted text.
        if page_text.strip():
            scored_pages.append({
                "page": item.get("page"),
                "document_name": item.get("document_name", "Uploaded PDF"),
                "score": score,
                "text": page_text
            })

    scored_pages.sort(
        key=lambda item: (item["score"], len(item["text"])),
        reverse=True
    )

    matched_pages = [item for item in scored_pages if item["score"] > 0]

    # If no terms matched, still let Gemini inspect a few non-empty pages.
    # This avoids the misleading "no relevant passages" warning caused
    # by keyword retrieval alone.
    if not matched_pages:
        matched_pages = sorted(
            scored_pages,
            key=lambda item: len(item["text"]),
            reverse=True
        )

    return matched_pages[:max_pages]


# ==========================================================
# 6A. SEMANTIC DOCUMENT INDEX AND RETRIEVAL
# ==========================================================
EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSIONS = 768


def split_page_into_chunks(page_text, chunk_size=1200, overlap=180):
    """Split a PDF page into overlapping text chunks for semantic indexing."""
    text_value = (page_text or "").strip()
    if not text_value:
        return []
    chunks = []
    start = 0
    while start < len(text_value):
        end = min(start + chunk_size, len(text_value))
        if end < len(text_value):
            # Prefer ending at a word boundary without creating tiny chunks.
            boundary = text_value.rfind(" ", start + int(chunk_size * 0.7), end)
            if boundary > start:
                end = boundary
        chunk = text_value[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text_value):
            break
        start = max(end - overlap, start + 1)
    return chunks


def get_workspace_document_hashes(workspace_id):
    connection = get_connection()
    rows = connection.execute(
        "SELECT filename, document_hash FROM documents WHERE workspace_id = ?",
        (workspace_id,)
    ).fetchall()
    connection.close()
    return {filename: document_hash for filename, document_hash in rows}


def ensure_semantic_index(workspace_id, document_pages, client, types):
    """Create and persist embeddings only for chunks not already indexed."""
    if not workspace_id or not document_pages:
        return 0

    document_hashes = get_workspace_document_hashes(workspace_id)
    pending = []
    for page_item in document_pages:
        document_name = page_item.get("document_name", "Uploaded PDF")
        document_hash = document_hashes.get(document_name)
        if not document_hash:
            fallback_source = f"{document_name}|{page_item.get('text', '')}"
            document_hash = hashlib.sha256(fallback_source.encode("utf-8")).hexdigest()

        page_number = int(page_item.get("page", 0) or 0)
        page_chunks = split_page_into_chunks(page_item.get("text", ""))
        for chunk_index, chunk_text in enumerate(page_chunks):
            pending.append({
                "document_hash": document_hash,
                "document_name": document_name,
                "page_number": page_number,
                "chunk_index": chunk_index,
                "chunk_text": chunk_text
            })

    connection = get_connection()
    existing_rows = connection.execute("""
        SELECT document_hash, page_number, chunk_index
        FROM semantic_chunks
        WHERE workspace_id = ? AND embedding_model = ?
    """, (workspace_id, EMBEDDING_MODEL)).fetchall()
    existing_keys = {(row[0], row[1], row[2]) for row in existing_rows}
    pending = [
        item for item in pending
        if (item["document_hash"], item["page_number"], item["chunk_index"]) not in existing_keys
    ]

    created_count = 0
    try:
        # Keep batches modest to avoid oversized embedding requests.
        for batch_start in range(0, len(pending), 32):
            batch = pending[batch_start:batch_start + 32]
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                # Gemini Embedding 2 treats a plain list of strings as parts
                # of one combined input. Wrap each chunk as its own Content so
                # the API returns one embedding per submitted chunk.
                contents=[
                    types.Content(parts=[types.Part.from_text(text=item["chunk_text"])])
                    for item in batch
                ],
                config=types.EmbedContentConfig(
                    output_dimensionality=EMBEDDING_DIMENSIONS
                )
            )
            embeddings = getattr(response, "embeddings", None) or []
            if len(embeddings) != len(batch):
                raise ValueError("Embedding response count did not match the submitted chunks.")

            for item, embedding in zip(batch, embeddings):
                values = getattr(embedding, "values", None)
                if not values:
                    raise ValueError("Gemini returned an empty document embedding.")
                connection.execute("""
                    INSERT OR IGNORE INTO semantic_chunks (
                        workspace_id, document_hash, document_name, page_number,
                        chunk_index, chunk_text, embedding_json, embedding_model, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    workspace_id, item["document_hash"], item["document_name"],
                    item["page_number"], item["chunk_index"], item["chunk_text"],
                    json.dumps(list(values)), EMBEDDING_MODEL, datetime.now().isoformat()
                ))
                created_count += 1
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return created_count


def cosine_similarity(vector_a, vector_b):
    """Return cosine similarity without requiring an extra vector database package."""
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    magnitude_a = sum(value * value for value in vector_a) ** 0.5
    magnitude_b = sum(value * value for value in vector_b) ** 0.5
    if not magnitude_a or not magnitude_b:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def retrieve_semantic_chunks(question, workspace_id, document_pages, client, types, max_chunks=8):
    """Retrieve document chunks by embedding similarity, retaining source/page metadata."""
    ensure_semantic_index(workspace_id, document_pages, client, types)
    query_response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSIONS
        )
    )
    query_embeddings = getattr(query_response, "embeddings", None) or []
    if not query_embeddings or not getattr(query_embeddings[0], "values", None):
        raise ValueError("Gemini did not return a query embedding.")
    query_vector = list(query_embeddings[0].values)

    connection = get_connection()
    rows = connection.execute("""
        SELECT document_name, page_number, chunk_text, embedding_json
        FROM semantic_chunks
        WHERE workspace_id = ? AND embedding_model = ?
    """, (workspace_id, EMBEDDING_MODEL)).fetchall()
    connection.close()

    scored_chunks = []
    for document_name, page_number, chunk_text, embedding_json in rows:
        try:
            stored_vector = json.loads(embedding_json)
            score = cosine_similarity(query_vector, stored_vector)
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
        scored_chunks.append({
            "document_name": document_name,
            "page": page_number,
            "text": chunk_text,
            "similarity": score
        })

    scored_chunks.sort(key=lambda item: item["similarity"], reverse=True)
    return scored_chunks[:max_chunks]


if pages:
    question = st.text_input(
        "Ask a project-related question",
        placeholder="Example: What technologies are used and how do I run the project?",
        key="gemini_project_question"
    )
    if st.button("Ask Gemini", type="primary", key="ask_gemini_button"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            if not pages:
                st.warning(
                    "No readable text was extracted from the uploaded PDFs. "
                    "If these are scanned PDFs, OCR is required before Gemini can search them."
                )
            else:
                try:
                    with st.spinner("Gemini is searching your project documents..."):
                        client, types = get_gemini_client()
                        if client is None:
                            st.error(
                                "Gemini API key not found. Check that your .env "
                                "file contains GEMINI_API_KEY=your_key and restart the app."
                            )
                        else:
                            try:
                                relevant_pages = retrieve_semantic_chunks(
                                    question, current_workspace_id(), pages, client, types
                                )
                                retrieval_method = "Semantic search"
                            except Exception as semantic_error:
                                # Keep the existing keyword retrieval as a resilient fallback.
                                relevant_pages = retrieve_relevant_pages(question, pages)
                                retrieval_method = "Keyword fallback"
                                st.warning(
                                    "Semantic search was temporarily unavailable. "
                                    "The existing keyword search is being used for this question."
                                )
                                st.caption(f"Semantic search detail: {semantic_error}")

                            if not relevant_pages:
                                st.warning("No relevant readable passages were found in the uploaded PDFs.")
                            else:
                                st.caption(f"Retrieval method: {retrieval_method}")
                                context_parts = []
                                for item in relevant_pages:
                                    page_text = item["text"][:7000]
                                    context_parts.append(
                                        f"--- SOURCE DOCUMENT: {item.get('document_name', 'Uploaded PDF')} | PAGE {item['page']} ---\n{page_text}"
                                    )
                                document_context = "\n\n".join(context_parts)
                                prompt = f"""
    You are DevHandover AI, a project documentation assistant.
    Answer the user's question using ONLY the source excerpts provided below.
    Do not use outside knowledge and do not invent missing details.
    If the excerpts do not contain enough information, clearly say:
    "The uploaded document does not provide enough information to answer this."
    You may explain what information is missing.
    Cite every factual claim with source document and page in this format: [Source: filename.pdf, Page 2].
    Only cite source names and page numbers that appear in the supplied excerpts.
    Keep the answer clear, practical, and easy to understand.
    Do not claim that an action, test, deployment, or configuration happened
    unless the source explicitly says so.
    USER QUESTION:
    {question}
    SOURCE EXCERPTS:
    {document_context}
    """
                                response = client.models.generate_content(
                                    model="gemini-3.5-flash-lite",
                                    contents=prompt,
                                    config=types.GenerateContentConfig(
                                        temperature=0.2,
                                        max_output_tokens=700
                                    )
                                )
                                answer = (response.text or "").strip()
                                if answer:
                                    st.session_state["gemini_last_question"] = question
                                    st.session_state["gemini_last_answer"] = answer
                                    st.session_state["gemini_last_sources"] = [
                                        {"document_name": item.get("document_name", "Uploaded PDF"), "page": item["page"]}
                                        for item in relevant_pages
                                    ]
                                else:
                                    st.warning(
                                        "Gemini returned an empty response. Please try again."
                                    )
                except Exception as error:
                    st.error(
                        "Gemini could not answer this question. "
                        "Check your internet connection, API quota, and model availability."
                    )
                    st.caption(f"Technical details: {error}")
    if st.session_state.get("gemini_last_answer"):
        st.subheader("Gemini's Answer")
        st.markdown(st.session_state["gemini_last_answer"])
        source_pages = st.session_state.get("gemini_last_sources", [])
        if source_pages:
            source_labels = [
                f"{item.get('document_name', 'Uploaded PDF')} · Page {item.get('page')}"
                if isinstance(item, dict) else f"Page {item}"
                for item in source_pages
            ]
            st.caption("Sources supplied to Gemini: " + "; ".join(source_labels))
        st.caption(
            "Answers are generated from retrieved PDF passages. Always verify "
            "important handover decisions against the original document."
        )
else:
    st.info("Upload a PDF to use the Gemini Knowledge Assistant.")
st.divider()
# ==========================================================
# 7. KNOWLEDGE GAP DETECTOR
# ==========================================================
st.markdown("<div id='knowledge-gaps'></div>", unsafe_allow_html=True)
st.header("4. Knowledge Gap Detector")
required_topics = {
    "Project Architecture": [
        "architecture",
        "system design",
        "workflow"
    ],
    "Technology Stack": [
        "technology stack",
        "tech stack",
        "technologies"
    ],
    "Installation & Setup": [
        "installation",
        "setup instructions",
        "getting started"
    ],
    "Database & Dependencies": [
        "database",
        "dependencies",
        "storage"
    ],
    "Troubleshooting": [
        "troubleshooting",
        "debugging",
        "common errors"
    ],
    "Team Responsibilities": [
        "team responsibilities",
        "team members",
        "roles",
        "primary owner",
        "backup owner",
        "ownership map",
        "domain owner"
    ],
    "Technical Decisions": [
        "technical decisions",
        "design decisions",
        "decision"
    ],
    "Risks & Limitations": [
        "risks",
        "limitations",
        "known issues"
    ]
}
if pages:
    if st.button("Analyze Knowledge Gaps"):
        document_text = extracted_text.lower()
        covered_topics = []
        missing_topics = []
        for topic, keywords in required_topics.items():
            if any(
                keyword in document_text
                for keyword in keywords
            ):
                covered_topics.append(topic)
            else:
                missing_topics.append(topic)
        col1, col2 = st.columns(2)
        col1.metric("Topics Found", len(covered_topics))
        col2.metric("Potential Knowledge Gaps", len(missing_topics))
        st.subheader("Covered Topics")
        for topic in covered_topics:
            st.write(f"✅ {topic}")
        st.subheader("Potential Knowledge Gaps")
        for topic in missing_topics:
            st.write(f"⚠️ {topic}")
        st.caption(
            "This is a preliminary keyword-based check. "
            "Missing keywords do not prove information is absent."
        )
else:
    st.info("Upload a PDF to analyze knowledge gaps.")

# Additional AI interview-driven gap dashboard (the original detector remains above).
if current_workspace_id() is not None:
    st.subheader("AI-Detected Knowledge Gaps")
    st.caption(
        "Gaps are recorded from Gemini's evaluation of interview answers. "
        "Severity is an AI-assisted prioritization and should be reviewed by a manager."
    )
    saved_gaps = get_knowledge_gaps(current_workspace_id())
    if saved_gaps:
        gap_df = pd.DataFrame(
            saved_gaps,
            columns=[
                "Gap ID", "Knowledge Area", "Missing / Incomplete Knowledge",
                "Severity", "Status", "Targeted Follow-up",
                "Interview Question", "Detected At"
            ]
        )
        st.dataframe(gap_df, use_container_width=True, hide_index=True)

        open_count = sum(1 for row in saved_gaps if row[4] == "Open")
        critical_count = sum(
            1 for row in saved_gaps
            if row[3] in {"Critical", "High"} and row[4] == "Open"
        )
        gap_metric_cols = st.columns(2)
        gap_metric_cols[0].metric("Open Knowledge Gaps", open_count)
        gap_metric_cols[1].metric("Critical / High Open Gaps", critical_count)

        with st.expander("Update a knowledge-gap status"):
            gap_options = {
                f"#{row[0]} · {row[1]} · {row[3]} · {row[2][:65]}": row[0]
                for row in saved_gaps
            }
            selected_gap_label = st.selectbox(
                "Select a gap", list(gap_options.keys()),
                key="selected_ai_gap_to_update"
            )
            selected_gap_status = st.selectbox(
                "New status", ["Open", "In Progress", "Resolved"],
                key="selected_ai_gap_status"
            )
            if st.button("Save gap status", key="save_ai_gap_status"):
                update_knowledge_gap_status(
                    gap_options[selected_gap_label],
                    current_workspace_id(),
                    selected_gap_status
                )
                st.success("Knowledge-gap status updated.")
                st.rerun()
    else:
        st.info(
            "No AI interview gaps have been recorded yet. Start an AI Knowledge "
            "Interview and submit an answer to begin detecting and tracking gaps."
        )
else:
    st.info("Create a workspace to view AI-detected knowledge gaps.")
st.divider()
# ==========================================================
# 8. PROJECT CONTINUITY RISK ENGINE
# ==========================================================

st.divider()
# ==========================================================
# 8. AI-GUIDED KNOWLEDGE INTERVIEW
# ==========================================================
st.markdown("<div id='knowledge-interview'></div>", unsafe_allow_html=True)
st.header("5. AI-Guided Knowledge Interview")
st.write(
    "Interview the outgoing knowledge holder. Gemini creates focused questions, "
    "checks whether each answer is sufficiently detailed, and asks follow-up questions."
)

if current_workspace_id() is None:
    st.info("Create a workspace before starting a knowledge interview.")
elif not pages:
    st.info("Upload project documentation before starting the interview.")
else:
    interview_topic_options = [
        "Project Architecture",
        "Technology Stack",
        "Installation & Setup",
        "Database & Dependencies",
        "Troubleshooting",
        "Team Responsibilities",
        "Technical Decisions",
        "Risks & Limitations",
        "Deployment & Operations",
        "Critical Undocumented Knowledge"
    ]

    interview_col1, interview_col2 = st.columns(2)
    with interview_col1:
        interview_topic = st.selectbox(
            "Knowledge area to interview",
            interview_topic_options,
            key="interview_topic"
        )
    with interview_col2:
        default_interviewee = (
            st.session_state.get("workspace", {}).get("outgoing", "")
        )
        interviewee = st.text_input(
            "Knowledge holder / interviewee",
            value=default_interviewee,
            key="interviewee_name"
        )

    if "active_interview_id" not in st.session_state:
        st.session_state["active_interview_id"] = None
    if "interview_pending_question" not in st.session_state:
        st.session_state["interview_pending_question"] = ""
    if "interview_structured_notes" not in st.session_state:
        st.session_state["interview_structured_notes"] = []

    if st.button(
        "Start New Interview",
        type="primary",
        disabled=not interviewee.strip(),
        key="start_knowledge_interview"
    ):
        new_id = create_knowledge_interview(
            current_workspace_id(), interview_topic, interviewee.strip()
        )
        st.session_state["active_interview_id"] = new_id
        st.session_state["interview_topic_active"] = interview_topic
        st.session_state["interview_pending_question"] = ""
        st.session_state["interview_structured_notes"] = []
        display_interview_number = get_interview_display_number(
            current_workspace_id(), new_id
        )
        st.success(
            f"Interview started. Interview ID: {display_interview_number}"
        )

    active_interview_id = st.session_state.get("active_interview_id")

    if active_interview_id:
        display_interview_number = get_interview_display_number(
            current_workspace_id(), active_interview_id
        )
        st.caption(
            f"Active interview #{display_interview_number} — "
            f"{st.session_state.get('interview_topic_active', interview_topic)}"
        )

        pending_question = st.session_state.get("interview_pending_question", "")

        # A new main question can only be generated when no follow-up is waiting.
        if st.button(
            "Generate Interview Question",
            key="generate_interview_question",
            disabled=bool(pending_question)
        ):
            try:
                client, types = get_gemini_client()
                if client is None:
                    st.error("Gemini API key not found. Check your .env file.")
                else:
                    with st.spinner("Preparing a focused interview question..."):
                        topic_pages = retrieve_relevant_pages(
                            st.session_state.get("interview_topic_active", interview_topic),
                            pages,
                            max_pages=5
                        )
                        source_context = "\n\n".join(
                            f"[Page {p['page']}]\n{p['text'][:3500]}"
                            for p in topic_pages
                        )
                        previous_notes = "\n".join(
                            st.session_state.get("interview_structured_notes", [])
                        )
                        prompt = f"""
You are the AI-guided knowledge interview agent in DevHandover AI.
Create ONE clear, practical interview question for the outgoing knowledge holder.
Interview topic: {st.session_state.get('interview_topic_active', interview_topic)}
Project: {st.session_state.get('workspace', {}).get('project', 'Unknown')}
Successor: {st.session_state.get('workspace', {}).get('successor', 'Unknown')}

Use the document excerpts to understand the project, but ask for practical
knowledge that a successor needs and that may be missing from documentation.
Focus on implementation details, decisions and rationale, dependencies,
failure recovery, operational steps, edge cases, or undocumented tips.
Do not repeat a question already covered in these notes:
{previous_notes}

IMPORTANT LANGUAGE AND SOURCE-QUALITY RULES:
- Write clear, grammatical English using complete technical terms.
- Do not copy OCR errors, corrupted fragments, random character strings,
  misspellings, or unexplained tokens from the excerpts.
- Use an acronym only when it is clearly defined or repeatedly used in the
  source. Otherwise write the full descriptive phrase.
- Never invent a tool, component, command, acronym, or project name.
- If an excerpt contains unclear wording, ask about the underlying concept
  using neutral language rather than repeating the unclear wording.
- Before returning, check that every technical term in the question is
  understandable and relevant to the selected interview topic.

Document excerpts:
{source_context}

Return only ONE polished interview question. Do not answer it.
"""
                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                temperature=0.4,
                                max_output_tokens=250
                            )
                        )
                        generated_question = (response.text or "").strip()
                        if generated_question:
                            st.session_state["interview_pending_question"] = generated_question
                            st.rerun()
                        else:
                            st.warning("Gemini did not generate a question. Try again.")
            except Exception as error:
                st.error("Could not generate the interview question.")
                st.caption(f"Technical details: {error}")

        pending_question = st.session_state.get("interview_pending_question", "")
        if pending_question:
            st.markdown("**Interview question**")
            st.info(pending_question)

            # A question-specific key prevents old form state from leaking into
            # the next follow-up question.
            question_form_key = "knowledge_interview_answer_" + hashlib.sha256(
                pending_question.encode("utf-8")
            ).hexdigest()[:12]
            with st.form(question_form_key):
                interview_answer = st.text_area(
                    "Outgoing employee's answer",
                    height=160,
                    placeholder="Enter the knowledge holder's answer here...",
                    key=question_form_key + "_text"
                )
                submit_interview_answer = st.form_submit_button(
                    "Evaluate Answer & Generate Follow-up"
                )

            if submit_interview_answer:
                if not interview_answer.strip():
                    st.warning("Enter an answer before submitting.")
                else:
                    try:
                        client, types = get_gemini_client()
                        if client is None:
                            st.error("Gemini API key not found. Check your .env file.")
                        else:
                            with st.spinner("Evaluating the answer and preparing a follow-up..."):
                                prompt = f"""
You are DevHandover AI's knowledge interview evaluator.
Assess the answer to the interview question below.
Return ONLY valid JSON with exactly these keys:
{{
  "completeness": "Complete, Partial, or Insufficient",
  "reason": "Brief explanation of what is covered or missing",
  "follow_up_question": "One focused follow-up question if more detail is needed, otherwise an empty string",
  "structured_note": "A concise factual handover note based only on the answer",
  "knowledge_area": "A concise knowledge-area label matching the interview topic",
  "gap_detected": true,
  "gap_description": "Specific missing, unclear, or undocumented knowledge; empty when no gap is found",
  "severity": "Critical, High, Medium, or Low"
}}

Rules:
- Mark Complete only if the answer is actionable and sufficiently specific.
- If Partial or Insufficient, ask a targeted follow-up about the missing detail.
- Set gap_detected to true when an important detail is missing, incomplete,
  unclear, or not actionable; otherwise false.
- Describe the exact missing knowledge in gap_description. Do not merely repeat
  the completeness label.
- Classify severity based on likely handover impact: Critical = blocks safe operation
  or essential transfer; High = major implementation/operation knowledge missing;
  Medium = useful detail incomplete; Low = minor clarification.
- If Partial or Insufficient, severity must not be lower than Medium.
- If Complete and no material gap remains, use gap_detected=false and severity=Low.
- Do not invent facts or fill gaps from general knowledge.
- Do not repeat malformed words, OCR artifacts, random fragments, or
  unexplained tokens from the question. Refer to the missing concept in clear,
  neutral language instead.
- Use only technical names and acronyms that are clearly supported by the
  question, answer, or supplied project context.
- If the answer is vague, ask for concrete steps, names of components,
  dependencies, commands, decision rationale, or recovery actions as appropriate.

Interview topic: {st.session_state.get('interview_topic_active', interview_topic)}
Question: {pending_question}
Answer: {interview_answer}
"""
                                evaluation = client.models.generate_content(
                                    model="gemini-3.5-flash-lite",
                                    contents=prompt,
                                    config=types.GenerateContentConfig(
                                        temperature=0.2,
                                        max_output_tokens=500,
                                        response_mime_type="application/json"
                                    )
                                )
                                raw_result = (evaluation.text or "").strip()
                                result = json.loads(raw_result)
                                completeness = str(
                                    result.get("completeness", "Partial")
                                ).strip().title()
                                if completeness not in {"Complete", "Partial", "Insufficient"}:
                                    completeness = "Partial"
                                reason = str(result.get("reason", "")).strip()
                                follow_up = str(
                                    result.get("follow_up_question", "") or ""
                                ).strip()
                                structured_note = str(
                                    result.get("structured_note", "") or ""
                                ).strip()
                                knowledge_area = str(
                                    result.get("knowledge_area", "")
                                    or st.session_state.get("interview_topic_active", interview_topic)
                                ).strip()
                                raw_gap_detected = result.get(
                                    "gap_detected", completeness != "Complete"
                                )
                                if isinstance(raw_gap_detected, str):
                                    gap_detected = raw_gap_detected.strip().lower() in {
                                        "true", "yes", "1"
                                    }
                                else:
                                    gap_detected = bool(raw_gap_detected)
                                gap_description = str(
                                    result.get("gap_description", "") or reason
                                ).strip()
                                severity = str(
                                    result.get("severity", "Medium")
                                ).strip().title()
                                if severity not in {"Critical", "High", "Medium", "Low"}:
                                    severity = "Medium"
                                if completeness in {"Partial", "Insufficient"} and severity == "Low":
                                    severity = "Medium"
                                if completeness == "Complete":
                                    gap_detected = bool(gap_detected and gap_description)

                                # If Gemini marks the answer incomplete but omits
                                # its follow-up, ask it once more for a targeted question.
                                if completeness in {"Partial", "Insufficient"} and not follow_up:
                                    try:
                                        followup_prompt = f"""
Write exactly ONE concise follow-up interview question. Do not answer it.
The answer was marked {completeness} because: {reason}
Topic: {st.session_state.get('interview_topic_active', interview_topic)}
Original question: {pending_question}
Interviewee answer: {interview_answer.strip()}
Ask only about the most important missing practical detail. Avoid asking
for information already supplied in the answer.
Use clear, grammatical English. Do not repeat OCR errors, malformed words,
random fragments, or unexplained acronyms from the original question/reason.
Never invent tool or component names; describe the missing concept neutrally.
"""
                                        followup_response = client.models.generate_content(
                                            model="gemini-3.5-flash-lite",
                                            contents=followup_prompt,
                                            config=types.GenerateContentConfig(
                                                temperature=0.2,
                                                max_output_tokens=150
                                            )
                                        )
                                        follow_up = (
                                            followup_response.text or ""
                                        ).strip().strip('"')
                                    except Exception:
                                        follow_up = ""

                                    # Deterministic fallback ensures an incomplete
                                    # answer never silently ends the interview.
                                    if not follow_up:
                                        follow_up = (
                                            "Could you describe the exact steps, "
                                            "tools or components involved, and give "
                                            "a practical example?"
                                        )

                                if completeness == "Complete":
                                    follow_up = ""

                                save_interview_response(
                                    active_interview_id,
                                    pending_question,
                                    interview_answer.strip(),
                                    completeness,
                                    follow_up,
                                    structured_note
                                )

                                # Persist the AI-detected gap separately; original
                                # interview responses and follow-up workflow are retained.
                                if gap_detected and gap_description:
                                    save_knowledge_gap(
                                        current_workspace_id(),
                                        active_interview_id,
                                        knowledge_area,
                                        gap_description,
                                        severity,
                                        follow_up,
                                        pending_question,
                                        interview_answer.strip()
                                    )

                                if structured_note:
                                    st.session_state.setdefault(
                                        "interview_structured_notes", []
                                    ).append(structured_note)
                                st.session_state["last_interview_evaluation"] = {
                                    "completeness": completeness,
                                    "reason": reason,
                                    "follow_up": follow_up,
                                    "note": structured_note,
                                    "gap_detected": gap_detected,
                                    "gap_description": gap_description if gap_detected else "",
                                    "severity": severity,
                                    "knowledge_area": knowledge_area
                                }
                                st.session_state["interview_pending_question"] = follow_up
                                st.session_state["interview_last_saved_message"] = (
                                    "Interview answer saved in SQLite."
                                )
                                st.rerun()
                    except json.JSONDecodeError:
                        st.error(
                            "Gemini returned an unreadable evaluation. "
                            "Please submit the answer again."
                        )
                    except Exception as error:
                        st.error("Could not evaluate the interview answer.")
                        st.caption(f"Technical details: {error}")

        saved_message = st.session_state.pop("interview_last_saved_message", None)
        if saved_message:
            st.success(saved_message)

        last_evaluation = st.session_state.get("last_interview_evaluation")
        if last_evaluation:
            st.subheader("Latest Answer Evaluation")
            st.write(f"**Completeness:** {last_evaluation['completeness']}")
            st.write(last_evaluation["reason"])
            if last_evaluation["note"]:
                st.markdown("**Structured handover note**")
                st.info(last_evaluation["note"])
            if last_evaluation.get("gap_detected"):
                st.warning(
                    f"Knowledge gap detected · {last_evaluation.get('severity', 'Medium')} · "
                    f"{last_evaluation.get('knowledge_area', 'Knowledge area')}"
                )
                st.write(last_evaluation.get("gap_description", ""))
                if last_evaluation.get("follow_up"):
                    st.caption("Targeted follow-up: " + last_evaluation["follow_up"])
            else:
                st.success("No material knowledge gap was detected in this answer.")
            if not last_evaluation["follow_up"]:
                st.success(
                    "No follow-up was required for the latest answer. "
                    "Generate the next question to continue the interview."
                )

        st.caption(
            "Interview notes are AI-generated drafts based on the interviewee's "
            "answer. The outgoing employee or project manager must review them."
        )

    with st.expander("Saved Interview History"):
        interview_rows = get_interview_history(current_workspace_id())
        if interview_rows:
            # Display interview numbers starting at 1 within each workspace.
            # Keep the original database IDs internally for response/evidence links.
            display_rows = []
            display_number_by_id = {}
            for saved_row in interview_rows:
                actual_interview_id = saved_row[0]
                if actual_interview_id not in display_number_by_id:
                    display_number_by_id[actual_interview_id] = (
                        get_interview_display_number(
                            current_workspace_id(), actual_interview_id
                        )
                    )
                display_rows.append(
                    (display_number_by_id[actual_interview_id],) + tuple(saved_row[1:])
                )
            interview_df = pd.DataFrame(
                display_rows,
                columns=[
                    "Interview ID", "Topic", "Interviewee", "Status",
                    "Interview Created", "Question", "Answer",
                    "Completeness", "Follow-up Question",
                    "Structured Note", "Response Created"
                ]
            )
            st.dataframe(interview_df, use_container_width=True, hide_index=True)
            notes = [
                row[9] for row in interview_rows if row[9]
            ]
            if notes:
                st.download_button(
                    "Download Interview Notes",
                    "\n\n".join(notes),
                    file_name="knowledge_interview_notes.txt",
                    mime="text/plain"
                )
        else:
            st.info("No interview responses have been saved yet.")


# ==========================================================
# 9. EVIDENCE VERIFICATION
# ==========================================================
st.markdown("<div id='evidence-verification'></div>", unsafe_allow_html=True)
st.header("6. Evidence Verification")
st.write(
    "Check whether knowledge captured during the outgoing employee interview "
    "is supported by the uploaded project documentation."
)
st.caption(
    "The AI compares interview answers with extracted PDF passages. "
    "A result is a review aid, not proof that a statement is true."
)

if current_workspace_id() is None:
    st.info("Create a workspace before verifying interview evidence.")
elif not pages:
    st.info("Upload project documentation before verifying evidence.")
else:
    evidence_interview_rows = get_interview_history(current_workspace_id())
    evidence_candidates = [
        row for row in evidence_interview_rows
        if row[5] and row[6] and row[6].strip()
    ]
    if not evidence_candidates:
        st.info(
            "Complete at least one outgoing-staff interview answer before "
            "running evidence verification."
        )
    else:
        st.write(
            f"{len(evidence_candidates)} saved interview response(s) are "
            "available for checking."
        )
        if st.button(
            "Verify Interview Answers Against PDF",
            type="primary",
            key="verify_interview_evidence"
        ):
            try:
                client, types = get_gemini_client()
                if client is None:
                    st.error("Gemini API key not found. Check your .env file.")
                else:
                    evidence_items = []
                    for row in evidence_candidates:
                        question_text = row[5] or ""
                        answer_text = row[6] or ""
                        search_text = question_text + " " + answer_text
                        matched = retrieve_relevant_pages(search_text, pages, max_pages=4)
                        excerpts = "\n\n".join(
                            f"[PDF page {item['page']}]\n{item['text'][:3500]}"
                            for item in matched
                        )
                        evidence_items.append({
                            "interview_id": row[0],
                            "topic": row[1],
                            "question": question_text,
                            "answer": answer_text,
                            "document_excerpts": excerpts or "No readable excerpts found."
                        })

                    prompt = f"""
You are an evidence-review assistant for DevHandover AI.
Compare each outgoing employee interview answer ONLY with the supplied PDF excerpts.
Return ONLY valid JSON with this exact structure:
{{
  "results": [
    {{
      "interview_id": 1,
      "status": "Supported",
      "evidence": "Short quote or concise description of the matching evidence",
      "pages": "1, 3",
      "reason": "Brief explanation"
    }}
  ]
}}
Allowed status values:
- Supported: the supplied excerpts clearly support the material claim.
- Partially Supported: only some details are supported or the evidence is incomplete.
- Unverified: the supplied excerpts do not provide enough evidence either way.
- Conflicting Evidence: the supplied excerpts appear to contradict the answer.
Rules:
- Never use outside knowledge.
- Do not treat absence of evidence as proof that the answer is false.
- Cite only page numbers explicitly shown in the excerpts.
- If no useful passage is provided, use Unverified and say so.
- Return one result for every item, preserving interview_id.

Interview answers and matching document excerpts:
{json.dumps(evidence_items, ensure_ascii=False)}
"""
                    with st.spinner("Comparing interview answers with PDF evidence..."):
                        response = client.models.generate_content(
                            model="gemini-3.5-flash-lite",
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                temperature=0.1,
                                max_output_tokens=2500,
                                response_mime_type="application/json"
                            )
                        )
                    parsed = json.loads((response.text or "").strip())
                    allowed_statuses = {
                        "Supported", "Partially Supported",
                        "Unverified", "Conflicting Evidence"
                    }
                    cleaned_results = []
                    ai_results = parsed.get("results", [])
                    # Gemini must never determine database/display IDs. Match each
                    # result to the saved interview response by its original order,
                    # then show the workspace-local interview number used in history.
                    for result_index, result in enumerate(ai_results):
                        if result_index >= len(evidence_candidates):
                            break
                        source_interview_id = evidence_candidates[result_index][0]
                        display_interview_id = get_interview_display_number(
                            current_workspace_id(), source_interview_id
                        )
                        status = str(result.get("status", "Unverified")).strip()
                        if status not in allowed_statuses:
                            status = "Unverified"
                        cleaned_results.append({
                            "Interview ID": display_interview_id,
                            "Verification Status": status,
                            "Evidence Found": str(result.get("evidence", "")),
                            "Source Pages": str(result.get("pages", "")),
                            "Review Notes": str(result.get("reason", ""))
                        })
                    st.session_state["evidence_verification_results"] = cleaned_results
                    save_evidence_verification_results(
                        current_workspace_id(), cleaned_results
                    )
                    st.success("Evidence verification completed and saved in SQLite.")
            except json.JSONDecodeError:
                st.error("Gemini returned an unreadable verification result. Please try again.")
            except Exception as error:
                st.error("Could not complete evidence verification.")
                st.caption(f"Technical details: {error}")

        verification_results = st.session_state.get("evidence_verification_results", [])
        if not verification_results:
            saved_verification_results, _ = get_latest_evidence_verification(
                current_workspace_id()
            )
            if saved_verification_results:
                verification_results = saved_verification_results
                st.session_state["evidence_verification_results"] = saved_verification_results
        if verification_results:
            st.subheader("Evidence Verification Results")
            verification_df = pd.DataFrame(verification_results)
            st.dataframe(verification_df, use_container_width=True, hide_index=True)
            counts = verification_df["Verification Status"].value_counts()
            metric_cols = st.columns(4)
            for col, status in zip(
                metric_cols,
                ["Supported", "Partially Supported", "Unverified", "Conflicting Evidence"]
            ):
                col.metric(status, int(counts.get(status, 0)))
            st.download_button(
                "Download Evidence Verification Report",
                verification_df.to_csv(index=False),
                file_name="evidence_verification_report.csv",
                mime="text/csv"
            )
            st.warning(
                "Review the cited PDF pages manually before accepting a claim. "
                "The current version verifies against extracted text and may "
                "miss scanned content, tables, or layout-dependent information."
            )


# ==========================================================
# 10. PROJECT KNOWLEDGE MAP
# ==========================================================
st.markdown("<div id='knowledge-map'></div>", unsafe_allow_html=True)
st.header("7. Project Knowledge Map")
st.write(
    "Explore how the main project knowledge areas connect to information "
    "found in the uploaded PDF and to knowledge captured during interviews."
)
st.caption(
    "This map is generated from extracted PDF text and saved interview records. "
    "It is a navigation aid, not an automatically verified architecture diagram."
)

knowledge_map_topics = {
    "Project Architecture": ["architecture", "system design", "module", "component", "workflow"],
    "Technology Stack": ["technology stack", "python", "streamlit", "framework", "library", "language"],
    "Installation & Setup": ["installation", "setup", "configuration", "environment", "getting started"],
    "Database & Dependencies": ["database", "sqlite", "dependency", "dependencies", "storage", "schema"],
    "Troubleshooting": ["troubleshooting", "debugging", "error", "exception", "common issues"],
    "Team Responsibilities": ["responsibilities", "team members", "roles", "owner", "ownership"],
    "Technical Decisions": ["technical decision", "design decision", "trade-off", "chosen because"],
    "Risks & Limitations": ["risk", "limitation", "known issue", "constraint", "failure"],
}

if current_workspace_id() is None:
    st.info("Create a workspace to generate its knowledge map.")
elif not pages:
    st.info("Upload project documentation to generate the knowledge map.")
else:
    knowledge_rows = []
    graph_lines = [
        "digraph ProjectKnowledge {",
        'graph [rankdir="LR", bgcolor="transparent", pad="0.2", nodesep="0.35", ranksep="0.7"];',
        'node [shape=box, style="rounded,filled", fontname="Arial", fontsize="10", color="#64748b", fillcolor="#e0f2fe", fontcolor="#0f172a"];',
        'edge [color="#94a3b8", arrowsize="0.7"];',
        'Project [label="Project Knowledge", shape=oval, fillcolor="#bfdbfe"];'
    ]
    for topic_index, (topic_name, keywords) in enumerate(knowledge_map_topics.items(), start=1):
        matched_pages = []
        for page_item in pages:
            page_text = (page_item.get("text") or "").lower()
            if any(keyword in page_text for keyword in keywords):
                matched_pages.append(page_item.get("page"))
        interview_matches = []
        try:
            all_interview_rows = get_interview_history(current_workspace_id())
            for interview_row in all_interview_rows:
                row_topic = str(interview_row[1] or "").lower()
                row_question = str(interview_row[5] or "").lower()
                if topic_name.lower() in row_topic or any(k in row_question for k in keywords):
                    if interview_row[6] and str(interview_row[6]).strip():
                        interview_matches.append(interview_row)
        except Exception:
            interview_matches = []

        if matched_pages:
            coverage = "Document evidence found"
            page_label = ", ".join(str(number) for number in matched_pages[:12])
        else:
            coverage = "No matching PDF text found"
            page_label = "—"
        knowledge_rows.append({
            "Knowledge Area": topic_name,
            "PDF Evidence": coverage,
            "Source Pages": page_label,
            "Interview Responses": len(interview_matches)
        })

        topic_node = f"Topic{topic_index}"
        graph_lines.append(
            f'{topic_node} [label="{topic_name}\\n{len(matched_pages)} page(s)", '
            f'fillcolor="{"#dcfce7" if matched_pages else "#fef3c7"}"];'
        )
        graph_lines.append(f"Project -> {topic_node};")
        for page_index, page_number in enumerate(matched_pages[:3], start=1):
            page_node = f"P{topic_index}_{page_index}"
            graph_lines.append(
                f'{page_node} [label="PDF page {page_number}", shape=note, fillcolor="#f1f5f9"];'
            )
            graph_lines.append(f"{topic_node} -> {page_node};")
    graph_lines.append("}")

    knowledge_df = pd.DataFrame(knowledge_rows)
    found_count = sum(1 for row in knowledge_rows if row["PDF Evidence"] == "Document evidence found")
    col1, col2, col3 = st.columns(3)
    col1.metric("Knowledge Areas", len(knowledge_rows))
    col2.metric("Areas with PDF Matches", found_count)
    col3.metric("Areas Without Matches", len(knowledge_rows) - found_count)

    st.subheader("Project Knowledge Relationships")
    st.graphviz_chart("\n".join(graph_lines), use_container_width=True)
    st.subheader("Knowledge Area Evidence Index")
    st.dataframe(knowledge_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Project Knowledge Map Data",
        knowledge_df.to_csv(index=False),
        file_name="project_knowledge_map.csv",
        mime="text/csv"
    )
    st.warning(
        "A page is linked when it contains one or more topic keywords. "
        "This first version does not understand diagram semantics or prove "
        "that a topic is fully documented. Review the linked pages manually."
    )

st.divider()

# ==========================================================
# 11. DOMAIN EXPERTISE MAP
# ==========================================================
st.markdown("<div id='expertise-map'></div>", unsafe_allow_html=True)
st.header("8. Domain Expertise Map")
st.write(
    "Record which team members understand each project knowledge area, "
    "identify single-person dependencies, and assign backup owners."
)
st.caption(
    "Entries are supplied or confirmed by the project team. The application "
    "does not infer employee expertise from names or interview text."
)

if current_workspace_id() is None:
    st.info("Create a workspace before building its domain expertise map.")
else:
    workspace_details = get_workspace(current_workspace_id())
    existing_expertise = get_domain_expertise(current_workspace_id())
    if existing_expertise.empty:
        outgoing_name = workspace_details[2] if workspace_details else ""
        successor_name = workspace_details[3] if workspace_details else ""
        expertise_seed = pd.DataFrame([
            {"Knowledge Area": area, "Team Member": "",
             "Expertise Level": "Not assessed", "Role": "Contributor",
             "Backup Member": "", "Evidence / Notes": ""}
            for area in [
                "Project Architecture", "Technology Stack", "Installation & Setup",
                "Database & Dependencies", "Troubleshooting",
                "Team Responsibilities", "Technical Decisions", "Risks & Limitations"
            ]
        ])
    else:
        expertise_seed = existing_expertise

    st.write("Add one row for each person and knowledge area they can support. "
             "Use multiple rows when several people share an area.")
    expertise_editor = st.data_editor(
        expertise_seed,
        key=f"domain_expertise_editor_{current_workspace_id()}",
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Knowledge Area": st.column_config.TextColumn("Knowledge Area", required=True),
            "Team Member": st.column_config.TextColumn("Team Member"),
            "Expertise Level": st.column_config.SelectboxColumn(
                "Expertise Level", options=["Not assessed", "Beginner", "Intermediate", "Expert"]
            ),
            "Role": st.column_config.SelectboxColumn(
                "Role", options=["Contributor", "Primary Owner", "Backup Owner"]
            ),
            "Backup Member": st.column_config.TextColumn("Backup Member"),
            "Evidence / Notes": st.column_config.TextColumn("Evidence / Notes")
        }
    )
    if st.button("Save Domain Expertise Map", key="save_domain_expertise"):
        save_domain_expertise(current_workspace_id(), expertise_editor)
        st.success("Domain expertise records saved to SQLite.")
        st.rerun()

    saved_expertise = get_domain_expertise(current_workspace_id())
    if not saved_expertise.empty:
        valid_rows = saved_expertise[
            saved_expertise["Team Member"].fillna("").str.strip() != ""
        ].copy()
        areas = sorted(saved_expertise["Knowledge Area"].dropna().unique().tolist())
        dependency_rows = []
        for area in areas:
            area_rows = valid_rows[valid_rows["Knowledge Area"] == area]
            primary_people = area_rows[
                (area_rows["Role"] == "Primary Owner") |
                (area_rows["Role"] == "Contributor")
            ]["Team Member"].dropna().astype(str).str.strip().unique().tolist()
            backup_people = area_rows[
                (area_rows["Role"] == "Backup Owner")
            ]["Team Member"].dropna().astype(str).str.strip().unique().tolist()
            named_backups = area_rows["Backup Member"].dropna().astype(str).str.strip().tolist()
            backup_people = sorted(set([x for x in backup_people + named_backups if x]))
            if not primary_people:
                status = "Owner not assigned"
            elif not backup_people:
                status = "Single-person dependency"
            else:
                status = "Backup identified"
            dependency_rows.append({
                "Knowledge Area": area,
                "Known Team Members": ", ".join(sorted(set(primary_people))),
                "Backup Members": ", ".join(backup_people),
                "Dependency Status": status
            })
        dependency_df = pd.DataFrame(dependency_rows)
        assigned_count = sum(1 for row in dependency_rows if row["Known Team Members"])
        single_owner_count = sum(1 for row in dependency_rows if row["Dependency Status"] == "Single-person dependency")
        missing_owner_count = sum(1 for row in dependency_rows if row["Dependency Status"] == "Owner not assigned")
        m1, m2, m3 = st.columns(3)
        m1.metric("Knowledge Areas", len(dependency_rows))
        m2.metric("Areas With Assigned Members", assigned_count)
        m3.metric("Single-Person Dependencies", single_owner_count)
        st.subheader("Expertise and Backup Coverage")
        st.dataframe(dependency_df, use_container_width=True, hide_index=True)
        if single_owner_count:
            st.warning(f"{single_owner_count} area(s) have a named team member but no backup. Assign and train a backup owner.")
        if missing_owner_count:
            st.info(f"{missing_owner_count} area(s) do not yet have a named owner. Complete the team assessment.")
        st.download_button(
            "Download Domain Expertise Report",
            saved_expertise.to_csv(index=False),
            file_name="domain_expertise_map.csv",
            mime="text/csv"
        )
    else:
        st.info("Add team members and save the map to see expertise coverage.")

st.divider()

# ==========================================================
# 12. HANDOVER CHECKPOINT TRACKER
# ==========================================================
st.markdown("<div id='checkpoint-tracker'></div>", unsafe_allow_html=True)
st.header("9. Handover Checkpoint Tracker")
st.write(
    "Track the important activities required to complete a project handover, "
    "assign owners and due dates, and record evidence of completion."
)
st.caption(
    "Checkpoint status is maintained by the project team. A checkpoint is "
    "considered complete only when the responsible team member updates it."
)

if current_workspace_id() is None:
    st.info("Create a workspace before adding handover checkpoints.")
else:
    workspace_id_for_checkpoints = current_workspace_id()
    saved_checkpoints = get_handover_checkpoints(workspace_id_for_checkpoints)
    if saved_checkpoints.empty:
        checkpoint_seed = pd.DataFrame([
            {"Checkpoint": "Project documentation reviewed",
             "Description": "Outgoing staff and successor review the available project documents.",
             "Owner": "", "Due Date": "", "Status": "Planned", "Evidence / Notes": ""},
            {"Checkpoint": "Technical knowledge transferred",
             "Description": "Architecture, technology stack, decisions and dependencies explained.",
             "Owner": "", "Due Date": "", "Status": "Planned", "Evidence / Notes": ""},
            {"Checkpoint": "Environment setup completed",
             "Description": "Successor installs dependencies and runs the project.",
             "Owner": "", "Due Date": "", "Status": "Planned", "Evidence / Notes": ""},
            {"Checkpoint": "Troubleshooting walkthrough completed",
             "Description": "Common failures, recovery steps and escalation paths reviewed.",
             "Owner": "", "Due Date": "", "Status": "Planned", "Evidence / Notes": ""},
            {"Checkpoint": "Successor readiness reviewed",
             "Description": "Successor demonstrates understanding and manager reviews outstanding tasks.",
             "Owner": "", "Due Date": "", "Status": "Planned", "Evidence / Notes": ""}
        ])
    else:
        checkpoint_seed = saved_checkpoints

    checkpoint_editor = st.data_editor(
        checkpoint_seed,
        key=f"handover_checkpoint_editor_{workspace_id_for_checkpoints}",
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Checkpoint": st.column_config.TextColumn("Checkpoint", required=True),
            "Description": st.column_config.TextColumn("Description"),
            "Owner": st.column_config.TextColumn("Owner"),
            "Due Date": st.column_config.TextColumn("Due Date (YYYY-MM-DD)"),
            "Status": st.column_config.SelectboxColumn(
                "Status", options=["Planned", "In Progress", "Completed", "Blocked"]
            ),
            "Evidence / Notes": st.column_config.TextColumn("Evidence / Notes")
        }
    )
    if st.button("Save Handover Checkpoints", key="save_handover_checkpoints"):
        save_handover_checkpoints(workspace_id_for_checkpoints, checkpoint_editor)
        st.success("Handover checkpoints saved to SQLite.")
        st.rerun()

    checkpoint_report = get_handover_checkpoints(workspace_id_for_checkpoints)
    if not checkpoint_report.empty:
        total_checkpoints = len(checkpoint_report)
        completed_checkpoints = int((checkpoint_report["Status"] == "Completed").sum())
        blocked_checkpoints = int((checkpoint_report["Status"] == "Blocked").sum())
        open_checkpoints = total_checkpoints - completed_checkpoints
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Checkpoints", total_checkpoints)
        c2.metric("Completed", completed_checkpoints)
        c3.metric("In Progress / Planned", open_checkpoints - blocked_checkpoints)
        c4.metric("Blocked", blocked_checkpoints)
        progress_value = completed_checkpoints / total_checkpoints if total_checkpoints else 0
        st.progress(progress_value, text=f"Handover completion: {progress_value:.0%}")

        today_text = datetime.now().date().isoformat()
        overdue_rows = checkpoint_report[
            (checkpoint_report["Due Date"].fillna("").astype(str).str.strip() != "") &
            (checkpoint_report["Due Date"].astype(str) < today_text) &
            (checkpoint_report["Status"] != "Completed")
        ]
        if not overdue_rows.empty:
            st.warning(f"{len(overdue_rows)} checkpoint(s) have a due date before today and are not completed. Verify the date format (YYYY-MM-DD).")
        if blocked_checkpoints:
            st.error(f"{blocked_checkpoints} checkpoint(s) are marked Blocked. Review their notes and assign actions.")
        st.subheader("Checkpoint Status")
        st.dataframe(checkpoint_report, use_container_width=True, hide_index=True)
        st.download_button(
            "Download Handover Checkpoint Report",
            checkpoint_report.to_csv(index=False),
            file_name="handover_checkpoint_report.csv",
            mime="text/csv"
        )
    else:
        st.info("Add checkpoints and save them to track handover progress.")

st.divider()

st.markdown("<div id='continuity-risk'></div>", unsafe_allow_html=True)
st.header("7. Project Continuity Risk Engine")
st.write(
    "Evaluate the vulnerability of important project knowledge areas."
)
if current_workspace_id() is None:
    st.info("Create a workspace before calculating or saving continuity risks.")
default_risk_data = pd.DataFrame([
    {
        "Knowledge Area": "System Architecture",
        "Primary Owner": "Employee A",
        "Backup Owner": "Employee B",
        "Knowledge Concentration": 80,
        "Business Impact": 90,
        "Documentation Weakness": 65
    },
    {
        "Knowledge Area": "Database Management",
        "Primary Owner": "Employee B",
        "Backup Owner": "Not Assigned",
        "Knowledge Concentration": 90,
        "Business Impact": 85,
        "Documentation Weakness": 75
    },
    {
        "Knowledge Area": "Deployment",
        "Primary Owner": "Employee C",
        "Backup Owner": "Employee A",
        "Knowledge Concentration": 55,
        "Business Impact": 80,
        "Documentation Weakness": 40
    },
    {
        "Knowledge Area": "Troubleshooting",
        "Primary Owner": "Employee A",
        "Backup Owner": "Not Assigned",
        "Knowledge Concentration": 85,
        "Business Impact": 70,
        "Documentation Weakness": 80
    }
])
if "risk_data" not in st.session_state:
    st.session_state["risk_data"] = default_risk_data.copy()
st.info(
    "Default risk rows are illustrative. Edit them using your actual project assessment."
)
edited_risk_data = st.data_editor(
    st.session_state["risk_data"],
    num_rows="dynamic",
    use_container_width=True,
    key="risk_editor",
    column_config={
        "Knowledge Concentration": st.column_config.NumberColumn(
            "Knowledge Concentration (%)",
            min_value=0,
            max_value=100
        ),
        "Business Impact": st.column_config.NumberColumn(
            "Business Impact (%)",
            min_value=0,
            max_value=100
        ),
        "Documentation Weakness": st.column_config.NumberColumn(
            "Documentation Weakness (%)",
            min_value=0,
            max_value=100
        )
    }
)
st.session_state["risk_data"] = edited_risk_data.copy()
if st.button("Calculate Continuity Risk", disabled=current_workspace_id() is None):
    if edited_risk_data.empty:
        st.warning("Add at least one knowledge area.")
    else:
        risk_results = []
        valid_data = True
        for _, row in edited_risk_data.iterrows():
            # Streamlit's dynamic data editor can include a trailing blank row.
            # Ignore only rows where every field is genuinely empty.
            row_values = [
                row.get("Knowledge Area"),
                row.get("Primary Owner"),
                row.get("Backup Owner"),
                row.get("Knowledge Concentration"),
                row.get("Business Impact"),
                row.get("Documentation Weakness"),
            ]
            def is_blank_risk_value(value):
                if pd.isna(value):
                    return True
                return str(value).strip().lower() in ("", "none", "nan", "nat")

            if all(is_blank_risk_value(value) for value in row_values):
                continue

            # A partially completed row is not silently ignored; report it clearly.
            area = row.get("Knowledge Area")
            if is_blank_risk_value(area):
                st.error("Enter a Knowledge Area for every row containing data.")
                valid_data = False
                break

            try:
                concentration = float(row["Knowledge Concentration"])
                impact = float(row["Business Impact"])
                weakness = float(row["Documentation Weakness"])
                if not all(
                    0 <= value <= 100
                    for value in [concentration, impact, weakness]
                ):
                    raise ValueError("Scores must be between 0 and 100.")
                risk_score = (
                    0.40 * concentration
                    + 0.35 * impact
                    + 0.25 * weakness
                )
                if risk_score < 35:
                    risk_level = "Low"
                elif risk_score < 65:
                    risk_level = "Moderate"
                else:
                    risk_level = "High"
                risk_results.append({
                    "Knowledge Area": str(area).strip(),
                    "Primary Owner": "" if is_blank_risk_value(row.get("Primary Owner")) else str(row.get("Primary Owner")).strip(),
                    "Backup Owner": "" if is_blank_risk_value(row.get("Backup Owner")) else str(row.get("Backup Owner")).strip(),
                    "Risk Score": round(risk_score, 1),
                    "Risk Level": risk_level
                })
            except (ValueError, TypeError):
                st.error(
                    "For each entered Knowledge Area, provide valid numeric "
                    "scores between 0 and 100 for all three risk fields."
                )
                valid_data = False
                break
        if valid_data and not risk_results:
            st.warning("Enter at least one complete knowledge-area row before calculating.")
            valid_data = False
        if valid_data and risk_results:
            risk_results_df = pd.DataFrame(risk_results)
            st.session_state["risk_results"] = risk_results_df
            save_risk_assessment(
                current_workspace_id(),
                risk_results_df
            )
            st.success("Risk assessment saved in SQLite!")
if "risk_results" in st.session_state:
    risk_results_df = st.session_state["risk_results"]
    st.subheader("Continuity Risk Dashboard")
    high_risks = len(
        risk_results_df[
            risk_results_df["Risk Level"] == "High"
        ]
    )
    moderate_risks = len(
        risk_results_df[
            risk_results_df["Risk Level"] == "Moderate"
        ]
    )
    low_risks = len(
        risk_results_df[
            risk_results_df["Risk Level"] == "Low"
        ]
    )
    average_risk = round(
        risk_results_df["Risk Score"].mean(),
        1
    )
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average Risk", f"{average_risk}/100")
    col2.metric("High Risk Areas", high_risks)
    col3.metric("Moderate Risk Areas", moderate_risks)
    col4.metric("Low Risk Areas", low_risks)
    st.subheader("Risk Assessment Results")
    st.dataframe(
        risk_results_df,
        use_container_width=True,
        hide_index=True
    )
    st.subheader("Risk Score by Knowledge Area")
    st.bar_chart(
        risk_results_df.set_index("Knowledge Area")[["Risk Score"]]
    )
    st.subheader("Recommended Actions")
    for _, row in risk_results_df.iterrows():
        area = row["Knowledge Area"]
        level = row["Risk Level"]
        if level == "High":
            st.error(
                f"{area}: High Risk — Arrange immediate knowledge transfer, "
                "confirm backup ownership, and document critical procedures."
            )
        elif level == "Moderate":
            st.warning(
                f"{area}: Moderate Risk — Improve documentation and "
                "schedule knowledge-sharing sessions."
            )
        else:
            st.success(
                f"{area}: Low Risk — Maintain documentation and "
                "periodically review backup readiness."
            )
    st.download_button(
        "Download Risk Report",
        risk_results_df.to_csv(index=False),
        file_name="continuity_risk_report.csv",
        mime="text/csv"
    )
    st.caption(
        "Formula: 40% Knowledge Concentration + "
        "35% Business Impact + 25% Documentation Weakness. "
        "These are illustrative assumptions, not validated predictions."
    )
st.divider()
# ==========================================================
# 9. SUCCESSOR READINESS
# ==========================================================
st.markdown("<div id='readiness'></div>", unsafe_allow_html=True)
st.header("7. Successor Readiness & Handover Verification")
st.write(
    "Track knowledge transfer activities and evaluate handover completion."
)
if current_workspace_id() is None:
    st.info("Create a workspace before evaluating successor readiness.")
if "readiness_data" not in st.session_state:
    st.session_state["readiness_data"] = {
        "documentation": False,
        "architecture": False,
        "setup": False,
        "troubleshooting": False,
        "responsibilities": False
    }
if "readiness_score" not in st.session_state:
    st.session_state["readiness_score"] = None
if "readiness_approved" not in st.session_state:
    st.session_state["readiness_approved"] = False
if "readiness_assessment_id" not in st.session_state:
    st.session_state["readiness_assessment_id"] = None
if "readiness_notes" not in st.session_state:
    st.session_state["readiness_notes"] = {
        "technical": "",
        "pending": ""
    }
if "workspace" in st.session_state:
    st.write(
        f"**Successor:** {st.session_state['workspace']['successor']}"
    )
else:
    st.info("Create a workspace to identify the successor.")
with st.form("readiness_form"):
    documentation = st.checkbox(
        "Successor has reviewed project documentation",
        value=st.session_state["readiness_data"]["documentation"]
    )
    architecture = st.checkbox(
        "Successor understands project architecture",
        value=st.session_state["readiness_data"]["architecture"]
    )
    setup = st.checkbox(
        "Successor has completed installation and setup",
        value=st.session_state["readiness_data"]["setup"]
    )
    troubleshooting = st.checkbox(
        "Successor understands common errors and troubleshooting",
        value=st.session_state["readiness_data"]["troubleshooting"]
    )
    responsibilities = st.checkbox(
        "Successor understands project roles and responsibilities",
        value=st.session_state["readiness_data"]["responsibilities"]
    )
    technical_notes = st.text_area(
        "Important technical knowledge transferred",
        value=st.session_state["readiness_notes"]["technical"]
    )
    pending_tasks = st.text_area(
        "Tasks or knowledge areas still pending",
        value=st.session_state["readiness_notes"]["pending"]
    )
    evaluate = st.form_submit_button("Evaluate Readiness", disabled=current_workspace_id() is None)
if evaluate:
    checklist = {
        "documentation": documentation,
        "architecture": architecture,
        "setup": setup,
        "troubleshooting": troubleshooting,
        "responsibilities": responsibilities
    }
    completed = sum(checklist.values())
    checklist_score = (completed / 5) * 70
    notes_score = 0
    if technical_notes.strip():
        notes_score += 15
    if pending_tasks.strip():
        notes_score += 15
    score = round(checklist_score + notes_score)
    st.session_state["readiness_data"] = checklist
    st.session_state["readiness_score"] = score
    st.session_state["readiness_notes"] = {
        "technical": technical_notes,
        "pending": pending_tasks
    }
    assessment_id = save_readiness_assessment(
        current_workspace_id(),
        score,
        completed,
        technical_notes,
        pending_tasks
    )
    st.session_state["readiness_assessment_id"] = assessment_id
    st.session_state["readiness_approved"] = False
    st.success("Readiness assessment saved in SQLite!")
if st.session_state["readiness_score"] is not None:
    score = st.session_state["readiness_score"]
    completed = sum(
        st.session_state["readiness_data"].values()
    )
    st.subheader("Successor Readiness Dashboard")
    col1, col2 = st.columns(2)
    col1.metric("Readiness Score", f"{score}/100")
    col2.metric("Completed Activities", f"{completed}/5")
    st.progress(score / 100)
    if score >= 85:
        st.success("High completion: Ready for manager review.")
    elif score >= 60:
        st.warning("Partial completion: More handover work is required.")
    else:
        st.error("Low completion: Significant handover work remains.")
    st.subheader("Activity Status")
    for item, status in st.session_state["readiness_data"].items():
        if status:
            st.write(f"✅ {item.replace('_', ' ').title()}")
        else:
            st.write(f"❌ {item.replace('_', ' ').title()}")
    st.subheader("Knowledge Transfer Summary")
    st.write(
        st.session_state["readiness_notes"]["technical"]
        or "No technical notes provided."
    )
    st.write("**Pending Tasks:**")
    st.write(
        st.session_state["readiness_notes"]["pending"]
        or "No pending tasks provided."
    )
    st.divider()
    st.subheader("Manager Verification")
    manager_name = st.text_input(
        "Manager Name",
        key="manager_name_input"
    )
    if st.button("Approve Handover"):
        assessment_id = st.session_state["readiness_assessment_id"]
        if score < 85:
            st.warning(
                "Readiness score is below 85. "
                "Complete more activities before approval."
            )
        elif not manager_name.strip():
            st.warning("Enter the manager's name.")
        elif assessment_id is None:
            st.error("No saved readiness assessment was found.")
        else:
            approve_readiness(
                assessment_id,
                manager_name
            )
            st.session_state["readiness_approved"] = True
            st.session_state["approved_manager"] = manager_name
            st.success("Handover approved and saved in SQLite!")
    if st.session_state["readiness_approved"]:
        st.success("Handover approval completed!")
        st.write(
            f"**Approved By:** "
            f"{st.session_state['approved_manager']}"
        )
        st.write(f"**Final Score:** {score}/100")
    st.caption(
        "This score measures recorded checklist completion, not independently "
        "verified technical understanding. Manager approval is a demo action, "
        "not a digital signature."
    )
st.divider()
# ==========================================================
# 10. EVIDENCE-BASED HANDOVER RISK & READINESS DASHBOARD
# ==========================================================
st.markdown("<div id='handover-dashboard'></div>", unsafe_allow_html=True)
st.header("8. Evidence-Based Handover Risk & Readiness Dashboard")
st.write(
    "A unified view of unresolved knowledge gaps, evidence-verification results, "
    "continuity risk, and successor preparation. This dashboard reads the "
    "existing workspace records and does not replace their individual modules."
)

if current_workspace_id() is None:
    st.info("Create or select a workspace to view the unified handover dashboard.")
else:
    dashboard_workspace_id = current_workspace_id()
    dashboard_gaps = get_knowledge_gaps(dashboard_workspace_id)
    dashboard_evidence, dashboard_evidence_at = get_latest_evidence_verification(
        dashboard_workspace_id
    )

    dashboard_connection = get_connection()
    latest_risk_row = dashboard_connection.execute("""
        SELECT risk_data, average_risk, created_at
        FROM risk_assessments
        WHERE workspace_id = ? ORDER BY id DESC LIMIT 1
    """, (dashboard_workspace_id,)).fetchone()
    latest_readiness_row = dashboard_connection.execute("""
        SELECT readiness_score, completed_activities, technical_notes,
               pending_tasks, manager_name, approved, created_at
        FROM readiness_assessments
        WHERE workspace_id = ? ORDER BY id DESC LIMIT 1
    """, (dashboard_workspace_id,)).fetchone()
    dashboard_connection.close()

    open_gaps = [gap for gap in dashboard_gaps if gap[4] != "Resolved"]
    critical_high_gaps = [gap for gap in open_gaps if gap[3] in ("Critical", "High")]
    unverified_evidence = [
        item for item in dashboard_evidence
        if item.get("Verification Status") in ("Unverified", "Partially Supported", "Conflicting Evidence")
    ]
    supported_evidence_count = sum(
        1 for item in dashboard_evidence
        if item.get("Verification Status") == "Supported"
    )

    risk_items = []
    average_risk_value = None
    risk_saved_at = None
    if latest_risk_row:
        risk_json, average_risk_value, risk_saved_at = latest_risk_row
        try:
            risk_items = json.loads(risk_json or "[]")
            if not isinstance(risk_items, list):
                risk_items = []
        except (TypeError, json.JSONDecodeError):
            risk_items = []

    readiness_score_value = None
    readiness_completed_value = None
    readiness_manager = None
    readiness_approved_value = False
    readiness_saved_at = None
    readiness_pending_text = ""
    if latest_readiness_row:
        (readiness_score_value, readiness_completed_value, readiness_technical,
         readiness_pending_text, readiness_manager, readiness_approved_value,
         readiness_saved_at) = latest_readiness_row

    dash_cols = st.columns(4)
    dash_cols[0].metric("Open Knowledge Gaps", len(open_gaps))
    dash_cols[1].metric("Critical / High Gaps", len(critical_high_gaps))
    dash_cols[2].metric("Evidence Items Needing Review", len(unverified_evidence))
    dash_cols[3].metric(
        "Successor Readiness",
        f"{readiness_score_value}/100" if readiness_score_value is not None else "Not assessed"
    )

    st.subheader("Continuity and evidence status")
    status_cols = st.columns(3)
    status_cols[0].metric(
        "Latest Average Risk",
        f"{float(average_risk_value):.1f}/100" if average_risk_value is not None else "Not assessed"
    )
    status_cols[1].metric("Evidence Supported", supported_evidence_count)
    status_cols[2].metric(
        "Manager Approval",
        "Approved" if readiness_approved_value else "Pending"
    )

    if dashboard_gaps:
        st.subheader("Knowledge gaps requiring attention")
        gap_dashboard_df = pd.DataFrame([
            {
                "Gap ID": gap[0],
                "Knowledge Area": gap[1],
                "Missing Knowledge": gap[2],
                "Severity": gap[3],
                "Status": gap[4],
                "Follow-up": gap[5] or "Not recorded"
            }
            for gap in dashboard_gaps
        ])
        st.dataframe(gap_dashboard_df, use_container_width=True, hide_index=True)
    else:
        st.info("No AI-detected knowledge gaps have been saved for this workspace yet.")

    if dashboard_evidence:
        st.subheader("Evidence verification requiring review")
        evidence_dashboard_df = pd.DataFrame(dashboard_evidence)
        st.dataframe(evidence_dashboard_df, use_container_width=True, hide_index=True)
        st.caption(f"Latest evidence run: {dashboard_evidence_at or 'Timestamp unavailable'}")
    else:
        st.info("No evidence-verification run has been saved for this workspace yet.")

    if risk_items:
        st.subheader("Highest continuity-risk areas")
        risk_dashboard_df = pd.DataFrame(risk_items)
        if "Risk Score" in risk_dashboard_df.columns:
            risk_dashboard_df = risk_dashboard_df.sort_values(
                "Risk Score", ascending=False
            )
        st.dataframe(risk_dashboard_df, use_container_width=True, hide_index=True)
        st.caption(
            f"Latest risk assessment: {risk_saved_at or 'Timestamp unavailable'}. "
            "Risk scores use the existing illustrative 40% / 35% / 25% formula."
        )
    else:
        st.info("No saved continuity-risk assessment is available yet.")

    if latest_readiness_row:
        st.subheader("Successor preparation")
        st.write(
            f"Checklist activities completed: {readiness_completed_value}/5. "
            f"Manager approval: {'Approved' if readiness_approved_value else 'Not approved'}."
        )
        if readiness_pending_text and readiness_pending_text.strip():
            st.warning(f"Pending successor tasks: {readiness_pending_text}")
        st.caption(
            f"Latest readiness assessment: {readiness_saved_at or 'Timestamp unavailable'}. "
            "The score reflects recorded checklist completion, not independently tested competence."
        )
    else:
        st.info("Successor readiness has not yet been assessed.")

    st.subheader("Recommended continuity action plan")
    action_count = 0
    for gap in critical_high_gaps:
        st.error(
            f"Resolve {gap[3]} gap in {gap[1]}: {gap[2]} "
            f"Next step: {gap[5] or 'Assign an owner and capture the missing knowledge.'}"
        )
        action_count += 1
    for item in unverified_evidence:
        st.warning(
            f"Review interview #{item.get('Interview ID', 'N/A')} evidence "
            f"({item.get('Verification Status', 'Needs review')}). Check source pages "
            f"{item.get('Source Pages') or 'not specified'} against the original PDF."
        )
        action_count += 1
    if risk_items:
        for item in sorted(
            risk_items,
            key=lambda value: float(value.get("Risk Score", 0) or 0),
            reverse=True
        )[:3]:
            if item.get("Risk Level") in ("High", "Moderate"):
                st.warning(
                    f"Strengthen {item.get('Knowledge Area', 'this knowledge area')}: "
                    f"{item.get('Risk Level')} continuity risk ({item.get('Risk Score', 'N/A')}/100). "
                    "Confirm a backup owner and document critical procedures."
                )
                action_count += 1
    if readiness_score_value is None:
        st.info("Action: complete the successor-readiness checklist and record pending tasks.")
        action_count += 1
    elif not readiness_approved_value:
        st.info("Action: manager should review unresolved gaps, evidence, and readiness before approval.")
        action_count += 1
    if action_count == 0:
        st.success(
            "No open high-priority actions were identified from the currently saved records. "
            "Continue periodic review with the project team."
        )

    st.caption(
        "This dashboard consolidates saved app records to support decisions. "
        "It does not independently prove that knowledge is correct or that a successor is competent."
    )

st.divider()
# ==========================================================
# 11. SAVED DATABASE HISTORY
# ==========================================================
st.markdown("<div id='project-history'></div>", unsafe_allow_html=True)
st.header("8. Saved Project History")
workspace_id = current_workspace_id()
if workspace_id is not None:
    risks, readiness, documents = get_saved_history(workspace_id)
    st.subheader("Saved Documents")
    if not documents.empty:
        st.dataframe(
            documents,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No saved documents yet.")
    st.subheader("Saved Risk Assessments")
    if not risks.empty:
        st.dataframe(
            risks,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No saved risk assessments yet.")
    st.subheader("Saved Successor Assessments")
    if not readiness.empty:
        st.dataframe(
            readiness,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No saved readiness assessments yet.")
else:
    st.info("Create a workspace to view saved project history.")
st.divider()
# ==========================================================
# 11. PROJECT STATUS
# ==========================================================
st.header("9. Project Status")
if "workspace" in st.session_state:
    st.success("Handover workspace is active.")
if pages:
    st.success("Project documentation has been processed.")
if "risk_results" in st.session_state:
    st.success("Continuity risk assessment completed.")
if st.session_state["readiness_score"] is not None:
    st.success("Successor readiness assessment completed.")
if st.session_state["readiness_approved"]:
    st.success("Manager approval completed.")
st.write(
    "DevHandover AI MVP — workspace management, PDF extraction, "
    "Gemini-powered document Q&A, preliminary gap detection, "
    "continuity risk scoring, successor readiness, and SQLite storage."
)
st.caption(
    "Future enhancements: stronger semantic retrieval, LLM-powered handover "
    "summaries, evidence-based successor assessments, predictive "
    "knowledge-loss intelligence, and project management integrations."
)


# ==========================================================
# 13. HANDOVER PACKAGE GENERATOR
# ==========================================================
def build_handover_package_pdf(workspace_id):
    """Build a PDF handover package from the active workspace's saved records."""
    workspace_row = get_workspace(workspace_id)
    if not workspace_row:
        raise ValueError("The active workspace could not be found.")

    connection = get_connection()
    document_rows = connection.execute("""
        SELECT filename, created_at
        FROM documents
        WHERE workspace_id = ?
        ORDER BY id DESC
    """, (workspace_id,)).fetchall()
    risk_rows = connection.execute("""
        SELECT risk_data, average_risk, created_at
        FROM risk_assessments
        WHERE workspace_id = ?
        ORDER BY id DESC
    """, (workspace_id,)).fetchall()
    readiness_rows = connection.execute("""
        SELECT readiness_score, completed_activities, technical_notes,
               pending_tasks, manager_name, approved, created_at
        FROM readiness_assessments
        WHERE workspace_id = ?
        ORDER BY id DESC
    """, (workspace_id,)).fetchall()
    connection.close()

    interview_rows = get_interview_history(workspace_id)
    expertise_df = get_domain_expertise(workspace_id)
    checkpoint_df = get_handover_checkpoints(workspace_id)

    project_name = workspace_row[1] or "Unnamed project"
    outgoing = workspace_row[2] or "Not specified"
    successor_name = workspace_row[3] or "Not specified"
    deadline = workspace_row[4] or "Not specified"

    report_lines = [
        "DEVHANDOVER AI - PROJECT HANDOVER PACKAGE",
        "=" * 62,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "1. WORKSPACE SUMMARY",
        f"Project: {project_name}",
        f"Outgoing employee: {outgoing}",
        f"Successor: {successor_name}",
        f"Handover deadline: {deadline}",
        "",
        "2. PROJECT DOCUMENTATION",
    ]

    if document_rows:
        for filename, created_at in document_rows:
            report_lines.append(f"- {filename or 'Unnamed document'} (saved: {created_at or 'unknown'})")
    else:
        report_lines.append("- No project PDF is saved in this workspace.")

    report_lines.extend(["", "3. KNOWLEDGE INTERVIEW SUMMARY"])
    if interview_rows:
        for row in interview_rows:
            interview_id, topic, interviewee, status, created_at = row[:5]
            question, answer, completeness = row[5:8]
            follow_up, structured_note = row[8:10]
            report_lines.extend([
                f"Interview #{interview_id} | Topic: {topic or 'Not specified'}",
                f"Interviewee: {interviewee or 'Not specified'} | Status: {status or 'Not specified'}",
                f"Question: {question or 'Not available'}",
                f"Answer: {answer or 'Not available'}",
                f"Completeness: {completeness or 'Not assessed'}",
            ])
            if follow_up:
                report_lines.append(f"Follow-up pending: {follow_up}")
            if structured_note:
                report_lines.append(f"Handover note: {structured_note}")
            report_lines.append("")
    else:
        report_lines.append("No interview responses have been saved.")

    report_lines.extend(["", "4. DOMAIN EXPERTISE AND BACKUP OWNERS"])
    if not expertise_df.empty:
        for _, row in expertise_df.iterrows():
            report_lines.append(
                f"- {row['Knowledge Area']}: {row['Team Member'] or 'No owner'}; "
                f"level: {row['Expertise Level'] or 'Not assessed'}; "
                f"role: {row['Role'] or 'Not specified'}; "
                f"backup: {row['Backup Member'] or 'Not assigned'}"
            )
            if row["Evidence / Notes"]:
                report_lines.append(f"  Notes: {row['Evidence / Notes']}")
    else:
        report_lines.append("No domain expertise records have been saved.")

    report_lines.extend(["", "5. CONTINUITY RISK ASSESSMENTS"])
    if risk_rows:
        for index, (risk_json, average_risk, created_at) in enumerate(risk_rows, start=1):
            report_lines.append(
                f"Assessment {index} | Average risk: {average_risk}/100 | Saved: {created_at}"
            )
            try:
                risk_items = json.loads(risk_json or "[]")
            except (TypeError, json.JSONDecodeError):
                risk_items = []
            for item in risk_items:
                report_lines.append(
                    f"- {item.get('Knowledge Area', 'Area')}: "
                    f"{item.get('Risk Score', 'N/A')}/100 "
                    f"({item.get('Risk Level', 'Not classified')}); "
                    f"primary: {item.get('Primary Owner', 'Not assigned')}; "
                    f"backup: {item.get('Backup Owner', 'Not assigned')}"
                )
    else:
        report_lines.append("No saved continuity risk assessment is available.")

    report_lines.extend(["", "6. HANDOVER CHECKPOINTS"])
    if not checkpoint_df.empty:
        total = len(checkpoint_df)
        completed_count = int((checkpoint_df["Status"] == "Completed").sum())
        progress_percent = completed_count / total if total else 0
        report_lines.append(
            f"Progress: {completed_count}/{total} checkpoints completed "
            f"({progress_percent:.0%})."
        )
        for _, row in checkpoint_df.iterrows():
            report_lines.append(
                f"- {row['Checkpoint']} | Status: {row['Status']} | "
                f"Owner: {row['Owner'] or 'Not assigned'} | "
                f"Due: {row['Due Date'] or 'Not set'}"
            )
            if row["Evidence / Notes"]:
                report_lines.append(f"  Evidence / notes: {row['Evidence / Notes']}")
    else:
        report_lines.append("No handover checkpoints have been saved.")

    report_lines.extend(["", "7. SUCCESSOR READINESS AND MANAGER REVIEW"])
    if readiness_rows:
        score, completed, technical_notes, pending_tasks, manager_name, approved, created_at = readiness_rows[0]
        report_lines.extend([
            f"Latest readiness score: {score}/100",
            f"Checklist activities completed: {completed}/5",
            f"Manager approval: {'Approved' if approved else 'Not approved'}",
            f"Manager: {manager_name or 'Not recorded'}",
            f"Assessment saved: {created_at or 'Unknown'}",
            f"Technical knowledge transferred: {technical_notes or 'Not provided'}",
            f"Pending tasks: {pending_tasks or 'None recorded'}",
        ])
    else:
        report_lines.append("No successor readiness assessment has been saved.")

    report_lines.extend([
        "",
        "8. EVIDENCE VERIFICATION",
    ])
    verification_results = st.session_state.get("evidence_verification_results", [])
    if verification_results:
        for item in verification_results:
            report_lines.append(
                f"- Interview #{item.get('Interview ID', 'N/A')}: "
                f"{item.get('Verification Status', 'Not assessed')}; "
                f"source pages: {item.get('Source Pages', 'Not specified')}; "
                f"notes: {item.get('Review Notes', '')}"
            )
    else:
        report_lines.append(
            "No evidence verification results are available in the current app session."
        )

    report_lines.extend([
        "",
        "IMPORTANT REVIEW NOTES",
        "- This package compiles records saved in the active workspace.",
        "- Interview completeness and AI evidence checks are review aids, not proof of correctness.",
        "- Risk scores depend on values entered by the project team.",
        "- Expertise and checkpoint information must be confirmed by responsible team members.",
        "- The manager should review the original documents and unresolved items before accepting the handover.",
    ])

    pdf_document = fitz.open()
    page = pdf_document.new_page(width=595, height=842)
    y_position = 48
    left_margin = 48
    body_width = 88

    for line_index, raw_line in enumerate(report_lines):
        is_heading = (
            raw_line.startswith("DEVHANDOVER AI")
            or (len(raw_line) > 2 and raw_line[0].isdigit() and raw_line[1:3] == ". ")
            or raw_line == "IMPORTANT REVIEW NOTES"
        )
        wrapped_lines = textwrap.wrap(raw_line, width=body_width) if raw_line else [""]
        for wrapped_line in wrapped_lines:
            font_size = 15 if raw_line.startswith("DEVHANDOVER AI") else (11 if is_heading else 9)
            line_height = 22 if font_size == 15 else (17 if is_heading else 13)
            if y_position + line_height > 790:
                page = pdf_document.new_page(width=595, height=842)
                y_position = 48
            if wrapped_line:
                page.insert_text(
                    (left_margin, y_position),
                    wrapped_line,
                    fontsize=font_size,
                    fontname="helv",
                    color=(0.12, 0.16, 0.22)
                )
            y_position += line_height

    pdf_bytes = pdf_document.tobytes()
    pdf_document.close()
    return pdf_bytes


st.divider()
st.markdown("<div id='handover-package'></div>", unsafe_allow_html=True)
st.header("10. Handover Package Generator")
st.write(
    "Compile the active workspace's saved interview notes, expertise map, "
    "continuity risk assessments, checkpoints, documentation references, "
    "and successor readiness into one downloadable PDF."
)
st.caption(
    "The package is generated from records currently saved in SQLite. "
    "Evidence-verification results are included only when available in this app session."
)

if current_workspace_id() is None:
    st.info("Create or restore a workspace before generating its handover package.")
else:
    if st.button(
        "Generate Handover Package PDF",
        type="primary",
        key="generate_handover_package"
    ):
        try:
            with st.spinner("Compiling the saved handover information..."):
                st.session_state["handover_package_pdf"] = build_handover_package_pdf(
                    current_workspace_id()
                )
            st.success("Handover package generated successfully.")
        except Exception as error:
            st.error("Could not generate the handover package.")
            st.caption(f"Technical details: {error}")

    if st.session_state.get("handover_package_pdf"):
        safe_project_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            st.session_state.get("workspace", {}).get("project", "project")
        ).strip("_") or "project"
        st.download_button(
            "Download Complete Handover Package",
            data=st.session_state["handover_package_pdf"],
            file_name=f"{safe_project_name}_handover_package.pdf",
            mime="application/pdf",
            key="download_handover_package"
        )

st.divider()
st.markdown("<div id='successor-workspace'></div>", unsafe_allow_html=True)
st.header("11. Successor Workspace and Knowledge Q&A")
st.write(
    "A dedicated learning area for the incoming employee to review handover "
    "knowledge and ask project-specific questions. Answers use uploaded PDF "
    "content and saved outgoing-staff interview notes when available."
)
st.caption(
    "The assistant must say when available sources do not contain an answer. "
    "PDF page references are shown separately from interview-note sources."
)

workspace_id_for_successor = current_workspace_id()
if workspace_id_for_successor is None:
    st.info("Create or restore a handover workspace to open the successor workspace.")
else:
    active_workspace = st.session_state.get("workspace", {})
    successor_display_name = active_workspace.get("successor", "Successor")
    st.subheader(f"Welcome, {successor_display_name}")
    st.markdown(
        f"**Project:** {active_workspace.get('project', 'Not specified')}  \n"
        f"**Outgoing employee:** {active_workspace.get('outgoing', 'Not specified')}  \n"
        f"**Handover deadline:** {active_workspace.get('deadline', 'Not specified')}"
    )

    successor_question = st.text_area(
        "What would you like to know about this project?",
        placeholder="Example: How do I install the project and run it locally?",
        key="successor_workspace_question",
        height=100
    )
    if st.button("Ask DevHandover AI", type="primary", key="successor_ask_button"):
        if not successor_question.strip():
            st.warning("Enter a question before submitting.")
        else:
            pdf_pages_for_successor = st.session_state.get("pages", [])
            relevant_successor_pages = retrieve_relevant_pages(
                successor_question, pdf_pages_for_successor, max_pages=6
            ) if pdf_pages_for_successor else []

            connection = get_connection()
            interview_note_rows = connection.execute("""
                SELECT ki.topic, ki.interviewee, ir.question, ir.answer,
                       ir.completeness, ir.structured_note
                FROM knowledge_interviews ki
                JOIN interview_responses ir ON ir.interview_id = ki.id
                WHERE ki.workspace_id = ?
                ORDER BY ir.id DESC LIMIT 30
            """, (workspace_id_for_successor,)).fetchall()
            connection.close()

            interview_context_parts = []
            for topic, interviewee, old_question, old_answer, completeness, note in interview_note_rows:
                content = note or old_answer or ""
                if content.strip():
                    interview_context_parts.append(
                        f"Topic: {topic or 'Not specified'}; Interviewee: {interviewee or 'Not specified'}; "
                        f"Completeness: {completeness or 'Not assessed'}\n"
                        f"Original question: {old_question or 'Not available'}\n"
                        f"Captured knowledge: {content[:1800]}"
                    )
            interview_context = "\n\n".join(interview_context_parts)[:12000]

            pdf_context_parts = []
            for item in relevant_successor_pages:
                pdf_context_parts.append(
                    f"--- PDF SOURCE PAGE {item.get('page')} ---\n{(item.get('text') or '')[:6000]}"
                )
            pdf_context = "\n\n".join(pdf_context_parts)[:18000]

            if not pdf_context.strip() and not interview_context.strip():
                st.warning(
                    "No readable PDF content or saved interview notes are available "
                    "for this workspace yet. Upload project documentation or complete "
                    "an outgoing-staff knowledge interview first."
                )
            else:
                try:
                    with st.spinner("Searching handover knowledge for an answer..."):
                        client, types = get_gemini_client()
                        if client is None:
                            st.error("Gemini API key not found. Check your local .env file and restart the app.")
                        else:
                            successor_prompt = f"""
You are the knowledge-transfer assistant inside DevHandover AI.
Answer the successor's question using ONLY the PDF excerpts and saved interview notes below.
Do not invent project-specific facts or use outside knowledge as if it were project evidence.
If sources do not answer the question, say clearly: 'The available handover sources do not provide enough information to answer this.'
You may identify exactly what should be clarified with the outgoing employee or manager.
Cite PDF claims using [PDF Page N], only for page numbers supplied below.
For interview-derived claims, label them [Outgoing-staff interview note]. Do not pretend interview notes are PDF evidence.
Give practical, beginner-friendly steps only when supported by the sources.

SUCCESSOR QUESTION:
{successor_question}

PDF EXCERPTS:
{pdf_context or 'No relevant PDF excerpts were available.'}

SAVED OUTGOING-STAFF INTERVIEW NOTES:
{interview_context or 'No saved interview notes were available.'}
"""
                            response = client.models.generate_content(
                                model="gemini-3.5-flash-lite",
                                contents=successor_prompt,
                                config=types.GenerateContentConfig(
                                    temperature=0.2, max_output_tokens=900
                                )
                            )
                            successor_answer = (response.text or "").strip()
                            if not successor_answer:
                                st.warning("Gemini returned an empty answer. Please try again.")
                            else:
                                page_numbers = [str(item.get("page")) for item in relevant_successor_pages]
                                source_types = []
                                if pdf_context.strip():
                                    source_types.append("Uploaded PDF")
                                if interview_context.strip():
                                    source_types.append("Outgoing-staff interview notes")
                                connection = get_connection()
                                connection.execute("""
                                    INSERT INTO successor_questions
                                    (workspace_id, successor_name, question, answer, source_pages, source_types, created_at)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                """, (
                                    workspace_id_for_successor, successor_display_name,
                                    successor_question.strip(), successor_answer,
                                    ", ".join(page_numbers), ", ".join(source_types),
                                    datetime.now().isoformat()
                                ))
                                connection.commit()
                                connection.close()
                                st.session_state["successor_last_answer"] = successor_answer
                                st.session_state["successor_last_question"] = successor_question.strip()
                                st.session_state["successor_last_pages"] = page_numbers
                                st.session_state["successor_last_source_types"] = source_types
                                st.success("Your question and answer have been saved to this workspace.")
                except Exception as error:
                    st.error("The successor assistant could not generate an answer.")
                    st.caption(f"Technical details: {error}")

    if st.session_state.get("successor_last_answer"):
        st.subheader("Latest Answer")
        st.markdown(st.session_state["successor_last_answer"])
        latest_pages = st.session_state.get("successor_last_pages", [])
        if latest_pages:
            st.caption("PDF pages supplied to Gemini: " + ", ".join(latest_pages))
        latest_types = st.session_state.get("successor_last_source_types", [])
        if latest_types:
            st.caption("Knowledge sources: " + "; ".join(latest_types))

    connection = get_connection()
    saved_successor_qa = connection.execute("""
        SELECT question, answer, source_pages, source_types, created_at
        FROM successor_questions WHERE workspace_id = ?
        ORDER BY id DESC LIMIT 10
    """, (workspace_id_for_successor,)).fetchall()
    connection.close()
    st.subheader("Successor Learning History")
    if saved_successor_qa:
        for index, (saved_question, saved_answer, source_pages, source_types, created_at) in enumerate(saved_successor_qa, start=1):
            with st.expander(f"{index}. {saved_question}"):
                st.markdown(saved_answer or "No answer saved.")
                st.caption(f"Sources: {source_types or 'Not recorded'} | PDF pages: {source_pages or 'None recorded'}")
                st.caption(f"Asked: {created_at or 'Unknown'}")
    else:
        st.info("No successor questions have been saved yet. Ask the first project question above.")

