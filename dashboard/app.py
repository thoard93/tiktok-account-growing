"""
TikTok Automation Dashboard
===========================
Streamlit-based dashboard for managing TikTok account automation.
"""

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# Configuration - Use Render API URL as default
API_BASE_URL = os.getenv("API_BASE_URL", "https://tiktok-automation-api-4o6b.onrender.com/api")

st.set_page_config(
    page_title="TikTok Automation",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Premium Dark Mode with High Contrast Text
st.markdown("""
<style>
    /* Premium Dark Theme with Readable Text */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff !important;
    }
    
    /* Force all text to be white/light */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label, 
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stMarkdown, .stMarkdown p, .stText, [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Make sidebar collapse button visible */
    [data-testid="collapsedControl"] {
        color: white !important;
        background: #6366f1 !important;
        border-radius: 8px !important;
    }
    
    button[kind="headerNoPadding"] {
        color: white !important;
    }
    
    .stMetric {
        background: linear-gradient(145deg, #1e1e3f, #252550);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .stMetric label, .stMetric [data-testid="stMetricValue"], 
    .stMetric [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }
    
    .magic-card {
        background: linear-gradient(145deg, #1a1a3e, #252560);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
        margin: 20px 0;
        color: #ffffff !important;
    }
    
    .magic-card h3, .magic-card ol, .magic-card li {
        color: #ffffff !important;
    }
    
    .magic-card strong {
        color: #a5b4fc !important;
    }
    
    /* Input fields */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #252550 !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    
    .stTextInput label, .stSelectbox label, .stTextArea label {
        color: #ffffff !important;
    }
    
    /* Dataframes/Tables */
    .stDataFrame, .stTable {
        color: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] {
        background: #1a1a3e;
    }
    
    /* Status colors */
    .status-active { color: #00ff88 !important; font-weight: bold; }
    .status-warming { color: #ffc107 !important; font-weight: bold; }
    .status-banned { color: #ff4757 !important; font-weight: bold; }
    .status-paused { color: #a0a0a0 !important; font-weight: bold; }
    
    /* Dropdown/Selectbox text visibility */
    .stSelectbox > div > div > div > div {
        color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #252550 !important;
        color: #ffffff !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
        color: #ffffff !important;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #8b5cf6, #a855f7) !important;
        transform: translateY(-2px);
    }
    
    /* Success/Error/Warning messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        color: #ffffff !important;
    }
    
    /* Radio buttons */
    .stRadio label {
        color: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


# ===========================
# API Helper Functions
# ===========================

def api_get(endpoint: str):
    """Make GET request to API."""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def api_post(endpoint: str, data: dict = None):
    """Make POST request to API."""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data or {}, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def api_delete(endpoint: str):
    """Make DELETE request to API."""
    try:
        response = requests.delete(f"{API_BASE_URL}{endpoint}", timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def api_post_long(endpoint: str, data: dict = None):
    """Make POST request with extended timeout for long-running operations like Magic Setup."""
    full_url = f"{API_BASE_URL}{endpoint}"
    try:
        # 5-minute timeout for operations like phone creation + TikTok install + account creation
        st.write(f"🔗 Calling: `{full_url}`")  # Debug output
        response = requests.post(full_url, json=data or {}, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        st.error("⏳ Operation is taking longer than expected. Check the 📊 Logs page for progress.")
        return None
    except requests.exceptions.ConnectionError as e:
        st.error(f"🔌 Connection Error to {full_url}: {e}")
        return None
    except Exception as e:
        st.error(f"API Error calling {full_url}: {type(e).__name__}: {e}")
        return None



# ===========================
# Sidebar Navigation
# ===========================

st.sidebar.title("📱 TikTok Automation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "✨ Magic Setup", "👤 Accounts", "🔐 Credentials", "🔄 Warmup", "🎬 Videos", "🌐 Proxies", "📊 Logs", "⚙️ GeeLark"]
)

# Version footer - update on each deploy
st.sidebar.markdown("---")
st.sidebar.caption(f"v0.4.2 | API: {API_BASE_URL[:40]}...")


# ===========================
# Dashboard Page
# ===========================

if page == "🏠 Dashboard":
    st.title("Dashboard")
    
    # Get stats
    stats = api_get("/dashboard/stats")
    
    if stats:
        # Metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Accounts", stats["total_accounts"])
        with col2:
            st.metric("Warming Up", stats["warming_up"], delta=None)
        with col3:
            st.metric("Active", stats["active"])
        with col4:
            st.metric("Posting", stats["posting"])
        with col5:
            st.metric("Banned", stats["banned"], delta_color="inverse")
        
        st.markdown("---")
        
        # Second row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Available Proxies", stats["available_proxies"])
        with col2:
            st.metric("Total Videos", stats["total_videos"])
        with col3:
            st.metric("Unposted Videos", stats["unposted_videos"])
        with col4:
            st.metric("Tasks Today", stats["tasks_today"])
    
    st.markdown("---")
    
    # Health check
    st.subheader("System Health")
    health = api_get("/health")
    if health:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Status:** {health['status']}")
            st.write(f"**GeeLark Connected:** {'✅' if health['geelark_connected'] else '❌'}")
        with col2:
            st.write(f"**Database Connected:** {'✅' if health['database_connected'] else '❌'}")
            st.write(f"**Last Check:** {health['timestamp'][:19]}")


# ===========================
# Magic Setup Page
# ===========================

elif page == "✨ Magic Setup":
    st.title("✨ Magic Setup")
    st.markdown("**Zero-touch automation**: Paste a proxy → Get a warmed TikTok account")
    
    st.markdown("""
    <div class="magic-card">
        <h3>🚀 What happens when you click "Launch":</h3>
        <ol>
            <li>Creates an <strong>Android 15</strong> cloud phone with your proxy</li>
            <li>Installs <strong>TikTok</strong> from the official app store</li>
            <li>Creates a <strong>new TikTok account</strong> with natural credentials</li>
            <li>Stores credentials <strong>securely encrypted</strong></li>
            <li>Starts the <strong>5-day warmup process</strong></li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Simple form - no complex session state
    with st.form("magic_setup_form"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            proxy_string = st.text_input(
                "🌐 Proxy String",
                placeholder="socks5://user:pass@1.2.3.4:1337  or  host:port:user:pass",
                help="Supports multiple formats: protocol://user:pass@host:port or host:port:user:pass"
            )
        
        with col2:
            name_prefix = st.text_input("Name Prefix (optional)", placeholder="MyBrand")
        
        # Submit button inside form - guaranteed to work
        submitted = st.form_submit_button("🚀 Launch Magic Setup", type="primary", use_container_width=True)
        
        if submitted:
            if not proxy_string:
                st.warning("⚠️ Please enter a proxy string")
            else:
                st.info("🔄 Starting Magic Setup... (this may take 2-5 minutes)")
                
                # Start async task - use long timeout for cold starts
                result = api_post_long("/accounts/full-setup-async", {
                    "proxy_string": proxy_string,
                    "name_prefix": name_prefix or "",
                    "max_retries": 5
                })
                
                if result and result.get("task_id"):
                    task_id = result["task_id"]
                    st.success(f"✅ Task started! ID: `{task_id}`")
                    st.markdown(f"👉 **[Check progress in Logs tab](#)** or wait here...")
                    
                    # Poll for completion
                    import time
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i in range(120):  # Max 10 minutes (120 * 5 seconds)
                        time.sleep(5)
                        task_status = api_get(f"/tasks/{task_id}")
                        
                        if task_status:
                            # Robust progress parsing - handle various formats
                            progress_val = task_status.get("progress", 0)
                            try:
                                progress = int(progress_val) if progress_val is not None else 0
                            except (ValueError, TypeError):
                                progress = 0  # Default if not a valid number
                            
                            current_step = task_status.get("current_step", "Working...")
                            status = task_status.get("status", "running")
                            
                            progress_bar.progress(max(0, min(progress, 100)) / 100)
                            status_text.markdown(f"**{status.upper()}**: {current_step}")
                            
                            if status == "complete":
                                st.balloons()
                                res = task_status.get("result", {})
                                st.success(f"""
                                🎉 **Account Created!**
                                - Account ID: `{res.get('account_id')}`
                                - Phone ID: `{res.get('phone_id')}`
                                """)
                                if res.get("credentials"):
                                    creds = res["credentials"]
                                    st.info(f"""
                                    **Credentials**: `{creds.get('username')}` / `{creds.get('email')}` / `{creds.get('password')}`
                                    """)
                                break
                            
                            elif status == "failed":
                                st.error(f"❌ Failed: {task_status.get('error')}")
                                break
                        else:
                            status_text.warning("Waiting for task status...")
                    else:
                        st.warning("⏰ Task taking too long. Check Logs tab for status.")
                
                elif result:
                    st.error(f"Error starting task: {result}")
                else:
                    st.error("Failed to connect to API")
    
    st.markdown("---")
    st.caption("💡 Tip: Use static residential proxies for best results. Each proxy should be unique.")


# ===========================
# Credentials Page
# ===========================

elif page == "🔐 Credentials":
    st.title("🔐 Secure Credentials Vault")
    st.markdown("View all stored TikTok account credentials")
    
    st.warning("⚠️ **Security Notice**: These are decrypted credentials. Handle with care.")
    
    credentials = api_get("/credentials")
    
    if credentials:
        # Create DataFrame
        df = pd.DataFrame([{
            "Account ID": c["account_id"],
            "Username": c["username"],
            "Email": c["email"],
            "Password": c["password"],
            "Phone ID": c.get("phone_id", "N/A"),
            "Created": c.get("created_at", "")[:19] if c.get("created_at") else ""
        } for c in credentials])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        if st.button("📥 Export as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="tiktok_credentials.csv",
                mime="text/csv"
            )
    else:
        st.info("No credentials stored yet. Use Magic Setup to create accounts!")


# ===========================
# Accounts Page
# ===========================

elif page == "👤 Accounts":
    st.title("Account Management")
    
    # Tabs
    tab1, tab2 = st.tabs(["📋 Account List", "➕ Create Accounts"])
    
    with tab1:
        # Filters
        col1, col2 = st.columns([1, 4])
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "created", "warming_up", "active", "posting", "paused", "banned"]
            )
        
        # Get accounts
        endpoint = "/accounts"
        if status_filter != "All":
            endpoint += f"?status={status_filter}"
        
        accounts_data = api_get(endpoint)
        
        if accounts_data and accounts_data["items"]:
            # Convert to DataFrame
            df = pd.DataFrame([{
                "ID": a["id"],
                "Name": a.get("geelark_profile_name", "N/A"),
                "Status": a["status"],
                "Username": a.get("tiktok_username", "-"),
                "📱 Phone": a.get("phone", "-"),  # HeroSMS number for manual reg
                "Followers": a["followers_count"],
                "Posts": a["posts_count"],
                "Warmup Day": a["warmup_day"],
                "Last Activity": a.get("last_activity", "-")
            } for a in accounts_data["items"]])
            
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            
            # Quick actions
            st.subheader("Quick Actions")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                account_id = st.number_input("Account ID", min_value=1, step=1)
            with col2:
                if st.button("▶️ Start"):
                    result = api_post(f"/accounts/{account_id}/start")
                    if result:
                        st.success("Phone started!")
            with col3:
                if st.button("⏹️ Stop"):
                    result = api_post(f"/accounts/{account_id}/stop")
                    if result:
                        st.success("Phone stopped!")
            with col4:
                if st.button("📱 Install TikTok"):
                    result = api_post(f"/accounts/{account_id}/install-tiktok")
                    if result:
                        st.success("TikTok installation started!")
            with col5:
                if st.button("🗑️ Delete", type="primary"):
                    result = api_delete(f"/accounts/{account_id}")
                    if result:
                        st.success(f"Account {account_id} deleted!")
                        st.rerun()
        else:
            st.info("No accounts found. Create some accounts to get started!")
    
    with tab2:
        st.subheader("Create New Accounts")
        
        with st.form("create_accounts"):
            count = st.number_input("Number of Accounts", min_value=1, max_value=50, value=5)
            name_prefix = st.text_input("Name Prefix", value="TikTok_Account")
            
            st.markdown("---")
            st.write("**Credentials (Optional)**")
            st.caption("Format: email,password - one per line")
            credentials_text = st.text_area("Credentials", height=100)
            
            submitted = st.form_submit_button("Create Accounts")
            
            if submitted:
                credentials = None
                if credentials_text.strip():
                    credentials = []
                    for line in credentials_text.strip().split("\n"):
                        parts = line.split(",")
                        if len(parts) >= 2:
                            credentials.append({
                                "email": parts[0].strip(),
                                "password": parts[1].strip()
                            })
                
                result = api_post("/accounts/batch", {
                    "count": count,
                    "name_prefix": name_prefix,
                    "credentials": credentials
                })
                
                if result:
                    st.success(f"Created {len(result)} accounts!")


# ===========================
# Warmup Page
# ===========================

elif page == "🔄 Warmup":
    st.title("Warmup Automation")
    
    # Pending warmups
    st.subheader("Accounts Pending Warmup")
    pending = api_get("/warmup/pending")
    
    if pending:
        df = pd.DataFrame([{
            "ID": a["id"],
            "Name": a.get("geelark_profile_name", "N/A"),
            "Day": a["warmup_day"],
            "Last Activity": a.get("last_activity", "-")
        } for a in pending])
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No accounts currently warming up.")
    
    st.markdown("---")
    
    # Actions
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Start Warmup")
        account_ids_str = st.text_input("Account IDs (comma-separated)")
        if st.button("🚀 Start Warmup"):
            if account_ids_str:
                ids = [int(x.strip()) for x in account_ids_str.split(",")]
                result = api_post("/warmup/start", {"account_ids": ids})
                if result:
                    st.success(f"Started: {result['started']}, Failed: {result['failed']}")
    
    with col2:
        st.subheader("Run Warmup Session")
        if st.button("▶️ Run Session for All Pending"):
            result = api_post("/warmup/run-session", {})
            if result:
                st.success(f"Success: {result['success']}, Failed: {result['failed']}, Completed: {result['completed']}")


# ===========================
# Videos Page
# ===========================

elif page == "🎬 Videos":
    st.title("Video Management")
    
    tab1, tab2 = st.tabs(["📋 Video Library", "📤 Upload Video"])
    
    with tab1:
        col1, col2 = st.columns([1, 4])
        with col1:
            posted_filter = st.selectbox("Filter", ["All", "Unposted", "Posted"])
        
        endpoint = "/videos"
        if posted_filter == "Unposted":
            endpoint += "?posted=false"
        elif posted_filter == "Posted":
            endpoint += "?posted=true"
        
        videos = api_get(endpoint)
        
        if videos and videos["items"]:
            df = pd.DataFrame([{
                "ID": v["id"],
                "Filename": v["filename"],
                "Caption": (v.get("caption", "") or "")[:50] + "...",
                "Posted": "✅" if v["is_posted"] else "❌",
                "Account": v.get("account_id", "-"),
                "Created": v["created_at"][:10]
            } for v in videos["items"]])
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No videos found. Upload some videos!")
    
    with tab2:
        st.subheader("Upload Video")
        
        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])
        caption = st.text_area("Caption")
        hashtags = st.text_input("Hashtags (comma-separated)")
        
        if st.button("📤 Upload") and uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            data = {"caption": caption, "hashtags": hashtags}
            
            try:
                response = requests.post(
                    f"{API_BASE_URL}/videos/upload",
                    files=files,
                    data=data,
                    timeout=60
                )
                if response.ok:
                    st.success("Video uploaded successfully!")
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")


# ===========================
# Proxies Page
# ===========================

elif page == "🌐 Proxies":
    st.title("Proxy Management")
    
    tab1, tab2 = st.tabs(["📋 Proxy List", "➕ Add Proxies"])
    
    with tab1:
        proxies = api_get("/proxies")
        
        if proxies:
            df = pd.DataFrame([{
                "ID": p["id"],
                "Host": p["host"],
                "Port": p["port"],
                "Protocol": p["protocol"],
                "Location": p.get("location", "-"),
                "Assigned": "✅" if p["is_assigned"] else "❌",
                "Active": "✅" if p["is_active"] else "❌"
            } for p in proxies])
            
            st.dataframe(df, use_container_width=True)
            
            available = len([p for p in proxies if not p["is_assigned"] and p["is_active"]])
            st.info(f"**{available}** proxies available for assignment")
        else:
            st.info("No proxies found. Add some proxies!")
    
    with tab2:
        st.subheader("Bulk Import Proxies")
        st.caption("Format: host:port:username:password (one per line)")
        
        proxy_text = st.text_area("Proxies", height=200)
        protocol = st.selectbox("Protocol", ["HTTP", "SOCKS5"])
        
        if st.button("➕ Import Proxies"):
            if proxy_text.strip():
                result = api_post("/proxies/bulk", {
                    "proxy_list": proxy_text,
                    "protocol": protocol
                })
                if result:
                    st.success(f"Imported {len(result)} proxies!")


# ===========================
# Logs Page
# ===========================

elif page == "📊 Logs":
    st.title("📊 Activity Logs & Status")
    
    # Real-time Status Overview
    st.subheader("🔄 System Status")
    
    # Get quick stats
    stats = api_get("/dashboard/stats")
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔥 Warming Up", stats.get("warming_up", 0))
        with col2:
            st.metric("✅ Active", stats.get("active", 0))
        with col3:
            st.metric("📱 Phones", stats.get("total_accounts", 0))
        with col4:
            st.metric("🚫 Banned", stats.get("banned", 0))
    
    st.markdown("---")
    
    # Tabs for different log views
    tab1, tab2 = st.tabs(["📋 Activity Feed", "⚠️ Errors Only"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            account_filter = st.number_input("Account ID (0 = all)", min_value=0, value=0)
        with col2:
            action_filter = st.selectbox(
                "Action Type",
                ["All", "account_created", "full_setup_started", "full_setup_completed",
                 "warmup_started", "warmup_session", "warmup_completed", 
                 "phone_stopped_after_warmup", "phone_started", "phone_stopped",
                 "video_posted", "ban_detected", "account_recovered", "phone_recreated"]
            )
        with col3:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        endpoint = "/logs?limit=50&"
        if account_filter > 0:
            endpoint += f"account_id={account_filter}&"
        if action_filter != "All":
            endpoint += f"action_type={action_filter}&"
        
        logs = api_get(endpoint.rstrip("?&"))
        
        if logs and logs.get("items"):
            for log in logs["items"]:
                # Color-coded status icons
                if log["success"]:
                    if "completed" in log["action_type"]:
                        icon = "🎉"
                    elif "started" in log["action_type"]:
                        icon = "🚀"
                    elif "stopped" in log["action_type"]:
                        icon = "⏹️"
                    elif "warmup" in log["action_type"]:
                        icon = "🔥"
                    else:
                        icon = "✅"
                else:
                    icon = "❌"
                
                # Format the log entry
                timestamp = log['created_at'][:19].replace('T', ' ')
                
                with st.container():
                    st.markdown(f"""
                    **{icon} {log['action_type'].replace('_', ' ').title()}** - Account #{log['account_id']}  
                    🕐 *{timestamp}*
                    """)
                    
                    # Show action details if available
                    if log.get("action_details"):
                        details = log["action_details"]
                        if isinstance(details, dict):
                            detail_str = " | ".join([f"**{k}**: {v}" for k, v in details.items() if v is not None][:4])
                            if detail_str:
                                st.caption(detail_str)
                    
                    if log.get("error_message"):
                        st.error(f"⚠️ {log['error_message']}")
                    
                    st.markdown("---")
        else:
            st.info("No activity logs yet. Start a Magic Setup to see logs here!")
    
    with tab2:
        st.subheader("⚠️ Recent Errors")
        
        error_logs = api_get("/logs?success=false&limit=20")
        
        if error_logs and error_logs.get("items"):
            for log in error_logs["items"]:
                timestamp = log['created_at'][:19].replace('T', ' ')
                
                st.error(f"""
                **❌ {log['action_type']}** - Account #{log['account_id']}  
                🕐 {timestamp}  
                **Error:** {log.get('error_message', 'Unknown error')}
                """)
                st.markdown("---")
        else:
            st.success("🎉 No errors! Everything is running smoothly.")


# ===========================
# GeeLark Page
# ===========================

elif page == "⚙️ GeeLark":
    st.title("GeeLark Direct Control")
    
    tab1, tab2, tab3 = st.tabs(["📱 Cloud Phones", "📋 Task History", "🔧 Task Management"])
    
    with tab1:
        st.subheader("Cloud Phones")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        phones = api_get("/geelark/phones")
        
        if phones and phones.get("items"):
            df = pd.DataFrame([{
                "ID": p["id"],
                "Name": p["serialName"],
                "Status": ["Started", "Starting", "Shutdown"][p.get("status", 2)],
                "OS": p.get("equipmentInfo", {}).get("osVersion", "-"),
                "Proxy": p.get("proxy", {}).get("server", "-") if p.get("proxy") else "-"
            } for p in phones["items"]])
            
            st.dataframe(df, use_container_width=True)
            
            # Quick controls
            st.subheader("Quick Controls")
            phone_ids = st.text_input("Phone IDs (comma-separated)")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("▶️ Start Phones"):
                    if phone_ids:
                        ids = [x.strip() for x in phone_ids.split(",")]
                        result = api_post("/geelark/phones/start", {"ids": ids})
                        if result:
                            st.success(f"Started {result.get('successAmount', 0)} phones")
            with col2:
                if st.button("⏹️ Stop Phones"):
                    if phone_ids:
                        ids = [x.strip() for x in phone_ids.split(",")]
                        result = api_post("/geelark/phones/stop", ids)
                        if result:
                            st.success("Phones stopped")
            
            st.markdown("---")
            
            # Warmup Controls - Easy selection!
            st.subheader("🔥 Run Warmup on Any Phone")
            
            # Create dropdown options from phone list
            phone_options = {f"{p['serialName']} ({p['id'][:8]}...)": p['id'] for p in phones['items']}
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                selected_phone = st.selectbox(
                    "Select Phone", 
                    options=list(phone_options.keys()),
                    help="Pick a phone to run teamwork warmup"
                )
            with col2:
                warmup_duration = st.number_input("Duration (min)", min_value=10, max_value=120, value=30)
            with col3:
                st.write("")  # Spacer
                st.write("")
                if st.button("🔥 Run Warmup", type="primary"):
                    if selected_phone:
                        phone_id = phone_options[selected_phone]
                        result = api_post("/geelark/warmup/run", {
                            "phone_id": phone_id,
                            "duration_minutes": warmup_duration
                        })
                        if result and result.get("success"):
                            st.success(f"Warmup started on {selected_phone}!")
                        else:
                            st.error(f"Failed: {result.get('message', 'Unknown error') if result else 'API error'}")
            
            st.caption("💡 To stop a warmup, go to **Task History** tab and cancel the task, or use **Task Management** tab.")
        else:
            st.info("No phones found in GeeLark. Create some phones first!")
    
    with tab2:
        st.subheader("Task History (Last 7 Days)")
        
        history = api_get("/geelark/tasks/history?size=50")
        
        if history and history.get("items"):
            task_types = {
                1: "Video Post",
                2: "AI Warmup",
                3: "Carousel Post",
                4: "Account Login",
                6: "Profile Edit",
                42: "Custom"
            }
            statuses = {
                1: "⏳ Waiting",
                2: "🔄 Running",
                3: "✅ Completed",
                4: "❌ Failed",
                7: "🚫 Cancelled"
            }
            
            df = pd.DataFrame([{
                "Task ID": t["id"],
                "Type": task_types.get(t["taskType"], "Unknown"),
                "Phone": t["serialName"],
                "Status": statuses.get(t["status"], "Unknown"),
                "Cost (s)": t.get("cost", "-")
            } for t in history["items"]])
            
            st.dataframe(df, use_container_width=True)
    
    with tab3:
        st.subheader("Task Management")
        
        task_ids = st.text_input("Task IDs (comma-separated)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Query Status"):
                if task_ids:
                    ids = [x.strip() for x in task_ids.split(",")]
                    result = api_post("/geelark/tasks/query", {"task_ids": ids})
                    if result:
                        st.json(result)
        
        with col2:
            if st.button("❌ Cancel Tasks"):
                if task_ids:
                    ids = [x.strip() for x in task_ids.split(",")]
                    result = api_post("/geelark/tasks/cancel", {"task_ids": ids})
                    if result:
                        st.success(f"Cancelled: {result.get('successAmount', 0)}")
        
        with col3:
            if st.button("🔄 Retry Tasks"):
                if task_ids:
                    ids = [x.strip() for x in task_ids.split(",")]
                    result = api_post("/geelark/tasks/retry", {"task_ids": ids})
                    if result:
                        st.success(f"Retried: {result.get('successAmount', 0)}")


# Footer
st.sidebar.markdown("---")
st.sidebar.caption("TikTok Automation v0.1.0")
