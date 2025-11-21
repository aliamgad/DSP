import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
from Task6.Task6 import FourierTransform, GetAmplitudeAndPhaseShift, ReadSignalFile

st.set_page_config(layout="wide", page_title="DFT / IDFT Analyzer")
st.title("📈 DFT / IDFT Signal Analyzer")

st.header("Input & Options")
input_type = st.radio("Input source:", ["Manual Input", "Upload File"], horizontal=True)

# Manual input
if input_type == "Manual Input":
    samples_text = st.text_input("Enter comma-separated samples", "1,0,0,0")
    try:
        samples = [float(x.strip()) for x in samples_text.split(",") if x.strip() != ""]
        if len(samples) == 0:
            st.error("Please enter at least one sample.")
            st.stop()
    except Exception:
        st.error("Invalid sample format; use comma-separated numbers.")
        st.stop()

# File upload
else:
    uploaded = st.file_uploader("Upload signal file (text)", type=["txt"])
    if uploaded is None:
        st.info("Upload a text file or switch to Manual Input.")
        st.stop()
    # Save uploaded to temp and parse using provided ReadSignalFile
    temp_path = "uploaded_signal_temp.txt"
    with open(temp_path, "wb") as f:
        f.write(uploaded.read())
    _, samples = ReadSignalFile(temp_path)
    if len(samples) == 0:
        st.error("Uploaded file could not be parsed by ReadSignalFile(). Check file format.")
        st.stop()
    # Cleanup temp file
    try:
        os.remove(temp_path)
    except:
        pass

# Sampling frequency
Fs = st.number_input("Sampling frequency (Hz)", min_value=0.1, value=1000.0, step=1.0, format="%.4f")

# Buttons on main page
col_calc, col_idft = st.columns(2)
compute_dft = col_calc.button("Compute DFT", use_container_width=True)
compute_idft = col_idft.button("Reconstruct (IDFT)", use_container_width=True)

# Helper: frequency axis (f_k = k * Fs / N)
def frequency_axis(N, Fs):
    return np.array([k * Fs / N for k in range(N)])

# Plotting helpers
def plot_stem_amplitude(freq, amp):
    fig, ax = plt.subplots(figsize=(10, 4))
    markerline, stemlines, baseline = ax.stem(freq, amp)
    plt.setp(stemlines, color="#FFC000", linewidth=2)
    plt.setp(markerline, marker="o", markersize=8, markeredgecolor="#FFC000", markerfacecolor="#FFC000")
    plt.setp(baseline, visible=True, color="0.8", linewidth=1)
    ax.set_xlabel("Frequency (Hz)", fontsize=11)
    ax.set_ylabel("|X[k]|", fontsize=11)
    ax.set_title("DFT Amplitude Spectrum (Frequency in Hz)", fontsize=12, fontweight="bold")
    ax.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
    return fig

def plot_stem_phase(freq, phase_deg):
    fig, ax = plt.subplots(figsize=(10, 4))
    markerline, stemlines, baseline = ax.stem(freq, phase_deg)
    plt.setp(stemlines, color="tab:blue", linewidth=2)
    plt.setp(markerline, marker="o", markersize=6, markeredgecolor="tab:blue", markerfacecolor="tab:blue")
    plt.setp(baseline, visible=True, color="0.8", linewidth=1)
    ax.set_xlabel("Frequency (Hz)", fontsize=11)
    ax.set_ylabel("Phase (degrees)", fontsize=11)
    ax.set_title("DFT Phase Spectrum", fontsize=12, fontweight="bold")
    ax.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
    return fig

# Compute & display DFT
if compute_dft:
    st.subheader("🔹 DFT Analysis Results")
    N = len(samples)
    FT = FourierTransform(samples, IDFT=False)
    amp, phase_rad = GetAmplitudeAndPhaseShift(FT)
    amp = np.array(amp)
    phase_deg = np.degrees(np.array(phase_rad))

    freq = frequency_axis(N, Fs)

    # Display frequency vs amplitude and phase
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Amplitude Spectrum**")
        fig_amp = plot_stem_amplitude(freq, amp)
        st.pyplot(fig_amp)
        plt.close(fig_amp)
    
    with col2:
        st.write("**Phase Spectrum**")
        fig_phase = plot_stem_phase(freq, phase_deg)
        st.pyplot(fig_phase)
        plt.close(fig_phase)
    
    # Display numerical data
    st.subheader("📊 Frequency Domain Data")
    data_df = {
        "Frequency (Hz)": np.round(freq, 4),
        "Amplitude |X[k]|": np.round(amp, 6),
        "Phase (degrees)": np.round(phase_deg, 4)
    }
    st.dataframe(data_df, use_container_width=True)

# Compute & display IDFT / reconstruction
if compute_idft:
    st.subheader("🔹 Signal Reconstruction (IDFT)")
    
    # Use DFT of input then IDFT to reconstruct
    FT = FourierTransform(samples, IDFT=False)
    reconstructed = FourierTransform(FT, IDFT=True)
    recon_real = [x.real for x in reconstructed]

    # Display reconstruction comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Original Signal**")
        fig_orig, ax_orig = plt.subplots(figsize=(10, 4))
        ax_orig.stem(range(len(samples)), samples, linefmt="tab:green", markerfmt="go")
        ax_orig.set_xlabel("Sample Index")
        ax_orig.set_ylabel("Amplitude")
        ax_orig.set_title("Original Signal")
        ax_orig.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
        st.pyplot(fig_orig)
        plt.close(fig_orig)
    
    with col2:
        st.write("**Reconstructed Signal (Real Part)**")
        fig_rec, ax_rec = plt.subplots(figsize=(10, 4))
        ax_rec.stem(range(len(recon_real)), recon_real, linefmt="tab:blue", markerfmt="bo")
        ax_rec.set_xlabel("Sample Index")
        ax_rec.set_ylabel("Amplitude")
        ax_rec.set_title("Reconstructed Signal")
        ax_rec.grid(True, linestyle=':', linewidth=0.7, alpha=0.5)
        st.pyplot(fig_rec)
        plt.close(fig_rec)

    # Display numerical comparison
    st.subheader("📊 Original vs Reconstructed")
    comparison_df = {
        "Sample #": range(len(samples)),
        "Original": np.round(samples, 6),
        "Reconstructed": np.round(recon_real, 6),
        "Error": np.round(np.array(recon_real) - np.array(samples), 8)
    }
    st.dataframe(comparison_df, use_container_width=True)
    
    # Calculate and display error metrics
    error_array = np.array(recon_real) - np.array(samples)
    mse = np.mean(error_array ** 2)
    rmse = np.sqrt(mse)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Mean Squared Error (MSE)", f"{mse:.2e}")
    col2.metric("Root Mean Squared Error (RMSE)", f"{rmse:.2e}")
    col3.metric("Max Absolute Error", f"{np.max(np.abs(error_array)):.2e}")
