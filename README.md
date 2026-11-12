# DevHandover AI

**AI-Powered Employee Knowledge Transfer and Handover Management
System**

DevHandover AI helps organizations capture, organize, verify, and
transfer critical project knowledge when employees move roles or leave
an organization. It combines multi-document knowledge retrieval,
AI-assisted interviews, knowledge-gap detection, evidence verification,
continuity-risk assessment, and successor-readiness tracking in one
Streamlit application.

-   **Live application:** https://devhandover-ai.streamlit.app
-   **GitHub repository:**
    https://github.com/suryanshraj2029/devhandover-ai
-   **Application entry point:** `app.py`

------------------------------------------------------------------------

## 1. Problem Statement

When an employee leaves or changes responsibilities, important project
knowledge can leave with them. Documentation may be incomplete,
operational decisions may exist only in an employee's experience, and
successors may not know which topics remain unclear.

Traditional handovers often rely on scattered documents, informal
conversations, and manual checklists. This can lead to: - Loss of
critical technical and operational knowledge. - Incomplete or outdated
project documentation. - Unidentified knowledge gaps. - Limited
visibility into handover progress and continuity risks. - Difficulty
determining whether a successor is prepared to take ownership.

## 2. Proposed Solution

DevHandover AI provides a structured, AI-assisted handover workflow. It
brings project documents, employee knowledge, evidence, identified gaps,
risk indicators, and successor-readiness activities together in one
workspace.

The system uses uploaded documentation as a knowledge source, captures
additional knowledge through structured interviews, identifies areas
that need clarification, and gives managers and successors a
consolidated view of handover progress.

AI-generated content and evaluation results are decision-support
information. The responsible employee or manager should review them
before treating them as verified.

------------------------------------------------------------------------

## 3. System Architecture

The application follows a Streamlit-based, modular Python architecture.
The user interacts with the Streamlit interface; application modules
coordinate PDF processing, retrieval, AI-assisted analysis, and
persistence.

### 3.1 High-Level Architecture

``` mermaid
flowchart TD
    U[Admin / Manager / Outgoing Staff / Successor]
    UI[Streamlit User Interface]
    APP[Application Logic and Workflow Controller]

    subgraph DOC[Document Knowledge Pipeline]
        UP[PDF Upload - Single or Multiple Documents]
        PDF[PyMuPDF Text Extraction]
        META[Document and Page Metadata]
        CHUNK[Text Chunking]
        EMB[Semantic Embedding and Indexing]
        RET[Semantic Retrieval]
        KW[Keyword Retrieval Fallback]
    end

    subgraph AI[AI-Assisted Intelligence]
        GEM[Google Gemini API]
        INT[AI Knowledge Interview]
        GAP[Knowledge Gap Detection]
        EVID[Evidence Verification]
        RISK[Continuity Risk Assessment]
        READY[Successor Readiness Evaluation]
    end

    subgraph DATA[Persistence and Outputs]
        DB[(SQLite Database)]
        HIST[Interview and Project History]
        DASH[Risk and Readiness Dashboard]
        PACK[Handover Package]
    end

    U --> UI --> APP
    APP --> UP --> PDF --> META --> CHUNK --> EMB
    APP --> RET
    EMB --> RET
    RET --> KW
    RET --> GEM
    APP --> GEM
    GEM --> INT
    GEM --> GAP
    RET --> EVID
    GEM --> GAP
    APP --> RISK
    APP --> READY
    APP <--> DB
    DB --> HIST
    GAP --> DASH
    EVID --> DASH
    RISK --> DASH
    READY --> DASH
    APP --> PACK
    DASH --> UI
    HIST --> UI
    PACK --> UI
```

### 3.2 Main Architecture Components

  -----------------------------------------------------------------------
  Component                           Responsibility
  ----------------------------------- -----------------------------------
  Streamlit UI                        Provides navigation and screens for
                                      the different user roles and
                                      handover activities.

  Application logic                   Coordinates workspaces, document
                                      processing, interviews, analysis,
                                      and handover workflows.

  PDF processor                       Uses PyMuPDF to extract text from
                                      uploaded PDF files page by page.

  Metadata and chunking               Splits extracted text into
                                      manageable passages while retaining
                                      document and page references.

  Knowledge index                     Supports semantic retrieval over
                                      indexed passages and keyword-based
                                      fallback retrieval.

  Gemini integration                  Supports AI-assisted question
                                      answering, interview analysis,
                                      follow-up generation, and
                                      knowledge-gap analysis.

  Evidence verification               Compares employee-provided answers
                                      with relevant extracted document
                                      passages.

  Risk and readiness modules          Calculate or summarize
                                      continuity-risk indicators and
                                      successor checklist progress.

  SQLite database                     Stores application records such as
                                      workspace and handover-related
                                      information.

  Handover dashboard and package      Brings together review information
                                      and presents structured handover
                                      outputs.
  -----------------------------------------------------------------------

### 3.3 Document Processing and Retrieval Flow

1.  A user uploads one or more PDF documents through the Streamlit
    interface.
2.  The PDF processor extracts text from each document using PyMuPDF.
3.  Extracted passages retain source metadata, including the document
    identity/name and page number.
4.  The text is divided into smaller chunks for indexing and retrieval.
5.  Semantic indexing makes passages searchable by meaning rather than
    exact wording alone.
6.  When a user asks a question, the system retrieves relevant passages
    using semantic retrieval, with keyword retrieval available as a
    fallback.
7.  Retrieved passages retain their source metadata so the Knowledge
    Assistant can show document and page references.
8.  The AI response can be reviewed against the cited source passages.

**Traceability principle:** source metadata travels with each indexed
chunk. This allows a retrieved passage to be connected back to its
original uploaded PDF and page, where that metadata is available.

### 3.4 Handover Intelligence Flow

``` mermaid
flowchart TD
    A[Uploaded Project Documents] --> B[Knowledge Index]
    C[Outgoing Employee Interview] --> D[Interview Answers]
    B --> E[Relevant Evidence Retrieval]
    D --> F[Answer and Evidence Review]
    E --> F
    F --> G[Knowledge Gap Detection]
    G --> H[Follow-up Questions]
    H --> C
    G --> I[Gap Status and Severity]
    F --> J[Evidence Verification Results]
    I --> K[Handover Risk and Readiness Dashboard]
    J --> K
    L[Successor Checklist] --> M[Readiness Evaluation]
    M --> K
    K --> N[Manager Review and Handover Package]
```

------------------------------------------------------------------------

## 4. Core Features

### 4.1 Workspace and Role-Based Workflow

-   Supports Admin, Manager, Outgoing Staff, and Successor roles.
-   Organizes handover work in project workspaces.
-   Provides workspace management and backup/restore workflows.

### 4.2 PDF Documentation Processing

-   Uploads project PDFs.
-   Extracts document text using PyMuPDF.
-   Preserves document and page information for source traceability.
-   Makes extracted content available to the knowledge workflow.

### 4.3 Knowledge Assistant

-   Answers questions using uploaded project documentation.
-   Uses semantic retrieval across indexed document content, with
    keyword-based retrieval as a fallback.
-   Displays source references such as document names and page numbers
    when available.
-   Helps users locate passages that support an answer.

### 4.4 AI Knowledge Interview

-   Generates questions for selected knowledge areas.
-   Captures the outgoing employee's answers.
-   Evaluates answers and can generate follow-up questions.
-   Maintains interview history and notes.

### 4.5 Knowledge and Expertise Maps

-   Organizes project knowledge areas and their relationships.
-   Helps visualize areas of expertise and knowledge ownership.

### 4.6 Handover Checkpoint Tracker

-   Tracks important knowledge-transfer activities.
-   Helps managers and successors monitor handover progress.

### 4.7 Project History and Successor Workspace

-   Maintains project and handover history.
-   Provides successors with a workspace to review project knowledge and
    ask questions.
-   Helps organize a structured handover package.

------------------------------------------------------------------------

## 5. Three Major Improvements

The following improvements extend the core handover workflow while
retaining the existing application modules.

### Improvement 1: Semantic, Multi-Document Knowledge Retrieval

**Objective:** Improve the Knowledge Assistant so it can retrieve
relevant knowledge across multiple uploaded PDF documents and preserve
the source of each retrieved passage.

**What this improvement adds** - Multiple-PDF document ingestion in the
knowledge workflow. - Text extraction from each uploaded PDF using
PyMuPDF. - Document-level and page-level source metadata. - Text
chunking so long documents can be indexed as smaller passages. -
Semantic retrieval so questions can find conceptually relevant passages
even when wording differs. - Keyword-based retrieval fallback when
semantic retrieval is unavailable or unsuitable. - Source-aware
retrieval results that can identify the document and page associated
with a passage. - Knowledge Assistant integration so answers can be
grounded in retrieved document content.

**How it works** 1. The user uploads multiple PDF files. 2. The
processor extracts text from each file. 3. The system associates
extracted text with its source document and page. 4. Text is split into
chunks and indexed for retrieval. 5. A user asks a question in the
Knowledge Assistant. 6. Relevant chunks are retrieved semantically, with
keyword fallback available. 7. Source metadata is used to show where
retrieved content came from.

**Value:** Users can search across project documentation in one workflow
and trace relevant passages to their source documents.

### Improvement 2: AI-Powered Knowledge Gap Detection

**Objective:** Identify project knowledge that is missing, incomplete,
unclear, or not adequately documented during employee handover.

**What this improvement adds** - Analysis of interview answers and
relevant knowledge areas. - Detection of incomplete or unclear
explanations. - Identification of topics that appear undocumented or
need additional evidence. - AI-generated, targeted follow-up
questions. - Gap severity categories: Critical, High, Medium, and Low. -
Persistent gap records in the application's database. - Gap status
tracking so the team can monitor follow-up work.

**How it works** 1. The outgoing employee answers an AI-generated
interview question. 2. The system evaluates the answer for completeness
and clarity. 3. Where appropriate, it compares the answer with available
project documentation. 4. It identifies areas that need clarification or
documentation. 5. It assigns an indicative severity and generates a
focused follow-up question. 6. The identified gap is recorded for review
and status tracking.

**Value:** The handover becomes proactive: instead of waiting for a
successor to discover missing knowledge, the team can identify and
address gaps during the transfer.

### Improvement 3: Evidence-Based Handover Risk and Readiness Dashboard

**Objective:** Bring important handover indicators together so managers
can review knowledge gaps, evidence status, continuity risk, successor
readiness, and approval progress.

**What this improvement adds** - A consolidated view of open knowledge
gaps and their severity/status. - Evidence-verification status,
including supported items and items needing review. - Continuity-risk
indicators and high-risk knowledge areas. - Successor-readiness
information based on recorded checklist progress. - Manager review and
approval status. - An action-plan view to help prioritize remaining
handover work.

**How it works** 1. The dashboard reads the available gap records and
their statuses. 2. It summarizes evidence-verification results. 3. It
presents continuity-risk indicators. 4. It summarizes successor
checklist completion. 5. It displays manager review/approval information
and outstanding actions. 6. Managers use the consolidated view to decide
what needs attention before handover completion.

**Value:** Managers get a more unified view of handover progress and can
prioritize unresolved risks and knowledge gaps.

### 5.1 How the Three Improvements Work Together

  -----------------------------------------------------------------------
  Improvement             Main question it helps  Output
                          answer                  
  ----------------------- ----------------------- -----------------------
  Semantic,               What do our uploaded    Relevant passages with
  multi-document          project documents say?  source references.
  retrieval                                       

  AI knowledge-gap        What knowledge is       Gap records, severity,
  detection               missing or needs        and follow-up
                          clarification?          questions.

  Evidence-based risk and What remains risky,     Consolidated gap,
  readiness dashboard     unsupported, or         evidence, risk,
                          incomplete before       readiness, and review
                          handover?               indicators.
  -----------------------------------------------------------------------

Together, these improvements create a connected workflow: retrieve
documented knowledge, identify what is missing, capture clarification
from employees, review supporting evidence, and monitor handover
readiness.

------------------------------------------------------------------------

## 6. Risk Assessment and Successor Readiness

### 6.1 Continuity Risk Assessment

The application presents continuity-risk indicators to help teams
identify areas that may need attention. The illustrative weighted
assessment uses: - Knowledge concentration: 40% - Business impact: 35% -
Documentation weakness: 25%

These weights are an assessment model used by the application. The
resulting score is a decision-support indicator and is not an objective
guarantee of actual business risk.

### 6.2 Successor Readiness Evaluation

The successor checklist can track activities such as: - Reviewing
project documentation. - Understanding project architecture. -
Completing installation and setup. - Understanding common errors and
troubleshooting. - Understanding project roles and responsibilities. -
Recording important technical knowledge transferred. - Recording pending
tasks or knowledge areas.

The readiness evaluation is based on recorded checklist completion and
supplied information. It should not be interpreted as independent proof
of technical competence.

------------------------------------------------------------------------

## 7. Technology Stack

  Area                   Technology
  ---------------------- ------------------------------------------
  User interface         Streamlit
  Programming language   Python
  PDF text extraction    PyMuPDF
  AI integration         Google Gemini (`google-genai`)
  Data storage           SQLite
  Knowledge retrieval    Semantic retrieval with keyword fallback
  Data handling          Pandas
  Source control         Git and GitHub
  Deployment             Streamlit Community Cloud

------------------------------------------------------------------------

## 8. Application Workflow

1.  **Create or select a workspace** for the project handover.
2.  **Upload project PDFs** to provide documentation context.
3.  **Ask questions** in the Knowledge Assistant and review source
    references.
4.  **Conduct AI-assisted interviews** with the outgoing employee.
5.  **Identify knowledge gaps** and use follow-up questions to clarify
    missing information.
6.  **Review evidence** by comparing interview answers with uploaded
    documentation.
7.  **Review knowledge maps, expertise maps, and checkpoints** to
    identify areas needing attention.
8.  **Assess continuity risk** and inspect high-risk knowledge areas.
9.  **Evaluate successor readiness** and record pending activities.
10. **Complete manager review** and prepare the handover package.

------------------------------------------------------------------------

## 9. Local Setup

### Prerequisites

-   Python 3.10 or a compatible newer Python version.
-   Git.
-   A Google Gemini API key if AI-powered features are enabled.

### Step 1: Clone the repository

``` bash
git clone https://github.com/suryanshraj2029/devhandover-ai.git
cd devhandover-ai
```

### Step 2: Create and activate a virtual environment

**Windows PowerShell**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies

``` bash
pip install -r requirements.txt
```

### Step 4: Configure the Gemini API key

If the current application reads its API key from environment variables,
create a local `.env` file in the project root:

``` env
GEMINI_API_KEY=your_gemini_api_key
```

Use the exact environment-variable name expected by the current
application code. Never commit `.env` or expose API keys in source code.

For Streamlit Community Cloud, add the required secret in **Manage app →
Settings → Secrets**, using the same key name expected by the
application.

### Step 5: Run the application

``` bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal, usually
`http://localhost:8501`.

------------------------------------------------------------------------

## 10. Deployment

The project is deployed using Streamlit Community Cloud.

**Live application:** https://devhandover-ai.streamlit.app

To deploy your own copy: 1. Push the project to a GitHub repository. 2.
Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with
GitHub. 3. Create an app and select the repository and branch. 4. Set
the main file path to `app.py`. 5. Configure required secrets, including
the Gemini API key, using the names expected by the code. 6. Deploy and
test the application.

------------------------------------------------------------------------

## 11. Security, Validation, and Limitations

-   Keep API keys, passwords, and private documents out of public
    repositories.
-   Do not commit `.env`, virtual-environment folders, or other secrets.
-   Review AI-generated interview notes, follow-up questions, and gap
    classifications before relying on them.
-   Evidence matching indicates whether an answer is supported by
    retrieved documentation; it does not independently prove that the
    statement is true.
-   Source references depend on the extracted text and retained metadata
    being available and correctly associated with the passage.
-   OCR for scanned or image-only PDFs should not be assumed unless it
    has been separately implemented and tested.
-   Continuity-risk scores and successor-readiness scores are
    decision-support indicators, not guarantees.
-   Manager approval recorded in the application is an application
    workflow action, not a digital signature or legal certification.
-   SQLite persistence on hosted environments may not be durable across
    all redeployments or restarts. Use an appropriate persistent
    database and tested backup strategy for production use.
-   Test multiple-document uploads, retrieval accuracy, source
    references, and all handover workflows with representative documents
    before relying on the application in an operational environment.

------------------------------------------------------------------------

## 12. Future Enhancements

Potential future improvements include: - OCR support for scanned PDF
documents. - Stronger production database and persistent storage
integration. - More extensive retrieval evaluation and source-grounding
tests. - Advanced access control and audit logging. - Automated
notifications and handover reminders. - Performance and security testing
for larger teams and document collections. - Additional integrations
with organizational knowledge and project-management systems.

------------------------------------------------------------------------

## 13. Project Purpose

DevHandover AI aims to reduce organizational knowledge loss by turning
employee experience and project documentation into a structured,
reviewable, and reusable handover process.

**Knowledge continuity. Risk visibility. Confident handovers.**

------------------------------------------------------------------------

## 14. Contributing

Contributions, bug reports, and suggestions are welcome.

1.  Create a branch for your work.
2.  Make focused changes and test them locally.
3.  Submit a pull request describing the change.

## 15. License

Add the license selected by the project owners before distributing this
repository for reuse.
