import streamlit as st

st.set_page_config(page_title="DSP Project", layout="wide")

st.title("DSP Project Dashboard")
st.markdown("👋 Welcome to the DSP Project Framework!")

st.markdown("### 📑 Available Tasks")

col1, col2, col3 , col5, col6, col7 = st.columns(6)
with col1:
    st.page_link("pages/Task1.py", label="🔢 Task 1 — Signal Operations")
with col2:
    st.page_link("pages/Task2.py", label="📈 Task 2 — Signal Generation")
with col3:
    st.page_link("pages/Task3.py", label="🔊 Task 3 — Signal Quantization")
with col5:
    st.page_link("pages/Task5.py", label="🎛️ Task 5 — Digital Filters")
with col6:
    st.page_link("pages/Task6.py", label="📉 Task 6 — Fourier Transform")
with col7:
    st.page_link("pages/Task7.py", label="🔍 Task 7 — Correlation Analysis")

st.markdown("---")
st.caption("Use the links above to navigate between DSP tasks.")
