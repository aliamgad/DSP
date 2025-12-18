# app.py
import streamlit as st
from Task7.Task7 import Corrlation, TimeDelay, ReadSignalsFromPoint3  # import your functions

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

# --- Signal Classification Section ---
st.subheader("Signal Classification")

# Default signal from Test1.txt
default_signal = "130,129,135,123,131,130,129,124,130,127,125,127,131,126,131,129,125,126,129,125,123,132,125,125,126,132,128,129,128,130,128,128,128,122,127,128,122,126,130,128,125,131,128,126,126,125,118,127,130,120,127,130,123,124,128,123,121,120,123,122,122,127,119,124,124,125,117,122,125,116,122,121,124,118,124,121,117,126,131,117,124,120,124,120,128,123,112,125,130,122,125,124,124,126,125,123,122,126,124,124,125,127,127,122,130,128,127,129,126,127,125,124,125,124,128,124,123,124,128,122,125,129,123,125,125,124,121,124,125,120,127,129,121,123,122,123,122,129,125,120,128,126,125,128,129,125,127,134,127,129,127,132,127,127,129,122,127,127,127,125,129,126,122,126,127,119,122,130,129,123,132,130,129,129,131,124,131,130,126,130,133,128,123,133,126,119,117,124,122,125,127,127,125,129,129,121,121,127,117,121,128,128,125,131,124,124,126,131,123,129,125,122,124,128,128,124,126,130,124,126,133,127,130,130,124,123,131,126,122,125,126,125,123,126,126,127,126,129,117,129,127,127,128,123,124,125,129,127,124,128,127"

signal_input = st.text_area("Enter signal to classify (comma-separated)", value=default_signal, height=100)

if st.button("Classify Signal"):
    try:
        test_signal = [float(x.strip()) for x in signal_input.split(",")]
        
        # Load training signals
        training_signals = ReadSignalsFromPoint3("Task7\\point3 Files")
        
        # Calculate correlations with both classes
        import numpy as np
        from Task7.Task7 import Corrlation
        
        corr_c1 = [max(Corrlation(test_signal, s)) for s in training_signals['Class 1'].values()]
        corr_c2 = [max(Corrlation(test_signal, s)) for s in training_signals['Class 2'].values()]
        
        avg_c1 = round(np.mean(corr_c1), 8)
        avg_c2 = round(np.mean(corr_c2), 8)
        
        classification = 'Class 1' if avg_c1 > avg_c2 else 'Class 2'
        
        st.success(f"Classification Result: **{classification}**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Class 1 Correlation", avg_c1)
        with col2:
            st.metric("Class 2 Correlation", avg_c2)
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
