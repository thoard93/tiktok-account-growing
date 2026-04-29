"""
JesusAI Growth Dashboard
========================
Streamlit dashboard for the JesusAI TikTok account-growth pipeline.
TAP method scheduler + Nano Banana Pro 2K + Kling 2.6 video generation.
"""

import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# ===========================
# Configuration
# ===========================

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

st.set_page_config(
    page_title="JesusAI Growth",
    page_icon="🙏",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ===========================
# JesusAI theme — deep navy + gold halo accent
# ===========================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&display=swap');

    :root {
        --jas-bg-deep: #0a0a1a;
        --jas-bg-card: #14142b;
        --jas-bg-card-hi: #1c1c3a;
        --jas-gold: #d4a64a;
        --jas-gold-hi: #f0c674;
        --jas-gold-soft: rgba(212, 166, 74, 0.15);
        --jas-text: #f3f0e8;
        --jas-text-dim: #a8a4b8;
        --jas-text-muted: #6f6c80;
    }

    .stApp {
        font-family: 'Inter', sans-serif;
        background: radial-gradient(ellipse at top, #15152e 0%, var(--jas-bg-deep) 60%) !important;
        color: var(--jas-text);
    }

    /* Sidebar — deep purple/navy with gold accents */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a1a 0%, #1a1330 100%);
        border-right: 1px solid var(--jas-gold-soft);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: var(--jas-gold-hi) !important;
        font-family: 'Cinzel', serif;
        letter-spacing: 1.5px;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown span,
    [data-testid="stSidebar"] .stMarkdown div {
        color: var(--jas-text) !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: var(--jas-text) !important;
        font-size: 1.02rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio label div {
        color: var(--jas-text) !important;
    }
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
        background: var(--jas-gold-soft);
        border-radius: 10px;
    }
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stMarkdown small {
        color: var(--jas-text-dim) !important;
    }

    /* Headings — Cinzel for the brand feel */
    h1, h2 { font-family: 'Cinzel', serif; letter-spacing: 1px; color: var(--jas-gold-hi); }
    h3, h4 { color: var(--jas-text); }

    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--jas-bg-card) 0%, var(--jas-bg-card-hi) 100%);
        border: 1px solid var(--jas-gold-soft);
        border-radius: 18px;
        padding: 20px 24px;
        margin-bottom: 14px;
        box-shadow: 0 1px 0 rgba(255,255,255,0.03) inset, 0 8px 24px rgba(0,0,0,0.25);
    }
    .metric-card h3 {
        color: var(--jas-text-dim);
        font-size: 0.78rem;
        font-weight: 600;
        margin: 0 0 8px 0;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-family: 'Inter', sans-serif;
    }
    .metric-card .value {
        color: var(--jas-gold-hi);
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.1;
        font-family: 'Cinzel', serif;
    }
    .metric-card .sub {
        color: var(--jas-text-muted);
        font-size: 0.78rem;
        margin-top: 6px;
    }

    /* Status badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-green { background: rgba(76, 175, 80, 0.18); color: #7fd684; }
    .badge-yellow { background: var(--jas-gold-soft); color: var(--jas-gold-hi); }
    .badge-red { background: rgba(244, 67, 54, 0.18); color: #ff7872; }
    .badge-blue { background: rgba(120, 150, 220, 0.18); color: #9ab2dc; }
    .badge-gray { background: rgba(158, 158, 158, 0.15); color: var(--jas-text-dim); }

    /* Log entry */
    .log-entry {
        display: flex;
        align-items: center;
        padding: 11px 16px;
        border-radius: 12px;
        margin-bottom: 6px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(212, 166, 74, 0.06);
        transition: background 0.15s ease;
    }
    .log-entry:hover {
        background: var(--jas-gold-soft);
    }

    /* Buttons — gold accent */
    .stButton > button {
        border-radius: 12px !important;
        border: 1px solid var(--jas-gold-soft) !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        border-color: var(--jas-gold) !important;
        box-shadow: 0 0 0 3px var(--jas-gold-soft);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--jas-gold) 0%, var(--jas-gold-hi) 100%) !important;
        color: #1a1330 !important;
        border: none !important;
    }
    .stButton > button[kind="primary"]:hover {
        filter: brightness(1.1);
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox > div > div {
        background: var(--jas-bg-card) !important;
        border-color: var(--jas-gold-soft) !important;
        color: var(--jas-text) !important;
    }

    /* Hide streamlit chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid var(--jas-gold-soft);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        font-weight: 600;
        color: var(--jas-text-dim) !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--jas-gold-hi) !important;
        border-bottom: 2px solid var(--jas-gold) !important;
    }

    /* Section header */
    .section-header {
        color: var(--jas-gold-hi);
        font-size: 1.3rem;
        font-weight: 700;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--jas-gold-soft);
        font-family: 'Cinzel', serif;
        letter-spacing: 1px;
    }

    /* Brand banner in sidebar */
    .jas-brand {
        background: linear-gradient(135deg, var(--jas-gold) 0%, var(--jas-gold-hi) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Cinzel', serif;
        font-weight: 800;
        font-size: 1.6rem;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)


# ===========================
# API Helpers (with response caching)
# ===========================
#
# Streamlit re-runs the whole script top-to-bottom on every interaction
# (tab switch, button click, input change). Without caching, a single
# tab switch on the Dashboard page fires 4 sequential API calls. With
# @st.cache_data(ttl=10), repeated switches reuse the response for 10s
# and feel instant. Mutations (POST/DELETE) clear the cache so the next
# read sees the fresh state.

@st.cache_resource
def _api_session():
    """Single requests.Session reused across calls — keeps TCP connection alive."""
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    return s


class _ApiError(Exception):
    """Internal — raised on failed api_get so cache_data doesn't memoize None."""


@st.cache_data(ttl=10, show_spinner=False)
def _api_get_cached(endpoint):
    """Cached fetch. Raises on failure so the bad response isn't memoized."""
    resp = _api_session().get(f"{API_BASE_URL}{endpoint}", timeout=15)
    if resp.status_code == 200:
        return resp.json()
    raise _ApiError(f"{resp.status_code}: {resp.text[:120]}")


def api_get(endpoint):
    """Public wrapper. Returns None on failure but does NOT cache the failure,
    so a 1s API blip doesn't pin "no data" in the dashboard for 10s."""
    try:
        return _api_get_cached(endpoint)
    except (_ApiError, Exception):
        return None


def _invalidate_cache():
    """Drop the api_get response cache after a mutation."""
    try:
        _api_get_cached.clear()
    except Exception:
        pass


def api_post(endpoint, data=None):
    try:
        resp = _api_session().post(f"{API_BASE_URL}{endpoint}", json=data or {}, timeout=30)
        if resp.status_code == 200:
            _invalidate_cache()
            return resp.json()
        return None
    except Exception:
        return None


def api_delete(endpoint):
    try:
        resp = _api_session().delete(f"{API_BASE_URL}{endpoint}", timeout=10)
        if resp.status_code == 200:
            _invalidate_cache()
            return resp.json()
        return None
    except Exception:
        return None


def status_badge(status):
    color_map = {
        "completed": "green", "success": "green", "active": "green",
        "started": "yellow", "running": "yellow", "warming_up": "yellow",
        "failed": "red", "error": "red", "banned": "red",
        "skipped": "gray", "created": "blue", "paused": "gray", "posting": "blue",
    }
    color = color_map.get(status, "gray")
    return f'<span class="badge badge-{color}">{status}</span>'


def format_time_ago(iso_str):
    if not iso_str:
        return "Never"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        diff = datetime.utcnow() - dt.replace(tzinfo=None)
        if diff.total_seconds() < 60:
            return "Just now"
        elif diff.total_seconds() < 3600:
            return f"{int(diff.total_seconds() / 60)}m ago"
        elif diff.total_seconds() < 86400:
            return f"{int(diff.total_seconds() / 3600)}h ago"
        else:
            return f"{int(diff.total_seconds() / 86400)}d ago"
    except Exception:
        return str(iso_str)[:16]


# ===========================
# Sidebar Navigation
# ===========================

st.sidebar.markdown("<div class='jas-brand'>🙏 JESUSAI</div>", unsafe_allow_html=True)
st.sidebar.caption("TAP-method TikTok account growth")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "⚡ Pipeline", "👤 Accounts", "🎬 Videos", "🎵 Sounds", "📱 Phones"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh data", use_container_width=True, help="Drop cached API responses"):
    _invalidate_cache()
    st.rerun()

st.sidebar.markdown(
    f"<small style='color: #a8a4b8;'>v3.0 · TAP method · <a href='{API_BASE_URL.replace('/api', '')}' "
    f"style='color: #d4a64a;'>API</a></small>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<small style='color: #6f6c80;'>Jesus vs Devil · Nano Banana Pro 2K + Kling 2.6</small>",
    unsafe_allow_html=True,
)


# ===========================
# PAGE: Dashboard
# ===========================

if page == "📊 Dashboard":
    st.markdown("## 📊 Dashboard")
    st.caption("System overview and pipeline health")
    
    pipeline_status = api_get("/pipeline/status")
    health = api_get("/health")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        scheduled = pipeline_status.get("scheduled_accounts", {}).get("total", 0) if pipeline_status else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>📱 Scheduled Accounts</h3>
            <div class="value">{scheduled}</div>
            <div class="sub">Active in pipeline</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        enabled = pipeline_status.get("pipeline_enabled", False) if pipeline_status else False
        status_text = "ACTIVE" if enabled else "DISABLED"
        status_color = "#66bb6a" if enabled else "#ef5350"
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ Pipeline</h3>
            <div class="value" style="color: {status_color}">{status_text}</div>
            <div class="sub">Master switch</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        warmup_ct = pipeline_status.get("scheduled_accounts", {}).get("warmup", 0) if pipeline_status else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>🔥 Warmup</h3>
            <div class="value">{warmup_ct}</div>
            <div class="sub">Accounts warming</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        posting_ct = pipeline_status.get("scheduled_accounts", {}).get("posting", 0) if pipeline_status else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>📤 Posting</h3>
            <div class="value">{posting_ct}</div>
            <div class="sub">Accounts posting</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Today's Pipeline Status
    st.markdown("### ⏱️ Today's Pipeline")
    
    if pipeline_status:
        today = pipeline_status.get("today", {})
        config = pipeline_status.get("config", {})
        
        phases = [
            ("🔥", "Warmup", "warmup", f"{config.get('warmup_hour_est', 8)}:00 AM EST"),
            ("🎬", "Video Generation", "video_gen", f"{config.get('video_gen_hour_est', 9)}:00 AM EST"),
            ("📤", "Posting", "posting", f"{config.get('posting_hours_est', '10,13,17')} EST"),
        ]
        
        cols = st.columns(3)
        for i, (icon, name, key, schedule_time) in enumerate(phases):
            with cols[i]:
                phase_data = today.get(key, {})
                phase_status = phase_data.get("status", "pending")
                
                if phase_status == "completed":
                    color = "#66bb6a"
                    bg = "rgba(76, 175, 80, 0.1)"
                elif phase_status == "started":
                    color = "#ffd54f"
                    bg = "rgba(255, 193, 7, 0.1)"
                elif phase_status == "failed":
                    color = "#ef5350"
                    bg = "rgba(244, 67, 54, 0.1)"
                else:
                    color = "#8080b0"
                    bg = "rgba(128, 128, 176, 0.05)"
                
                st.markdown(f"""
                <div style="background: {bg}; border: 1px solid {color}30; border-radius: 14px; padding: 20px; text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
                    <div style="color: #e0e0ff; font-weight: 600; font-size: 1rem;">{name}</div>
                    <div style="color: {color}; font-weight: 700; font-size: 0.85rem; margin-top: 6px; text-transform: uppercase;">{phase_status}</div>
                    <div style="color: #8080b0; font-size: 0.75rem; margin-top: 4px;">📅 {schedule_time}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("### 📋 Recent Activity")
    
    logs_data = api_get("/pipeline/logs?days=3")
    if logs_data and logs_data.get("logs"):
        logs = logs_data["logs"][:15]
        
        for log in logs:
            phase_icons = {"warmup": "🔥", "video_gen": "🎬", "posting": "📤"}
            icon = phase_icons.get(log["phase"], "📝")
            phase_name = log["phase"].replace("_", " ").title()
            badge = status_badge(log["status"])
            account = log.get("account_name") or ""
            time_str = format_time_ago(log.get("started_at"))
            duration = f" · {log['duration_seconds']:.0f}s" if log.get("duration_seconds") else ""
            error = f" — {log['error'][:60]}" if log.get("error") else ""
            
            st.markdown(f"""
            <div class="log-entry">
                <span style="font-size: 1.3rem; margin-right: 12px;">{icon}</span>
                <span style="color: #e0e0ff; font-weight: 500; min-width: 140px;">{phase_name}</span>
                {badge}
                <span style="color: #a0a0c0; margin-left: 12px; flex: 1;">{account}{error}</span>
                <span style="color: #8080b0; font-size: 0.8rem;">{time_str}{duration}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No pipeline activity yet. Enable the pipeline and schedule some accounts to get started!")
    
    # Health
    st.markdown("### 🏥 System Health")
    if health:
        col1, col2 = st.columns(2)
        with col1:
            gl = "✅ Connected" if health.get("geelark_connected") else "❌ Disconnected"
            st.markdown(f"**Phone Provider:** {gl}")
            st.markdown("**Database:** ✅ Connected")
        with col2:
            st.markdown("**Scheduler:** ✅ Active")
            st.markdown("**Version:** v2.0.0")
    else:
        st.error("Cannot reach API backend")
    
    # ===========================
    # Follower Growth Chart
    # ===========================
    
    st.markdown("---")
    st.markdown("### 📈 Follower Growth")
    
    chart_col1, chart_col2 = st.columns([3, 1])
    with chart_col2:
        days_range = st.selectbox("Date Range", [7, 14, 30, 60], index=2, format_func=lambda x: f"Last {x} days")
        if st.button("📸 Take Snapshot Now", use_container_width=True):
            snap_result = api_post("/followers/snapshot")
            if snap_result and snap_result.get("success"):
                st.success(f"Snapshot taken! {snap_result.get('accounts_tracked', 0)} accounts tracked")
                st.rerun()
            else:
                st.error("Snapshot failed")
    
    with chart_col1:
        history = api_get(f"/followers/history?days={days_range}")
        if history and history.get("accounts"):
            accounts_data = history["accounts"]
            
            # Build DataFrame for chart
            chart_data = {}
            for acct_name, snapshots in accounts_data.items():
                for snap in snapshots:
                    date = snap["date"]
                    if date not in chart_data:
                        chart_data[date] = {}
                    chart_data[date][acct_name] = snap["followers"]
            
            if chart_data:
                df = pd.DataFrame.from_dict(chart_data, orient="index")
                df.index = pd.to_datetime(df.index)
                df = df.sort_index()
                
                st.line_chart(df, use_container_width=True)
                
                # Current stats table
                st.markdown("**Current Follower Counts:**")
                stats_cols = st.columns(min(len(accounts_data), 4))
                for i, (name, snaps) in enumerate(accounts_data.items()):
                    with stats_cols[i % len(stats_cols)]:
                        latest = snaps[-1] if snaps else {}
                        followers = latest.get("followers", 0)
                        
                        # Total growth over selected range
                        if len(snaps) >= 2:
                            total_growth = followers - snaps[0]["followers"]
                            total_str = f"+{total_growth}" if total_growth >= 0 else str(total_growth)
                            total_color = "#66bb6a" if total_growth >= 0 else "#ef5350"
                            
                            # Avg per day
                            num_days = max(len(snaps) - 1, 1)
                            avg_per_day = total_growth / num_days
                            avg_str = f"+{avg_per_day:.1f}" if avg_per_day >= 0 else f"{avg_per_day:.1f}"
                            
                            # Last 7 days growth
                            week_snaps = [s for s in snaps if s["date"] >= str(pd.Timestamp.now().date() - pd.Timedelta(days=7))]
                            if len(week_snaps) >= 2:
                                week_growth = week_snaps[-1]["followers"] - week_snaps[0]["followers"]
                                week_str = f"+{week_growth}" if week_growth >= 0 else str(week_growth)
                                week_color = "#66bb6a" if week_growth >= 0 else "#ef5350"
                            else:
                                week_str = "—"
                                week_color = "#8080b0"
                        else:
                            total_str = "—"
                            total_color = "#8080b0"
                            avg_str = "—"
                            week_str = "—"
                            week_color = "#8080b0"
                        
                        st.markdown(f"""
                        <div class="metric-card" style="padding: 14px;">
                            <div style="color: #a0a0d0; font-size: 0.8rem;">{name}</div>
                            <div style="color: #e0e0ff; font-size: 1.5rem; font-weight: 700;">{followers}</div>
                            <div style="display: flex; justify-content: space-between; margin-top: 6px;">
                                <div>
                                    <div style="color: #8080b0; font-size: 0.65rem;">7-DAY</div>
                                    <div style="color: {week_color}; font-size: 0.85rem; font-weight: 600;">{week_str}</div>
                                </div>
                                <div>
                                    <div style="color: #8080b0; font-size: 0.65rem;">AVG/DAY</div>
                                    <div style="color: {total_color}; font-size: 0.85rem; font-weight: 600;">{avg_str}</div>
                                </div>
                                <div>
                                    <div style="color: #8080b0; font-size: 0.65rem;">{days_range}D TOTAL</div>
                                    <div style="color: {total_color}; font-size: 0.85rem; font-weight: 600;">{total_str}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No follower data yet. Click 'Take Snapshot Now' to start tracking!")
        else:
            st.info("No follower data yet. Click 'Take Snapshot Now' to start tracking! Snapshots are auto-taken daily at 11 PM EST.")


# ===========================
# PAGE: Pipeline
# ===========================

elif page == "⚡ Pipeline":
    st.markdown("## ⚡ Pipeline Control")
    st.caption("Configure and monitor the automated daily pipeline")
    
    config_resp = api_get("/schedule/config")
    
    # Master toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Master Pipeline Switch")
        st.caption("When enabled, the pipeline runs automatically every day at the configured times.")
    with col2:
        current_enabled = config_resp.get("enabled", False) if config_resp else False
        new_enabled = st.toggle("Pipeline Active", value=current_enabled, key="pipeline_toggle")
        if new_enabled != current_enabled:
            result = api_post("/schedule/config", {"enabled": new_enabled})
            if result and result.get("success"):
                st.success("Pipeline " + ("ENABLED" if new_enabled else "DISABLED"))
                st.rerun()
    
    st.markdown("---")
    
    # Schedule Config
    st.markdown("### ⏰ Schedule Settings (EST)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        warmup_hour = st.number_input(
            "Warmup Hour (EST)", min_value=1, max_value=23,
            value=config_resp.get("warmup_hour_est", 8) if config_resp else 8
        )
    with col2:
        vidgen_hour = st.number_input(
            "Video Gen Hour (EST)", min_value=1, max_value=23,
            value=config_resp.get("video_gen_hour_est", 9) if config_resp else 9
        )
    with col3:
        posting_hours = st.text_input(
            "Posting Hours (EST)",
            value=config_resp.get("posting_hours_est", "10,13,17") if config_resp else "10,13,17"
        )
    with col4:
        posts_per = st.number_input(
            "Posts per Account", min_value=1, max_value=10,
            value=config_resp.get("posts_per_phone", 3) if config_resp else 3
        )
    
    if st.button("💾 Save Schedule", use_container_width=True):
        result = api_post("/schedule/config", {
            "warmup_hour_est": warmup_hour,
            "video_gen_hour_est": vidgen_hour,
            "posting_hours_est": posting_hours,
            "posts_per_phone": posts_per,
        })
        if result and result.get("success"):
            st.success("Schedule saved!")
            st.rerun()
        else:
            st.error("Failed to save schedule")
    
    st.markdown("---")
    
    # Manual triggers
    st.markdown("### 🎮 Manual Triggers")
    st.caption("Trigger pipeline phases immediately (respects account scheduling)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔥 Run Warmup Now", use_container_width=True, type="primary"):
            result = api_post("/pipeline/trigger/warmup")
            if result:
                st.success("Warmup triggered!")
            else:
                st.error("Failed to trigger warmup")
    with col2:
        if st.button("🎬 Generate Videos Now", use_container_width=True, type="primary"):
            result = api_post("/pipeline/trigger/video_gen")
            if result:
                st.success("Video generation triggered!")
            else:
                st.error("Failed to trigger video gen")
    with col3:
        if st.button("📤 Post Videos Now", use_container_width=True, type="primary"):
            result = api_post("/pipeline/trigger/posting")
            if result:
                st.success("Posting triggered!")
            else:
                st.error("Failed to trigger posting")
    
    st.markdown("---")
    
    # Pipeline Logs
    st.markdown("### 📋 Pipeline Activity Log")
    
    log_col1, log_col2 = st.columns(2)
    with log_col1:
        log_days = st.selectbox("Show logs from", [1, 3, 7, 14], index=1,
                                format_func=lambda x: f"Last {x} day{'s' if x > 1 else ''}")
    with log_col2:
        phase_filter = st.selectbox("Filter by phase", ["All", "warmup", "video_gen", "posting"])
    
    endpoint = f"/pipeline/logs?days={log_days}"
    if phase_filter != "All":
        endpoint += f"&phase={phase_filter}"
    
    logs_data = api_get(endpoint)
    
    if logs_data and logs_data.get("logs"):
        df_data = []
        for log in logs_data["logs"]:
            phase_icons = {"warmup": "🔥", "video_gen": "🎬", "posting": "📤"}
            df_data.append({
                "Phase": f"{phase_icons.get(log['phase'], '📝')} {log['phase'].replace('_', ' ').title()}",
                "Status": log["status"].upper(),
                "Account": log.get("account_name") or "—",
                "Duration": f"{log['duration_seconds']:.0f}s" if log.get("duration_seconds") else "—",
                "Error": (log.get("error") or "")[:50],
                "Time": format_time_ago(log.get("started_at")),
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(logs_data['logs'])} entries")
    else:
        st.info("No pipeline logs yet.")


# ===========================
# PAGE: Accounts
# ===========================

elif page == "👤 Accounts":
    st.markdown("## 👤 Account Management")
    st.caption("Manage accounts and their scheduling status")
    
    tab1, tab2, tab3 = st.tabs(["📋 Account List", "➕ Add Account", "🔐 Credentials"])
    
    with tab1:
        st.markdown("### Scheduled Accounts")
        st.caption("Toggle scheduling on/off for each account. Accounts are synced from cloud phones.")
        
        # Sync button — pulls phones into Account table
        col_sync1, col_sync2, col_sync3 = st.columns([2, 1, 1])
        with col_sync2:
            if st.button("🔄 Sync from Phones", use_container_width=True, type="primary"):
                with st.spinner("Syncing phones..."):
                    result = api_post("/accounts/sync-geelark")
                    if result and result.get("success"):
                        created = result.get("created", 0)
                        found = result.get("phones_found", 0)
                        total = result.get("total_accounts", 0)
                        st.success(f"Synced! Found {found} phones, created {created} new accounts. {total} total.")
                        st.rerun()
                    else:
                        st.error("Failed to sync phones")
        with col_sync3:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state["confirm_clear"] = True
        
        if st.session_state.get("confirm_clear"):
            st.warning("⚠️ This will delete ALL accounts and activity logs. Are you sure?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Yes, clear everything", type="primary"):
                    result = api_post("/accounts/clear")
                    if result and result.get("success"):
                        st.success(f"Cleared {result.get('deleted', 0)} accounts")
                        st.session_state["confirm_clear"] = False
                        st.rerun()
                    else:
                        st.error("Failed to clear accounts")
            with c2:
                if st.button("❌ Cancel"):
                    st.session_state["confirm_clear"] = False
                    st.rerun()
        
        # Fetch accounts
        accounts_data = api_get("/accounts/scheduled")
        
        if accounts_data and accounts_data.get("accounts"):
            accounts = accounts_data["accounts"]
            
            # Summary + bulk actions
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                scheduled_ct = sum(1 for a in accounts if a.get("schedule_enabled"))
                st.markdown(f"**{len(accounts)} accounts** · **{scheduled_ct} scheduled**")
            with col2:
                if st.button("✅ Schedule All"):
                    all_ids = [a["id"] for a in accounts]
                    api_post("/accounts/schedule/bulk", {"account_ids": all_ids, "enabled": True})
                    st.rerun()
            with col3:
                if st.button("❌ Unschedule All"):
                    all_ids = [a["id"] for a in accounts]
                    api_post("/accounts/schedule/bulk", {"account_ids": all_ids, "enabled": False})
                    st.rerun()
            
            st.markdown("---")
            
            # Column headers
            hdr = st.columns([3, 2, 2, 1, 1, 1, 1])
            with hdr[0]:
                st.caption("**NAME**")
            with hdr[1]:
                st.caption("**TT USERNAME**")
            with hdr[2]:
                st.caption("**PHONE ID**")
            with hdr[3]:
                st.caption("**STATUS**")
            with hdr[4]:
                st.caption("**SCHEDULED**")
            with hdr[5]:
                st.caption("**WARMUP**")
            with hdr[6]:
                st.caption("**POSTING**")
            
            # Account rows
            for account in accounts:
                cols = st.columns([3, 2, 2, 1, 1, 1, 1])
                
                with cols[0]:
                    name = account.get("name", "Unknown")
                    st.markdown(f"**{name}**")
                
                with cols[1]:
                    current_un = account.get("tiktok_username", "") or ""
                    new_un = st.text_input(
                        "TT", value=current_un,
                        key=f"tt_un_{account['id']}",
                        label_visibility="collapsed",
                        placeholder="@username"
                    )
                    if new_un != current_un:
                        api_post(f"/accounts/{account['id']}/schedule", {"tiktok_username": new_un})
                        st.rerun()
                
                with cols[2]:
                    pid = account.get("phone_id", "")
                    st.caption(f"📱 {pid[:15]}..." if len(pid) > 15 else f"📱 {pid}" if pid else "No phone")
                
                with cols[3]:
                    status = account.get("status", "unknown")
                    st.markdown(status_badge(status), unsafe_allow_html=True)
                
                with cols[4]:
                    is_sched = account.get("schedule_enabled", False)
                    new_sched = st.checkbox(
                        "On", value=is_sched,
                        key=f"sched_{account['id']}",
                        label_visibility="collapsed"
                    )
                    if new_sched != is_sched:
                        api_post(f"/accounts/{account['id']}/schedule", {"enabled": new_sched})
                        st.rerun()
                
                with cols[5]:
                    if account.get("schedule_enabled"):
                        w_val = account.get("schedule_warmup", True)
                        new_w = st.checkbox(
                            "W", value=w_val,
                            key=f"warmup_{account['id']}",
                            label_visibility="collapsed"
                        )
                        if new_w != w_val:
                            api_post(f"/accounts/{account['id']}/schedule", {"warmup": new_w})
                            st.rerun()
                    else:
                        st.write("—")
                
                with cols[6]:
                    if account.get("schedule_enabled"):
                        p_val = account.get("schedule_posting", True)
                        new_p = st.checkbox(
                            "P", value=p_val,
                            key=f"posting_{account['id']}",
                            label_visibility="collapsed"
                        )
                        if new_p != p_val:
                            api_post(f"/accounts/{account['id']}/schedule", {"posting": new_p})
                            st.rerun()
                    else:
                        st.write("—")
        
        else:
            st.warning("No accounts in database yet. Click **🔄 Sync from Phones** above to import your cloud phones as accounts.")
    
    with tab2:
        st.markdown("### ➕ Add New Account")
        
        # Quick bulk import for MultiLogin phones
        st.markdown("#### 📱 Quick Import from MultiLogin")
        st.caption("Paste your phone profile IDs from MultiLogin desktop app (one per line: `name,profile_id`)")
        
        bulk_input = st.text_area(
            "Phones (name,profile_id per line)",
            placeholder="test3,60808076967123628\ntester2,60807983892132892\ntester,60807725947499324",
            height=120
        )
        
        if st.button("🚀 Import Phones", type="primary", use_container_width=True):
            if bulk_input.strip():
                phones = []
                for line in bulk_input.strip().split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 2:
                        phones.append({"name": parts[0], "profile_id": parts[1]})
                    elif len(parts) == 1 and parts[0]:
                        phones.append({"name": f"Phone {parts[0][:8]}", "profile_id": parts[0]})
                
                if phones:
                    result = api_post("/accounts/import", {"phones": phones})
                    if result and result.get("success"):
                        created = result.get("created", 0)
                        skipped = result.get("skipped", 0)
                        st.success(f"✅ Imported {created} phone(s)! ({skipped} duplicates skipped)")
                        st.rerun()
                    else:
                        st.error("Import failed — check server logs")
                else:
                    st.error("No valid entries found. Use format: name,profile_id")
            else:
                st.warning("Please paste phone data first")
        
        st.markdown("---")
        st.markdown("#### ✏️ Manual Entry")
        
        with st.form("create_account"):
            col1, col2 = st.columns(2)
            with col1:
                acct_name = st.text_input("Account Name", placeholder="e.g. TikTok_Account_01")
                acct_email = st.text_input("Email", placeholder="optional")
                acct_password = st.text_input("Password", type="password", placeholder="optional")
            with col2:
                acct_phone = st.text_input("Phone Number", placeholder="optional")
                acct_phone_id = st.text_input("Phone ID", placeholder="From MultiLogin/GeeLark dashboard")
                auto_schedule = st.checkbox("Auto-schedule for pipeline", value=True)
            
            if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
                if acct_name:
                    # Use import endpoint for reliable account creation
                    result = api_post("/accounts/import", {
                        "phones": [{
                            "name": acct_name,
                            "profile_id": acct_phone_id or f"manual-{acct_name}"
                        }]
                    })
                    if result and result.get("success"):
                        st.success(f"Account '{acct_name}' created!")
                        st.rerun()
                    else:
                        st.error("Failed to create account")
                else:
                    st.warning("Please enter an account name")
    
    with tab3:
        st.markdown("### 🔐 Stored Credentials")
        creds = api_get("/credentials")
        if creds and creds.get("credentials"):
            cred_data = []
            for c in creds["credentials"]:
                cred_data.append({
                    "Account": c.get("account_name", "Unknown"),
                    "Username": c.get("tiktok_username", "—"),
                    "Email": c.get("email", "—"),
                    "Created": c.get("created_at", "—")[:10] if c.get("created_at") else "—",
                })
            df = pd.DataFrame(cred_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No credentials stored yet.")


# ===========================
# PAGE: Videos
# ===========================

elif page == "🎬 Videos":
    st.markdown("## 🎬 Video Management")
    st.caption("Generate AI videos and manage your video library")
    
    tab1, tab2, tab3 = st.tabs(["🤖 AI Generate", "📚 Video Library", "📤 Post to TikTok"])
    
    with tab1:
        st.markdown("### 🤖 Generate JesusAI Videos")
        st.caption("Jesus vs Devil competitions · Nano Banana Pro 2K → Kling 2.6 · ~$0.22/video")

        competitions = [
            "Random",
            "Arm Wrestling", "Tug of War", "Chess", "Jogging",
            "Swimming", "Running", "Cycling", "Kayak Racing",
            "Horseback Riding", "Rock Climbing",
        ]

        with st.form("generate_video"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                video_count = st.number_input("Videos", min_value=1, max_value=20, value=3)
            with col2:
                competition = st.selectbox("Competition", competitions)
            with col3:
                mode = st.selectbox("Mode", ["realistic", "cartoon"])
            with col4:
                skip_overlay = st.checkbox("Skip overlay", value=False)

            if st.form_submit_button("✨ Generate", use_container_width=True, type="primary"):
                payload = {
                    "count": video_count,
                    "mode": mode,
                    "skip_overlay": skip_overlay,
                }
                if competition != "Random":
                    payload["competition"] = competition
                endpoint = "/videos/batch" if video_count > 1 else "/videos/generate"
                with st.spinner(f"Queuing {video_count} JesusAI video(s)..."):
                    result = api_post(endpoint, payload)
                    if result and result.get("job_id"):
                        st.success(f"Generation started — Job ID: `{result['job_id']}`")
                    else:
                        st.error("Failed to start video generation")
    
    with tab2:
        st.markdown("### 📚 Video Library")
        
        videos = api_get("/videos/list")
        if videos and videos.get("videos"):
            st.markdown(f"**{len(videos['videos'])} videos available**")
            for v in videos["videos"]:
                fname = v.get('filename', 'Unknown')
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                with col1:
                    st.markdown(f"🎬 **{fname}**")
                with col2:
                    size = v.get('size_mb', 0)
                    st.caption(f"{size:.1f} MB" if size else "—")
                with col3:
                    st.caption(v.get('created', v.get('created_at', '—'))[:16])
                with col4:
                    if st.button("▶️", key=f"preview_{fname}", help="Preview video"):
                        st.session_state[f"show_preview_{fname}"] = not st.session_state.get(f"show_preview_{fname}", False)
                with col5:
                    if st.button("🗑️", key=f"del_{fname}"):
                        api_delete(f"/videos/{fname}")
                        st.rerun()
                
                # Show video preview if toggled
                if st.session_state.get(f"show_preview_{fname}", False):
                    preview_url = f"{API_BASE_URL}/videos/download/{fname}"
                    st.video(preview_url)
        else:
            st.info("No videos in library. Generate some using the AI Generate tab!")
    
    with tab3:
        st.markdown("### 📤 Post Videos to TikTok")
        
        phones = api_get("/geelark/phones")
        videos = api_get("/videos/list")
        
        if phones and phones.get("items") and videos and videos.get("videos"):
            phone_options = {f"{p['serialName']} ({p['id'][:8]}...)": p['id'] for p in phones['items']}
            video_options = [v['filename'] for v in videos['videos']]
            
            with st.form("post_videos"):
                selected_phones = st.multiselect("Select Phones", options=list(phone_options.keys()))
                selected_videos = st.multiselect("Select Videos", options=video_options)
                
                col1, col2 = st.columns(2)
                with col1:
                    caption = st.text_input("Caption", value="")
                    hashtags = st.text_input(
                        "Hashtags",
                        value="#jesus #jesussaves #jesuslovesyou #fyp #foryou #christian",
                    )
                with col2:
                    auto_start = st.checkbox("Auto-start phones", value=True)
                    auto_stop = st.checkbox("Auto-stop phones after", value=True)
                    auto_delete = st.checkbox("Delete video after posting", value=True)
                
                if st.form_submit_button("📤 Post Now", use_container_width=True, type="primary"):
                    if selected_phones and selected_videos:
                        phone_ids = [phone_options[p] for p in selected_phones]
                        result = api_post("/videos/post/batch", {
                            "videos": selected_videos,
                            "phone_ids": phone_ids,
                            "caption": caption,
                            "hashtags": hashtags,
                            "auto_start": auto_start,
                            "auto_stop": auto_stop,
                            "auto_delete": auto_delete,
                            "distribute_mode": "round_robin"
                        })
                        if result:
                            st.success(f"Posting started! Job ID: {result.get('job_id', 'unknown')}")
                        else:
                            st.error("Failed to start posting")
                    else:
                        st.warning("Select at least one phone and one video")
        else:
            if not phones or not phones.get("items"):
                st.warning("No phones available. Create phones in MultiLogin first.")
            if not videos or not videos.get("videos"):
                st.warning("No videos available. Generate videos first.")


# ===========================
# PAGE: Sounds
# ===========================

elif page == "🎵 Sounds":
    st.markdown("## 🎵 Sound Library")
    st.caption("Sounds attached randomly to JesusAI videos. Drop in your trending TikTok audio here.")

    upload_col, info_col = st.columns([2, 1])
    with upload_col:
        uploaded = st.file_uploader(
            "Upload sound (mp3 / wav / m4a / ogg)",
            type=["mp3", "wav", "m4a", "ogg"],
            accept_multiple_files=False,
        )
        if uploaded is not None:
            files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type or "audio/mpeg")}
            try:
                resp = requests.post(f"{API_BASE_URL}/sounds/upload", files=files, timeout=60)
                if resp.status_code == 200:
                    j = resp.json()
                    st.success(f"Uploaded `{j['filename']}` ({j['size_kb']} KB)")
                    st.rerun()
                else:
                    st.error(f"Upload failed: {resp.status_code} {resp.text[:200]}")
            except Exception as e:
                st.error(f"Upload error: {e}")

    with info_col:
        st.markdown(
            """
            <div class='metric-card' style='padding: 14px; font-size: 0.85rem;'>
              <div style='color: var(--jas-gold-hi); font-weight: 600; margin-bottom: 6px;'>How it works</div>
              <div style='color: var(--jas-text-dim);'>
                Each generated video gets a random sound from this library, muxed in by FFmpeg.
                Drop in trending TikTok audio for organic-feeling posts.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Library")

    sounds = api_get("/sounds/list")
    if sounds and sounds.get("sounds"):
        st.markdown(f"**{sounds['count']} sound(s) available**")
        for s in sounds["sounds"]:
            cols = st.columns([3, 2, 1, 1])
            with cols[0]:
                st.markdown(f"🎵 **{s['filename']}**")
                st.caption(s.get("path", ""))
            with cols[1]:
                st.caption(f"{s.get('size_kb', 0)} KB · modified {s.get('modified_at', '')[:16]}")
            with cols[2]:
                if st.button("▶️", key=f"play_{s['filename']}", help="Preview"):
                    st.session_state[f"sound_play_{s['filename']}"] = not st.session_state.get(
                        f"sound_play_{s['filename']}", False,
                    )
            with cols[3]:
                if st.button("🗑️", key=f"sound_del_{s['filename']}", help="Delete"):
                    api_delete(f"/sounds/{s['filename']}")
                    st.rerun()

            if st.session_state.get(f"sound_play_{s['filename']}", False):
                st.audio(f"{API_BASE_URL}/sounds/download/{s['filename']}")
    else:
        st.info("No sounds in library yet. Upload an mp3 above to get started.")


# ===========================
# PAGE: Phones
# ===========================

elif page == "📱 Phones":
    st.markdown("## 📱 Cloud Phones")
    st.caption("Direct cloud phone management")
    
    tab1, tab2, tab3 = st.tabs(["📱 Cloud Phones", "📋 Task History", "✨ Magic Setup"])
    
    with tab1:
        st.markdown("### Cloud Phones")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔄 Refresh Phone List"):
                st.rerun()
        with col2:
            if st.button("📥 Sync All to Accounts"):
                result = api_post("/accounts/sync-geelark")
                if result and result.get("success"):
                    st.success(f"Synced! {result.get('created', 0)} new accounts. Go to Accounts tab to schedule them.")
                else:
                    st.error("Failed to sync")
        
        phones = api_get("/geelark/phones")
        
        if phones and phones.get("items"):
            for phone in phones["items"]:
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
                
                with col1:
                    name = phone.get("serialName", "Unknown")
                    phone_id = phone.get("id", "")
                    st.markdown(f"**{name}**")
                    st.caption(f"ID: {phone_id[:20]}...")
                
                with col2:
                    status = phone.get("status", -1)
                    status_map = {0: "🟢 Running", 1: "🔴 Stopped", 2: "🟡 Starting"}
                    st.markdown(status_map.get(status, f"⚪ Unknown ({status})"))
                
                with col3:
                    if st.button("▶️", key=f"start_{phone_id}", help="Start"):
                        api_post("/geelark/phones/start", {"phone_ids": [phone_id]})
                        st.success("Starting...")
                        st.rerun()
                
                with col4:
                    if st.button("⏹️", key=f"stop_{phone_id}", help="Stop"):
                        api_post("/geelark/phones/stop", {"phone_ids": [phone_id]})
                        st.success("Stopping...")
                        st.rerun()
                
                with col5:
                    if st.button("🔥", key=f"warmup_{phone_id}", help="Warmup"):
                        api_post("/geelark/warmup/run", {
                            "phone_id": phone_id, "duration_minutes": 10,
                            "action": "browse video",
                            "keywords": ["jesus", "jesus saves", "christian"],
                        })
                        st.success("Warmup started!")
                
                st.markdown("---")
        else:
            st.info("No phones found.")
    
    with tab2:
        st.markdown("### Task History")
        task_ids_input = st.text_input("Query Task IDs (comma-separated)", placeholder="task-id-1, task-id-2")
        if task_ids_input and st.button("🔍 Query"):
            ids = [x.strip() for x in task_ids_input.split(",")]
            result = api_post("/geelark/tasks/query", {"task_ids": ids})
            if result:
                st.json(result)
    
    with tab3:
        st.markdown("### ✨ Magic Setup")
        st.caption("Create a new cloud phone, install TikTok, and prepare for automation")
        
        setup_tab1, setup_tab2 = st.tabs(["🔧 Single Setup", "🎯 Batch Setup"])
        
        with setup_tab1:
            with st.form("magic_setup"):
                proxy_string = st.text_input("Proxy String", placeholder="protocol://user:pass@host:port")
                name_prefix = st.text_input("Name Prefix", value="tiktok")
                auto_schedule = st.checkbox("Auto-add to pipeline schedule", value=True)
                
                if st.form_submit_button("✨ Launch Magic Setup", use_container_width=True, type="primary"):
                    if proxy_string:
                        result = api_post("/accounts/full-setup-async", {
                            "proxy_string": proxy_string,
                            "name_prefix": name_prefix,
                            "max_retries": 5
                        })
                        if result:
                            st.success(f"Magic Setup launched! Task ID: {result.get('task_id')}")
                    else:
                        st.warning("Enter a proxy string")
        
        with setup_tab2:
            st.markdown("**Paste multiple proxies (one per line) to create accounts in bulk.**")
            proxies_text = st.text_area("Proxies (one per line)", height=150)
            batch_prefix = st.text_input("Name Prefix", value="tiktok", key="batch_prefix")
            batch_enroll = st.checkbox("Auto-enroll in scheduler", value=True, key="batch_enroll")
            
            if st.button("🚀 Launch Batch Setup", use_container_width=True, type="primary"):
                if proxies_text.strip():
                    proxies = [p.strip() for p in proxies_text.strip().split("\n") if p.strip()]
                    result = api_post("/magic-setup/batch", {
                        "proxies": proxies, "name_prefix": batch_prefix, "auto_enroll": batch_enroll
                    })
                    if result:
                        st.success(f"Batch setup launched for {len(proxies)} proxies!")
                    else:
                        st.error("Failed to start batch setup")
                else:
                    st.warning("Enter at least one proxy")
