import streamlit as st

st.set_page_config(page_title="DSP Project", layout="wide")

st.title("DSP Project Dashboard")

st.markdown("👋 Welcome to the DSP project app!")

st.markdown("### 📑 Available Tasks")

# Use page links for navigation
col1, = st.columns(1)

with col1:
    st.page_link("pages/Task1.py", label="➡️ Task 1: Signal Operations", icon="🔢")

st.markdown("---")
st.caption("Use the sidebar or the buttons above to navigate between tasks.")
