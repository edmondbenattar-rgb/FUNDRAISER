# 🎯 Fundraiser — Opportunity Intelligence Platform

![Status](https://img.shields.io/badge/status-LIVE-green)
![Version](https://img.shields.io/badge/version-1.0-blue)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Python](https://img.shields.io/badge/python-3.9+-blue)

**Fundraiser** is an AI-powered platform that identifies, scores, and tracks funding opportunities for media production companies, digital media agencies, and youth advocacy NGOs in the MENA region and beyond.

## 🌍 Live Dashboard

**[Access the live dashboard](https://share.streamlit.io)**

Accessible from anywhere in the world. No login required for demo mode.

## ✨ Key Features

### 🔍 Real-Time Opportunity Scanning
- Monitors **12+ funding sources** simultaneously
- AFAC, Doha Film Institute, EU Creative Europe, Google News Initiative, British Council MENA, UNESCO, UN agencies, bilateral development programs, and more
- Automatic deadline tracking and urgency alerts
- Support for North Africa, Mediterranean, and MENA regions

### 🤖 Intelligent Scoring System
Opportunities ranked on 6 weighted dimensions:
- **Relevance** (30%) — How well does this match your activities?
- **Eligibility** (25%) — Is your organization/country eligible?
- **Funding Size** (15%) — Is the amount worth the effort?
- **Win Probability** (15%) — Realistic chance of success
- **Strategic Value** (10%) — Opens doors to future funding
- **Timeline Feasibility** (5%) — Deadline is realistic

### 📊 Interactive Dashboard
- **Live table** with filters, sorting, and deep dives
- **Alert system** for urgent deadlines (< 21 days)
- **Pipeline management** — Track proposals from shortlist → submission → decision
- **Entity-type matching** — Filter for production, digital media, or NGO funding
- **Export-ready** — Copy opportunity details for your files

### 🛠️ Three Operational Modes

1. **Dashboard Mode** — Browse shortlisted opportunities, filter, sort, view alerts
2. **Live Scan Mode** — Real-time funding source search (requires Claude API key)
3. **Pipeline Mode** — Manage your application workflow in a Kanban-style interface

### 🎬 Multi-Entity Support

Fundraiser supports three independent organizational types:

**Entity 1: Production Agency**
- Feature films, documentaries, TV series, advertising, post-production
- Target: Film funds, co-production markets, distribution support

**Entity 2: Digital Media Agencies** (2x)
- Social media content, web series, podcasts, digital campaigns
- Target: Media innovation grants, startup/SME programs

**Entity 3: NGO (Youth Training & Advocacy)**
- Youth media training, civic engagement, awareness campaigns
- Target: Civil society grants, development programs, capacity building

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[QUICK_START.md](./QUICK_START.md)** | Get dashboard online in 10 minutes |
| **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** | Advanced setup (database, CI/CD, custom domain) |
| **[FUNDRAISER_SYSTEM.md](./FUNDRAISER_SYSTEM.md)** | Full AI agent system instructions (6 phases) |
| **[API.md](./API.md)** | REST API documentation (for integrations) |

---

## 🚀 Getting Started

### Option 1: Use the Live Dashboard (Easiest)

1. Go to [your-dashboard-url.streamlit.app](https://share.streamlit.io)
2. Explore the demo opportunities
3. (Optional) Add your Claude API key to enable Live Scan

**No installation required!**

### Option 2: Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/fundraiser-dashboard.git
cd fundraiser-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py

# Open http://localhost:8501 in your browser
```

### Option 3: Deploy Your Own Instance

See [QUICK_START.md](./QUICK_START.md) for step-by-step GitHub + Streamlit Cloud setup.

---

## 🎯 Funding Sources Tracked

### Film & Audiovisual
- **AFAC** (Arab Fund for Arts & Culture)
- **Doha Film Institute**
- **EU Creative Europe MEDIA**
- **Hubert Bals Fund** (IFFR)
- **World Cinema Fund** (Berlinale)
- **TorinoFilmLab**
- **Sundance Documentary Fund**
- **Aide aux Cinémas du Monde** (CNC France)
- **Arab Cinema Center**
- **Al Jazeera Documentary Channel**

### Digital Media & Innovation
- **Google News Initiative**
- **Meta Journalism Project**
- **International Fund for Public Interest Media**
- **Thomson Reuters Foundation**
- **Internews**
- **DW Akademie**
- **Canal France International (CFI)**
- **BBC Media Action**
- **USAID Media Development**

### NGO & Civil Society
- **European Union** (EIDHR, ENI, Erasmus+, CERV)
- **UN Agencies** (UNDP, UNICEF, UNESCO, UN Women, UNFPA)
- **USAID / MCC**
- **GIZ** (Germany)
- **AFD** / Expertise France
- **British Council MENA**
- **Danish Arab Partnership Programme**
- **Swiss Development Cooperation**
- **Ford Foundation**
- **Open Society Foundations**
- **Drosos Foundation**
- **Anna Lindh Foundation**
- **National Endowment for Democracy**
- **Free Press Unlimited**
- **Hivos Foundation**

### Regional & Bilateral
- **African Development Bank**
- **Islamic Development Bank**
- **ALECSO**
- **Agence Tunisienne de Coopération Technique**

---

## 💻 Technical Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit (Python) |
| **Backend** | Python 3.9+ |
| **AI/ML** | Anthropic Claude API |
| **Hosting** | Streamlit Cloud (free) or your own server |
| **Database** | Optional (local JSON or external) |
| **Version Control** | GitHub |

### Dependencies

```
streamlit>=1.40.0        # Web app framework
anthropic>=0.42.0        # Claude AI integration
requests>=2.31.0         # HTTP requests
pandas>=2.0.0            # Data handling
```

---

## 🔐 Security & Privacy

✅ **What we do:**
- No personal data stored on servers
- API keys NOT logged or cached
- All funding source data is public
- HTTPS only
- CSRF protection enabled

✅ **What we don't do:**
- Sell your data
- Track users
- Store credentials
- Monitor applications
- Share with third parties

---

## 📊 Data Model

Each opportunity is a structured JSON object:

```json
{
  "rank": 1,
  "title": "AFAC Media Fund 2026",
  "funder": "Arab Fund for Arts & Culture",
  "amount": "€15,000 - €45,000",
  "currency": "EUR",
  "deadline": "2026-05-30",
  "daysLeft": 55,
  "score": 4.8,
  "entities": ["production"],
  "status": "open|urgent|closed",
  "url": "https://...",
  "notes": "Ideal for feature films",
  "eligibility": {
    "geographic": ["Tunisia", "North Africa", "MENA"],
    "entity_type": ["company", "partnership"],
    "sector": ["film", "audiovisual"],
    "other_requirements": "..."
  }
}
```

---

## 🎓 How the Agent Works (6 Phases)

### Phase 1: Opportunity Discovery
- Systematic scraping of 30+ funding sources
- Daily/weekly/monthly monitoring cycles
- Extraction of key metadata (title, amount, deadline, eligibility)

### Phase 2: Scoring & Shortlisting
- Automated ranking on 6 weighted dimensions
- Auto-disqualify if not eligible
- Output: Ranked shortlist (top 10-20)

### Phase 3: User Validation
- Present shortlist to human decision-maker
- Approve/reject/modify based on feedback
- Learning loop: adjust future scoring based on feedback

### Phase 4: Proposal Writing
- AI-generated proposal drafts in English or French
- Funder-aligned narratives
- Budget templates with activity justification
- Estimated time: 3-5 hours for a full proposal

### Phase 5: Proposal Validation
- Quality checklist against funder requirements
- Verification that all sections are included
- Budget-narrative alignment check
- Ready-to-submit confirmation

### Phase 6: Submission & Tracking
- Pre-submission verification
- Portfolio of submitted materials
- Deadline reminders
- Results tracking

---

## 🛠️ Customization

### Add Your Organization's Data

Edit `streamlit_app.py` and update:

```python
ORGANIZATION = {
    "name": "Your Organization",
    "type": "production|digital|ngo",
    "country": "Tunisia",
    "annual_budget": 50000,
    "languages": ["Arabic", "French", "English"],
    "past_projects": [...],
    "partnerships": [...]
}
```

### Modify Scoring Weights

In the Fundraiser Agent system instructions, adjust weights:

```python
SCORING_CRITERIA = {
    "relevance": 0.30,
    "eligibility": 0.25,
    "funding_size": 0.15,
    "win_probability": 0.15,
    "strategic_value": 0.10,
    "timeline": 0.05
}
```

### Change UI Colors

Edit the `COLORS` dict in `streamlit_app.py`:

```python
COLORS = {
    "accent": "#f0b429",      # Primary (yellow)
    "accent2": "#3b82f6",     # Secondary (blue)
    "accent3": "#10b981",     # Tertiary (green)
    "red": "#ef4444",         # Alerts
    "bg": "#0a0b0d",          # Dark background
}
```

---

## 📈 Roadmap

### v1.1 (Next Month)
- [ ] Database integration (Airtable / Firebase)
- [ ] Email notifications for urgent deadlines
- [ ] Multi-language UI (Arabic, French)
- [ ] CSV export

### v1.5 (Q2 2026)
- [ ] Proposal generator (integrates with Claude Opus)
- [ ] Word document export (.docx)
- [ ] Calendar sync (Google Calendar, Outlook)
- [ ] Team workspace (role-based access)

### v2.0 (Q3 2026)
- [ ] Custom scoring model (per organization)
- [ ] Impact tracking (acceptance rate, funding amounts won)
- [ ] Funder relationship tracking
- [ ] Budget planning tools

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** this repo
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Commit** (`git commit -m 'Add: amazing feature'`)
5. **Push** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

### Guidelines
- Keep code clean and commented
- Follow PEP 8 style guide
- Test locally before submitting PR
- Update README if adding features

---

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE.md](./LICENSE.md) for details.

**In summary:** Use it freely for your organization, commercial or non-profit. Give credit where due.

---

## 🙋 Support & Questions

- **📧 Email:** contact@yourorg.com
- **🐛 Report bugs:** [GitHub Issues](https://github.com/YOUR_USERNAME/fundraiser-dashboard/issues)
- **💬 Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/fundraiser-dashboard/discussions)
- **📖 Documentation:** See `/docs` folder
- **🎓 Training:** See `FUNDRAISER_SYSTEM.md` for full system instructions

---

## 🌟 Credits & Acknowledgments

**Built with:**
- [Streamlit](https://streamlit.io) — Web app framework
- [Anthropic Claude](https://anthropic.com) — AI engine
- [GitHub](https://github.com) — Version control & hosting

**Inspired by:**
- AFAC, Jamaity, Culture Funding Watch
- European funding transparency initiatives
- Nonprofit tech innovation in the MENA region

---

## 📊 Project Stats

- **Lines of code:** 880+ (Streamlit app)
- **Funding sources monitored:** 12+ (extensible)
- **Entity types supported:** 3 (production, digital media, NGO)
- **Languages:** English, French, Arabic (roadmap)
- **Deployment time:** < 10 minutes
- **Maintenance:** Minimal (auto-deploy on GitHub push)

---

## 📣 Share Your Success

Found funding through Fundraiser? We'd love to hear about it!

Tag us: `#FundraiserAgent` `#FundingForMedia` `#MENA`

Example post:
> We found €30,000 in EU funding for our documentary using @FundraiserAgent. This tool is a game-changer for media orgs in North Africa. Highly recommend! 🚀

---

## 🎯 Vision

**Fundraiser's mission:** Lower barriers to funding for talented media makers and social impact organizations in the MENA region.

**Our belief:** Access to funding should not require expensive consultants or English speakers. Technology can democratize opportunity discovery.

---

## ⚡ Quick Links

| Link | Purpose |
|------|---------|
| [Live Dashboard](https://share.streamlit.io) | Use it now |
| [GitHub](https://github.com/YOUR_USERNAME/fundraiser-dashboard) | Fork & contribute |
| [System Instructions](./FUNDRAISER_SYSTEM.md) | Deep dive into the agent |
| [Deployment Guide](./DEPLOYMENT_GUIDE.md) | Self-hosting |
| [API Docs](./API.md) | Integrate with your tools |

---

**Last updated:** April 2026  
**Version:** 1.0 (Production Ready)  
**Status:** ✅ LIVE & MAINTAINED

---

Made with ❤️ for media makers and social impact leaders in Africa & the Middle East.
