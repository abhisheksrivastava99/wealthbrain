import streamlit as st
import os
from dotenv import load_dotenv
from agents.router import RouterAgent
import pandas as pd

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Wealth Brain AI Concierge",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Minimalist Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f8f9fa;
        color: #1e1e1e;
    }
    
    /* Force Sidebar Background to White */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e9ecef;
    }
    
    /* Force sidebar text color */
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] div, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #1f2937 !important;
    }
    
    /* Style Sidebar Buttons (Back to Families) */
    section[data-testid="stSidebar"] .stButton button {
        background-color: #ffffff;
        color: #1f2937;
        border: 1px solid #d1d5db;
        transition: all 0.2s;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        border-color: #213E87;
        color: #213E87;
        background-color: #f3f4f6;
    }
    
    h1, h2, h3 {
        color: #111827;
        font-weight: 700;
    }
    
    /* Chat Message Styling */
    .stChatMessage {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 0.5rem;
    }
    
    /* Force text color in chat messages */
    .stChatMessage, .stChatMessage p, .stChatMessage div {
        color: #1f2937 !important;
    }
    
    /* Fix Expander Styling (View Portfolio Data) */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        color: #1f2937 !important;
    }
    
    div[data-testid="stExpander"] details {
        background-color: white !important;
        color: #1f2937 !important;
    }

    div[data-testid="stExpander"] summary {
        color: #1f2937 !important;
        font-weight: 600;
        background-color: white !important;
    }
    
    div[data-testid="stExpander"] summary:hover {
        color: #213E87 !important;
    }

    /* Force text color when expanded */
    div[data-testid="stExpander"] details[open] summary {
        color: #1f2937 !important;
    }

    div[data-testid="stExpander"] div[role="button"] p {
        color: #1f2937 !important;
    }
    
    /* Force SVG icon color (the arrow) */
    div[data-testid="stExpander"] svg {
        fill: #1f2937 !important;
        color: #1f2937 !important;
    }
    
    /* Hide Dataframe Toolbar (Search, Download, Fullscreen) */
    div[data-testid="stElementToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Ensure Dataframe text is visible if toolbar persists */
    div[data-testid="stDataFrame"] {
        color: #1f2937 !important;
    }
    
</style>
""", unsafe_allow_html=True)

# Session State Management
if "selected_family" not in st.session_state:
    st.session_state.selected_family = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Router Agent (Cached per family)
@st.cache_resource
def get_router_agent(family_name):
    return RouterAgent(family_name=family_name)

def reset_session():
    st.session_state.selected_family = None
    st.session_state.messages = []

# --- Home Page: Family Selection ---
if st.session_state.selected_family is None:
    st.title("🏦 Wealth Brain")
    st.markdown("### Select a Family Office to Manage")
    st.markdown("---")
    
    # CSS to make buttons look like cards ONLY on this page
    st.markdown("""
    <style>
    div.stButton > button {
        background-color: white;
        color: #1f2937;
        height: 240px; /* Increased height */
        width: 100%;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        white-space: pre-wrap; /* Allow newlines */
        line-height: 1.6;
        font-size: 1.3rem; /* Increased font size */
    }
    
    div.stButton > button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
        color: #3b82f6;
        background-color: white;
    }
    
    div.stButton > button:active {
        background-color: #f3f4f6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    families = [
        {"name": "Wayne", "icon": "🦇", "desc": "Gotham's Finest"},
        {"name": "Lannister", "icon": "🦁", "desc": "Always Pays Debts"},
        {"name": "Stark", "icon": "🐺", "desc": "Winter is Coming"},
        {"name": "Targaryen", "icon": "🐉", "desc": "Fire and Blood"},
        {"name": "Baratheon", "icon": "🦌", "desc": "Ours is the Fury"},
    ]
    
    cols = st.columns(len(families))
    
    for i, family in enumerate(families):
        with cols[i]:
            # Create a label with newlines for Icon, Name, and Desc
            # Note: Streamlit buttons treat newlines as breaks
            label = f"{family['icon']}\n\n{family['name']}\n\n{family['desc']}"
            
            if st.button(label, key=f"btn_{family['name']}", use_container_width=True):
                st.session_state.selected_family = family['name']
                st.rerun()

# --- Chat Interface ---
else:
    family = st.session_state.selected_family
    
    # Sidebar
    with st.sidebar:
        if st.button("← Back to Families"):
            reset_session()
            st.rerun()
            
        st.title(f"{family} Family Office")
        st.markdown("---")
        
        st.subheader("Data Status")
        
        # Portfolio Status
        try:
            df = pd.read_csv("data/portfolio.csv")
            family_df = df[df['Family'] == family]
            total_aum = family_df['Value_USD'].sum()
            
            st.metric("Total AUM", f"${total_aum:,.0f}")
            st.success(f"Connected to Portfolio ({len(family_df)} Assets)")
            
            with st.expander("View Portfolio Data"):
                st.dataframe(family_df)
        except Exception as e:
            st.error(f"Portfolio Data Error: {str(e)}")
            
        # Legal Docs Status
        try:
            doc_path = f"data/legal_docs/{family.lower()}"
            if os.path.exists(doc_path):
                doc_count = len([name for name in os.listdir(doc_path) if name.endswith(".txt")])
                st.success(f"Connected to Legal Docs ({doc_count} Files)")
            else:
                st.warning("No legal docs found.")
        except Exception as e:
            st.error(f"Legal Docs Error: {str(e)}")
            
        st.markdown("---")
        st.markdown("**System Status:** 🟢 Online")

    # Main Chat Area
    st.title(f"AI Concierge for House {family}")
    st.markdown(f"Ask me about the {family} portfolio, legal documents, or market trends.")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("How can I help you today?"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Generate Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            try:
                # Initialize Router with selected family
                router = get_router_agent(family)
                
                # Route and Execute
                result = router.route_and_execute(prompt)
                
                agent_name = result.get("agent", "Unknown")
                response_text = result.get("response", "No response generated.")
                
                # Format the final output
                final_output = f"**[{agent_name} Agent]**\n\n{response_text}"
                
                # FINAL SAFETY CLEAN: Remove <think> tags if they slipped through
                import re
                final_output = re.sub(r'<think>.*?</think>', '', final_output, flags=re.DOTALL | re.IGNORECASE).strip()
                
                message_placeholder.markdown(final_output)
                
                # Add assistant message to history
                st.session_state.messages.append({"role": "assistant", "content": final_output})
                
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
