import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from Task2.Task2 import generate_signal

st.set_page_config(page_title="Task 2 — Signal Generation", layout="wide")

st.title("Task 2 — Signal Generation Framework")

st.markdown("""
### 🎛️ Generate and Visualize Signals
Use this page to generate **sine** or **cosine** signals, choose their parameters,
and visualize them in **continuous** or **discrete** form.
You can display **two signals simultaneously** either on the same plot or in two subplots.
""")

# Sidebar controls
st.sidebar.header("Signal Generation Settings")

# Representation type
representation = st.sidebar.radio("Representation Type", ["Continuous", "Discrete"])

# Display mode
display_mode = st.sidebar.radio("Display Mode", ["Same Plot", "Separate Subplots"])

# --- Signal 1 parameters ---
st.sidebar.subheader("Signal 1 Parameters")
sig1_type = st.sidebar.selectbox("Signal 1 Type", ["Sine", "Cosine"], key="sig1_type")
A1 = st.sidebar.number_input("Amplitude A₁", value=1.0, step=0.1)
theta1 = st.sidebar.number_input("Phase Shift θ₁ (radians)", value=0.0, step=0.1)
f1 = st.sidebar.number_input("Analog Frequency f₁ (Hz)", value=5.0, step=1.0)
fs1 = st.sidebar.number_input("Sampling Frequency fₛ₁ (Hz)", value=50.0, step=1.0)
duration1 = st.sidebar.number_input("Duration (seconds)", value=1.0, step=0.1)

# --- Signal 2 parameters ---
st.sidebar.subheader("Signal 2 Parameters")
sig2_type = st.sidebar.selectbox("Signal 2 Type", ["Sine", "Cosine"], key="sig2_type")
A2 = st.sidebar.number_input("Amplitude A₂", value=1.0, step=0.1)
theta2 = st.sidebar.number_input("Phase Shift θ₂ (radians)", value=0.0, step=0.1)
f2 = st.sidebar.number_input("Analog Frequency f₂ (Hz)", value=8.0, step=1.0)
fs2 = st.sidebar.number_input("Sampling Frequency fₛ₂ (Hz)", value=50.0, step=1.0)
duration2 = st.sidebar.number_input("Duration (seconds) for Signal 2", value=1.0, step=0.1)

# --- Generate signals using DSP logic ---
t1, x1 = generate_signal(sig1_type, A1, theta1, f1, fs1, duration1)
t2, x2 = generate_signal(sig2_type, A2, theta2, f2, fs2, duration2)

# --- Plot ---
fig, axes = plt.subplots(1 if display_mode == "Same Plot" else 2, 1, figsize=(8, 4))

if display_mode == "Same Plot":
    ax = axes
    if representation == "Continuous":
        ax.plot(t1, x1, label="Signal 1", color="blue")
        ax.plot(t2, x2, label="Signal 2", color="red", linestyle="--")
    else:
        ax.stem(t1, x1, linefmt="b-", markerfmt="bo", basefmt="k-")
        ax.stem(t2, x2, linefmt="r--", markerfmt="ro", basefmt="k-")
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_title(f"{representation} Representation — Both Signals")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend()
else:
    ax1, ax2 = axes
    # Signal 1
    if representation == "Continuous":
        ax1.plot(t1, x1, color="blue")
    else:
        ax1.stem(t1, x1, linefmt="b-", markerfmt="bo", basefmt="k-")
    ax1.axhline(0, color="black", linewidth=1)
    ax1.axvline(0, color="black", linewidth=1)
    ax1.set_title(f"Signal 1 ({sig1_type})")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")

    # Signal 2
    if representation == "Continuous":
        ax2.plot(t2, x2, color="red", linestyle="--")
    else:
        ax2.stem(t2, x2, linefmt="r--", markerfmt="ro", basefmt="k-")
    ax2.axhline(0, color="black", linewidth=1)
    ax2.axvline(0, color="black", linewidth=1)
    ax2.set_title(f"Signal 2 ({sig2_type})")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Amplitude")

fig.tight_layout()
st.pyplot(fig)

# --- Tables below the graph ---
st.markdown("### 📋 Signal Samples")

col1, col2 = st.columns(2)
with col1:
    df1 = pd.DataFrame({"Time": t1, "x₁(t)": x1})
    st.write("**Signal 1 Data**")
    st.dataframe(df1)
with col2:
    df2 = pd.DataFrame({"Time": t2, "x₂(t)": x2})
    st.write("**Signal 2 Data**")
    st.dataframe(df2)

st.caption("Task 2 — Signal Generation Framework for DSP Project")
