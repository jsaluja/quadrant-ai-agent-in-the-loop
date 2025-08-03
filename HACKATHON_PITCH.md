# Quadrant AI - Hackathon Pitch

## 🧠 Inspiration

Ever feel drowning in your inbox? We do too! With the average knowledge worker receiving 121 emails per day and spending 2.6 hours daily managing them, email overload has become a productivity killer. The Eisenhower Matrix is a proven decision-making framework used by executives, but manually applying it to hundreds of emails is impossible.

We were inspired to bridge this gap by creating an **AI-powered agent** that automatically triages your emails using the four-quadrant system (Do Now, Schedule, Delegate, Ignore) and even **speaks to you** about your most urgent items—because sometimes you need to hear about that critical client issue while you're grabbing coffee!

## 🚀 What it does

Quadrant AI is an **agentic workflow system** that transforms email chaos into actionable intelligence:

- **🤖 Smart Classification**: Uses SOTA LLMs to analyze email content and automatically categorize using the Eisenhower Matrix
- **📧 Multi-Source Integration**: Connects to multiple email providers. Gmail API was used for this hackathon
- **🎯 Priority Quadrants**: 
  - **Do Now** (Urgent + Important): Server outages, client emergencies
  - **Schedule** (Important, Not Urgent): Strategic planning, training programs
  - **Delegate** (Urgent, Not Important): Meeting requests, routine approvals
  - **Ignore** (Neither): Newsletters, spam, FYIs
- **🗣️ Voice Agent Integration**: Uses VAPI to create voice summaries of your most critical emails
- **📊 Engaging UI**: Clean Gradio interface showing your prioritized inbox
- **🔍 Smart Filtering**: Custom Gmail queries for targeted email analysis

## 🛠️ How we built it

Our **agentic workflow** leverages multiple AI systems working in harmony:

**Core Stack:**
- **Frontend**: Gradio for rapid prototyping
- **LLM Engine**: Ollama (Phi3) for local prototyping  Claude Sonnet 4 for production deployment
- **Voice AI**: VAPI integration for audio summaries, VAPI Cole, Deepgram transcriber, Nova3 transcription model
- **Email Integration**: Gmail API with OAuth2 authentication
- **Orchestration**: Python with async workflows

**AI Agent Architecture:**
1. **Email Ingestion Agent**: Fetches and preprocesses emails from Gmail
2. **Classification Agent**: LLM-powered analysis using structured prompts
3. **Voice Synthesis Agent**: Converts urgent emails to spoken summaries
4. **UI Orchestration Agent**: Manages real-time updates and user interactions

**Key Technical Innovations:**
- **Context-Aware Prompting**: Engineered prompts that understand business urgency vs. importance
- **Fallback Systems**: Fallback to local YAML, Olama for local prototyping
- **Real-time Processing**: Live classification with progress indicators
- **Privacy-First**: Local LLM processing keeps sensitive emails secure

## 🏔️ Challenges we ran into

- **LLM Consistency**: Getting reliable categorization required extensive prompt engineering and temperature tuning
- **Gmail API Complexity**: OAuth flows and rate limiting made real-time email fetching tricky
- **Voice Integration**: Synchronizing VAPI calls with email processing workflows
- **Email Parsing**: Handling diverse email formats (HTML, plain text, attachments)

## 🏆 Accomplishments that we're proud of

- **Built a Complete Agentic System**: Multiple AI agents working together seamlessly
- **Real-World Utility**: Actual time savings for email management (tested with real inboxes!)
- **Privacy-Conscious**: Local LLM processing protects sensitive business communications
- **Intuitive UX**: Non-technical users can immediately understand and use the system
- **Voice Innovation**: First email triage system with integrated voice summaries
- **Scalable Architecture**: Handles 5-50 emails with consistent performance

## 🎓 What we learned

- **Prompt Engineering is an Art**: Small changes in LLM prompts dramatically affect classification accuracy
- **User Context Matters**: The same email can be urgent or ignorable depending on the recipient's role
- **AI Workflows Need Fallbacks**: Robust systems require graceful failure modes
- **Voice Adds Emotional Intelligence**: Hearing about urgent emails creates different user engagement than reading
- **Demo Data Design**: Creating realistic test emails that showcase all use cases is surprisingly challenging

## 🌟 What's next for Quadrant AI

**Immediate Roadmap:**
- **Mobile / Voice first**: Upgrade from desktop web client to native mobile app
- **Multi-Account Support**: Handle multiple Gmail accounts and multiple email providers.
- **Learning Capabilities**: Train on user corrections to improve personal classification accuracy
- **Calendar Integration**: Auto-schedule "Schedule" quadrant items
- **Team Features**: Shared inboxes and delegation workflows

**Vision for Scale:**
- **Enterprise Deployment**: Slack/Teams integration for organizational email intelligence
- **Advanced Agents**: AI that drafts responses for different quadrants, schedules calendar invites
- **Workflow Automation**: Auto-forward "Delegate" emails to appropriate team members
- **Analytics Dashboard**: Team productivity insights and email pattern analysis
- **Mobile App**: Voice-first mobile experience for email triage on-the-go

**Ultimate Goal**: Transform Quadrant AI into the **operating system for knowledge work**—where every piece of information is automatically prioritized, routed, and actioned by intelligent agents, freeing humans to focus on what truly matters.

---

*Quadrant AI: Because your inbox shouldn't run your life. Your AI should.*
