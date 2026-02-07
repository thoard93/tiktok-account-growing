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
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%);
    }
    [data-testid="stSidebar"] .stMarkdown h1 {
        color: #e0e0ff;
        font-size: 1.4rem;
        font-weight: 700;
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
    
    /* Pipeline status card */
    .pipeline-card {
        background: linear-gradient(135deg, #1a1a40 0%, #252560 100%);
        border: 1px solid rgba(100, 100, 255, 0.15);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .pipeline-card h2 {
        color: #c0c0ff;
        font-size: 1.1rem;
        margin: 0 0 16px 0;
    }
    
    /* Phase indicators */
    .phase-row {
        display: flex;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .phase-row:last-child { border-bottom: none; }
    .phase-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin-right: 16px;
    }
    .phase-icon.warmup { background: rgba(255, 152, 0, 0.15); }
    .phase-icon.vidgen { background: rgba(156, 39, 176, 0.15); }
    .phase-icon.posting { background: rgba(0, 188, 212, 0.15); }
    
    /* Log table */
    .log-entry {
        display: flex;
        align-items: center;
        padding: 10px 16px;
        border-radius: 10px;
        margin-bottom: 6px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Account row */
    .account-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 20px;
        border-radius: 12px;
        margin-bottom: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: background 0.2s;
    }
    .account-row:hover {
        background: rgba(255, 255, 255, 0.06);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s;
    }
    
    /* Section headers */
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# ===========================
# API Helpers
# ===========================

def api_get(endpoint):
    """GET request to API."""
    try:
        resp = requests.get(f"{API_BASE_URL}{endpoint}", timeout=15)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception as e:
        return None

def api_post(endpoint, data=None):
    """POST request to API."""
    try:
        resp = requests.post(f"{API_BASE_URL}{endpoint}", json=data or {}, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception as e:
        return None

def api_delete(endpoint):
    """DELETE request to API."""
    try:
        resp = requests.delete(f"{API_BASE_URL}{endpoint}", timeout=10)
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception as e:
        return None


def status_badge(status):
    """Return HTML badge for a status string."""
    color_map = {
        "completed": "green", "success": "green", "active": "green",
        "started": "yellow", "running": "yellow", "warming_up": "yellow",
        "failed": "red", "error": "red", "banned": "red",
        "skipped": "gray", "created": "blue", "paused": "gray",
    }
    color = color_map.get(status, "gray")
    return f'<span class="badge badge-{color}">{status}</span>'


def format_time_ago(iso_str):
    """Format an ISO timestamp as relative time."""
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
st.sidebar.caption(f"v2.0.0 | API: {API_BASE_URL[:35]}...")
st.sidebar.caption("Built for automation 🤖")


# ===========================
# PAGE: Dashboard
# ===========================

if page == "📊 Dashboard":
    st.markdown("## 📊 Dashboard")
    st.caption("System overview and pipeline health")
    
    # Fetch data
    pipeline_status = api_get("/pipeline/status")
    health = api_get("/health")
    
    # Row 1: Quick stats
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
    
    # Row 2: Today's Pipeline Status
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
    
    # Row 3: Recent Pipeline Activity
    st.markdown("### 📋 Recent Activity")
    
    logs_data = api_get("/pipeline/logs?days=3")
    if logs_data and logs_data.get("logs"):
        logs = logs_data["logs"][:15]  # Last 15 entries
        
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
    
    # Health check
    st.markdown("### 🏥 System Health")
    if health:
        col1, col2 = st.columns(2)
        with col1:
            gl_status = "✅ Connected" if health.get("geelark_connected") else "❌ Disconnected"
            st.markdown(f"**GeeLark API:** {gl_status}")
            st.markdown(f"**Database:** ✅ Connected")
        with col2:
            st.markdown(f"**Scheduler:** ✅ Active" if health.get("scheduler_active", True) else "**Scheduler:** ❌ Inactive")
            st.markdown(f"**Version:** v2.0.0")
    else:
        st.error("Cannot reach API backend")


# ===========================
# PAGE: Pipeline
# ===========================

elif page == "⚡ Pipeline":
    st.markdown("## ⚡ Pipeline Control")
    st.caption("Configure and monitor the automated daily pipeline")
    
    # Fetch current config
    config_resp = api_get("/schedule/config")
    pipeline_status = api_get("/pipeline/status")
    
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
            if result:
                st.rerun()
    
    st.markdown("---")
    
    # Schedule Configuration
    st.markdown("### ⏰ Schedule Settings (EST)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        warmup_hour = st.number_input(
            "Warmup Hour (EST)",
            min_value=1, max_value=23,
            value=config_resp.get("warmup_hour_est", 8) if config_resp else 8,
            help="Hour in EST when warmup starts"
        )
    
    with col2:
        vidgen_hour = st.number_input(
            "Video Gen Hour (EST)",
            min_value=1, max_value=23,
            value=config_resp.get("video_gen_hour_est", 9) if config_resp else 9,
            help="Hour in EST when video generation starts"
        )
    
    with col3:
        posting_hours = st.text_input(
            "Posting Hours (EST)",
            value=config_resp.get("posting_hours_est", "10,13,17") if config_resp else "10,13,17",
            help="Comma-separated hours in EST"
        )
    
    with col4:
        posts_per = st.number_input(
            "Posts per Account",
            min_value=1, max_value=10,
            value=config_resp.get("posts_per_phone", 3) if config_resp else 3
        )
    
    if st.button("💾 Save Schedule", use_container_width=True):
        update_data = {
            "warmup_hour_est": warmup_hour,
            "video_gen_hour_est": vidgen_hour,
            "posting_hours_est": posting_hours,
            "posts_per_phone": posts_per,
        }
        result = api_post("/schedule/config", update_data)
        if result:
            st.success("Schedule saved! Changes take effect on next server restart.")
            st.rerun()
    
    st.markdown("---")
    
    # Manual triggers
    st.markdown("### 🎮 Manual Triggers")
    st.caption("Trigger pipeline phases immediately (respects account scheduling)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔥 Run Warmup Now", use_container_width=True, type="primary"):
            result = api_post("/pipeline/trigger/warmup")
            if result:
                st.success("Warmup triggered! Check logs for progress.")
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
    
    log_days = st.selectbox("Show logs from", [1, 3, 7, 14], index=1, format_func=lambda x: f"Last {x} day{'s' if x > 1 else ''}")
    phase_filter = st.selectbox("Filter by phase", ["All", "warmup", "video_gen", "posting"], index=0)
    
    endpoint = f"/pipeline/logs?days={log_days}"
    if phase_filter != "All":
        endpoint += f"&phase={phase_filter}"
    
    logs_data = api_get(endpoint)
    
    if logs_data and logs_data.get("logs"):
        logs = logs_data["logs"]
        
        # Convert to DataFrame for nice display
        df_data = []
        for log in logs:
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
        st.caption(f"Showing {len(logs)} entries")
    else:
        st.info("No pipeline logs yet. Trigger a phase or wait for the automatic schedule.")


# ===========================
# PAGE: Accounts
# ===========================

elif page == "👤 Accounts":
    st.markdown("## 👤 Account Management")
    st.caption("Manage accounts and their scheduling status")
    
    tab1, tab2, tab3 = st.tabs(["📋 Account List", "➕ Add Account", "🔐 Credentials"])
    
    with tab1:
        st.markdown("### Scheduled Accounts")
        st.caption("Toggle scheduling on/off for each account. Scheduled accounts are included in the daily pipeline.")
        
        accounts_data = api_get("/accounts/scheduled")
        
        if accounts_data and accounts_data.get("accounts"):
            accounts = accounts_data["accounts"]
            
            # Bulk actions
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.markdown(f"**{len(accounts)} accounts total** · "
                           f"**{sum(1 for a in accounts if a.get('schedule_enabled'))} scheduled**")
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
            with col4:
                if st.button("🔄 Refresh"):
                    st.rerun()
            
            st.markdown("---")
            
            # Account table
            for account in accounts:
                col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 1, 1, 1, 1])
                
                with col1:
                    name = account.get("name", "Unknown")
                    username = account.get("tiktok_username")
                    if username:
                        st.markdown(f"**{name}** · @{username}")
                    else:
                        st.markdown(f"**{name}**")
                
                with col2:
                    phone_id = account.get("phone_id", "")
                    st.caption(f"📱 {phone_id[:12]}..." if phone_id else "No phone")
                
                with col3:
                    status = account.get("status", "unknown")
                    st.markdown(status_badge(status), unsafe_allow_html=True)
                
                with col4:
                    # Schedule toggle
                    is_scheduled = account.get("schedule_enabled", False)
                    new_val = st.checkbox(
                        "Sched", 
                        value=is_scheduled, 
                        key=f"sched_{account['id']}",
                        label_visibility="collapsed"
                    )
                    if new_val != is_scheduled:
                        api_post(f"/accounts/{account['id']}/schedule", {"enabled": new_val})
                        st.rerun()
                
                with col5:
                    # Warmup sub-toggle (only if scheduled)
                    if account.get("schedule_enabled"):
                        warmup_val = st.checkbox(
                            "W", value=account.get("schedule_warmup", True),
                            key=f"warmup_{account['id']}", label_visibility="collapsed",
                            help="Include in warmup"
                        )
                        if warmup_val != account.get("schedule_warmup", True):
                            api_post(f"/accounts/{account['id']}/schedule", {"warmup": warmup_val})
                            st.rerun()
                    else:
                        st.write("—")
                
                with col6:
                    # Posting sub-toggle
                    if account.get("schedule_enabled"):
                        posting_val = st.checkbox(
                            "P", value=account.get("schedule_posting", True),
                            key=f"posting_{account['id']}", label_visibility="collapsed",
                            help="Include in posting"
                        )
                        if posting_val != account.get("schedule_posting", True):
                            api_post(f"/accounts/{account['id']}/schedule", {"posting": posting_val})
                            st.rerun()
                    else:
                        st.write("—")
                
                st.markdown("", unsafe_allow_html=True)  # Spacer
            
            # Legend
            st.markdown("---")
            st.caption("Column headers: **Name** | **Phone ID** | **Status** | **Scheduled ✅** | **Warmup 🔥** | **Posting 📤**")
        
        else:
            st.info("No accounts found. Create accounts via Magic Setup or add them manually.")
    
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
                        # Set phone ID and scheduling if provided
                        acct_id = result.get("id")
                        if acct_id and acct_phone_id:
                            # Update with phone ID
                            api_post(f"/accounts/{acct_id}/update", {
                                "geelark_profile_id": acct_phone_id
                            })
                        if acct_id and auto_schedule:
                            api_post(f"/accounts/{acct_id}/schedule", {
                                "enabled": True, "warmup": True, "posting": True
                            })
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
            
            # Export
            if st.button("📥 Export as CSV"):
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "credentials.csv", "text/csv")
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
        st.caption("AI-generated teamwork trend videos with originality effects")
        
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
                        "count": video_count,
                        "style_hint": style_hint,
                        "skip_overlay": skip_overlay
                    })
                    if result:
                        job_id = result.get("job_id")
                        st.success(f"Video generation started! Job ID: {job_id}")
                    else:
                        st.error("Failed to start video generation")
        
        # Job status
        st.markdown("### Active Jobs")
        jobs = api_get("/videos/jobs")
        if jobs and jobs.get("jobs"):
            for job in jobs["jobs"]:
                status = job.get("status", "unknown")
                progress = job.get("progress", 0)
                
                col1, col2, col3 = st.columns([2, 4, 1])
                with col1:
                    st.markdown(f"**{job['job_id'][:8]}...**")
                with col2:
                    st.progress(progress / 100 if progress else 0, text=f"{status} ({progress}%)")
                with col3:
                    st.markdown(status_badge(status), unsafe_allow_html=True)
        else:
            st.info("No active generation jobs")
    
    with tab2:
        st.markdown("### 📚 Video Library")
        
        videos = api_get("/videos/list")
        if videos and videos.get("videos"):
            video_list = videos["videos"]
            st.markdown(f"**{len(video_list)} videos available**")
            
            for v in video_list:
                col1, col2, col3, col4 = st.columns([4, 2, 2, 1])
                with col1:
                    st.markdown(f"🎬 **{v.get('filename', 'Unknown')}**")
                with col2:
                    size = v.get('size_mb', 0)
                    st.caption(f"{size:.1f} MB" if size else "—")
                with col3:
                    created = v.get('created', '')
                    st.caption(created[:16] if created else "—")
                with col4:
                    if st.button("🗑️", key=f"del_vid_{v.get('filename', '')}"):
                        api_delete(f"/videos/{v.get('filename', '')}")
                        st.rerun()
        else:
            st.info("No videos in library. Generate some using the AI Generate tab!")
    
    with tab3:
        st.markdown("### 📤 Post Videos to TikTok")
        st.caption("Post videos to your GeeLark phones")
        
        # Fetch phones and videos
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
                            st.success(f"Posting job started! Job ID: {result.get('job_id', 'unknown')}")
                        else:
                            st.error("Failed to start posting")
                    else:
                        st.warning("Select at least one phone and one video")
        else:
            if not phones or not phones.get("items"):
                st.warning("No phones available. Add phones in GeeLark first.")
            if not videos or not videos.get("videos"):
                st.warning("No videos available. Generate videos first.")
        
        # Posting job status
        st.markdown("---")
        st.markdown("### 📊 Posting Job Status")
        
        if "posting_job_id" not in st.session_state:
            st.session_state.posting_job_id = ""
        
        job_id_input = st.text_input("Job ID to check", value=st.session_state.posting_job_id)
        if job_id_input:
            job_status = api_get(f"/videos/post/status/{job_id_input}")
            if job_status:
                st.json(job_status)


# ===========================
# PAGE: GeeLark
# ===========================

elif page == "⚙️ GeeLark":
    st.markdown("## ⚙️ GeeLark Cloud Phones")
    st.caption("Direct GeeLark phone management")
    
    tab1, tab2, tab3 = st.tabs(["📱 Cloud Phones", "📋 Task History", "✨ Magic Setup"])
    
    with tab1:
        st.markdown("### Cloud Phones")
        
        if st.button("🔄 Refresh Phone List"):
            st.rerun()
        
        phones = api_get("/geelark/phones")
        
        if phones and phones.get("items"):
            for phone in phones["items"]:
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
                
                with col1:
                    name = phone.get("serialName", "Unknown")
                    phone_id = phone.get("id", "")
                    st.markdown(f"**{name}**")
                    st.caption(f"ID: {phone_id[:16]}...")
                
                with col2:
                    status = phone.get("status", -1)
                    status_map = {0: "🟢 Running", 1: "🔴 Stopped", 2: "🟡 Starting"}
                    st.markdown(status_map.get(status, f"⚪ Unknown ({status})"))
                
                with col3:
                    if st.button("▶️", key=f"start_{phone_id}", help="Start phone"):
                        result = api_post("/geelark/phones/start", {"phone_ids": [phone_id]})
                        if result:
                            st.success("Starting...")
                            st.rerun()
                
                with col4:
                    if st.button("⏹️", key=f"stop_{phone_id}", help="Stop phone"):
                        result = api_post("/geelark/phones/stop", {"phone_ids": [phone_id]})
                        if result:
                            st.success("Stopping...")
                            st.rerun()
                
                with col5:
                    if st.button("🔥", key=f"warmup_{phone_id}", help="Run warmup"):
                        result = api_post("/geelark/warmup/run", {
                            "phone_id": phone_id,
                            "duration_minutes": 20,
                            "action": "search video",
                            "keywords": ["teamwork trend", "teamwork challenge"]
                        })
                        if result:
                            st.success("Warmup started!")
                
                st.markdown("---")
        else:
            st.info("No phones found. Create phones via Magic Setup or GeeLark dashboard.")
    
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
        st.caption("Create a new GeeLark phone with proxy, install TikTok, and prepare for automation")
        
        setup_tab1, setup_tab2 = st.tabs(["🔧 Single Setup", "🎯 Batch Setup"])
        
        with setup_tab1:
            with st.form("magic_setup"):
                proxy_string = st.text_input(
                    "Proxy String",
                    placeholder="protocol://user:pass@host:port or host:port:user:pass"
                )
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
                        st.warning("Please enter a proxy string")
        
        with setup_tab2:
            st.markdown("**Paste multiple proxies (one per line) to create accounts in bulk.**")
            
            proxies_text = st.text_area("Proxies (one per line)", height=150, placeholder="protocol://user:pass@host:port")
            batch_prefix = st.text_input("Name Prefix", value="tiktok", key="batch_prefix")
            batch_auto_enroll = st.checkbox("Auto-enroll in scheduler", value=True, key="batch_enroll")
            
            if st.button("🚀 Launch Batch Setup", use_container_width=True, type="primary"):
                if proxies_text.strip():
                    proxies = [p.strip() for p in proxies_text.strip().split("\n") if p.strip()]
                    if proxies:
                        result = api_post("/magic-setup/batch", {
                            "proxies": proxies,
                            "name_prefix": batch_prefix,
                            "auto_enroll": batch_auto_enroll
                        })
                        if result:
                            st.success(f"Batch setup launched for {len(proxies)} proxies!")
                        else:
                            st.error("Failed to start batch setup")
                else:
                    st.warning("Please enter at least one proxy")
