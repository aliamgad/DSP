import streamlit as st
import numpy as np
import pandas as pd
from Task5.Task5 import Convolution, Derivative, MovingAvg, ReadSignalFile
import os

st.title("DSP Signal Processing GUI")

# File upload
task = st.selectbox("Select DSP Task", ["Convolution", "Derivative", "Moving Average"])

# Get the base path for test cases
base_path = os.path.join(os.path.dirname(__file__), "..", "Task5", "testcases")

if task == "Convolution":
    st.subheader("Convolution of Two Signals")
    
    try:
        signal1_path = os.path.join(base_path, "Convolution testcases", "Signal 1.txt")
        signal2_path = os.path.join(base_path, "Convolution testcases", "Signal 2.txt")
        Idx, S = Convolution(signal1_path, signal2_path)
        
        st.line_chart(pd.DataFrame({"Amplitude": S}, index=Idx))
        st.write("Output Signal:")
        st.dataframe(pd.DataFrame({"Index": Idx, "Amplitude": S}))
    except Exception as e:
        st.error(f"Error: {e}")

elif task == "Derivative":
    st.subheader("Derivative of a Signal")
    
    degree = st.selectbox("Derivative Degree", [1, 2])
    
    try:
        signal_path = os.path.join(base_path, "Derivative testcases", "Derivative_input.txt")
        Idx, S = Derivative(signal_path, degree=degree)
        
        st.line_chart(pd.DataFrame({"Amplitude": S}, index=list(Idx)))
        st.write("Output Signal:")
        st.dataframe(pd.DataFrame({"Index": Idx, "Amplitude": S}))
    except Exception as e:
        st.error(f"Error: {e}")

elif task == "Moving Average":
    st.subheader("Moving Average of a Signal")
    
    window = st.number_input("Window Size", min_value=1, value=3)
    
    try:
        signal_path = os.path.join(base_path, "Moving Average testcases", "MovingAvg_input.txt")
        Idx, S = MovingAvg(signal_path, window=int(window))
        
        st.line_chart(pd.DataFrame({"Amplitude": S}, index=Idx))
        st.write("Output Signal:")
        st.dataframe(pd.DataFrame({"Index": Idx, "Amplitude": S}))
    except Exception as e:
        st.error(f"Error: {e}")