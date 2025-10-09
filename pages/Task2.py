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
t1_cont, x1_cont, t1_disc, x1_disc = generate_signal(sig1_type, A1, theta1, f1, fs1, duration1)
t2_cont, x2_cont, t2_disc, x2_disc = generate_signal(sig2_type, A2, theta2, f2, fs2, duration2)

# --- Show Streamlit warnings if sampling theorem is violated ---
if fs1 < 2 * f1:
    st.warning("⚠️ Signal 1 violates the Sampling Theorem: fs₁ < 2f₁")
if fs2 < 2 * f2:
    st.warning("⚠️ Signal 2 violates the Sampling Theorem: fs₂ < 2f₂")

# --- Plot ---
fig, axes = plt.subplots(1 if display_mode == "Same Plot" else 2, 1, figsize=(8, 4))

if display_mode == "Same Plot":
    ax = axes
    if representation == "Continuous":
        ax.plot(t1_cont, x1_cont, label="Signal 1", color="blue")
        ax.plot(t2_cont, x2_cont, label="Signal 2", color="red", linestyle="--")
    else:
        if len(t1_disc) == 0 or len(t2_disc) == 0:
            ax.text(0.5, 0.5, "⚠️ Sampling theorem violated (fs < 2fmax)",
                    fontsize=10, ha='center', va='center', transform=ax.transAxes, color='red')
        else:
            ax.stem(t1_disc, x1_disc, linefmt="b-", markerfmt="bo", basefmt="k-")
            ax.stem(t2_disc, x2_disc, linefmt="r--", markerfmt="ro", basefmt="k-")

    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_title(f"{representation} Representation — Both Signals")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.legend()

else:
    ax1, ax2 = axes
    # Signal 1
    if representation == "Continuous":
        ax1.plot(t1_cont, x1_cont, color="blue")
    else:
        if len(t1_disc) == 0:
            ax1.text(0.5, 0.5, "⚠️ fs₁ < 2f₁", fontsize=10, ha='center', va='center',
                     transform=ax1.transAxes, color='red')
        else:
            ax1.stem(t1_disc, x1_disc, linefmt="b-", markerfmt="bo", basefmt="k-")
    ax1.axhline(0, color='black', linewidth=1)
    ax1.axvline(0, color='black', linewidth=1)
    ax1.set_title(f"Signal 1 ({sig1_type})")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")

    # Signal 2
    if representation == "Continuous":
        ax2.plot(t2_cont, x2_cont, color="red", linestyle="--")
    else:
        if len(t2_disc) == 0:
            ax2.text(0.5, 0.5, "⚠️ fs₂ < 2f₂", fontsize=10, ha='center', va='center',
                     transform=ax2.transAxes, color='red')
        else:
            ax2.stem(t2_disc, x2_disc, linefmt="r--", markerfmt="ro", basefmt="k-")
    ax2.axhline(0, color='black', linewidth=1)
    ax2.axvline(0, color='black', linewidth=1)
    ax2.set_title(f"Signal 2 ({sig2_type})")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Amplitude")

fig.tight_layout()
st.pyplot(fig)

# --- Tables below the graph ---
st.markdown("### 📋 Signal Samples")

col1, col2 = st.columns(2)
with col1:
    df1 = pd.DataFrame({"Time (Continuous)": t1_cont, "x₁(t)": x1_cont})
    st.write("**Signal 1 Data (Continuous)**")
    st.dataframe(df1)
with col2:
    df2 = pd.DataFrame({"Time (Continuous)": t2_cont, "x₂(t)": x2_cont})
    st.write("**Signal 2 Data (Continuous)**")
    st.dataframe(df2)

st.caption("Task 2 — Signal Generation Framework for DSP Project")
