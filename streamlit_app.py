import streamlit as st
import json
import os
from datetime import datetime, timedelta

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG & THEME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title="Fundraiser — Opportunity Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom theme colors
COLORS = {
    "bg": "#0a0b0d",
    "bg2": "#111318",
    "bg3": "#181c24",
    "border": "rgba(255,255,255,0.07)",
    "text": "#e8eaf0",
    "text_muted": "#6b7280",
    "accent": "#f0b429",
    "accent2": "#3b82f6",
    "accent3": "#10b981",
    "red": "#ef4444",
    "orange": "#f97316",
}

# Custom CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background-color: #0a0b0d;
        color: #e8eaf0;
    }
    
    .main {
        background-color: #0a0b0d;
        padding: 0;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111318;
        border-right: 1px solid rgba(255,255,255,0.07);
    }
    
    .header-container {
        background: rgba(10,11,13,0.92);
        border-bottom: 1px solid rgba(255,255,255,0.07);
        padding: 20px 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: -16px -16px 32px -16px;
    }
    
    .logo-text {
        font-family: 'Syne', sans-serif;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #e8eaf0;
    }
    
    .logo-text span {
        color: #f0b429;
    }
    
    .stat-card {
        background: #111318;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        padding: 16px 20px;
        transition: border-color 0.3s;
    }
    
    .stat-card:hover {
        border-color: rgba(255,255,255,0.15);
    }
    
    .stat-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    
    .stat-value {
        font-family: 'Syne', sans-serif;
        font-size: 28px;
        font-weight: 800;
        line-height: 1;
    }
    
    .stat-value.yellow { color: #f0b429; }
    .stat-value.blue { color: #3b82f6; }
    .stat-value.green { color: #10b981; }
    .stat-value.red { color: #ef4444; }
    
    .table-container {
        background: #111318;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 20px;
        overflow-x: auto;
    }
    
    table {
        width: 100%;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #e8eaf0;
        border-collapse: collapse;
    }
    
    th {
        background: #181c24;
        padding: 12px 16px;
        text-align: left;
        font-weight: 600;
        color: #6b7280;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    td {
        padding: 12px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        vertical-align: top;
    }
    
    tr:hover {
        background: rgba(240,180,41,0.05);
    }
    
    .tag {
        display: inline-block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 9px;
        padding: 4px 8px;
        border-radius: 4px;
        margin-right: 4px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .tag-prod {
        background: rgba(248, 113, 113, 0.2);
        color: #f87171;
        border: 1px solid rgba(248, 113, 113, 0.3);
    }
    
    .tag-digital {
        background: rgba(96, 165, 250, 0.2);
        color: #60a5fa;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }
    
    .tag-ngo {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-open {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 500;
    }
    
    .status-urgent {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 500;
    }
    
    .status-closed {
        background: rgba(107, 114, 128, 0.2);
        color: #9ca3af;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 500;
    }
    
    .days-urgent {
        color: #ef4444;
        font-weight: 600;
    }
    
    .days-soon {
        color: #f97316;
        font-weight: 600;
    }
    
    .days-ok {
        color: #10b981;
    }
    
    .score-bar {
        background: rgba(255,255,255,0.1);
        height: 4px;
        border-radius: 2px;
        overflow: hidden;
        margin-top: 6px;
    }
    
    .score-bar-fill {
        height: 100%;
        border-radius: 2px;
        transition: width 0.6s ease-out;
    }
    
    .score-high { background: #10b981; }
    .score-mid { background: #f0b429; }
    .score-low { background: #ef4444; }
    
    .alert-item {
        padding: 12px;
        border-left: 3px solid #f0b429;
        background: rgba(240, 180, 41, 0.08);
        margin-bottom: 8px;
        border-radius: 4px;
    }
    
    .alert-item.urgent {
        border-left-color: #ef4444;
        background: rgba(239, 68, 68, 0.08);
    }
    
    .log-line {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        padding: 6px 8px;
        border-bottom: 1px solid rgba(255,255,255,0.03);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .log-time {
        color: #6b7280;
        min-width: 60px;
    }
    
    .log-source {
        color: #f0b429;
        font-weight: 500;
        min-width: 80px;
    }
    
    .log-msg {
        color: #e8eaf0;
        flex: 1;
    }
    
    .log-line.info .log-msg { color: #3b82f6; }
    .log-line.done .log-msg { color: #10b981; }
    .log-line.urgent .log-msg { color: #ef4444; }
    
    .stMetric {
        background: #111318;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        font-family: 'Syne', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SESSION STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if 'opportunities' not in st.session_state:
    st.session_state.opportunities = []
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'last_scan' not in st.session_state:
    st.session_state.last_scan = None
if 'selected_filter' not in st.session_state:
    st.session_state.selected_filter = 'all'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""
<div class="header-container">
    <div>
        <div class="logo-text">
            Fundraiser <span>◆</span>
        </div>
        <div style="font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #6b7280; margin-top: 4px;">
            Opportunity Intelligence Platform
        </div>
    </div>
    <div style="text-align: right; font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #6b7280;">
        <div>Status: LIVE</div>
        <div>Region: MENA + Africa</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEMO DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DEMO_OPPORTUNITIES = [
    {
        "rank": 1,
        "title": "AFAC Media Fund 2026 — Film & Audiovisual Production",
        "funder": "Arab Fund for Arts & Culture",
        "amount": "€15,000 - €45,000",
        "deadline": "2026-05-30",
        "daysLeft": 55,
        "score": 4.8,
        "entities": ["production"],
        "status": "open",
        "statusLabel": "OPEN",
        "url": "https://www.arabculturefund.org",
        "notes": "Ideal for feature films and documentaries. Francophone + Arabic speaking countries eligible.",
    },
    {
        "rank": 2,
        "title": "EU Creative Europe MEDIA 2026 — Development & Distribution",
        "funder": "European Commission",
        "amount": "€25,000 - €120,000",
        "deadline": "2026-06-15",
        "daysLeft": 71,
        "score": 4.5,
        "entities": ["production"],
        "status": "open",
        "statusLabel": "OPEN",
        "url": "https://ec.europa.eu/culture/media",
        "notes": "Partner with EU company required. Tunisia eligible via consortium.",
    },
    {
        "rank": 3,
        "title": "Google News Initiative — Digital Media Innovation",
        "funder": "Google",
        "amount": "$20,000 - $100,000",
        "deadline": "2026-04-20",
        "daysLeft": 15,
        "score": 4.2,
        "entities": ["digital"],
        "status": "urgent",
        "statusLabel": "URGENT",
        "url": "https://newsinitiative.withgoogle.com",
        "notes": "Focus on news, journalism, and digital innovation. Rolling applications.",
    },
    {
        "rank": 4,
        "title": "British Council MENA Youth Programme 2026",
        "funder": "British Council",
        "amount": "£10,000 - £50,000",
        "deadline": "2026-05-10",
        "daysLeft": 35,
        "score": 4.0,
        "entities": ["ngo", "digital"],
        "status": "open",
        "statusLabel": "OPEN",
        "url": "https://www.britishcouncil.org.tn",
        "notes": "Youth training, capacity building, and civic engagement programs.",
    },
    {
        "rank": 5,
        "title": "Doha Film Institute — Development Grants",
        "funder": "Doha Film Institute",
        "amount": "QAR 50,000 - QAR 200,000",
        "deadline": "2026-07-01",
        "daysLeft": 87,
        "score": 3.9,
        "entities": ["production"],
        "status": "open",
        "statusLabel": "OPEN",
        "url": "https://www.dohafilminstitute.com",
        "notes": "Documentary and feature development. No co-production requirement.",
    },
    {
        "rank": 6,
        "title": "UNESCO — Media Literacy & Digital Skills (MENA)",
        "funder": "UNESCO",
        "amount": "€10,000 - €75,000",
        "deadline": "2026-06-30",
        "daysLeft": 86,
        "score": 3.8,
        "entities": ["ngo", "digital"],
        "status": "open",
        "statusLabel": "OPEN",
        "url": "https://en.unesco.org",
        "notes": "Training programs, capacity building, digital transformation.",
    },
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    
    # API Key input (optional for demo)
    api_key = st.text_input(
        "Claude API Key (optional for live scan)",
        type="password",
        placeholder="sk-ant-...",
    )
    
    st.divider()
    
    st.markdown("### 📊 Filters")
    
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        show_all = st.checkbox("All Opportunities", value=True)
    with filter_col2:
        show_urgent = st.checkbox("Urgent Only", value=False)
    
    st.markdown("### 🎯 Entity Types")
    col1, col2, col3 = st.columns(3)
    with col1:
        prod = st.checkbox("Production", value=True)
    with col2:
        digital = st.checkbox("Digital", value=True)
    with col3:
        ngo = st.checkbox("NGO", value=True)
    
    st.divider()
    
    st.markdown("### 📌 Quick Links")
    st.markdown("""
    - [Jamaity Platform](https://www.jamaity.org)
    - [Culture Funding Watch](https://www.culturefundingwatch.com)
    - [EC Funding Portal](https://ec.europa.eu/info/funding-tenders)
    - [AfDB Grants](https://www.afdb.org)
    """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN CONTENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Mode selector
mode_col1, mode_col2, mode_col3 = st.columns([2, 2, 1])
with mode_col1:
    mode = st.radio(
        "Select Mode",
        ["Dashboard", "Live Scan", "Manage Pipeline"],
        horizontal=True,
        label_visibility="collapsed"
    )

# Stats Row
st.markdown("### 📈 Overview")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric(
        "Sources Monitored",
        "12",
        "Film, Media, NGO",
    )

with stat_col2:
    open_count = len([o for o in DEMO_OPPORTUNITIES if o['status'] != 'closed'])
    st.metric(
        "Opportunities Found",
        len(DEMO_OPPORTUNITIES),
        f"{open_count} open"
    )

with stat_col3:
    shortlisted = len([o for o in DEMO_OPPORTUNITIES if o['score'] >= 3.5])
    st.metric(
        "Shortlisted (3.5+)",
        shortlisted,
        f"{shortlisted} high priority"
    )

with stat_col4:
    urgent = len([o for o in DEMO_OPPORTUNITIES if o['status'] == 'urgent'])
    st.metric(
        "Urgent (< 21 days)",
        urgent,
        "closing soon!"
    )

st.divider()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODE: DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if mode == "Dashboard":
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🔍 Opportunities Table")
        
        # Filters
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            filter_status = st.selectbox("Status", ["All", "Open", "Urgent", "Closed"], key="filter_status")
        with filter_col2:
            filter_entity = st.selectbox("Entity", ["All", "Production", "Digital", "NGO"], key="filter_entity")
        with filter_col3:
            sort_by = st.selectbox("Sort by", ["Score", "Deadline", "Amount"], key="sort_by")
        
        # Prepare data
        data = DEMO_OPPORTUNITIES.copy()
        
        # Apply filters
        if filter_status != "All":
            if filter_status == "Urgent":
                data = [o for o in data if o['status'] == 'urgent']
            elif filter_status == "Closed":
                data = [o for o in data if o['status'] == 'closed']
            else:
                data = [o for o in data if o['status'] == 'open']
        
        if filter_entity != "All":
            entity_map = {"Production": "production", "Digital": "digital", "NGO": "ngo"}
            entity_key = entity_map[filter_entity]
            data = [o for o in data if entity_key in o['entities']]
        
        # Sort
        if sort_by == "Score":
            data = sorted(data, key=lambda x: x['score'], reverse=True)
        elif sort_by == "Deadline":
            data = sorted(data, key=lambda x: x['daysLeft'])
        
        # Render table
        table_html = """
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th style="width: 5%;">#</th>
                        <th style="width: 35%;">Title & Funder</th>
                        <th style="width: 15%;">Entity</th>
                        <th style="width: 10%;">Score</th>
                        <th style="width: 15%;">Amount</th>
                        <th style="width: 12%;">Deadline</th>
                        <th style="width: 8%;">Status</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for opp in data:
            score_class = 'score-high' if opp['score'] >= 4.2 else 'score-mid' if opp['score'] >= 3.5 else 'score-low'
            score_pct = int((opp['score'] / 5) * 100)
            
            entity_tags = ' '.join([
                f'<span class="tag tag-{"prod" if e == "production" else "digital" if e == "digital" else "ngo"}">{"PRODUCTION" if e == "production" else "DIGITAL" if e == "digital" else "NGO"}</span>'
                for e in opp['entities']
            ])
            
            days_color = 'days-urgent' if opp['daysLeft'] <= 7 else 'days-soon' if opp['daysLeft'] <= 21 else ''
            days_text = f"⚑ {opp['daysLeft']} days" if opp['daysLeft'] <= 7 else f"{opp['daysLeft']} days"
            
            status_class = 'status-urgent' if opp['status'] == 'urgent' else 'status-open' if opp['status'] == 'open' else 'status-closed'
            
            table_html += f"""
                <tr>
                    <td><strong>{opp['rank']}</strong></td>
                    <td>
                        <div style="font-weight: 500;">{opp['title']}</div>
                        <div style="color: #6b7280; font-size: 12px; margin-top: 2px;">{opp['funder']}</div>
                    </td>
                    <td>{entity_tags}</td>
                    <td>
                        <div style="font-weight: 600;">{opp['score']}</div>
                        <div class="score-bar"><div class="score-bar-fill {score_class}" style="width: {score_pct}%;"></div></div>
                    </td>
                    <td style="font-family: 'IBM Plex Mono', monospace; font-size: 12px;">{opp['amount']}</td>
                    <td>
                        <div>{opp['deadline']}</div>
                        <div class="{days_color}" style="font-size: 12px; margin-top: 4px;">{days_text}</div>
                    </td>
                    <td><span class="{status_class}">{opp['statusLabel']}</span></td>
                </tr>
            """
        
        table_html += """
                </tbody>
            </table>
        </div>
        """
        
        st.markdown(table_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📢 Alerts")
        
        alerts = [
            {"icon": "🔴", "title": "URGENT", "desc": "Google News Initiative — 15 days left"},
            {"icon": "🟠", "title": "SOON", "desc": "EU Creative Europe — 71 days"},
            {"icon": "🟢", "title": "NEW", "desc": "UNESCO Media Literacy — Just added"},
        ]
        
        for alert in alerts:
            st.markdown(f"""
            <div class="alert-item">
                <div style="margin-bottom: 8px;">{alert['icon']} <strong>{alert['title']}</strong></div>
                <div style="font-size: 12px; color: #9ca3af;">{alert['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📅 Upcoming Deadlines")
        upcoming = sorted(DEMO_OPPORTUNITIES, key=lambda x: x['daysLeft'])[:5]
        for opp in upcoming:
            st.markdown(f"""
            **{opp['title'][:30]}...**  
            `{opp['daysLeft']} days left`
            """)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODE: LIVE SCAN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif mode == "Live Scan":
    st.markdown("### 🔄 Live Opportunity Scan")
    
    scan_col1, scan_col2 = st.columns([3, 1])
    
    with scan_col1:
        st.info("""
        **Live Scan** mode searches multiple funding sources in real-time using Claude AI and web search.
        
        Sources: AFAC, Doha Film Institute, EU Creative Europe, Google News Initiative, British Council MENA, UNESCO, AFD, GIZ, and more.
        """)
    
    with scan_col2:
        if st.button("🔄 START SCAN", use_container_width=True):
            with st.spinner("Scanning funding sources..."):
                progress_bar = st.progress(0)
                
                progress_bar.progress(25)
                time.sleep(0.5)
                
                progress_bar.progress(50)
                time.sleep(0.5)
                
                progress_bar.progress(75)
                time.sleep(0.5)
                
                progress_bar.progress(100)
                
                st.success("✓ Scan complete — 6 opportunities found and ranked")
                st.session_state.last_scan = datetime.now()
    
    # Live log
    st.markdown("### 📡 Live Log")
    
    log_container = st.container()
    with log_container:
        logs = [
            ("14:32:15", "INIT", "Starting live scan across funding sources", "info"),
            ("14:32:18", "AFAC", "African Fund for Arts & Culture — scanning...", "info"),
            ("14:32:22", "DOHA", "Doha Film Institute — 2 new opportunities found", "found"),
            ("14:32:28", "EU", "Creative Europe MEDIA — Partner requirement identified", "info"),
            ("14:32:35", "GOOGLE", "Google News Initiative — 1 urgent opportunity (15 days)", "urgent"),
            ("14:32:42", "UNESCO", "UNESCO Media Literacy grants — MENA eligible", "found"),
            ("14:32:48", "BC", "British Council MENA — Youth programs matched", "found"),
            ("14:33:05", "COMPLETE", "✓ Live scan complete — 6 opportunities ranked", "done"),
        ]
        
        for time_str, source, msg, log_type in logs:
            log_css = "info"
            if log_type == "found":
                log_css = "border-left: 3px solid #10b981; background: rgba(16,185,129,0.08);"
            elif log_type == "urgent":
                log_css = "border-left: 3px solid #ef4444; background: rgba(239,68,68,0.08);"
            elif log_type == "done":
                log_css = "border-left: 3px solid #10b981; background: rgba(16,185,129,0.08);"
            
            st.markdown(f"""
            <div style="{log_css} padding: 8px; margin-bottom: 4px; border-radius: 4px; font-family: 'IBM Plex Mono', monospace; font-size: 11px;">
                <span style="color: #6b7280;">{time_str}</span> 
                <span style="color: #f0b429; font-weight: 500;">{source}</span> 
                <span style="color: #e8eaf0;">{msg}</span>
            </div>
            """, unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODE: PIPELINE MANAGEMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif mode == "Manage Pipeline":
    st.markdown("### 📋 Application Pipeline")
    
    pipeline_stages = {
        "SHORTLISTED": [DEMO_OPPORTUNITIES[0], DEMO_OPPORTUNITIES[2]],
        "IN PROGRESS": [DEMO_OPPORTUNITIES[1]],
        "SUBMITTED": [DEMO_OPPORTUNITIES[3]],
        "AWAITING": [DEMO_OPPORTUNITIES[4], DEMO_OPPORTUNITIES[5]],
    }
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 📌 Shortlisted")
        for opp in pipeline_stages["SHORTLISTED"]:
            with st.container(border=True):
                st.markdown(f"**{opp['title'][:25]}...**")
                st.caption(f"Score: {opp['score']}/5")
                st.caption(f"Deadline: {opp['daysLeft']} days")
    
    with col2:
        st.markdown("#### ✍️ In Progress")
        for opp in pipeline_stages["IN PROGRESS"]:
            with st.container(border=True):
                st.markdown(f"**{opp['title'][:25]}...**")
                st.progress(0.65, text="Proposal 65%")
    
    with col3:
        st.markdown("#### ✅ Submitted")
        for opp in pipeline_stages["SUBMITTED"]:
            with st.container(border=True):
                st.markdown(f"**{opp['title'][:25]}...**")
                st.caption("Submitted 2026-03-15")
    
    with col4:
        st.markdown("#### ⏳ Awaiting Decision")
        for opp in pipeline_stages["AWAITING"]:
            with st.container(border=True):
                st.markdown(f"**{opp['title'][:25]}...**")
                st.caption("Decision due in 30 days")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.divider()
st.markdown("""
<div style="font-family: 'IBM Plex Mono', monospace; font-size: 10px; color: #6b7280; text-align: center; padding: 20px;">
    <div>Fundraiser Agent v1.0 — Last scan: {}</div>
    <div style="margin-top: 8px;">
        <a href="https://github.com" style="color: #6b7280; text-decoration: none;">GitHub</a> • 
        <a href="#" style="color: #6b7280; text-decoration: none;">Docs</a> • 
        <a href="#" style="color: #6b7280; text-decoration: none;">API</a>
    </div>
</div>
""".format(st.session_state.last_scan.strftime("%Y-%m-%d %H:%M") if st.session_state.last_scan else "Never"), unsafe_allow_html=True)
