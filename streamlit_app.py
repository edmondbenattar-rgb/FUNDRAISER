import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Fundraiser — Opportunity Intelligence",
    page_icon="\U0001f3af",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove all Streamlit chrome so the custom HTML takes over
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header[data-testid="stHeader"] {display: none;}
    footer {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
    [data-testid="stVerticalBlock"] { gap: 0 !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fundraiser — Opportunity Intelligence</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@300;400;500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0b0d;
    --bg2: #111318;
    --bg3: #181c24;
    --border: rgba(255,255,255,0.07);
    --border-bright: rgba(255,255,255,0.15);
    --text: #e8eaf0;
    --text-muted: #6b7280;
    --text-dim: #3a3f4a;
    --accent: #f0b429;
    --accent2: #3b82f6;
    --accent3: #10b981;
    --red: #ef4444;
    --orange: #f97316;
    --purple: #a78bfa;
    --mono: 'IBM Plex Mono', monospace;
    --display: 'Syne', sans-serif;
    --body: 'Inter', sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--body);
    font-size: 14px;
    line-height: 1.6;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Grain overlay */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    opacity: 0.4;
  }

  /* Layout */
  .shell {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 32px;
  }

  /* Header */
  header {
    border-bottom: 1px solid var(--border);
    padding: 20px 0;
    position: sticky;
    top: 0;
    background: rgba(10,11,13,0.92);
    backdrop-filter: blur(12px);
    z-index: 100;
  }

  .header-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .logo {
    font-family: var(--display);
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .logo-dot {
    width: 8px; height: 8px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
  }

  @keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.7); }
  }

  .logo span { color: var(--accent); }
  .logo-gaddour { color: var(--red); }

  .header-meta {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    text-align: right;
    line-height: 1.8;
  }

  /* Mode toggle */
  .mode-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
  }

  .mode-label {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .toggle-wrap {
    display: flex;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: hidden;
  }

  .toggle-btn {
    padding: 6px 16px;
    font-family: var(--mono);
    font-size: 11px;
    cursor: pointer;
    border: none;
    background: transparent;
    color: var(--text-muted);
    transition: all 0.2s;
    letter-spacing: 0.5px;
  }

  .toggle-btn.active {
    background: var(--accent);
    color: #000;
    font-weight: 500;
  }

  .api-key-wrap {
    display: none;
    align-items: center;
    gap: 8px;
    margin-left: 16px;
    flex: 1;
    max-width: 400px;
  }

  .api-key-wrap.visible { display: flex; }

  .api-input {
    flex: 1;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 12px;
    color: var(--text);
    font-family: var(--mono);
    font-size: 11px;
    outline: none;
    transition: border-color 0.2s;
  }

  .api-input:focus { border-color: var(--accent2); }
  .api-input::placeholder { color: var(--text-dim); }

  /* Main scan button */
  .scan-btn {
    margin-left: auto;
    padding: 8px 24px;
    background: var(--accent);
    color: #000;
    border: none;
    border-radius: 6px;
    font-family: var(--display);
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: 0.3px;
  }

  .scan-btn:hover { background: #f5c842; transform: translateY(-1px); }
  .scan-btn:active { transform: translateY(0); }
  .scan-btn:disabled { background: var(--text-dim); color: var(--text-muted); cursor: not-allowed; transform: none; }

  .btn-icon { font-size: 14px; }

  /* Stats row */
  .stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 32px;
  }

  .stat-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    transition: border-color 0.3s;
  }

  .stat-card:hover { border-color: var(--border-bright); }

  .stat-label {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
  }

  .stat-value {
    font-family: var(--display);
    font-size: 28px;
    font-weight: 800;
    line-height: 1;
  }

  .stat-value.yellow { color: var(--accent); }
  .stat-value.blue { color: var(--accent2); }
  .stat-value.green { color: var(--accent3); }
  .stat-value.red { color: var(--red); }

  .stat-sub {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    margin-top: 4px;
  }

  /* Two-col layout */
  .main-grid {
    display: grid;
    grid-template-columns: 1fr 340px;
    gap: 24px;
    margin-bottom: 32px;
  }

  /* Live feed */
  .panel {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }

  .panel-header {
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .panel-title {
    font-family: var(--display);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.3px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .live-indicator {
    width: 6px; height: 6px;
    background: var(--accent3);
    border-radius: 50%;
  }

  .live-indicator.scanning {
    animation: blink 0.8s ease-in-out infinite;
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
  }

  .panel-badge {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-muted);
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 2px 8px;
  }

  /* Feed log */
  .feed-log {
    padding: 16px 20px;
    height: 280px;
    overflow-y: auto;
    font-family: var(--mono);
    font-size: 11.5px;
    line-height: 1.9;
    color: var(--text-muted);
  }

  .feed-log::-webkit-scrollbar { width: 4px; }
  .feed-log::-webkit-scrollbar-track { background: transparent; }
  .feed-log::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }

  .log-line {
    display: flex;
    gap: 10px;
    animation: fadeSlideIn 0.3s ease forwards;
    opacity: 0;
  }

  @keyframes fadeSlideIn {
    from { opacity: 0; transform: translateX(-6px); }
    to { opacity: 1; transform: translateX(0); }
  }

  .log-time { color: var(--text-dim); min-width: 50px; }
  .log-source { color: var(--accent2); min-width: 130px; }
  .log-msg { color: var(--text-muted); }
  .log-line.found .log-msg { color: var(--accent3); }
  .log-line.urgent .log-msg { color: var(--orange); }
  .log-line.done .log-msg { color: var(--accent); }
  .log-line.info .log-msg { color: var(--text-muted); }

  /* Alerts panel */
  .alerts-panel {
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .alert-item {
    padding: 14px 18px;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 12px;
    align-items: flex-start;
    transition: background 0.2s;
  }

  .alert-item:last-child { border-bottom: none; }
  .alert-item:hover { background: rgba(255,255,255,0.02); }

  .alert-icon { font-size: 14px; margin-top: 1px; flex-shrink: 0; }

  .alert-content {}

  .alert-title {
    font-family: var(--display);
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 3px;
    color: var(--text);
  }

  .alert-desc {
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.5;
  }

  .alert-item.urgent { border-left: 2px solid var(--red); }
  .alert-item.warn { border-left: 2px solid var(--orange); }
  .alert-item.info { border-left: 2px solid var(--accent2); }
  .alert-item.good { border-left: 2px solid var(--accent3); }

  /* Results table section */
  .results-section { margin-bottom: 32px; }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
  }

  .section-title {
    font-family: var(--display);
    font-size: 18px;
    font-weight: 800;
    letter-spacing: -0.3px;
  }

  .section-title span { color: var(--accent); }

  .filter-row {
    display: flex;
    gap: 8px;
  }

  .filter-chip {
    padding: 4px 12px;
    border-radius: 20px;
    border: 1px solid var(--border);
    font-family: var(--mono);
    font-size: 10px;
    cursor: pointer;
    color: var(--text-muted);
    background: transparent;
    transition: all 0.2s;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }

  .filter-chip:hover, .filter-chip.active {
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
  }

  /* Table */
  .table-wrap {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }

  thead tr {
    border-bottom: 1px solid var(--border-bright);
  }

  th {
    padding: 12px 16px;
    font-family: var(--mono);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-dim);
    text-align: left;
    font-weight: 500;
    white-space: nowrap;
  }

  th.sortable { cursor: pointer; user-select: none; }
  th.sortable:hover { color: var(--text-muted); }

  tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
    animation: rowIn 0.4s ease forwards;
    opacity: 0;
  }

  @keyframes rowIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  tbody tr:last-child { border-bottom: none; }
  tbody tr:hover { background: rgba(255,255,255,0.025); }

  td {
    padding: 14px 16px;
    vertical-align: middle;
  }

  /* Rank cell */
  .rank-cell {
    font-family: var(--display);
    font-size: 20px;
    font-weight: 800;
    color: var(--text-dim);
    width: 40px;
  }

  .rank-cell.top { color: var(--accent); }

  /* Title cell */
  .opp-title {
    font-family: var(--display);
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 3px;
    color: var(--text);
  }

  .opp-funder {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-muted);
  }

  /* Notes cell */
  .opp-notes {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    line-height: 1.55;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    max-width: 260px;
  }

  td.notes-cell {
    vertical-align: top;
    padding-top: 16px;
  }

  /* Donor cell */
  .opp-donor {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--accent2);
    line-height: 1.5;
  }

  /* Duration cell */
  .duration-val {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text-muted);
    white-space: nowrap;
  }

  .duration-na {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
  }

  /* Countdown cell */
  .countdown-wrap {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 3px;
  }

  .countdown-num {
    font-family: var(--display);
    font-size: 18px;
    font-weight: 800;
    line-height: 1;
  }

  .countdown-label {
    font-family: var(--mono);
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-dim);
  }

  .countdown-urgent { color: var(--red); }
  .countdown-soon   { color: var(--orange); }
  .countdown-ok     { color: var(--accent3); }
  .countdown-closed { color: var(--text-dim); text-decoration: line-through; }

  /* Entity tags */
  .tag {
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 4px;
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.3px;
    margin: 1px 2px;
    white-space: nowrap;
  }

  .tag-prod { background: rgba(167,139,250,0.12); color: var(--purple); border: 1px solid rgba(167,139,250,0.25); }
  .tag-digital { background: rgba(59,130,246,0.12); color: var(--accent2); border: 1px solid rgba(59,130,246,0.25); }
  .tag-ngo { background: rgba(16,185,129,0.12); color: var(--accent3); border: 1px solid rgba(16,185,129,0.25); }

  /* Score bar */
  .score-wrap {
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
  }

  .score-num {
    font-family: var(--display);
    font-size: 15px;
    font-weight: 800;
    min-width: 30px;
    color: var(--text);
  }

  .score-bar-bg {
    width: 60px;
    height: 4px;
    background: var(--bg3);
    border-radius: 2px;
    overflow: hidden;
  }

  .score-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1s ease 0.5s;
    width: 0;
  }

  .score-bar-fill.high { background: var(--accent3); }
  .score-bar-fill.mid { background: var(--accent); }
  .score-bar-fill.low { background: var(--red); }

  /* Deadline cell */
  .deadline-wrap {}

  .deadline-date {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text);
  }

  .deadline-days {
    font-family: var(--mono);
    font-size: 10px;
    margin-top: 2px;
  }

  .days-urgent { color: var(--red); font-weight: 500; }
  .days-soon { color: var(--orange); }
  .days-ok { color: var(--accent3); }
  .days-closed { color: var(--text-dim); text-decoration: line-through; }

  /* Amount */
  .amount {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--text);
    white-space: nowrap;
  }

  /* Status badge */
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: var(--mono);
    font-size: 10px;
    font-weight: 500;
    white-space: nowrap;
    letter-spacing: 0.3px;
  }

  .status-badge::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .status-open { background: rgba(16,185,129,0.1); color: var(--accent3); border: 1px solid rgba(16,185,129,0.2); }
  .status-open::before { background: var(--accent3); }
  .status-urgent { background: rgba(239,68,68,0.1); color: var(--red); border: 1px solid rgba(239,68,68,0.2); }
  .status-urgent::before { background: var(--red); animation: blink 0.8s infinite; }
  .status-closed { background: rgba(107,114,128,0.1); color: var(--text-dim); border: 1px solid var(--border); }
  .status-closed::before { background: var(--text-dim); }
  .status-flagged { background: rgba(240,180,41,0.1); color: var(--accent); border: 1px solid rgba(240,180,41,0.2); }
  .status-flagged::before { background: var(--accent); }

  /* Link button */
  .link-btn {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 12px;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 5px;
    color: var(--text-muted);
    font-family: var(--mono);
    font-size: 10px;
    text-decoration: none;
    transition: all 0.2s;
    white-space: nowrap;
    cursor: pointer;
  }

  .link-btn:hover {
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
  }

  /* Empty state */
  .empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-dim);
  }

  .empty-state .big-icon { font-size: 40px; margin-bottom: 12px; opacity: 0.4; }

  .empty-state p {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--text-dim);
  }

  /* Loading spinner for scan button */
  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .spinner {
    width: 12px; height: 12px;
    border: 2px solid rgba(0,0,0,0.3);
    border-top-color: #000;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
  }

  /* Progress bar */
  .progress-wrap {
    padding: 0 20px 16px;
    display: none;
  }

  .progress-wrap.visible { display: block; }

  .progress-label {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-muted);
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
  }

  .progress-bg {
    height: 2px;
    background: var(--bg3);
    border-radius: 1px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: var(--accent);
    width: 0%;
    transition: width 0.4s ease;
    border-radius: 1px;
  }

  /* Footer */
  footer {
    border-top: 1px solid var(--border);
    padding: 20px 0;
    margin-top: 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .footer-left {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    line-height: 1.8;
  }

  .footer-right {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--text-dim);
    text-align: right;
    line-height: 1.8;
  }

  /* Responsive */
  @media (max-width: 900px) {
    .main-grid { grid-template-columns: 1fr; }
    .stats-row { grid-template-columns: repeat(2, 1fr); }
    .shell { padding: 0 16px; }
  }
</style>
</head>
<body>

<header>
  <div class="shell">
    <div class="header-inner">
      <div class="logo">
        <div class="logo-dot"></div>
        FUND<span>RAISER</span> &nbsp;<span class="logo-gaddour">GADDOUR</span>
      </div>
      <div class="header-meta">
        <div id="clock">—</div>
        <div>Tunis, TN · v1.0 MVP</div>
      </div>
    </div>
  </div>
</header>

<div class="shell" style="padding-top:24px;">

  <!-- Mode bar -->
  <div class="mode-bar">
    <span class="mode-label">Mode</span>
    <div class="toggle-wrap">
      <button class="toggle-btn active" id="btn-demo" onclick="setMode('demo')">◉ DEMO</button>
      <button class="toggle-btn" id="btn-live" onclick="setMode('live')">⚡ LIVE</button>
    </div>
    <div class="api-key-wrap" id="api-key-wrap">
      <input class="api-input" type="password" id="api-key" placeholder="sk-ant-api03-… (your Anthropic API key)">
      <span style="font-family:var(--mono);font-size:10px;color:var(--text-dim);">stored in memory only</span>
    </div>
    <button class="scan-btn" id="scan-btn" onclick="startScan()">
      <span class="btn-icon">⟳</span> SCAN OPPORTUNITIES
    </button>
  </div>

  <!-- Stats -->
  <div class="stats-row">
    <div class="stat-card">
      <div class="stat-label">Sources Scanned</div>
      <div class="stat-value yellow" id="stat-sources">0</div>
      <div class="stat-sub" id="stat-sources-sub">awaiting scan</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Opportunities Found</div>
      <div class="stat-value blue" id="stat-found">0</div>
      <div class="stat-sub" id="stat-found-sub">awaiting scan</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Shortlisted</div>
      <div class="stat-value green" id="stat-shortlisted">0</div>
      <div class="stat-sub" id="stat-shortlisted-sub">score ≥ 3.5/5</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Urgent (≤7 days)</div>
      <div class="stat-value red" id="stat-urgent">0</div>
      <div class="stat-sub" id="stat-urgent-sub">action required</div>
    </div>
  </div>

  <!-- Main grid: feed + alerts -->
  <div class="main-grid">

    <!-- Feed panel -->
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">
          <div class="live-indicator" id="live-dot"></div>
          SCAN LOG
        </div>
        <span class="panel-badge" id="feed-badge">IDLE</span>
      </div>
      <div class="progress-wrap" id="progress-wrap">
        <div class="progress-label">
          <span id="progress-source">Initializing…</span>
          <span id="progress-pct">0%</span>
        </div>
        <div class="progress-bg"><div class="progress-fill" id="progress-fill"></div></div>
      </div>
      <div class="feed-log" id="feed-log">
        <div style="color:var(--text-dim);font-size:11px;padding-top:8px;">
          Press SCAN to begin opportunity discovery.<br>
          Demo mode replays last scan. Live mode calls Claude API in real time.
        </div>
      </div>
    </div>

    <!-- Alerts panel -->
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">⚑ PIPELINE ALERTS</div>
        <span class="panel-badge" id="alerts-count">0</span>
      </div>
      <div class="alerts-panel" id="alerts-panel">
        <div style="padding:20px;font-family:var(--mono);font-size:11px;color:var(--text-dim);">
          No alerts yet. Run a scan to populate.
        </div>
      </div>
    </div>

  </div>

  <!-- Results table -->
  <div class="results-section" id="results-section">
    <div class="section-header">
      <div class="section-title">RANKED <span>OPPORTUNITIES</span></div>
      <div class="filter-row">
        <button class="filter-chip active" onclick="filterTable('all', this)">ALL</button>
        <button class="filter-chip" onclick="filterTable('production', this)">PRODUCTION</button>
        <button class="filter-chip" onclick="filterTable('digital', this)">DIGITAL</button>
        <button class="filter-chip" onclick="filterTable('ngo', this)">NGO</button>
        <button class="filter-chip" onclick="filterTable('urgent', this)">URGENT</button>
      </div>
    </div>
    <div class="table-wrap">
      <table id="results-table">
        <thead>
          <tr>
            <th style="width:3%;">#</th>
            <th style="width:16%;">OPPORTUNITY</th>
            <th style="width:10%;">DONOR</th>
            <th style="width:18%;">NOTES</th>
            <th style="width:8%;">ENTITY FIT</th>
            <th style="width:6%;" class="sortable" onclick="sortByScore()">SCORE ↕</th>
            <th style="width:10%;">AMOUNT</th>
            <th style="width:8%;">DURATION</th>
            <th style="width:9%;">DEADLINE</th>
            <th style="width:7%;">COUNTDOWN</th>
            <th style="width:7%;">STATUS</th>
            <th style="width:3%;">↗</th>
          </tr>
        </thead>
        <tbody id="table-body">
          <tr>
            <td colspan="12">
              <div class="empty-state">
                <div class="big-icon">◎</div>
                <p>No results yet — press SCAN OPPORTUNITIES to begin</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

</div><!-- /shell -->

<footer>
  <div class="shell" style="width:100%;display:flex;justify-content:space-between;align-items:center;">
    <div class="footer-left">
      FUNDRAISER v1.0 · Opportunity Intelligence for Tunisian Media &amp; Social Impact<br>
      Entities: Production Agency · Digital Media (×2) · NGO
    </div>
    <div class="footer-right">
      Sources: Jamaity · AFAC · UNESCO · CFW · EU · UN agencies<br>
      Last scan: <span id="last-scan-time">never</span>
    </div>
  </div>
</footer>

<script>
// ═══════════════════════════════════════════════════════
// CLOCK
// ═══════════════════════════════════════════════════════
function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent =
    now.toLocaleDateString('en-GB', {day:'2-digit',month:'short',year:'numeric'}) + ' · ' +
    now.toLocaleTimeString('en-GB', {hour:'2-digit',minute:'2-digit',second:'2-digit'});
}
setInterval(updateClock, 1000);
updateClock();

// ═══════════════════════════════════════════════════════
// AUTO-LOAD EXISTING RESULTS ON PAGE OPEN
// ═══════════════════════════════════════════════════════
window.addEventListener('DOMContentLoaded', () => {
  // Try to restore last live scan from localStorage (persists across refreshes)
  let restored = false;
  try {
    const saved = localStorage.getItem('fundraiser:last-scan');
    if (saved) {
      const scan = JSON.parse(saved);
      if (scan.data && scan.data.length > 0) {
        allData = scan.data;
        renderTable(allData);
        renderAlerts(scan.alerts && scan.alerts.length ? scan.alerts : DEMO_ALERTS);
        animateCounter('stat-sources', scan.sources || 1);
        animateCounter('stat-found', allData.length);
        animateCounter('stat-shortlisted', allData.filter(o => o.score >= 3.5).length);
        animateCounter('stat-urgent', allData.filter(o => o.status === 'urgent').length);
        document.getElementById('stat-sources-sub').textContent = scan.sourcesList || 'jamaity';
        document.getElementById('stat-found-sub').textContent = 'across all sources';
        document.getElementById('stat-shortlisted-sub').textContent = 'score ≥ 3.5/5';
        document.getElementById('alerts-count').textContent = String((scan.alerts || DEMO_ALERTS).length);
        const urgentOppR = allData.find(o => o.status === 'urgent');
        document.getElementById('stat-urgent-sub').textContent = urgentOppR
          ? urgentOppR.title.substring(0, 25) + ' — ' + (urgentOppR.daysLeft > 0 ? urgentOppR.daysLeft + ' days' : 'CLOSED')
          : 'none this cycle';
        document.getElementById('last-scan-time').textContent = scan.scanTime || 'unknown';
        document.getElementById('feed-badge').textContent = 'LAST LIVE SCAN';
        addLogLine('SYSTEM', '✓ Live scan restored from localStorage (' + allData.length + ' results)', 'done');
        addLogLine('SYSTEM', 'Sources: ' + (scan.sourcesList || 'jamaity') + ' — scanned ' + (scan.scanTime || ''), 'info');
        restored = true;
      }
    }
  } catch(e) { /* no saved scan or parse error — fall through to demo */ }

  if (!restored) {
    // No saved scan — show demo data
    allData = DEMO_OPPORTUNITIES;
    renderTable(allData);
    renderAlerts(DEMO_ALERTS);
    animateCounter('stat-sources', 6);
    animateCounter('stat-found', 5);
    animateCounter('stat-shortlisted', 5);
    animateCounter('stat-urgent', DEMO_OPPORTUNITIES.filter(o => o.status === 'urgent').length);
    document.getElementById('stat-sources-sub').textContent = 'jamaity, afac, unesco, cfw, eu, coe';
    document.getElementById('stat-found-sub').textContent = 'across all sources';
    const urgentOpp0 = DEMO_OPPORTUNITIES.find(o => o.status === 'urgent');
    const urgentSub0 = urgentOpp0
      ? urgentOpp0.title.substring(0, 25) + ' — ' + (urgentOpp0.daysLeft > 0 ? urgentOpp0.daysLeft + ' days' : 'CLOSED')
      : 'none this cycle';
    document.getElementById('stat-urgent-sub').textContent = urgentSub0;
    document.getElementById('alerts-count').textContent = DEMO_ALERTS.length.toString();
    const loadDate = new Date();
    const loadDateStr = loadDate.toLocaleDateString('en-GB', {day:'2-digit',month:'short',year:'numeric'});
    document.getElementById('last-scan-time').textContent = '05 Apr 2026 (loaded ' + loadDateStr + ')';
    document.getElementById('feed-badge').textContent = 'LAST SCAN: 05 APR 2026';
    const summaryLines = [
      { source:'SYSTEM',   msg:'Last scan loaded — 05 April 2026', type:'done' },
      { source:'JAMAITY',  msg:'3 opportunities found (CoE, Fablabs, Pouvoir d\'Agir)', type:'found' },
      { source:'AFAC',     msg:'Documentary Film Grant — deadline passed (−3 days)', type:'urgent' },
      { source:'UNESCO',   msg:'IFCD Cultural Diversity — deadline 6 May 2026', type:'found' },
      { source:'CFW',      msg:'Pro database requires subscription — partial scan', type:'info' },
      { source:'SCORING',  msg:'5 shortlisted · 1 urgent · 1 flagged for Cycle 2', type:'done' },
    ];
    summaryLines.forEach((l, i) => {
      setTimeout(() => addLogLine(l.source, l.msg, l.type), i * 120);
    });
  }
});

// ═══════════════════════════════════════════════════════
// MODE
// ═══════════════════════════════════════════════════════
let currentMode = 'demo';

function setMode(mode) {
  currentMode = mode;
  document.getElementById('btn-demo').classList.toggle('active', mode === 'demo');
  document.getElementById('btn-live').classList.toggle('active', mode === 'live');
  const apiWrap = document.getElementById('api-key-wrap');
  if (mode === 'live') {
    apiWrap.classList.add('visible');
  } else {
    apiWrap.classList.remove('visible');
  }
}

// ═══════════════════════════════════════════════════════
// DEMO DATA — results from actual scan session
// ═══════════════════════════════════════════════════════
// ── Helper: compute days left from ISO deadline string ──────────────────────
function daysFromNow(isoDate) {
  const today = new Date(); today.setHours(0,0,0,0);
  const d     = new Date(isoDate); d.setHours(0,0,0,0);
  return Math.round((d - today) / 86400000);
}

// ── Helper: derive live status from days left ────────────────────────────────
function liveStatus(days, forcedClosed) {
  if (forcedClosed || days < 0) return { status:'closed',  statusLabel:'CLOSED' };
  if (days <= 7)                 return { status:'urgent',  statusLabel:'URGENT' };
  return                                { status:'open',    statusLabel:'OPEN' };
}

// ── Raw opportunity definitions (deadlines as ISO strings) ───────────────────
const RAW_OPPORTUNITIES = [
  {
    rank: 1,
    title: "AFAC Documentary Film Grant — Production & Post-Production Cycle 1",
    funder: "Arab Fund for Arts and Culture (AFAC)",
    url: "https://www.arabculturefund.org/Programs/7",
    entities: ["production"],
    score: 4.6,
    scores: { relevance:5, eligibility:5, size:4, winProb:4, strategic:5, timeline:0 },
    amount: "Up to USD 50,000",
    duration: "N/A",
    deadline: "2026-04-02",
    deadlineLabel: "2 Apr 2026",
    forcedClosed: true,
    closedNote: "CLOSED — Next cycle (Cinema grant) opens ~June 2026",
    notes: "Cycle 1 closed. Next cycle (Cinema, Music, Photography) opens ~June 2026. Begin dossier preparation now. Tunisia explicitly eligible; AFAC has funded Tunisian cinema (Youssef Chebbi, 2025).",
    source: "AFAC"
  },
  {
    rank: 2,
    title: "CoE — Accord-cadre Audiovisual Production Services (Lot 2)",
    funder: "Council of Europe, Tunis Bureau",
    url: "https://eproc.coe.int/callfortenders/11042#details",
    entities: ["production","digital"],
    score: 4.4,
    scores: { relevance:5, eligibility:5, size:4, winProb:4, strategic:5, timeline:3 },
    amount: "Framework contract to 2030",
    duration: "To 31 Dec 2030",
    deadline: "2026-04-10",
    deadlineLabel: "10 Apr 2026 — 15h00 Tunis",
    forcedClosed: false,
    notes: "Register on E-Proc platform TODAY at eproc.coe.int (1 business day lead time). Submit 3+ examples of past audiovisual work. Selected companies get multi-year recurring paid production work through 2030.",
    source: "Jamaity / CoE"
  },
  {
    rank: 3,
    title: "UNESCO / IFCD — International Fund for Cultural Diversity 2026",
    funder: "UNESCO / IFCD",
    url: "https://www.unesco.org/creativity/en/international-fund-cultural-diversity",
    entities: ["production","ngo"],
    score: 4.3,
    scores: { relevance:4, eligibility:5, size:5, winProb:3, strategic:5, timeline:4 },
    amount: "Up to USD 100,000",
    duration: "12 – 24 months",
    deadline: "2026-05-06",
    deadlineLabel: "6 May 2026",
    forcedClosed: false,
    notes: "Largest grant this cycle. Joint Production Agency + NGO application strongly recommended. Frame as structural sector development, not a single film. UNESCO prioritises youth, gender equality, Africa/MENA.",
    source: "UNESCO"
  },
  {
    rank: 4,
    title: "Pouvoir d'Agir des Jeunes 2026",
    funder: "Fondation de France / Solidarité Laïque Tunisie",
    url: "https://jamaity.org/bailleur/solidarite-laique-2/",
    entities: ["ngo"],
    score: 4.1,
    scores: { relevance:5, eligibility:5, size:2, winProb:4, strategic:3, timeline:3 },
    amount: "€12,000 – €30,000",
    duration: "Up to 2 years",
    deadline: "2026-05-15",
    deadlineLabel: "~May 2026 (TBC)",
    forcedClosed: false,
    notes: "2026 edition live. Targets registered Tunisian associations working with youth 18–30. Digital media literacy and civic engagement explicitly eligible. Confirm exact deadline directly with Solidarité Laïque Tunisie.",
    source: "Jamaity"
  },
  {
    rank: 5,
    title: "Fablabs dans les 24 gouvernorats — Appel à propositions (ANPR)",
    funder: "ANPR — Agence Nationale de Promotion de la Recherche",
    url: "https://jamaity.org/opportunity/appel-a-propositions-a-lattention-des-associations-en-vue-du-renforcement-ou-la-creation-de-fablabs-dans-les-24-gouvernorats/",
    entities: ["ngo","digital"],
    score: 3.9,
    scores: { relevance:3, eligibility:5, size:2, winProb:4, strategic:4, timeline:4 },
    amount: "TBD — public funding",
    duration: "N/A",
    deadline: "2026-04-24",
    deadlineLabel: "24 Apr 2026",
    forcedClosed: false,
    notes: "National programme — no international competition. Frame as digital media production training for youth in underserved regions. Contact ANPR directly for budget details.",
    source: "Jamaity"
  }
];

// ── Hydrate with live daysLeft + status ──────────────────────────────────────
const DEMO_OPPORTUNITIES = RAW_OPPORTUNITIES.map(o => {
  const days = daysFromNow(o.deadline);
  const { status, statusLabel } = liveStatus(days, o.forcedClosed);
  return {
    ...o,
    daysLeft: days,
    status,
    statusLabel: o.forcedClosed ? o.closedNote : statusLabel
  };
});

const _coeDays    = daysFromNow('2026-04-10');
const _unescoDays = daysFromNow('2026-05-06');
const _fablabDays = daysFromNow('2026-04-24');
const DEMO_ALERTS = [
  { type: "urgent", icon: "🔴", title: "ACTION NOW — CoE Lot 2", desc: "Council of Europe Tunis Bureau: Register on E-Proc platform TODAY. Deadline: 10 Apr 2026 15h00 Tunis time. Framework contract to 2030. Score: 4.4/5." + (_coeDays > 0 ? ' (' + _coeDays + ' days left)' : ' — CLOSED') },
  { type: "warn",   icon: "🟠", title: "AFAC CYCLE 2 — PREP NOW", desc: "Documentary Film Grant Cycle 1 closed (2 Apr). Cinema & Music grants open ~June 2026. Up to USD 50,000. Begin dossier immediately — Score: 4.6/5." },
  { type: "info",   icon: "🔵", title: "UNESCO IFCD — " + (_unescoDays > 0 ? _unescoDays + " DAYS" : "CLOSED"), desc: "Largest grant this cycle: up to USD 100,000 / 12–24 months. Joint Production Agency + NGO application strongly recommended. Deadline: 6 May 2026. Score: 4.3/5." },
  { type: "good",   icon: "🟢", title: "Pouvoir d'Agir des Jeunes", desc: "Fondation de France / Solidarité Laïque Tunisie — €12K–30K. 2026 edition LIVE. 20 grants per cycle, high win probability. Confirm exact deadline with SLT. Score: 4.1/5." },
  { type: "good",   icon: "🟢", title: "Fablabs ANPR — " + (_fablabDays > 0 ? _fablabDays + " DAYS" : "CLOSED"), desc: "Tunisian national programme across 24 governorates. No international competition. Frame as digital media / youth training. Deadline: 24 Apr 2026. Score: 3.9/5." }
];

const DEMO_LOG_SEQUENCE = [
  { delay: 300,  type:'info',   source:'SYSTEM',        msg:'Initializing Fundraiser scan engine…' },
  { delay: 700,  type:'info',   source:'SYSTEM',        msg:'Mode: DEMO — replaying scan of 5 Apr 2026' },
  { delay: 1200, type:'info',   source:'JAMAITY',       msg:'Fetching jamaity.org/opportunites…' },
  { delay: 1800, type:'found',  source:'JAMAITY',       msg:'Found: Fablabs 24 gouvernorats (ANPR) — deadline 24 Apr' },
  { delay: 2200, type:'found',  source:'JAMAITY',       msg:'Found: CoE Lot 2 audiovisual production tender — 10 Apr' },
  { delay: 2700, type:'urgent', source:'JAMAITY',       msg:'⚑ URGENT: CoE deadline in 5 days — flagging immediately' },
  { delay: 3100, type:'info',   source:'JAMAITY',       msg:'Checking Solidarité Laïque / Fondation de France…' },
  { delay: 3600, type:'found',  source:'JAMAITY',       msg:'Found: Pouvoir d\'Agir des Jeunes 2026 — ~May deadline' },
  { delay: 4000, type:'info',   source:'AFAC',          msg:'Fetching arabculturefund.org/Programs…' },
  { delay: 4600, type:'found',  source:'AFAC',          msg:'Found: Documentary Film Grant — deadline was 2 Apr' },
  { delay: 5000, type:'urgent', source:'AFAC',          msg:'⚑ Deadline passed (−3 days) — flagging for Cycle 2 (June)' },
  { delay: 5500, type:'found',  source:'AFAC',          msg:'Found: Visual Arts Grant — deadline 2 Apr (closed)' },
  { delay: 5900, type:'found',  source:'AFAC',          msg:'Found: Performing Arts Grant — deadline 2 Apr (closed)' },
  { delay: 6300, type:'info',   source:'UNESCO',        msg:'Fetching IFCD 2026 call for proposals…' },
  { delay: 6900, type:'found',  source:'UNESCO',        msg:'Found: IFCD Cultural Diversity — deadline 6 May — up to USD 100K' },
  { delay: 7400, type:'info',   source:'CFW',           msg:'Checking culturefundingwatch.com (public feed)…' },
  { delay: 7900, type:'info',   source:'CFW',           msg:'Pro database requires subscription — partial scan only' },
  { delay: 8400, type:'info',   source:'EU PORTALS',    msg:'Checking ec.europa.eu — MENA / Mediterranean filter…' },
  { delay: 8900, type:'info',   source:'EU PORTALS',    msg:'No new open calls matching profile this cycle' },
  { delay: 9400, type:'info',   source:'SCORING',       msg:'Applying scoring model: 6 criteria × weighted scores…' },
  { delay: 9900, type:'info',   source:'SCORING',       msg:'0 auto-disqualified · 5 shortlisted (score ≥ 3.5)' },
  { delay:10400, type:'done',   source:'COMPLETE',      msg:'✓ Scan complete — 5 opportunities ranked · 1 urgent action required' },
];

const DEMO_SOURCES = ['JAMAITY','AFAC','UNESCO','CFW','EU PORTALS','SCORING'];

// ═══════════════════════════════════════════════════════
// SCAN ORCHESTRATOR
// ═══════════════════════════════════════════════════════
let scanning = false;
let allData = [];

function startScan() {
  if (scanning) return;
  if (currentMode === 'live') {
    runLiveScan();
  } else {
    runDemoScan();
  }
}

function runDemoScan() {
  scanning = true;
  resetUI();

  const btn = document.getElementById('scan-btn');
  btn.disabled = true;
  btn.innerHTML = '<div class="spinner"></div> SCANNING…';

  document.getElementById('live-dot').classList.add('scanning');
  document.getElementById('feed-badge').textContent = 'SCANNING';
  document.getElementById('progress-wrap').classList.add('visible');

  let sourcesHit = new Set();
  let foundCount = 0;

  DEMO_LOG_SEQUENCE.forEach((entry, i) => {
    setTimeout(() => {
      addLogLine(entry.source, entry.msg, entry.type);

      // Update source count
      if (!['SYSTEM','SCORING','COMPLETE'].includes(entry.source)) {
        sourcesHit.add(entry.source);
        animateCounter('stat-sources', sourcesHit.size);
        document.getElementById('stat-sources-sub').textContent = [...sourcesHit].join(', ').toLowerCase();
      }

      // Update found count
      if (entry.type === 'found') {
        foundCount++;
        animateCounter('stat-found', foundCount);
      }

      // Update progress bar
      const pct = Math.round((i / DEMO_LOG_SEQUENCE.length) * 100);
      document.getElementById('progress-fill').style.width = pct + '%';
      document.getElementById('progress-pct').textContent = pct + '%';
      document.getElementById('progress-source').textContent = 'Scanning ' + entry.source + '…';

    }, entry.delay);
  });

  // After all log lines, populate results
  const totalDuration = DEMO_LOG_SEQUENCE[DEMO_LOG_SEQUENCE.length - 1].delay + 600;

  setTimeout(() => {
    document.getElementById('progress-fill').style.width = '100%';
    document.getElementById('progress-pct').textContent = '100%';
    document.getElementById('progress-source').textContent = 'Complete';

    allData = DEMO_OPPORTUNITIES;
    renderTable(allData);
    renderAlerts(DEMO_ALERTS);

    // Final stats
    animateCounter('stat-shortlisted', 5);
    animateCounter('stat-urgent', 1);
    document.getElementById('stat-shortlisted-sub').textContent = 'score ≥ 3.5/5';
    const urgentOpp = allData.find(o => o.status === 'urgent');
    const urgentSub = urgentOpp
      ? urgentOpp.title.substring(0, 25) + ' — ' + (urgentOpp.daysLeft > 0 ? urgentOpp.daysLeft + ' days' : 'CLOSED')
      : 'none this cycle';
    document.getElementById('stat-urgent-sub').textContent = urgentSub;
    document.getElementById('alerts-count').textContent = '5';
    document.getElementById('last-scan-time').textContent = new Date().toLocaleString('en-GB');
    document.getElementById('feed-badge').textContent = 'COMPLETE';
    document.getElementById('live-dot').classList.remove('scanning');
    document.getElementById('progress-wrap').classList.remove('visible');

    btn.disabled = false;
    btn.innerHTML = '<span class="btn-icon">⟳</span> RESCAN';
    scanning = false;
  }, totalDuration);
}

// ═══════════════════════════════════════════════════════
// LIVE SCAN — calls Claude API
// ═══════════════════════════════════════════════════════
// ═══════════════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS FOR AGENTIC PIPELINE
// ═══════════════════════════════════════════════════════════════════════════

// ── setProgress(source, percent) — Update progress bar UI ───────────────────
function setProgress(source, percent) {
  document.getElementById('progress-source').textContent = source;
  document.getElementById('progress-fill').style.width = percent + '%';
  document.getElementById('progress-pct').textContent = percent + '%';
}

// ── safeParseArray(text) — Extract and parse JSON array from text ──────────
function safeParseArray(text) {
  if (!text) return [];
  try {
    const match = text.match(/\[[\s\S]*\]/);
    if (match) return JSON.parse(match[0]);
  } catch(e) {
    // Parsing failed
  }
  return [];
}

// ── callClaude(messages, systemPrompt, apiKey) — Agentic loop handler ──────
async function callClaude(messages, systemPrompt, apiKey) {
  /**
   * Handles agentic loop: tool_use + multi-turn message handling.
   * Returns accumulated text output.
   */
  const API_HEADERS = {
    'Content-Type': 'application/json',
    'x-api-key': apiKey,
    'anthropic-version': '2023-06-01',
    'anthropic-dangerous-direct-browser-access': 'true'
  };

  let accumulatedText = '';
  let turnCount = 0;
  const MAX_TURNS = 8;

  while (turnCount < MAX_TURNS) {
    turnCount++;

    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: API_HEADERS,
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 4000,
        system: systemPrompt,
        messages: messages
      })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error('API error: ' + (err.error?.message || response.status));
    }

    const data = await response.json();

    // Accumulate text blocks
    for (const block of data.content) {
      if (block.type === 'text') accumulatedText += block.text;
    }

    // If end_turn, we're done
    if (data.stop_reason === 'end_turn') break;

    // If tool_use, append assistant turn and tool results (won't happen for pure text)
    if (data.stop_reason === 'tool_use') {
      messages.push({ role: 'assistant', content: data.content });
      const toolResults = data.content
        .filter(b => b.type === 'tool_use')
        .map(b => ({
          type: 'tool_result',
          tool_use_id: b.id,
          content: b.output || ''
        }));
      messages.push({ role: 'user', content: toolResults });
      continue;
    }

    // max_tokens or other stop reason
    break;
  }

  return accumulatedText;
}

// ═══════════════════════════════════════════════════════════════════════════
// PIPELINE STEP: JAMAITY
// ═══════════════════════════════════════════════════════════════════════════

async function stepJamaity(apiKey) {
  /**
   * Jamaity pipeline step:
   * 1. Define 4 Jamaity filter URLs
   * 2. Call Claude to fetch & extract raw opportunity cards
   * 3. Score & convert French dates to ISO, assign entity tags
   * 4. Return array with source: 'Jamaity' tag
   */

  const JAMAITY_URLS = [
    'https://jamaity.org/opportunites/?opportunity_type=tous',
    'https://jamaity.org/opportunites/?opportunity_type=appel-a-projets',
    'https://jamaity.org/opportunites/?page=2',
    'https://jamaity.org/opportunites/?opportunity_theme=cinema'
  ];

  addLogLine('JAMAITY', 'Fetching opportunities from 4 Jamaity filter URLs…', 'info');
  setProgress('Jamaity: Fetching opportunities', 15);

  // ── CALL 1: Fetch URLs and extract raw card data ───────────────────────────
  const fetchPrompt = `Extract funding opportunities from these Jamaity pages. For each card found, extract:
- title (French text as-is)
- funder (organization name)
- type (call type: "Appel à projets", "Bourse", etc.)
- deadline_text (raw deadline text as shown, e.g. "15 mai 2026", "Avant le 30 avril")
- url (direct link to opportunity)

Return ONLY a JSON array with these fields (in French where applicable). If no opportunities found, return [].`;

  let rawCards = [];
  try {
    const urlsText = JAMAITY_URLS.map((url, i) => `URL ${i+1}: ${url}`).join('\n');
    const fetchMessages = [
      {
        role: 'user',
        content: `${fetchPrompt}\n\nFetch these URLs and extract cards:\n${urlsText}`
      }
    ];

    const cardText = await callClaude(fetchMessages, '', apiKey);
    rawCards = safeParseArray(cardText);
    addLogLine('JAMAITY', 'Extracted ' + rawCards.length + ' raw cards', 'info');
  } catch(e) {
    addLogLine('JAMAITY', 'Error fetching URLs: ' + e.message, 'urgent');
    return [];
  }

  if (rawCards.length === 0) {
    addLogLine('JAMAITY', 'No opportunities found', 'info');
    return [];
  }

  setProgress('Jamaity: Scoring & normalizing dates', 50);

  // ── CALL 2: Score cards, convert dates, assign entities ────────────────────
  const scoringPrompt = `You are scoring Jamaity funding opportunities for these Tunisian entities:
1. EMPIRIQ — Production Agency: Films, documentaries, TV, post-production, animations
2. FREESH — Digital Media (youth 20–35): Social media, brand storytelling, video for digital, podcasts
3. ATDCE — NGO (youth training): Youth content creation training, civic engagement, advocacy

For each opportunity:
- SCORE (1–5 float): Fit for at least one entity (5=perfect, 1=marginal, 0=exclude)
- ENTITIES (array): Which of ["production", "digital", "ngo"] it fits
- DEADLINE_ISO (YYYY-MM-DD): Convert French deadline text to ISO date. If ambiguous, use most likely (e.g. "15 mai 2026" → "2026-05-15")
- AMOUNT: Budget/grant size (leave blank if not stated)
- NOTES: 1–2 sentence strategic fit

Return ONLY a JSON array with fields: title, funder, url, score, entities, deadline_iso, amount, notes
If score < 1.5, exclude from results.`;

  let scoredOpps = [];
  try {
    const cardsText = JSON.stringify(rawCards, null, 2);
    const scoreMessages = [
      {
        role: 'user',
        content: `${scoringPrompt}\n\nScore these cards:\n${cardsText}`
      }
    ];

    const scoreText = await callClaude(scoreMessages, '', apiKey);
    scoredOpps = safeParseArray(scoreText);
    addLogLine('JAMAITY', 'Scored & normalized ' + scoredOpps.length + ' opportunities', 'found');
  } catch(e) {
    addLogLine('JAMAITY', 'Error scoring: ' + e.message, 'urgent');
    return [];
  }

  // ── Transform into pipeline output format ──────────────────────────────────
  const result = scoredOpps.map(opp => ({
    title: opp.title || '(untitled)',
    funder: opp.funder || 'Jamaity',
    url: opp.url || 'https://jamaity.org',
    entities: opp.entities || [],
    score: opp.score || 0,
    amount: opp.amount || 'TBD',
    duration: 'N/A',
    deadlineLabel: opp.deadline_text || opp.deadline_iso || '(not specified)',
    deadline: opp.deadline_iso || '2026-12-31',
    notes: opp.notes || '',
    source: 'Jamaity'
  }));

  setProgress('Jamaity: Complete', 65);
  addLogLine('JAMAITY', '✓ Jamaity step complete — ' + result.length + ' opportunities ready', 'done');

  return result;
}

// ═══════════════════════════════════════════════════════════════════════════
// MAIN ORCHESTRATOR: runLiveScan (Agentic Pipeline)
// ═══════════════════════════════════════════════════════════════════════════

async function runLiveScan() {
  const apiKey = document.getElementById('api-key').value.trim();
  if (!apiKey || !apiKey.startsWith('sk-ant')) {
    addLogLine('SYSTEM', '✗ Please enter a valid Anthropic API key (sk-ant-…)', 'urgent');
    return;
  }

  scanning = true;
  resetUI();
  const btn = document.getElementById('scan-btn');
  btn.disabled = true;
  btn.innerHTML = '<div class="spinner"></div> SCANNING…';
  document.getElementById('live-dot').classList.add('scanning');
  document.getElementById('feed-badge').textContent = 'LIVE SCAN';
  document.getElementById('progress-wrap').classList.add('visible');

  addLogLine('SYSTEM', 'Initiating agentic scan pipeline…', 'info');
  addLogLine('SYSTEM', 'Step 1: Jamaity', 'info');

  try {
    // ── Run pipeline steps ────────────────────────────────────────────────────
    setProgress('Starting pipeline', 5);

    // Step 1: Jamaity
    const jamaityOpps = await stepJamaity(apiKey);
    let allOpps = [...jamaityOpps];

    // (Placeholder for future steps: AFAC, UNESCO, CFW, etc.)
    // TODO: stepAFAC(apiKey)
    // TODO: stepUNESCO(apiKey)
    // etc.

    setProgress('Finalizing results', 85);

    // ── Post-process: Enrich with rank, daysLeft, status ──────────────────────
    const enriched = allOpps
      .sort((a, b) => (b.score || 0) - (a.score || 0))
      .map((o, i) => {
        const days = o.deadline ? daysFromNow(o.deadline) : 999;
        const { status, statusLabel } = liveStatus(days, days < 0);
        return {
          ...o,
          rank: i + 1,
          daysLeft: days,
          status: o.status || status,
          statusLabel: o.statusLabel || statusLabel
        };
      });

    allData = enriched;

    enriched.forEach(o => {
      const typeIcon = o.status === 'urgent' ? 'urgent' : 'found';
      addLogLine(o.source?.toUpperCase() || 'SOURCE', o.title?.substring(0, 50) + ' — ' + (o.deadlineLabel || '?'), typeIcon);
    });

    addLogLine('COMPLETE', '✓ Pipeline complete — ' + enriched.length + ' opportunities ranked', 'done');

    renderTable(enriched);

    const urgentCount = enriched.filter(o => o.status === 'urgent').length;
    animateCounter('stat-sources', 1); // Only Jamaity for now
    animateCounter('stat-found', enriched.length);
    animateCounter('stat-shortlisted', enriched.filter(o => o.score >= 3.5).length);
    animateCounter('stat-urgent', urgentCount);
    document.getElementById('stat-sources-sub').textContent = 'jamaity';
    document.getElementById('stat-found-sub').textContent = 'from Jamaity';
    document.getElementById('stat-shortlisted-sub').textContent = 'score ≥ 3.5/5';
    const liveUrgentOpp = enriched.find(o => o.status === 'urgent');
    const liveUrgentSub = liveUrgentOpp
      ? liveUrgentOpp.title.substring(0, 25) + ' — ' + (liveUrgentOpp.daysLeft > 0 ? liveUrgentOpp.daysLeft + ' days' : 'CLOSED')
      : 'none this cycle';
    document.getElementById('stat-urgent-sub').textContent = liveUrgentSub;

    const liveAlerts = enriched
      .filter(o => o.status === 'urgent' || o.notes)
      .slice(0, 5)
      .map(o => ({
        type: o.status === 'urgent' ? 'urgent' : 'info',
        icon: o.status === 'urgent' ? '🔴' : '🔵',
        title: o.title?.substring(0, 40),
        desc: o.notes || o.deadlineLabel
      }));

    renderAlerts(liveAlerts.length ? liveAlerts : DEMO_ALERTS);
    document.getElementById('alerts-count').textContent = liveAlerts.length;
    const scanTime = new Date().toLocaleString('en-GB');
    document.getElementById('last-scan-time').textContent = scanTime;
    document.getElementById('feed-badge').textContent = 'COMPLETE';
    document.getElementById('live-dot').classList.remove('scanning');
    document.getElementById('progress-fill').style.width = '100%';
    document.getElementById('progress-pct').textContent = '100%';
    setProgress('Complete', 100);
    setTimeout(() => { document.getElementById('progress-wrap').classList.remove('visible'); }, 800);

    // ── Persist results to localStorage ───────────────────────────────────────
    try {
      const toSave = {
        data: enriched,
        alerts: liveAlerts,
        sources: 1,
        sourcesList: 'jamaity',
        scanTime: scanTime,
        savedAt: new Date().toISOString()
      };
      const payload = JSON.stringify(toSave);
      if (payload.length < 4000000) {
        localStorage.setItem('fundraiser:last-scan', payload);
        addLogLine('SYSTEM', '✓ Results saved — will survive page refresh', 'done');
      } else {
        addLogLine('SYSTEM', '⚠ Payload too large to cache (' + (payload.length/1024).toFixed(0) + 'KB)', 'urgent');
      }
    } catch(e) {
      addLogLine('SYSTEM', '⚠ localStorage save failed: ' + e.message, 'urgent');
    }

  } catch(e) {
    addLogLine('ERROR', 'Pipeline error: ' + e.message, 'urgent');
    document.getElementById('live-dot').classList.remove('scanning');
    document.getElementById('feed-badge').textContent = 'ERROR';
    document.getElementById('progress-wrap').classList.remove('visible');
  }

  btn.disabled = false;
  btn.innerHTML = '<span class="btn-icon">⟳</span> RESCAN';
  scanning = false;
}

// ═══════════════════════════════════════════════════════
// UI HELPERS
// ═══════════════════════════════════════════════════════
function resetUI() {
  document.getElementById('feed-log').innerHTML = '';
  document.getElementById('table-body').innerHTML = `
    <tr><td colspan="12">
      <div class="empty-state"><div class="big-icon">◎</div><p>Scanning in progress…</p></div>
    </td></tr>`;
  document.getElementById('alerts-panel').innerHTML = `
    <div style="padding:20px;font-family:var(--mono);font-size:11px;color:var(--text-dim);">Scanning…</div>`;
  ['stat-sources','stat-found','stat-shortlisted','stat-urgent'].forEach(id => {
    document.getElementById(id).textContent = '0';
  });
  document.getElementById('progress-fill').style.width = '0%';
  document.getElementById('progress-pct').textContent = '0%';
}

function addLogLine(source, msg, type) {
  const log = document.getElementById('feed-log');
  const now = new Date();
  const time = now.toLocaleTimeString('en-GB', {hour:'2-digit', minute:'2-digit', second:'2-digit'});

  const line = document.createElement('div');
  line.className = 'log-line ' + (type || 'info');
  line.innerHTML = `
    <span class="log-time">${time}</span>
    <span class="log-source">${source}</span>
    <span class="log-msg">${msg}</span>
  `;
  log.appendChild(line);
  log.scrollTop = log.scrollHeight;
}

function animateCounter(id, target) {
  const el = document.getElementById(id);
  const start = parseInt(el.textContent) || 0;
  const duration = 600;
  const startTime = performance.now();

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(start + (target - start) * eased);
    if (progress < 1) requestAnimationFrame(update);
  }
  requestAnimationFrame(update);
}

// ═══════════════════════════════════════════════════════
// TABLE RENDER
// ═══════════════════════════════════════════════════════
function renderTable(data) {
  const tbody = document.getElementById('table-body');
  tbody.innerHTML = '';

  data.forEach((opp, idx) => {
    const tr = document.createElement('tr');
    tr.dataset.entities = (opp.entities || []).join(',');
    tr.dataset.status = opp.status || 'open';
    tr.style.animationDelay = (idx * 80) + 'ms';

    // Score bar color
    const scoreClass = opp.score >= 4.2 ? 'high' : opp.score >= 3.5 ? 'mid' : 'low';
    const scorePct = (opp.score / 5 * 100).toFixed(0);

    // Entity tags
    const entityTags = (opp.entities || []).map(e => {
      const cls = e === 'production' ? 'tag-prod' : e === 'digital' ? 'tag-digital' : 'tag-ngo';
      const label = e === 'production' ? 'PRODUCTION' : e === 'digital' ? 'DIGITAL' : 'NGO';
      return `<span class="tag ${cls}">${label}</span>`;
    }).join('');

    // Status badge
    const statusMap = {
      open: 'status-open',
      urgent: 'status-urgent',
      closed: 'status-closed',
      flagged: 'status-flagged'
    };
    const statusClass = statusMap[opp.status] || 'status-open';
    const statusText = opp.statusLabel || opp.status?.toUpperCase() || 'OPEN';

    // Countdown display (goes in its own cell now)
    let countdownHtml = '';
    if (opp.daysLeft < 0) {
      countdownHtml = `<div class="countdown-wrap"><div class="countdown-num countdown-closed">${Math.abs(opp.daysLeft)}</div><div class="countdown-label">days ago</div></div>`;
    } else if (opp.daysLeft <= 7) {
      countdownHtml = `<div class="countdown-wrap"><div class="countdown-num countdown-urgent">${opp.daysLeft}</div><div class="countdown-label" style="color:var(--red);">⚑ days left</div></div>`;
    } else if (opp.daysLeft <= 21) {
      countdownHtml = `<div class="countdown-wrap"><div class="countdown-num countdown-soon">${opp.daysLeft}</div><div class="countdown-label" style="color:var(--orange);">days left</div></div>`;
    } else {
      countdownHtml = `<div class="countdown-wrap"><div class="countdown-num countdown-ok">${opp.daysLeft}</div><div class="countdown-label">days left</div></div>`;
    }

    // Duration display
    const durationHtml = (opp.duration && opp.duration !== 'N/A')
      ? `<div class="duration-val">${escHtml(opp.duration)}</div>`
      : `<div class="duration-na">N/A</div>`;

    tr.innerHTML = `
      <td><div class="rank-cell ${opp.rank <= 2 ? 'top' : ''}">${opp.rank}</div></td>
      <td>
        <div class="opp-title">${escHtml(opp.title)}</div>
      </td>
      <td>
        <div class="opp-donor">${escHtml(opp.funder)}</div>
      </td>
      <td class="notes-cell">
        ${opp.notes ? `<div class="opp-notes">${escHtml(opp.notes)}</div>` : '<span style="color:var(--text-dim);font-family:var(--mono);font-size:10px;">—</span>'}
      </td>
      <td>${entityTags}</td>
      <td>
        <div class="score-wrap">
          <div class="score-num">${opp.score}</div>
          <div class="score-bar-bg">
            <div class="score-bar-fill ${scoreClass}" style="width:${scorePct}%"></div>
          </div>
        </div>
      </td>
      <td><div class="amount">${escHtml(opp.amount)}</div></td>
      <td>${durationHtml}</td>
      <td>
        <div class="deadline-date">${escHtml(opp.deadlineLabel)}</div>
      </td>
      <td>${countdownHtml}</td>
      <td><span class="status-badge ${statusClass}">${statusText}</span></td>
      <td>
        <a class="link-btn" href="${escHtml(opp.url)}" target="_blank" rel="noopener" title="${escHtml(opp.title)}">
          ↗
        </a>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // Trigger score bar animations after render
  setTimeout(() => {
    document.querySelectorAll('.score-bar-fill').forEach(bar => {
      const pct = bar.style.width;
      bar.style.width = '0';
      requestAnimationFrame(() => {
        setTimeout(() => { bar.style.width = pct; }, 100);
      });
    });
  }, 200);
}

function escHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ═══════════════════════════════════════════════════════
// ALERTS RENDER
// ═══════════════════════════════════════════════════════
function renderAlerts(alerts) {
  const panel = document.getElementById('alerts-panel');
  panel.innerHTML = '';
  alerts.forEach(a => {
    const div = document.createElement('div');
    div.className = 'alert-item ' + a.type;
    div.innerHTML = `
      <div class="alert-icon">${a.icon}</div>
      <div class="alert-content">
        <div class="alert-title">${escHtml(a.title)}</div>
        <div class="alert-desc">${escHtml(a.desc)}</div>
      </div>
    `;
    panel.appendChild(div);
  });
}

// ═══════════════════════════════════════════════════════
// FILTER & SORT
// ═══════════════════════════════════════════════════════
let sortDir = -1;

function filterTable(filter, btn) {
  document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');

  const rows = document.querySelectorAll('#table-body tr');
  rows.forEach(row => {
    if (filter === 'all') {
      row.style.display = '';
    } else if (filter === 'urgent') {
      row.style.display = row.dataset.status === 'urgent' ? '' : 'none';
    } else {
      const entities = (row.dataset.entities || '').split(',');
      row.style.display = entities.includes(filter) ? '' : 'none';
    }
  });
}

function sortByScore() {
  if (!allData.length) return;
  sortDir *= -1;
  const sorted = [...allData]
    .sort((a, b) => sortDir * (a.score - b.score))
    .map((o, i) => ({ ...o, rank: i + 1 }));
  renderTable(sorted);
}
</script>
</body>
</html>
"""

components.html(DASHBOARD_HTML, height=1300, scrolling=True)
