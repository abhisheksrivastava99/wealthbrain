
***

# Product Requirements Document: Wealth Brain AI Concierge ("The Wealth Brain")
**Version:** 2.0 (Comprehensive Technical Spec)
**Target Audience:** Engineering Team (Thrymr) & AI Developers
**Context:** Wealth Management Platform for UHNWIs & Family Offices

## 1. System Overview
The **Wealth Brain AI Concierge** is a Hybrid RAG (Retrieval-Augmented Generation) system designed to act as an intelligent "Wealth Analyst" for high-net-worth clients. It unifies three distinct data domains into a single conversational interface:
1.  **Structured Financial Data:** Real-time portfolio values, asset allocation, and exposure (SQL/CSV).
2.  **Unstructured Legal Data:** Trust deeds, wills, insurance policies, and entity structures (PDF/Docs).
3.  **External Market Intelligence:** Live market trends, tax regulations, and geopolitical news (Perplexity API).

## 2. Core Architecture: The "Tri-Agent" Router
The system follows a **Router-Agent** pattern. A central "Master Router" (LLM) analyzes the user's intent and dispatches the query to one (or multiple) specialist tools.

### 2.1. The Master Router (Orchestrator)
*   **Role:** Intent classification & Response synthesis.
*   **Input:** User's natural language query.
*   **Logic:**
    *   *Intent A:* **Quantitative/Portfolio** -> Route to `Analyst_Agent`.
    *   *Intent B:* **Qualitative/Legal** -> Route to `Lawyer_Agent`.
    *   *Intent C:* **External/Market** -> Route to `Researcher_Agent` (Perplexity).
    *   *Intent D:* **Hybrid** -> Decompose query, call multiple agents, and synthesize the result.
*   **Output:** A unified, coherent answer with citations.

### 2.2. Agent A: The Analyst (Structured Data)
*   **Goal:** Answer questions about "How much," "Where," "Distribution," and "Performance."
*   **Tech Stack:** LangChain `PandasDataFrameAgent` or `SQLDatabaseChain`.
*   **Data Source:** `portfolio.csv` (Mock) / `Client_Assets_DB` (Prod).
*   **Capabilities:**
    *   Filtering (`WHERE Location = 'Singapore'`)
    *   Aggregation (`SUM(Value)`)
    *   Grouping (`GROUP BY Asset_Class`)
    *   Math (`(Value / Total_AUM) * 100`)

### 2.3. Agent B: The Lawyer (Unstructured Data)
*   **Goal:** Answer questions about "Who," "Terms," "Clauses," and "Entities."
*   **Tech Stack:** RAG Pipeline (RecursiveCharacterTextSplitter + FAISS/ChromaDB + OpenAI Embeddings).
*   **Data Source:** `legal_docs/` (PDFs of Wills, Trusts, Insurance).
*   **Key Config:**
    *   *Chunk Size:* 1000 tokens (to capture full legal clauses).
    *   *Overlap:* 100 tokens (to maintain context).
    *   *Retrieval:* MMR (Maximal Marginal Relevance) to reduce redundancy.

### 2.4. Agent C: The Researcher (External Intelligence)
*   **Goal:** Answer questions about market context, tax laws, and macroeconomics.
*   **Tech Stack:** **Perplexity API** (`sonar-reasoning` model).
*   **Role:** Provides the "Why" behind the internal data.
*   **Guardrails:** Must strictly answer the market question and NOT hallucinate internal client data.

## 3. Data Schemas (Mock Data Structure)

### 3.1. Portfolio Data (`portfolio.csv`)
The `Analyst_Agent` must understand these specific columns:
| Column Name | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `Asset_ID` | String | Unique Identifier | `A001` |
| `Asset_Name` | String | Descriptive Name | `DBS High-Yield Account` |
| `Asset_Class` | Enum | Category | `Cash`, `Equities`, `Real Estate`, `Art` |
| `Location` | Enum | Jurisdiction | `Singapore`, `Switzerland`, `USA` |
| `Value_USD` | Float | Current Market Value | `2500000.00` |
| `Custodian` | String | Bank/Holder | `DBS`, `Goldman Sachs`, `Freeport` |
| `Liquidity` | Enum | Ease of Sale | `High`, `Medium`, `Illiquid` |
| `Entity_Owner` | String | Legal Owner | `Wayne Family Trust` |

### 3.2. Legal Documents (Context)
The `Lawyer_Agent` needs to index text containing:
*   **Beneficiaries:** Who gets what.
*   **Trustees:** Who manages the assets.
*   **Conditions:** "Only after age 25", "Only if married."
*   **Insurance:** Coverage limits and exclusions.

## 4. Functional Requirements

### 4.1. Query Handling
*   **F.R.1 - Multi-Turn Memory:** The system must remember previous questions in the session (e.g., "How much is the Villa?" -> "Who lives there?").
*   **F.R.2 - Source Citation:** Every answer must cite its source.
    *   *Analyst:* "Source: Portfolio Data (Row 3)"
    *   *Lawyer:* "Source: Last Will & Testament (Page 4)"
    *   *Researcher:* "Source: Perplexity (Bloomberg, Reuters)"

### 4.2. Security & Privacy (Critical)
*   **F.R.3 - Data Isolation:** In the final system, vector stores must be partitioned by `Client_ID`. User A must NEVER query User B's embeddings.
*   **F.R.4 - PII Redaction:** (Future Scope) Sensitive PII (Passport Numbers) should be masked before being sent to LLMs where possible.

### 4.3. User Interface (Streamlit MVP)
*   **F.R.5 - Sidebar:** Display the loaded documents and data status (e.g., "Connected to 6 Assets").
*   **F.R.6 - Thinking State:** Visualize the "Routing" decision (e.g., "Searching Legal Docs..." vs "Calculating Portfolio...").

## 5. Prompt Engineering Strategy (System Prompts)

### 5.1. Router Prompt
> "You are the Wealth Concierge Router. You have access to three tools: 'Analyst' (for numbers/assets), 'Lawyer' (for documents/trusts), and 'Researcher' (for external market news).
> Analyze the user's question.
> - If it requires math or database lookups, use 'Analyst'.
> - If it requires reading legal text, use 'Lawyer'.
> - If it asks about the world, news, or laws, use 'Researcher'.
> - If unsure, ask clarifying questions. Do NOT make up answers."

### 5.2. Analyst Prompt
> "You are a Data Analyst for a Family Office. You have access to a dataframe `df`.
> When asked for 'Total', sum the `Value_USD` column.
> When asked for 'Liquidity', filter by the `Liquidity` column.
> Always output the final answer in a complete sentence: 'The total value is $X'."

## 6. Technology Stack (MVP)
*   **Language:** Python 3.10+
*   **Framework:** LangChain (latest version)
*   **LLM:** OpenAI GPT-4o (Main Brain), Perplexity `sonar-reasoning` (Research)
*   **Frontend:** Streamlit
*   **Vector DB:** FAISS (Local) or ChromaDB
*   **Environment:** Local `.env` management for API keys.

## 7. Testing Scenarios (Acceptance Criteria)
1.  **Scenario: The Math Test**
    *   *Query:* "What is my total allocation to Real Estate?"
    *   *Success:* Correctly sums `Value_USD` where `Asset_Class == 'Real Estate'`.
2.  **Scenario: The Legal Test**
    *   *Query:* "Can I sell the SpaceX shares immediately?"
    *   *Success:* Retrieves the clause about the "2030 lock-up period" from the text file.
3.  **Scenario: The Market Test**
    *   *Query:* "What is the current inflation rate in the UK?"
    *   *Success:* Perplexity returns the current real-time rate with a citation.
4.  **Scenario: The Hybrid Test**
    *   *Query:* "I own a Villa in London. How is the UK property market doing?"
    *   *Success:* Router identifies "Villa" (Internal) and "UK Market" (External), calls both, and synthesizes: "You own the Mayfair Villa (Value: $8.5M). The UK property market is currently..."