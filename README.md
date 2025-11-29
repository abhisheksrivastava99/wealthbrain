# Wealth Brain: WM AI Concierge 🏦

**Wealth Brain** is an intelligent, agentic AI concierge designed for Ultra-High-Net-Worth (UHNW) family offices. It acts as a unified "Wealth Analyst," capable of answering complex questions about financial portfolios, legal documents, and external market intelligence.

Built with **Python**, **Streamlit**, and **LangChain**, it employs a **Router-Agent Architecture** to dynamically dispatch queries to specialist agents.

---

## 🚀 Features

*   **Multi-Family Support**: Manage multiple family offices (Wayne, Lannister, Stark, Targaryen, Baratheon) with isolated data contexts.
*   **Hybrid RAG System**: Combines structured data analysis (SQL/CSV) with unstructured document retrieval (Vector RAG).
*   **Tri-Agent Architecture**:
    *   **Analyst Agent**: Python/Pandas agent for quantitative portfolio analysis (AUM, asset allocation, performance).
    *   **Lawyer Agent**: RAG-based agent for querying legal documents (Wills, Trust Deeds, Insurance Policies).
    *   **Researcher Agent**: Perplexity-powered agent for real-time market intelligence and macro analysis.
*   **Smart Routing**: A Master Router (LLM) intelligently classifies user intent and routes queries to the correct agent or combines them for hybrid insights.
*   **Modern UI**: A polished, responsive Streamlit interface with family selection, dynamic dashboards, and "Chief Investment Officer" persona briefings.

---

## 🛠️ Tech Stack

*   **Frontend**: Streamlit (Custom CSS & Theming)
*   **Orchestration**: LangChain
*   **LLMs**: OpenAI GPT-4o (Router, Analyst, Lawyer), Perplexity `sonar-reasoning` (Researcher)
*   **Data**: Pandas (Structured), FAISS (Vector Store)
*   **Environment**: Python 3.10+

---

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd wealth-brain
    ```

2.  **Create a virtual environment** (Recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**:
    Create a `.env` file in the root directory and add your API keys:
    ```ini
    OPENAI_API_KEY=sk-...
    PERPLEXITY_API_KEY=pplx-...
    ```

---

##  ▶️ Usage

1.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

2.  **Navigate**:
    *   Select a **Family Office** from the home page cards.
    *   Use the **Chat Interface** to ask questions.
    *   View **Real-time Data** in the sidebar and "View Portfolio Data" expander.

### Example Queries
*   **Analyst**: "What is the total value of the Wayne family portfolio?"
*   **Lawyer**: "Who are the beneficiaries in the Stark Trust Deed?"
*   **Researcher**: "How does the latest Fed rate hike affect the real estate market?"
*   **Hybrid**: "How do the new tariffs affect my specific assets?" (Triggers smart portfolio mapping).

---

## 📂 Project Structure

```
wealth-brain/
├── agents/                 # AI Agent Definitions
│   ├── analyst.py          # Pandas DataFrame Agent
│   ├── lawyer.py           # RAG Document Agent
│   ├── researcher.py       # Perplexity Market Agent
│   └── router.py           # Master Orchestrator
├── data/                   # Mock Data Storage
│   ├── portfolio.csv       # Structured Financial Data
│   └── legal_docs/         # Unstructured Text Documents
├── .streamlit/             # Streamlit Configuration
│   └── config.toml         # Theme & Color Settings
├── app.py                  # Main Streamlit Application
├── generate_docs.py        # Script to generate mock legal docs
├── requirements.txt        # Python Dependencies
└── README.md               # Project Documentation
```

---

## 🛡️ License

This project is for demonstration purposes.
