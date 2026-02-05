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
    
    /* ===== MOBILE RESPONSIVE STYLES ===== */
    @media (max-width: 768px) {
        /* Fix sidebar for iOS - proper sizing and touch targets */
        [data-testid="stSidebar"] {
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
        }
        
        /* Make sidebar nav items touch-friendly */
        [data-testid="stSidebar"] .stRadio > div {
            gap: 8px !important;
        }
        
        [data-testid="stSidebar"] .stRadio label {
            padding: 14px 16px !important;
            min-height: 48px !important;
            font-size: 16px !important;
            display: flex !important;
            align-items: center !important;
            margin-bottom: 4px !important;
            border-radius: 8px !important;
            background: rgba(255,255,255,0.05) !important;
        }
        
        [data-testid="stSidebar"] .stRadio label:active {
            background: rgba(99, 102, 241, 0.3) !important;
        }
        
        /* Larger buttons for touch */
        .stButton > button {
            padding: 16px 24px !important;
            font-size: 16px !important;
            min-height: 52px !important;
            width: 100% !important;
            -webkit-tap-highlight-color: transparent;
        }
        
        /* Full-width inputs */
        .stTextInput, .stSelectbox, .stMultiSelect, .stNumberInput {
            width: 100% !important;
        }
        
        /* Stack columns vertically */
        [data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
            min-width: 100% !important;
        }
        
        /* Larger touch targets for multiselect */
        .stMultiSelect [data-baseweb="tag"] {
            padding: 10px 14px !important;
            font-size: 15px !important;
            min-height: 40px !important;
        }
        
        /* Make multiselect dropdown items bigger */
        [data-baseweb="popover"] li {
            padding: 14px 16px !important;
            min-height: 48px !important;
        }
        
        /* Bigger text for readability */
        .stMarkdown p, .stText {
            font-size: 16px !important;
        }
        
        /* Make metrics stack nicely */
        .stMetric {
            padding: 15px !important;
            margin-bottom: 10px !important;
        }
        
        /* Full-width progress bar */
        .stProgress {
            width: 100% !important;
        }
        
        /* Tabs - bigger touch targets */
        .stTabs [data-baseweb="tab"] {
            padding: 12px 16px !important;
            font-size: 14px !important;
            min-height: 44px !important;
        }
        
        /* Form submit buttons full width */
        [data-testid="stFormSubmitButton"] button {
            width: 100% !important;
            min-height: 52px !important;
        }
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


def api_post(endpoint: str, data: dict = None, long_timeout: bool = False):
    """Make POST request to API. Use long_timeout=True for video generation."""
    try:
        # Video generation can take 5+ minutes
        timeout = 600 if long_timeout else 30
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data or {}, timeout=timeout)
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
st.sidebar.caption(f"v0.7.0 | API: {API_BASE_URL[:40]}...")


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
    st.title("🎬 Video Management")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🤖 AI Generate", "📋 Video Library", "📤 Post to TikTok", "📁 Upload Manual", "📅 Scheduled Posts", "📊 Task Logs"])
    
    # ===== AI GENERATE TAB =====
    with tab1:
        st.subheader("🤖 AI Teamwork Video Generator")
        st.caption("Generate POV videos for teamwork trend using AI (Cost: ~$0.24/video)")
        
        col1, col2 = st.columns(2)
        with col1:
            video_count = st.number_input("Videos to Generate", min_value=1, max_value=20, value=3)
        with col2:
            video_style = st.selectbox(
                "Scene Style",
                ["Random (Mixed)", "Nature Park", "Beach", "Forest", "City", "Mountain"]
            )
        
        # Text overlay options
        text_overlay = st.selectbox(
            "Text Overlay",
            ["Random", "teamwork trend", "teamwork ifb", "teamwork makes the dream work", 
             "let's go teamwork", "teamwork challenge", "teamwork goals 💪"]
        )
        
        skip_overlay = st.checkbox("Skip text overlay (add later in TikTok editor)", value=False)
        
        # Cost estimate
        estimated_cost = video_count * 0.24
        st.info(f"💰 Estimated cost: **${estimated_cost:.2f}** for {video_count} videos")
        
        if st.button("🎥 Generate Videos", type="primary", use_container_width=True):
            # Map style selection
            style_map = {
                "Random (Mixed)": None,
                "Nature Park": "nature park",
                "Beach": "beach",
                "Forest": "forest",
                "City": "city",
                "Mountain": "mountain"
            }
            
            # Start job (returns immediately with job_id)
            if video_count == 1:
                result = api_post("/videos/generate", {
                    "style": style_map.get(video_style),
                    "text_overlay": None if text_overlay == "Random" else text_overlay,
                    "skip_overlay": skip_overlay
                })
            else:
                result = api_post("/videos/batch", {
                    "count": video_count,
                    "styles": [style_map.get(video_style)] if video_style != "Random (Mixed)" else None,
                    "skip_overlay": skip_overlay
                })
            
            if result and result.get("job_id"):
                job_id = result["job_id"]
                st.info(f"🚀 Video generation started! Job ID: **{job_id}**")
                st.markdown("⏳ Generating videos takes 2-5 minutes per video. Check the **Video Library** tab for results.")
                st.markdown(f"You can also poll status at: `/api/videos/job/{job_id}`")
            elif result:
                st.warning(f"Unexpected response: {result}")
    
    # ===== VIDEO LIBRARY TAB =====
    with tab2:
        st.subheader("📋 Generated Videos")
        
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🔄 Refresh", key="refresh_videos"):
                st.rerun()
        
        # Get generated videos from new API
        gen_videos = api_get("/videos/list")
        
        if gen_videos and gen_videos.get("videos"):
            st.write(f"**{gen_videos['count']} videos** in library")
            
            for vid in gen_videos["videos"]:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"**{vid['filename']}**")
                        st.caption(f"Size: {vid['size_mb']} MB | Created: {vid['created_at'][:16]}")
                    with col2:
                        # Download link
                        download_url = f"{API_BASE_URL}/videos/download/{vid['filename']}"
                        st.markdown(f"[📥 Download]({download_url})")
                    with col3:
                        # Preview toggle
                        if st.button("👁️ Preview", key=f"preview_{vid['filename']}"):
                            st.session_state[f"show_preview_{vid['filename']}"] = not st.session_state.get(f"show_preview_{vid['filename']}", False)
                    with col4:
                        if st.button("🗑️", key=f"del_{vid['filename']}"):
                            result = api_delete(f"/videos/{vid['filename']}")
                            if result and result.get("success"):
                                st.success("Deleted!")
                                st.rerun()
                    
                    # Show video preview if toggled
                    if st.session_state.get(f"show_preview_{vid['filename']}", False):
                        video_url = f"{API_BASE_URL}/videos/download/{vid['filename']}"
                        st.video(video_url)
                
                st.markdown("---")
        else:
            st.info("No videos generated yet. Use the 'AI Generate' tab to create teamwork videos!")
        
        # Also show old video library
        st.subheader("📁 Uploaded Videos (Legacy)")
        old_videos = api_get("/videos")
        if old_videos and old_videos.get("items"):
            for v in old_videos["items"]:
                col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 1, 1])
                with col1:
                    st.write(f"**#{v['id']}**")
                with col2:
                    st.write(v["filename"])
                with col3:
                    st.write("✅" if v["is_posted"] else "❌")
                with col4:
                    st.write(v.get("account_id") or "-")
                with col5:
                    if st.button("🗑️", key=f"del_legacy_{v['id']}"):
                        result = api_delete(f"/videos/legacy/{v['id']}")
                        if result:
                            st.success("Deleted!")
                            st.rerun()
        else:
            st.info("No legacy videos uploaded.")
    
    # ===== POST TO TIKTOK TAB =====
    with tab3:
        st.subheader("📤 Post Videos to TikTok")
        st.caption("Select videos and phones to post to TikTok via GeeLark")
        
        # Get available videos
        gen_videos = api_get("/videos/list")
        available_videos = []
        selected_videos = []  # Initialize to prevent NameError
        
        if gen_videos and gen_videos.get("videos"):
            available_videos = [v["filename"] for v in gen_videos["videos"]]
        
        if not available_videos:
            st.warning("No videos available. Generate videos in the 'AI Generate' tab first!")
        else:
            # Video selection
            selected_videos = st.multiselect(
                "Select Videos to Post",
                options=available_videos,
                default=available_videos[:1],  # Default to first video
                help="Choose which videos to post"
            )
            
            st.caption(f"📽️ {len(selected_videos)} video(s) selected")
        
        # Get phones
        phones = api_get("/geelark/phones")
        
        if phones and phones.get("items"):
            phone_options = {f"{p['serialName']} ({p['id'][:8]}...)": p['id'] for p in phones['items']}
            
            selected_phones = st.multiselect(
                "Select Phones",
                options=list(phone_options.keys()),
                help="Videos will be posted from these phones"
            )
            
            # Get caption
            caption_result = api_get("/videos/caption")
            if caption_result:
                st.write("**Suggested Caption:**")
                st.info(caption_result.get("full_description", ""))
                
                custom_caption = st.text_area(
                    "Custom Caption (or leave blank for random)",
                    value="",
                    placeholder=caption_result.get("caption", "")
                )
                
                hashtags = st.text_input(
                    "Hashtags",
                    value=caption_result.get("hashtags", "#teamwork #teamworktrend #fyp")
                )
            else:
                custom_caption = st.text_area("Caption", value="")
                hashtags = st.text_input("Hashtags", value="#teamwork #fyp #viral")
            
            st.markdown("---")
            
            # Status info
            can_post = selected_phones and available_videos and selected_videos
            
            if st.button("📤 Start Posting", type="primary", use_container_width=True, disabled=not can_post):
                phone_ids = [phone_options[p] for p in selected_phones]
                
                with st.spinner("Uploading videos and creating posting tasks..."):
                    result = api_post("/videos/post/batch", {
                        "videos": selected_videos,
                        "phone_ids": phone_ids,
                        "caption": custom_caption,
                        "hashtags": hashtags
                    })
                    
                    if result:
                        if result.get("successful", 0) > 0:
                            st.success(f"✅ Created {result['successful']} posting task(s)!")
                            
                            with st.expander("View Details"):
                                for r in result.get("results", []):
                                    if r.get("success"):
                                        st.write(f"✅ {r.get('video')} → {r.get('phone_id', '')[:8]}... (Task: {r.get('task_id', 'N/A')})")
                                    else:
                                        st.write(f"❌ {r.get('video')}: {r.get('error')}")
                        else:
                            st.error(f"❌ All tasks failed")
                            for r in result.get("results", []):
                                st.error(f"Error: {r.get('error')}")
                    else:
                        st.error("Failed to create posting tasks")
            
            if not can_post:
                if not selected_videos:
                    st.info("👆 Select videos to post")
                elif not selected_phones:
                    st.info("👆 Select phones to post from")
        else:
            st.warning("No phones available. Set up phones in the GeeLark page first.")
    
    # ===== UPLOAD MANUAL TAB =====
    with tab4:
        st.subheader("📁 Upload Video Manually")
        
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
    
    # ===== SCHEDULED POSTS TAB =====
    with tab5:
        st.subheader("📅 Automated Daily Video Posts")
        st.caption("Schedule automatic video generation and posting to TikTok")
        
        st.markdown("---")
        
        # Current schedule status
        st.write("**🕐 Current Schedule:**")
        col1, col2 = st.columns(2)
        with col1:
            st.info("🎥 **Video Generation:** Daily at 9:00 AM EST")
        with col2:
            st.info("📤 **Auto-Posting:** 10 AM, 1 PM, 5 PM EST")
        
        st.markdown("---")
        
        # Configuration
        st.write("**⚙️ Configuration:**")
        
        # Fetch phones for selection
        phones_data = api_get("/geelark/phones")
        available_phones = []
        if phones_data and phones_data.get("items"):
            available_phones = phones_data["items"]
        
        if available_phones:
            phone_options = {f"{p['serialName']} ({p['id'][:8]}...)": p['id'] for p in available_phones}
            
            # Phone selection (stored in session state)
            if "scheduled_phones" not in st.session_state:
                st.session_state.scheduled_phones = []
            
            selected_phones = st.multiselect(
                "📱 Phones for Daily Posting",
                options=list(phone_options.keys()),
                default=[k for k in phone_options.keys() if phone_options[k] in st.session_state.scheduled_phones],
                help="Select which phones should receive daily video posts"
            )
            
            # Update session state with selected phone IDs
            st.session_state.scheduled_phones = [phone_options[name] for name in selected_phones]
            
            if not selected_phones:
                st.warning("⚠️ Select at least one phone for automated posting")
        else:
            st.warning("⚠️ No phones available. Create phones in GeeLark first.")
            st.session_state.scheduled_phones = []
        
        col1, col2 = st.columns(2)
        with col1:
            daily_videos = st.number_input(
                "Videos to Generate Daily",
                min_value=1,
                max_value=10,
                value=3,
                help="Number of teamwork videos to generate each day"
            )
        with col2:
            posts_per_phone = st.number_input(
                "Posts per Phone per Day",
                min_value=1,
                max_value=5,
                value=1,
                help="How many times each phone should post daily"
            )
        
        # Estimated costs
        num_phones = len(st.session_state.get("scheduled_phones", [])) or 1
        daily_cost = daily_videos * 0.24
        monthly_cost = daily_cost * 30
        st.write(f"💰 **Estimated Cost:** ${daily_cost:.2f}/day (~${monthly_cost:.2f}/month)")
        st.caption(f"📱 {num_phones} phone(s) selected × {posts_per_phone} post(s)/day = {num_phones * posts_per_phone} total posts/day")
        
        st.markdown("---")
        
        # Manual triggers
        st.write("**🎮 Manual Controls:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎥 Generate Videos Now", use_container_width=True):
                result = api_post("/videos/batch", {
                    "count": daily_videos,
                    "styles": None,  # Random
                    "skip_overlay": False
                })
                if result and result.get("job_id"):
                    st.success(f"🚀 Generation started! Job ID: **{result['job_id']}**")
                    st.info("Check the **Video Library** tab in 2-5 minutes for results.")
                else:
                    st.error("Failed to start video generation")
        
        with col2:
            # Only enable if phones are selected and videos exist
            can_post = len(st.session_state.get("scheduled_phones", [])) > 0
            
            if st.button("📤 Post Now", use_container_width=True, disabled=not can_post):
                # Get available videos
                videos_resp = api_get("/videos/list")
                if videos_resp and videos_resp.get("videos"):
                    video_filenames = videos_resp["videos"][:3]  # Post up to 3
                    phone_ids = st.session_state.scheduled_phones
                    
                    with st.spinner(f"📤 Posting {len(video_filenames)} video(s) to {len(phone_ids)} phone(s)..."):
                        result = api_post("/videos/post/batch", {
                            "videos": video_filenames,
                            "phone_ids": phone_ids,
                            "caption": "",
                            "hashtags": "#teamwork #teamworktrend #fyp #viral",
                            "auto_start": True,
                            "auto_stop": True
                        }, long_timeout=True)
                        
                        if result and result.get("success"):
                            st.success(f"✅ Posted {result.get('successful', 0)}/{result.get('total', 0)} successfully!")
                            st.info("Check the **Task Logs** tab to monitor progress")
                        else:
                            st.error(f"Posting failed: {result}")
                else:
                    st.error("No videos available. Generate some first!")
            
            if not can_post:
                st.caption("⚠️ Select phones above to enable posting")
        
        st.markdown("---")
        
        # Scheduling Controls
        st.write("**📅 Scheduling Controls:**")
        
        # Initialize scheduling state
        if "scheduling_enabled" not in st.session_state:
            st.session_state.scheduling_enabled = False
        
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            if not st.session_state.scheduling_enabled:
                if st.button("✅ Enable Daily Scheduling", use_container_width=True, type="primary", 
                             disabled=not st.session_state.get("scheduled_phones")):
                    st.session_state.scheduling_enabled = True
                    st.success("🎉 Daily scheduling enabled!")
                    st.info(f"📱 Phones: {len(st.session_state.scheduled_phones)} | 🎥 Videos/day: {daily_videos} | 📤 Posts/phone: {posts_per_phone}")
                    st.rerun()
            else:
                st.success("✅ Scheduling is **ENABLED**")
        
        with col2:
            if st.session_state.scheduling_enabled:
                if st.button("⏹️ Disable Scheduling", use_container_width=True):
                    st.session_state.scheduling_enabled = False
                    st.warning("Scheduling disabled")
                    st.rerun()
        
        with col3:
            if st.session_state.scheduling_enabled:
                st.caption(f"📱 {len(st.session_state.get('scheduled_phones', []))} phones configured")
        
        if not st.session_state.get("scheduled_phones"):
            st.warning("⚠️ Select phones above before enabling scheduling")
        
        st.markdown("---")
        
        # Status info
        st.write("**📊 Status:**")
        gen_videos = api_get("/videos/list")
        if gen_videos:
            st.success(f"✅ {gen_videos.get('count', 0)} videos ready in library")
        else:
            st.warning("No videos generated yet")
        
        # Show scheduling log summary
        if st.session_state.scheduling_enabled:
            st.info("🔄 Next scheduled run: Check server logs for exact times")
    
    # ===== TASK LOGS TAB =====
    with tab6:
        st.subheader("📊 Video Posting Task Logs")
        st.caption("Monitor the status of video posting tasks (taskType=1)")
        
        # Refresh button
        if st.button("🔄 Refresh Task Status", key="refresh_video_tasks"):
            st.rerun()
        
        # Fetch tasks with task_type=1 (video posting)
        tasks_result = api_post("/geelark/tasks/query", {
            "task_type": 1,  # Video posting tasks only
            "page": 1,
            "page_size": 50
        })
        
        if tasks_result and tasks_result.get("items"):
            tasks = tasks_result["items"]
            
            # Status mapping
            status_map = {
                1: "⏳ Pending",
                2: "🔄 Running",
                3: "✅ Success",
                4: "❌ Failed",
                5: "⏸️ Cancelled"
            }
            
            # Create dataframe
            df_data = []
            for t in tasks:
                status = status_map.get(t.get("status"), f"Unknown ({t.get('status')})")
                created = t.get("createTime", "")
                if created:
                    try:
                        created = datetime.fromisoformat(created.replace("Z", "+00:00")).strftime("%m/%d %H:%M")
                    except:
                        pass
                
                df_data.append({
                    "Task ID": t.get("id", "")[:12] + "...",
                    "Phone": t.get("serialName", "Unknown"),
                    "Status": status,
                    "Description": (t.get("videoDesc", "") or "")[:50] + "..." if t.get("videoDesc") else "-",
                    "Created": created,
                    "Error": t.get("failReason", "-")
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Summary stats
            success_count = sum(1 for t in tasks if t.get("status") == 3)
            failed_count = sum(1 for t in tasks if t.get("status") == 4)
            pending_count = sum(1 for t in tasks if t.get("status") in [1, 2])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("✅ Success", success_count)
            with col2:
                st.metric("❌ Failed", failed_count)
            with col3:
                st.metric("⏳ Pending/Running", pending_count)
        else:
            st.info("No video posting tasks found. Post some videos to see task status here!")


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
    
    tab1, tab2, tab3, tab4 = st.tabs(["📱 Cloud Phones", "📋 Task History", "🔧 Task Management", "📅 Scheduled Warmups"])
    
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
            
            # Warmup Controls - Multi-select + Warmup Modes
            st.subheader("🔥 Run Warmup on Selected Phones")
            
            # Create dropdown options from phone list
            phone_options = {f"{p['serialName']} ({p['id'][:8]}...)": p['id'] for p in phones['items']}
            
            # Multi-select for phones (mobile-friendly: full width)
            selected_phones = st.multiselect(
                "Select Phones (can pick multiple)", 
                options=list(phone_options.keys()),
                help="Pick one or more phones to run warmup"
            )
            
            # Settings in columns (stacks on mobile)
            col1, col2 = st.columns(2)
            with col1:
                warmup_mode = st.selectbox(
                    "Warmup Mode",
                    options=["🚀 Enhanced Teamwork (+ Comments/Likes)", "🎯 Teamwork Trend (Search Only)", "📱 General FYP Browse"],
                    help="Enhanced: Chains warmup + comments + likes. Teamwork: Searches keywords. General: Just browses."
                )
            with col2:
                warmup_duration = st.number_input("Duration (min)", min_value=10, max_value=120, value=30)
            
            # Show advanced options for enhanced mode
            enhanced_mode = "Enhanced" in warmup_mode
            if enhanced_mode:
                st.caption("🔗 **Enhanced Mode** chains: Warmup → AI Comments → Random Likes")
                adv_col1, adv_col2 = st.columns(2)
                with adv_col1:
                    enable_comments = st.checkbox("Enable AI Comments", value=True, help="15% chance to leave relevant teamwork comments")
                with adv_col2:
                    enable_likes = st.checkbox("Enable Random Likes", value=True, help="30% chance to like videos")
            else:
                enable_comments = False
                enable_likes = False
            
            # Big mobile-friendly button
            if st.button("🔥 Run Warmup on Selected", type="primary", use_container_width=True):
                if selected_phones:
                    successes = []
                    failures = []
                    
                    # Determine warmup action based on mode
                    if "Enhanced" in warmup_mode or "Teamwork" in warmup_mode:
                        action = "search video"
                        keywords = ["teamwork trend", "teamwork challenge", "teamwork goals", "teamwork makes the dream work"]
                    else:
                        action = "browse video"
                        keywords = None
                    
                    # Progress bar for batch
                    progress = st.progress(0, text="Starting warmups...")
                    
                    for i, phone_name in enumerate(selected_phones):
                        phone_id = phone_options[phone_name]
                        result = api_post("/geelark/warmup/run", {
                            "phone_id": phone_id,
                            "duration_minutes": warmup_duration,
                            "action": action,
                            "keywords": keywords,
                            "enhanced": enhanced_mode,
                            "enable_comments": enable_comments,
                            "enable_likes": enable_likes
                        })
                        
                        if result and result.get("success"):
                            successes.append(phone_name)
                        else:
                            failures.append(f"{phone_name}: {result.get('message', 'Unknown') if result else 'API error'}")
                        
                        progress.progress((i + 1) / len(selected_phones), text=f"Started {i + 1}/{len(selected_phones)}")
                    
                    # Show results
                    if successes:
                        st.success(f"✅ Warmup started on {len(successes)} phone(s): {', '.join(successes)}")
                    if failures:
                        st.error(f"❌ Failed: {'; '.join(failures)}")
                else:
                    st.warning("Please select at least one phone!")
            
            st.caption("💡 **Teamwork Mode** searches for teamwork content. **General** just browses FYP. Stop warmups in Task History tab.")
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
            
            # Common failure codes for quick reference
            fail_codes = {
                20116: "Not logged in",
                20122: "TikTok start failed",
                20129: "Device offline",
                20124: "Homepage timeout",
                20109: "No network connection",
                20008: "Language not English",
                20003: "Execution timeout",
                29999: "Unknown error"
            }
            
            # GeeLark pricing: $0.007/min (base rate)
            COST_PER_MINUTE = 0.007
            
            def calc_usd_cost(cost_seconds):
                if cost_seconds and isinstance(cost_seconds, (int, float)):
                    return f"${(cost_seconds / 60 * COST_PER_MINUTE):.3f}"
                return "-"
            
            df = pd.DataFrame([{
                "Task ID": t["id"],
                "Type": task_types.get(t["taskType"], "Unknown"),
                "Phone": t["serialName"],
                "Status": statuses.get(t["status"], "Unknown"),
                "Fail Reason": fail_codes.get(t.get("failCode"), t.get("failDesc", "-")) if t["status"] == 4 else "-",
                "Time (s)": t.get("cost", "-"),
                "Cost (USD)": calc_usd_cost(t.get("cost"))
            } for t in history["items"]])
            
            st.dataframe(df, use_container_width=True)
            
            # Show cost summary
            total_seconds = sum(t.get("cost", 0) or 0 for t in history["items"])
            total_usd = total_seconds / 60 * COST_PER_MINUTE
            st.caption(f"💰 **Total usage shown:** {total_seconds:,}s ({total_seconds/60:.1f} min) = **${total_usd:.2f}** @ $0.007/min")
    
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
    
    with tab4:
        st.subheader("📅 Scheduled Daily Warmups")
        st.caption("Set up automatic warmups that run every day at the specified time.")
        
        # Initialize schedules in session state if not exists
        if "warmup_schedules" not in st.session_state:
            st.session_state.warmup_schedules = []
        
        # Fetch phones for schedule creation
        phones = api_get("/geelark/phones")
        
        if phones and phones.get("items"):
            phone_options = {f"{p['serialName']} ({p['id'][:8]}...)": p['id'] for p in phones['items']}
            
            st.markdown("### Create New Schedule")
            
            # Schedule creation form
            with st.form("create_schedule"):
                schedule_phones = st.multiselect(
                    "Select Phones for Schedule",
                    options=list(phone_options.keys()),
                    help="These phones will run warmup daily"
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    schedule_time = st.time_input("Daily Run Time", value=None)
                with col2:
                    schedule_duration = st.number_input("Duration (min)", min_value=15, max_value=120, value=30)
                with col3:
                    schedule_mode = st.selectbox(
                        "Warmup Mode",
                        options=["🎯 Teamwork Trend", "📱 General FYP"]
                    )
                
                submitted = st.form_submit_button("➕ Create Schedule", use_container_width=True)
                
                if submitted:
                    if schedule_phones and schedule_time:
                        new_schedule = {
                            "id": len(st.session_state.warmup_schedules) + 1,
                            "phones": schedule_phones,
                            "phone_ids": [phone_options[p] for p in schedule_phones],
                            "time": schedule_time.strftime("%H:%M"),
                            "duration": schedule_duration,
                            "mode": schedule_mode,
                            "enabled": True
                        }
                        st.session_state.warmup_schedules.append(new_schedule)
                        
                        # Also save to API for persistence
                        api_post("/warmup/schedules", new_schedule)
                        
                        st.success(f"✅ Schedule created! Daily at {schedule_time.strftime('%I:%M %p')}")
                        st.rerun()
                    else:
                        st.warning("Please select phones and a time!")
            
            # Display existing schedules
            if st.session_state.warmup_schedules:
                st.markdown("### Active Schedules")
                
                for i, schedule in enumerate(st.session_state.warmup_schedules):
                    with st.container():
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        
                        with col1:
                            status = "🟢" if schedule.get("enabled", True) else "🔴"
                            st.write(f"{status} **{schedule['time']}** - {len(schedule['phones'])} phone(s)")
                            st.caption(f"{schedule['mode']} | {schedule['duration']}min | {', '.join(schedule['phones'][:2])}{'...' if len(schedule['phones']) > 2 else ''}")
                        
                        with col2:
                            if st.button("▶️", key=f"run_{i}", help="Run now"):
                                # Trigger warmup immediately
                                for phone_name in schedule['phones']:
                                    phone_id = phone_options.get(phone_name)
                                    if phone_id:
                                        action = "search video" if "Teamwork" in schedule['mode'] else "browse video"
                                        keywords = ["teamwork trend", "teamwork challenge"] if "Teamwork" in schedule['mode'] else None
                                        api_post("/geelark/warmup/run", {
                                            "phone_id": phone_id,
                                            "duration_minutes": schedule['duration'],
                                            "action": action,
                                            "keywords": keywords
                                        })
                                st.success("Warmup triggered!")
                                st.rerun()
                        
                        with col3:
                            toggle_label = "⏸️" if schedule.get("enabled", True) else "▶️"
                            if st.button(toggle_label, key=f"toggle_{i}", help="Enable/Disable"):
                                st.session_state.warmup_schedules[i]["enabled"] = not schedule.get("enabled", True)
                                st.rerun()
                        
                        with col4:
                            if st.button("🗑️", key=f"delete_{i}", help="Delete"):
                                st.session_state.warmup_schedules.pop(i)
                                st.rerun()
                        
                        st.markdown("---")
            else:
                st.info("No schedules yet. Create one above!")
            
            st.markdown("---")
            st.caption("💡 **Note:** Schedules run automatically on the server. You can close your browser and they'll still execute. Check Task History for results.")
        else:
            st.info("No phones found. Add phones in GeeLark first!")


# Footer
st.sidebar.markdown("---")
st.sidebar.caption("TikTok Automation v0.1.0")
