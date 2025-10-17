import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from Task3.Task3 import quantizeSignal

# --- Page setup ---
st.set_page_config(page_title="Task 3 — Signal Quantization", layout="wide")
st.title("🔧 Task 3 — Signal Quantization")

st.markdown("""
This application performs **uniform quantization** of an input signal.  
Select a signal file and specify either the **number of bits** or the **number of levels**.  
The results update automatically and display:
- The **quantized signal**
- The **quantization error**
- The **encoded (binary) signal**
""")

# --- Sidebar setup ---
st.sidebar.header("⚙️ Quantization Settings")

# Locate Task3 folder
task3_folder = Path(__file__).resolve().parents[1] / "Task3"
available_signals = [p.name for p in task3_folder.glob("Quan*_input.txt")]

if not available_signals:
    st.error("No signal files (Quan*_input.txt) found in the Task3 folder!")
    st.stop()

# Select a signal file
selected_signal = st.sidebar.selectbox("Select Signal File", available_signals)
signal_path = task3_folder / selected_signal

# Choose quantization mode
mode = st.sidebar.radio("Select Mode", ["Number of Levels", "Number of Bits"])

if mode == "Number of Levels":
    num_levels = st.sidebar.number_input("Number of Levels", min_value=2, value=8, step=1)
    IsBits = False
else:
    num_levels = st.sidebar.number_input("Number of Bits", min_value=1, value=3, step=1)
    IsBits = True

# --- Automatically run quantization whenever inputs change ---
try:
    indices, codes, q_signal, error = quantizeSignal(str(signal_path), num_levels, IsBits)

    # Recover original signal for plotting
    signal = np.array(q_signal) - np.array(error)

    # --- Layout: 3 columns side-by-side ---
    col1, col2, col3 = st.columns(3)

    # --- Column 1: Quantized Signal ---
    with col1:
        st.subheader("📈 Quantized Signal")
        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.plot(signal, label="Original", alpha=0.7)
        ax1.step(range(len(signal)), q_signal, where="mid", label="Quantized", linewidth=1.5)
        ax1.set_xlabel("Sample Index")
        ax1.set_ylabel("Amplitude")
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)

    # --- Column 2: Quantization Error ---
    with col2:
        st.subheader("📉 Quantization Error")
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.plot(error, color="orange", label="Error (q - x)")
        ax2.axhline(0, color="black", linewidth=0.8)
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

    # --- Column 3: Encoded Signal ---
    with col3:
        st.subheader("💾 Encoded Signal")
        st.markdown(f"Total samples: **{len(codes)}**")
        st.text_area("All Encoded Binary Values", "\n".join(codes), height=400)

    # Success message below columns
    st.success(f"Quantization displayed for {selected_signal} ✅")

except Exception as e:
    st.error(f"Error during quantization: {e}")
