# app.py
import streamlit as st
from Task7.Task7 import Corrlation, TimeDelay  # import your functions

st.title("DSP Tools: Correlation & Time Delay Estimation")

# --- Inputs ---
fs = st.number_input("Sampling frequency (Hz)", min_value=1, value=100)

S1_input = st.text_input("Enter signal S1 (comma-separated)", "1,2,3,1,2,6,8,2,4")
S2_input = st.text_input("Enter signal S2 (comma-separated)", "2,6.1,8,2.02,4,1,2.2,3,1.06")

S1 = [float(x.strip()) for x in S1_input.split(",")]
S2 = [float(x.strip()) for x in S2_input.split(",")]

# --- Correlation Section ---
st.subheader("Correlation")

if st.button("Compute Correlation"):
    corr = Corrlation(S2, S1)  # use your Corrlation function
    st.write("Correlation values:")
    st.write(corr)
    # Optional: plot
    st.line_chart(corr)

# --- Time Delay Section ---
st.subheader("Time Delay Estimation")

if st.button("Compute Time Delay"):
    delay = TimeDelay(S1, S2, fs)  # use your TimeDelay function
    st.write(f"Estimated Time Delay: {delay} seconds")
