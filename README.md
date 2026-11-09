# 🚀 DevHandover AI
### AI-Powered Project Knowledge Continuity & Employee Handover Management Platform

**DevHandover AI** is an intelligent knowledge management platform designed to prevent critical project knowledge from being lost when employees leave, change roles, or transfer responsibilities.

It helps organizations preserve technical knowledge, identify knowledge gaps, assess continuity risks, conduct structured knowledge interviews, and prepare successors to take over projects confidently.

---

## 🎯 Problem Statement

When an experienced employee leaves an organization, important project knowledge can disappear with them.

This may result in:
- Loss of technical knowledge and project decisions.
- Difficulty understanding existing codebases and architecture.
- Delays in onboarding replacement employees.
- Dependency on a single employee for critical information.
- Increased project continuity risks.

## 💡 Our Solution

DevHandover AI provides an AI-assisted platform that converts project documentation and knowledge-sharing information into structured, searchable, and actionable handover information.

It supports outgoing employees, incoming successors, managers, and backup team members throughout the handover process.

## ✨ Key Features

### 1. Project Workspace Management
- Create and manage project workspaces.
- Maintain project-specific handover information.
- Manage existing workspaces.

### 2. PDF Knowledge Extraction
- Upload project documentation in PDF format.
- Extract text using PyMuPDF.
- Preserve page-level references for knowledge retrieval.

### 3. AI Project Knowledge Assistant
- Ask questions about uploaded project documentation.
- Generate answers using Gemini AI.
- Display relevant PDF page references.
- Help successors understand technical information.

### 4. Knowledge Gap Detector
- Identify missing or insufficient project documentation.
- Analyze important knowledge areas such as architecture, technology stack, setup, troubleshooting, and responsibilities.

### 5. Continuity Risk Assessment
- Evaluate knowledge concentration.
- Assess business impact.
- Identify documentation weaknesses.
- Calculate continuity risk scores.
- Suggest actions to reduce identified risks.

### 6. AI-Guided Knowledge Interview
- Generate knowledge-transfer questions using Gemini.
- Evaluate employee responses.
- Identify incomplete answers.
- Suggest follow-up questions.
- Save interview records.

### 7. Evidence Verification
- Support verification of handover information using available evidence.
- Help distinguish documented information from information that needs further confirmation.

### 8. Project Knowledge Map
- Organize project knowledge into important technical areas.
- Display available documentation evidence and interview coverage.

### 9. Domain Expertise Map
- Identify primary and backup knowledge owners.
- Track expertise levels across project knowledge areas.
- Highlight single-person knowledge dependencies.

### 10. Handover Checkpoint Tracker
- Create handover checkpoints.
- Assign responsible team members.
- Set due dates.
- Track Planned, In Progress, Completed, and Blocked tasks.
- Monitor handover progress.

### 11. Successor Readiness Assessment
- Evaluate successor understanding.
- Track documentation review, architecture understanding, setup, troubleshooting, and responsibilities.
- Calculate readiness scores.
- Support manager review and approval.

### 12. Successor Knowledge Workspace
- Allow successors to ask project-related questions.
- Retrieve information from project documentation and saved interview notes.
- Maintain successor learning history.

### 13. Handover Package Generator
- Generate a consolidated PDF handover package.
- Include relevant project information, knowledge records, risk assessments, checkpoints, and readiness details.

### 14. Data Persistence
- Store project information using SQLite.
- Maintain workspace-specific records.
- Retrieve saved information across application sessions.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | User interface |
| Gemini AI | AI-powered question generation and answers |
| PyMuPDF | PDF text extraction |
| SQLite | Database and data persistence |
| Pandas | Data processing and reporting |
| Python-dotenv | Environment variable management |

## 🏗️ System Architecture

```text
              USER
                |
                v
        STREAMLIT INTERFACE
                |
                v
        PROJECT WORKSPACE
                |
        +-------+--------+
        |                |
        v                v
    PDF UPLOAD      KNOWLEDGE INTERVIEWS
        |                |
        v                v
     PyMuPDF          Gemini AI
        |                |
        +-------+--------+
                |
                v
       KNOWLEDGE PROCESSING
                |
        +-------+--------+
        |       |        |
        v       v        v
      KNOWLEDGE RISK   SUCCESSOR
       GAPS    ENGINE  READINESS
        |       |        |
        +-------+--------+
                |
                v
          SQLITE DATABASE
                |
                v
       HANDOVER REPORTS
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.11 or higher
- Visual Studio Code
- Git
- Gemini API key

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/devhandover-ai.git
```

### Step 2: Open the Project

```bash
cd devhandover-ai
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key.

**Important:** Never upload your `.env` file or API key to GitHub.

### Step 7: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧪 Testing

The application can be tested using a sample project documentation PDF.

Suggested testing areas:

- PDF upload and text extraction.
- AI-generated project questions and answers.
- Knowledge gap identification.
- Continuity risk calculations.
- Knowledge interview evaluation.
- Domain expertise and ownership.
- Handover checkpoint tracking.
- Successor readiness assessment.
- Handover PDF generation.
- Workspace data persistence.

## ⚠️ Current Limitations

- The current PDF uploader supports a single document at a time; multiple-file upload is not yet implemented.
- Scanned PDFs requiring OCR are not currently supported by the standard text-extraction workflow.
- Keyword-based retrieval may not identify every relevant passage, especially when different terminology is used.
- AI-generated responses should be reviewed and verified by a human.
- Continuity risk scores are indicators for decision support, not guaranteed predictions.
- The application currently uses local SQLite storage.

## 🔒 Security and Privacy

- Keep API keys in environment variables.
- Do not commit `.env` files, databases, backups, or confidential project documents.
- Use synthetic, anonymized, or authorized sample documents for demonstrations.
- Review generated handover information before approving it.

## 🚀 Future Enhancements

1. Multiple PDF and document uploads with combined knowledge retrieval.
2. OCR support for scanned documents and improved multi-column PDF extraction.
3. Semantic search using embeddings and vector databases.
4. Role-based authentication and access control.
5. Automated backup and restore management.
6. Integration with project management and documentation platforms.

## 👥 Project Information

**Project Name:** DevHandover AI

**Category:** Artificial Intelligence | Knowledge Management | Workforce Continuity

**Purpose:** Preserve organizational knowledge and make employee handovers more reliable, structured, and efficient.

---

### ⭐ Our Vision

**"No project should lose its knowledge when an employee leaves."**

DevHandover AI aims to transform employee handovers from an informal knowledge-transfer process into a structured, evidence-supported, and AI-assisted continuity system.