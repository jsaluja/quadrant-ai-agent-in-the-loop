# 📧 Quadrant AI - Intelligent Email Triage System

> Transform your email chaos into actionable intelligence using AI-powered agents and the Eisenhower Matrix

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)](https://gradio.app/)
[![Gmail API](https://img.shields.io/badge/Gmail-API-red.svg)](https://developers.google.com/gmail/api)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🧠 What is Quadrant AI?

Quadrant AI is an **agentic workflow system** that automatically triages your emails using the proven Eisenhower Matrix framework. With multiple AI agents working in harmony, it transforms email overload into organized, actionable intelligence - and even **speaks to you** about your most urgent items!

### 🎯 How It Aligns with Agentic Workflows

**"Build autonomous agents that think, act, and execute"** - This perfectly describes Quadrant AI's core architecture.

#### Our Autonomous Agent System:

**🧠 THINKS**: 
- Classification Agent uses advanced reasoning to understand email context, sender relationships, and business impact
- Context-aware prompting enables the AI to distinguish between truly urgent items vs. false alarms
- System learns patterns: "Server down" emails are always urgent, while "newsletter" emails rarely are

**⚡ ACTS**:
- Email Ingestion Agent automatically fetches and preprocesses emails from multiple sources
- Voice Synthesis Agent proactively creates audio summaries for critical items
- UI Orchestration Agent manages real-time updates and user interactions without manual intervention

**🚀 EXECUTES**:
- Complete end-to-end workflow: Email → Analysis → Classification → Voice Alert → Dashboard Update
- Autonomous decision-making using the Eisenhower Matrix framework
- Self-healing fallback systems (Gmail API → Local processing when needed)
- Real-time execution with progress tracking and error handling

## 🚀 Features

- **🤖 Smart Classification**: Uses SOTA LLMs to analyze email content and automatically categorize using the Eisenhower Matrix
- **📧 Multi-Source Integration**: Connects to multiple email providers (Gmail API implemented)
- **🎯 Priority Quadrants**: 
  - **Do Now** (Urgent + Important): Server outages, client emergencies
  - **Schedule** (Important, Not Urgent): Strategic planning, training programs
  - **Delegate** (Urgent, Not Important): Meeting requests, routine approvals
  - **Ignore** (Neither): Newsletters, spam, FYIs
- **🗣️ Voice Agent Integration**: Uses VAPI to create voice summaries of critical emails
- **📊 Engaging UI**: Clean Gradio interface showing your prioritized inbox
- **🔍 Smart Filtering**: Custom Gmail queries for targeted email analysis
- **🔒 Privacy-First**: Local LLM processing keeps sensitive emails secure

## 🛠️ Architecture

### AI Agent Components:
1. **Email Ingestion Agent**: Fetches and preprocesses emails from Gmail
2. **Classification Agent**: LLM-powered analysis using structured prompts
3. **Voice Synthesis Agent**: Converts urgent emails to spoken summaries
4. **UI Orchestration Agent**: Manages real-time updates and user interactions

### Tech Stack:
- **Frontend**: Gradio for rapid prototyping
- **LLM Engine**: Ollama (Phi3) for local prototyping / Claude Sonnet 4 for production
- **Voice AI**: VAPI integration with Cole voice, Deepgram transcriber, Nova3 transcription
- **Email Integration**: Gmail API with OAuth2 authentication
- **Orchestration**: Python with async workflows

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Gmail account (for real email integration)
- Ollama installed locally (for LLM processing)
- VAPI account (for voice features)

### 1. Clone the Repository

```bash
git clone https://github.com/jsaluja/quadrant-ai-agent-in-the-loop.git
cd quadrant-ai-agent-in-the-loop
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Gmail API (Optional - for real emails)

Follow the detailed instructions in [`GMAIL_SETUP.md`](GMAIL_SETUP.md) to:
1. Enable Gmail API in Google Cloud Console
2. Create OAuth 2.0 credentials
3. Download `credentials.json` to project root

### 4. Set Up Ollama (for local LLM)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the Phi3 model
ollama pull phi3
```

### 5. Configure Environment Variables

```bash
export VAPI_PUBLIC_KEY="your_vapi_public_key"
export VAPI_PRIVATE_KEY="your_vapi_private_key"
export VAPI_ASSISTANT_ID="your_vapi_assistant_id"
```

### 6. Run the Application

```bash
python quadrant_ai_assistant.py
```

The Gradio interface will launch at `http://localhost:7860`

## 📧 Usage

### With Gmail Integration:
1. ✅ Check "Gmail" option
2. 🔢 Set max emails to fetch (5-50)
3. 🔍 Enter Gmail query (e.g., `is:unread`, `from:boss@company.com`)
4. 🚀 Click "Classify Emails"

### Demo Mode:
1. ❌ Uncheck "Gmail" option
2. 🚀 Click "Classify Emails" to use sample data from `emails.yaml`

### Voice Features:
- 🔊 When "Do Now" emails are found, the system automatically creates voice summaries
- 🎧 Listen to urgent email alerts through VAPI integration

## 🎯 Email Classification Examples

| Email Subject | Category | Reason |
|---------------|----------|--------|
| "URGENT: Server Down" | **Do Now** | Production impact, immediate action needed |
| "Q4 Strategic Planning" | **Schedule** | Important for business, not time-sensitive |
| "Meeting Request for Next Week" | **Delegate** | Urgent response needed, low importance |
| "Newsletter: Industry Updates" | **Ignore** | Neither urgent nor immediately important |

## 🔧 Configuration

### Gmail Queries
Use standard Gmail search syntax:
- `is:unread` - Only unread emails
- `from:boss@company.com` - From specific sender
- `subject:urgent` - Contains keyword in subject
- `newer_than:1d` - From last 24 hours

### LLM Models
- **Local**: Phi3 via Ollama (privacy-focused)
- **Production**: Claude Sonnet 4 (higher accuracy)

## 🏗️ Project Structure

```
quadrant-ai-agent-in-the-loop/
├── quadrant_ai_assistant.py    # Main application
├── requirements.txt            # Python dependencies
├── emails.yaml                # Sample email data
├── GMAIL_SETUP.md             # Gmail API setup guide
├── HACKATHON_PITCH.md         # Hackathon submission details
├── credentials.json           # Gmail OAuth credentials (you create)
├── token.json                 # Gmail auth tokens (auto-generated)
└── README.md                  # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🚀 Roadmap

### Immediate Features:
- [ ] Mobile/Voice-first native app
- [ ] Multi-account email support
- [ ] Learning from user corrections
- [ ] Calendar integration for scheduling
- [ ] Team delegation workflows

### Long-term Vision:
- [ ] Enterprise Slack/Teams integration
- [ ] AI-powered response drafting
- [ ] Advanced analytics dashboard
- [ ] Workflow automation engine
- [ ] Operating system for knowledge work

## 🏆 Hackathon Details

Built for the **Agentic Workflows** track, demonstrating:
- ✅ Multi-agent coordination
- ✅ Autonomous decision-making
- ✅ Adaptive behavior handling
- ✅ Proactive action execution
- ✅ Complex workflow orchestration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Eisenhower Matrix](https://todoist.com/productivity-methods/eisenhower-matrix) for the productivity framework
- [Ollama](https://ollama.ai/) for local LLM capabilities
- [VAPI](https://vapi.ai/) for voice AI integration
- [Gradio](https://gradio.app/) for rapid UI development
- [Gmail API](https://developers.google.com/gmail/api) for email integration

---

**Quadrant AI: Because your inbox shouldn't run your life. Your AI should.**

*Transform email chaos → Actionable intelligence → Voice-enabled alerts → Productive workflow*
