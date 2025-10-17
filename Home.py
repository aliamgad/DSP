import streamlit as st

st.set_page_config(page_title="DSP Project", layout="wide")

st.title("DSP Project Dashboard")
st.markdown("👋 Welcome to the DSP Project Framework!")

st.markdown("### 📑 Available Tasks")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/Task1.py", label="🔢 Task 1 — Signal Operations")
with col2:
    st.page_link("pages/Task2.py", label="📈 Task 2 — Signal Generation")
with col3:
    st.page_link("pages/Task3.py", label="🔊 Task 3 — Signal Quantization")

st.markdown("---")
st.caption("Use the links above to navigate between DSP tasks.")
