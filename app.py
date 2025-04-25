import streamlit as st
# Core modules
from core.auth import auth_component, initialize_auth
from core.companion import code_companion_interface
from core.analyzer import document_analyzer_interface
from core.debugger import code_debugger_interface
from core.price_checker import price_comparison_interface  # ✅ New import for Price Comparison Tool
from core.code_review import code_review_interface  # Add this if Code Review is a feature

# Initialize authentication
initialize_auth()

# Check login state
if not st.session_state.get("logged_in"):
    auth_component()
    st.stop()

# Sidebar
st.sidebar.header(f"👋 Welcome, {st.session_state.current_user}")
app_mode = st.sidebar.radio(
    "Select Mode",
    [
        "Code Companion",
        "Document Analyzer",
        "Code Debugger Tool",
        "Price Comparison Tool",  # ✅ New Tool Added
        "Code Review Tool"  # Add this if Code Review is part of the app
    ]
)

# Routing
if app_mode == "Code Companion":
    code_companion_interface()
elif app_mode == "Document Analyzer":
    document_analyzer_interface()
elif app_mode == "Code Debugger Tool":
    code_debugger_interface()
elif app_mode == "Price Comparison Tool":  # ✅ Route to Price Tool
    price_comparison_interface()
elif app_mode == "Code Review Tool":  # Add this routing for Code Review Tool if needed
    code_review_interface()

# Option to log out
if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state.current_user = None
    st.experimental_rerun()
