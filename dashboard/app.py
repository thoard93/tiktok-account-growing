"""
TikTok Automation Dashboard v2.0
================================
Streamlit dashboard with modern design, pipeline management, and account scheduling.
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
    page_title="TikTok Automation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===========================
# Custom CSS — Modern Dark Theme
# ===========================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { font-family: 'Inter', sans-serif; }
    
    /* Sidebar - bright text for readability */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown span,
    [data-testid="stSidebar"] .stMarkdown div {
        color: #e0e0ff !important;
    }
    
    /* Sidebar radio buttons - BRIGHT white text */
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] .stRadio label div {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
    }
    
    /* Sidebar caption text */
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] .stMarkdown small {
        color: #a0a0d0 !important;
    }
    
    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e1e3f 0%, #2a2a5a 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 12px;
    }
    .metric-card h3 {
        color: #a0a0c0;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0 0 8px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card .value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .metric-card .sub {
        color: #8080b0;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .badge-green { background: rgba(76, 175, 80, 0.2); color: #66bb6a; }
    .badge-yellow { background: rgba(255, 193, 7, 0.2); color: #ffd54f; }
    .badge-red { background: rgba(244, 67, 54, 0.2); color: #ef5350; }
    .badge-blue { background: rgba(33, 150, 243, 0.2); color: #42a5f5; }
    .badge-gray { background: rgba(158, 158, 158, 0.2); color: #bdbdbd; }
    
    /* Log entry */
    .log-entry {
        display: flex;
        align-items: center;
        padding: 10px 16px;
        border-radius: 10px;
        margin-bottom: 6px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Section header */
    .section-header {
        color: #e0e0ff;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(100, 100, 255, 0.2);
    }
    
    /* Hide streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; }
    .stTabs [data-baseweb="tab"] { border-radius: 10px 10px 0 0; font-weight: 500; }
</style>
""", unsafe_allow_html=True)


# ===========================
# API Helpers
# ===========================

def api_get(endpoint):
    try:
        resp = requests.get(f"{API_BASE_URL}{endpoint}", timeout=15)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None

def api_post(endpoint, data=None):
    try:
        resp = requests.post(f"{API_BASE_URL}{endpoint}", json=data or {}, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception:
        return None

def api_delete(endpoint):
    try:
        resp = requests.delete(f"{API_BASE_URL}{endpoint}", timeout=10)
        if resp.status_code == 200:
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

st.sidebar.markdown("# 🚀 TikTok Automation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "⚡ Pipeline", "👤 Accounts", "🎬 Videos", "⚙️ GeeLark"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<small style='color: #a0a0d0;'>v2.0.0 | <a href='{API_BASE_URL.replace('/api', '')}' style='color: #9090ff;'>API</a></small>", unsafe_allow_html=True)
st.sidebar.markdown("<small style='color: #8080b0;'>Built for automation 🤖</small>", unsafe_allow_html=True)


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
            st.markdown(f"**GeeLark API:** {gl}")
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
        st.caption("Toggle scheduling on/off for each account. Accounts are synced from GeeLark phones.")
        
        # Sync button — pulls GeeLark phones into Account table
        col_sync1, col_sync2 = st.columns([3, 1])
        with col_sync2:
            if st.button("🔄 Sync from GeeLark", use_container_width=True, type="primary"):
                with st.spinner("Syncing phones from GeeLark..."):
                    result = api_post("/accounts/sync-geelark")
                    if result and result.get("success"):
                        created = result.get("created", 0)
                        total = result.get("total_accounts", 0)
                        st.success(f"Synced! {created} new accounts created. {total} total accounts.")
                        st.rerun()
                    else:
                        st.error("Failed to sync from GeeLark")
        
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
            st.warning("No accounts in database yet. Click **🔄 Sync from GeeLark** above to import your GeeLark phones as accounts.")
    
    with tab2:
        st.markdown("### ➕ Add New Account")
        
        with st.form("create_account"):
            col1, col2 = st.columns(2)
            with col1:
                acct_name = st.text_input("Account Name", placeholder="e.g. TikTok_Account_01")
                acct_email = st.text_input("Email", placeholder="optional")
                acct_password = st.text_input("Password", type="password", placeholder="optional")
            with col2:
                acct_phone = st.text_input("Phone Number", placeholder="optional")
                acct_phone_id = st.text_input("GeeLark Phone ID", placeholder="From GeeLark dashboard")
                auto_schedule = st.checkbox("Auto-schedule for pipeline", value=True)
            
            if st.form_submit_button("Create Account", use_container_width=True, type="primary"):
                if acct_name:
                    result = api_post("/accounts", {
                        "name": acct_name,
                        "email": acct_email,
                        "password": acct_password,
                        "phone": acct_phone,
                    })
                    if result:
                        acct_id = result.get("id")
                        if acct_id and acct_phone_id:
                            api_post(f"/accounts/{acct_id}/update", {"geelark_profile_id": acct_phone_id})
                        if acct_id and auto_schedule:
                            api_post(f"/accounts/{acct_id}/schedule", {"enabled": True, "warmup": True, "posting": True})
                        st.success(f"Account '{acct_name}' created!")
                        st.rerun()
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
        st.markdown("### 🤖 Generate Teamwork Videos")
        
        with st.form("generate_video"):
            col1, col2, col3 = st.columns(3)
            with col1:
                video_count = st.number_input("Number of Videos", min_value=1, max_value=20, value=3)
            with col2:
                style_hint = st.selectbox("Style", ["nature", "beach", "city", "sunset", "mountains", "forest", "ocean"])
            with col3:
                skip_overlay = st.checkbox("Skip text overlay", value=False)
            
            if st.form_submit_button("🎬 Generate Videos", use_container_width=True, type="primary"):
                with st.spinner(f"Generating {video_count} videos..."):
                    result = api_post("/videos/generate", {
                        "count": video_count, "style_hint": style_hint, "skip_overlay": skip_overlay
                    })
                    if result:
                        st.success(f"Video generation started! Job ID: {result.get('job_id')}")
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
                    hashtags = st.text_input("Hashtags",
                        value="#teamwork #teamworktrend #teamworkchallenge #teamworkmakesthedream #letsgo")
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
                st.warning("No phones available. Add phones in GeeLark first.")
            if not videos or not videos.get("videos"):
                st.warning("No videos available. Generate videos first.")


# ===========================
# PAGE: GeeLark
# ===========================

elif page == "⚙️ GeeLark":
    st.markdown("## ⚙️ GeeLark Cloud Phones")
    st.caption("Direct GeeLark phone management")
    
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
                            "phone_id": phone_id, "duration_minutes": 20,
                            "action": "search video",
                            "keywords": ["teamwork trend", "teamwork challenge"]
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
        st.caption("Create a new GeeLark phone, install TikTok, and prepare for automation")
        
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
