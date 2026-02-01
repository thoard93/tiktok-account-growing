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

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

st.set_page_config(
    page_title="TikTok Automation",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
    }
    .status-active { color: #00ff00; }
    .status-warming { color: #ffaa00; }
    .status-banned { color: #ff0000; }
    .status-paused { color: #888888; }
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


# ===========================
# Sidebar Navigation
# ===========================

st.sidebar.title("📱 TikTok Automation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Dashboard", "👤 Accounts", "🔄 Warmup", "🎬 Videos", "🌐 Proxies", "📊 Logs", "⚙️ GeeLark"]
)


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
                "Followers": a["followers_count"],
                "Posts": a["posts_count"],
                "Warmup Day": a["warmup_day"],
                "Last Activity": a.get("last_activity", "-")
            } for a in accounts_data["items"]])
            
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            
            # Quick actions
            st.subheader("Quick Actions")
            col1, col2, col3, col4 = st.columns(4)
            
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
    st.title("Activity Logs")
    
    col1, col2 = st.columns(2)
    with col1:
        account_filter = st.number_input("Filter by Account ID", min_value=0, value=0)
    with col2:
        action_filter = st.selectbox(
            "Filter by Action",
            ["All", "account_created", "warmup_started", "warmup_session", 
             "warmup_completed", "video_posted", "phone_started", "phone_stopped"]
        )
    
    endpoint = "/logs?"
    if account_filter > 0:
        endpoint += f"account_id={account_filter}&"
    if action_filter != "All":
        endpoint += f"action_type={action_filter}&"
    
    logs = api_get(endpoint.rstrip("?&"))
    
    if logs and logs["items"]:
        for log in logs["items"]:
            status = "✅" if log["success"] else "❌"
            st.markdown(f"""
            **{status} {log['action_type']}** - Account #{log['account_id']}  
            *{log['created_at'][:19]}*
            """)
            if log.get("error_message"):
                st.error(f"Error: {log['error_message']}")
            st.markdown("---")
    else:
        st.info("No logs found.")


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
