# 🤖 Multi-Agent Autonomous Research & Critique System

A modular, multi-agent AI research pipeline powered by **LangChain**, **Google Gemini** (`gemini-3.6-flash`), and **Tavily AI Search**. This system automates the complete lifecycle of investigative research: querying live web intelligence, extracting deep webpage content, synthesizing structured executive reports, and conducting rigorous peer review and criticism.

---

📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Project Directory Structure](#-project-directory-structure)
- [Installation & Environment Setup](#-installation--environment-setup)
- [Configuration & API Keys](#-configuration--api-keys)
- [Usage & Execution](#-usage--execution)
  - [1. Running the Baseline Pipeline](#1-running-the-baseline-pipeline)
  - [2. Running the Structured Output Pipeline](#2-running-the-structured-output-pipeline)
  - [3. Verifying Gemini API Connectivity](#3-verifying-gemini-api-connectivity)
- [Comparison: Baseline vs. Structured (`claude/`)](#-comparison-baseline-vs-structured-claude)
- [Output Examples](#-output-examples)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)
- [Future Enhancements](#-future-enhancements)

---

## 🌟 Overview

Conducting in-depth research requires finding relevant sources, reading deep into source articles, distilling key takeaways into a coherent synthesis, and critically verifying the quality of the findings.

This multi-agent architecture divides cognitive labor into specialized functional units:
1. **Search Agent**: Identifies top search results, snippets, and reliable URLs via Tavily.
2. **Scraper Agent**: Inspects candidate URLs, fetches web pages, strips boilerplate (scripts, navs, footers), and extracts dense textual context.
3. **Writer Chain**: Synthesizes search snippets and deep scraped text into a formal report with introduction, key findings, conclusion, and citations.
4. **Critic Chain**: Evaluates the synthesized report against editorial criteria, scoring it out of 10 and offering actionable critiques.



🚀 Key Features

- **Agentic Decision Making**: Uses LangChain's `create_agent` framework equipped with tool-calling capabilities.
- **Deep Web Intelligence**: Integrates Tavily API for real-time search and custom BeautifulSoup4 extractors for full-text web scraping.
- **Dual Pipeline Architectures**:
  - **Standard Text Pipeline** (`pipeline.py`): Quick string generation and console logging.
  - **Structured Schema Pipeline** (`claude/pipeline.py`): Uses `StructuredOutputParser` and `ResponseSchema` to ensure valid, machine-readable JSON dictionary outputs.
- **Strict Quality Control**: Automated critic agent delivers transparent feedback, scoring, and verdict for iterative review.
- **Robust Error Handling**: Non-crashing fallbacks for web requests, scraping timeouts, and SSL variances.

---

## 🏗️ System Architecture

```
                  ┌───────────────────────┐
                  │      User Topic       │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │  Step 1: Search Agent │ ──► [Tavily Search API]
                  └───────────┬───────────┘
                              │ Search Results (URLs + Snippets)
                              ▼
                  ┌───────────────────────┐
                  │ Step 2: Scraper Agent │ ──► [Web Scraper (BS4)]
                  └───────────┬───────────┘
                              │ Scraped Context (De-cluttered Text)
                              ▼
                  ┌───────────────────────┐
                  │  Step 3: Writer Chain │ ──► [Gemini 3.6 Flash]
                  └───────────┬───────────┘
                              │ Synthesized Research Report
                              ▼
                  ┌───────────────────────┐
                  │  Step 4: Critic Chain │ ──► [Score + Strengths + Verdict]
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │ Final Research State  │
                  └───────────────────────┘
```

---

## 📂 Project Directory Structure

```plaintext
Mulit-Agent system/
├── .env                       # Local environment variables & secrets (API keys)
├── requirement.txt            # System dependencies and package pinning
├── test.py                    # Sanity check for Gemini SDK connectivity
│
├── agents.py                  # Baseline agent declarations & LLM chains
├── pipeline.py                # Baseline sequential workflow orchestrator
├── tools.py                   # Custom agent tools (web_search, web_scraper)
│
├── claude/                    # Enhanced variant with Structured Output Parsers
│   ├── agents.py              # Structured response schemas for Writer & Critic
│   ├── pipeline.py            # Formatted dictionary logging orchestrator
│   └── tools.py               # Tool definitions matching the variant
│
├── README.md                  # System manual and technical overview
├── FLOW.md                    # Data flow and architectural state transitions
└── EXECUTIONPLAN.md           # Operational guide, troubleshooting, and execution steps
```

---

## ⚙️ Installation & Environment Setup

### Prerequisites
- **Python**: Version `3.10` or higher recommended.
- **Virtual Environment tool**: `venv` or `conda`.

### 1. Clone or Open Workspace
Ensure you are in the workspace root directory:
```bash
cd "c:\Users\LENOVO\Desktop\Mulit-Agent system"
```

### 2. Activate Virtual Environment
Use the existing virtual environment or create a fresh one:

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If script execution is disabled, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

**Windows Command Prompt (cmd):**
```cmd
.venv\Scripts\activate.bat
```

### 3. Install Required Dependencies
Install the pinned packages from [requirement.txt](file:///c:/Users/LENOVO/Desktop/Mulit-Agent%20system/requirement.txt):
```bash
pip install -r requirement.txt
```

---

## 🔑 Configuration & API Keys

The pipeline requires API credentials stored in a `.env` file at the root of the project:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_google_gemini_api_key_here

# Tavily AI Search API Key
TAVILY_API_KEY=your_tavily_api_key_here
```

### How to obtain keys:
1. **Google Gemini API Key**: Generate a free or paid API key on the [Google AI Studio](https://aistudio.google.com/).
2. **Tavily Search API Key**: Generate an API key with 1,000 free monthly queries on [Tavily AI](https://tavily.com/).

---

## 💻 Usage & Execution

### 1. Running the Baseline Pipeline
The standard sequential pipeline logs free-form text responses:

```bash
python pipeline.py
```
**Interactive Prompt:**
```text
Enter the research topic: Breakthroughs in Quantum Computing 2026
```

### 2. Running the Structured Output Pipeline
The structured variant parses reports and evaluations into strict schema-driven Python dictionaries:

```bash
python claude/pipeline.py
```
**Interactive Prompt:**
```text
Enter the research topic: Solid-State Battery Commercialization
```

### 3. Verifying Gemini API Connectivity
To verify that your Gemini API key is valid before executing the full pipeline:

```bash
python test.py
```
**Expected Output:**
```text
Gemini API key loaded: True
Hello! How can I help you today?
```

---

## ⚖️ Comparison: Baseline vs. Structured (`claude/`)

| Metric / Dimension | Baseline ([pipeline.py](file:///c:/Users/LENOVO/Desktop/Mulit-Agent%20system/pipeline.py)) | Structured ([claude/pipeline.py](file:///c:/Users/LENOVO/Desktop/Mulit-Agent%20system/claude/pipeline.py)) |
| :--- | :--- | :--- |
| **Output Type** | Plain strings / `AIMessage` content | Typed Python dictionaries |
| **Parsing Mechanism** | None (Raw model string output) | `StructuredOutputParser` via `ResponseSchema` |
| **Report Format** | Fenced text markdown | Dict keys: `introduction`, `key_findings`, `conclusion`, `sources` |
| **Critic Format** | Fenced text markdown | Dict keys: `score`, `strengths`, `areas_to_improve`, `verdict` |
| **Downstream Integration** | Human-readable console display | Machine-readable for databases, APIs, and UI frontend dashboards |

---

## 📊 Output Examples

### Sample Final Report (Structured)
```json
{
  "introduction": "Recent developments in solid-state battery technology have marked a pivotal shift in energy storage...",
  "key_findings": [
    "Sulfide-based solid electrolytes achieve ionic conductivity exceeding liquid counterparts at room temperature.",
    "Automotive manufacturers have initiated pilot manufacturing lines targeting commercial deployment by 2027.",
    "Manufacturing yield and interface impedance degradation remain key challenges under thermal cycling."
  ],
  "conclusion": "Solid-state batteries are progressing rapidly from laboratory proofs of concept to automotive pilot lines.",
  "sources": [
    "https://example.com/energy/solid-state-breakthrough",
    "https://example.com/materials/battery-electrolytes-2026"
  ]
}
```

### Sample Critic Review
```json
{
  "score": "8.5/10",
  "strengths": [
    "Clear differentiation of ionic conductivity benchmarks.",
    "Comprehensive citation of industrial pilot programs."
  ],
  "areas_to_improve": [
    "Include cost per kilowatt-hour projections.",
    "Provide deeper details on degradation under sub-zero temperatures."
  ],
  "verdict": "A high-quality, technically sound research summary with strong potential for executive briefing."
}
```

---

## 🛠️ Troubleshooting & FAQs

- **`google.genai.errors.APIError: 403 / 400`**: Check that your `GEMINI_API_KEY` is loaded and that the model specified (`gemini-3.6-flash`) is accessible with your API tier.
- **`TavilyClient Exception: Invalid API Key`**: Ensure `TAVILY_API_KEY` in `.env` is populated without enclosing quotes or accidental spaces.
- **`OutputParserException: Failed to parse...`**: Occurs occasionally in `claude/pipeline.py` if the LLM adds extraneous commentary. Rerun the script or lower temperature to `0` (already default).
- **SSL Certificate Errors during Scraping**: `web_scraper` uses `verify=False` to handle self-signed certificates gracefully.

---

## 🔭 Future Enhancements

1. **LangGraph StateGraph Integration**: Implement cyclic feedback where the Critic sends actionable suggestions back to the Writer for automated refinement loops until a target score (e.g. 9/10) is achieved.
2. **Parallel Scraping**: Concurrent async scraping of multiple top URLs using `aiohttp`.
3. **Export Formats**: Automatic export of the final report to PDF, Markdown, and Notion.
4. **Interactive UI**: Web dashboard using Streamlit or FastAPI with real-time agent thought streaming.
