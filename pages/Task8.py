import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Task8.Task8 import filter_design, apply_filter, ReadSignalFile
import tempfile
import os

st.set_page_config(page_title="FIR Filter Design & Application", layout="wide")

# Title
st.title("🔧 FIR Filter Design & Application")
st.markdown("---")

# ============================================================================
# FILTER DESIGN SECTION
# ============================================================================
st.header("📊 Filter Design")
col1, col2, col3, col4 = st.columns(4)

with col1:
    filter_type = st.selectbox(
        "Filter Type",
        ["lowpass", "highpass", "bandpass", "bandstop"],
        index=0,  # Default: lowpass
        key="filter_type_design"
    )

with col2:
    fs = st.number_input("Sampling Frequency (FS)", value=8000, min_value=1000, step=100)

with col3:
    stop_band_atten = st.number_input(
        "Stop Band Attenuation (dB)", 
        value=50,  # Default: 50 (Test Case 1)
        min_value=21, 
        max_value=74,
        step=1
    )

with col4:
    trans_band = st.number_input("Transition Band (Hz)", value=500, min_value=50, step=50)  # Default: 500 (Test Case 1)

# Cutoff frequencies based on filter type
if filter_type in ["lowpass", "highpass"]:
    fc = st.number_input("Cutoff Frequency (Hz)", value=1500, min_value=100, step=100)  # Default: 1500 (Test Case 1)
    fc_list = [fc]
else:  # bandpass, bandstop
    col_fc1, col_fc2 = st.columns(2)
    with col_fc1:
        fc1 = st.number_input("Lower Cutoff Frequency (Hz)", value=150, min_value=50, step=50)
    with col_fc2:
        fc2 = st.number_input("Upper Cutoff Frequency (Hz)", value=250, min_value=100, step=50)
    fc_list = [fc1, fc2]

if st.button("🔨 Design Filter", key="design_btn"):
    try:
        n, filter_coefficients = filter_design(filter_type, fs, stop_band_atten, fc_list, trans_band)
        
        st.success("✅ Filter designed successfully!")
        
        # Display filter info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filter Order", len(filter_coefficients) - 1)
        with col2:
            st.metric("Number of Coefficients", len(filter_coefficients))
        with col3:
            st.metric("Filter Type", filter_type.upper())
        
        # Plot filter coefficients
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Time domain
        ax1.stem(n, filter_coefficients, basefmt=' ')
        ax1.set_xlabel('Sample Index')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Filter Coefficients (Time Domain)')
        ax1.grid(True, alpha=0.3)
        
        # Frequency response
        w = np.linspace(0, np.pi, 1000)
        h = np.zeros_like(w, dtype=complex)
        for k, coef in enumerate(filter_coefficients):
            h += coef * np.exp(-1j * w * (k - len(filter_coefficients)//2))
        
        ax2.plot(w/np.pi * fs/2, 20*np.log10(np.abs(h) + 1e-10))
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Magnitude (dB)')
        ax2.set_title('Frequency Response')
        ax2.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # Display coefficients table
        with st.expander("📋 View Filter Coefficients"):
            coef_df = {"Index": n.tolist(), "Coefficient": filter_coefficients.tolist()}
            st.dataframe(coef_df, use_container_width=True)
        
        # Store in session state for later use
        st.session_state.filter_n = n
        st.session_state.filter_coefficients = filter_coefficients
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

st.markdown("---")

# ============================================================================
# SIGNAL FILTERING SECTION
# ============================================================================
st.header("🎛️ Signal Filtering")
    
# Quick load test case files
st.subheader("📂 Load Test Case Files")
col1, col2, col3 = st.columns(3)

test_case_path = "Task8/FIR test cases/Testcase 2"

with col1:
    if st.button("📥 Load Test Case 2 (ECG Signal)", key="load_test2"):
        try:
            test_file = os.path.join(test_case_path, "ecg400.txt")
            if os.path.exists(test_file):
                idx, signal = ReadSignalFile(test_file)
                st.session_state.signal_idx = idx
                st.session_state.signal_data = signal
                st.session_state.test_case_loaded = True
                st.success("✅ Test Case 2 loaded successfully!")
            else:
                st.error(f"❌ File not found: {test_file}")
        except Exception as e:
            st.error(f"❌ Error loading test case: {str(e)}")

with col2:
    if st.button("🔄 Clear Loaded Signal", key="clear_signal"):
        if "signal_data" in st.session_state:
            del st.session_state.signal_data
            del st.session_state.signal_idx
            del st.session_state.test_case_loaded
        st.success("✅ Signal cleared!")

with col3:
    st.write("")  # Spacer

st.markdown("---")

# File upload
uploaded_file = st.file_uploader("Or Upload ECG Signal File (.txt)", type=['txt'])

signal_loaded = False
idx = None
signal = None

if uploaded_file is not None:
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        # Read signal
        idx, signal = ReadSignalFile(tmp_path)
        os.unlink(tmp_path)
        signal_loaded = True
        st.success(f"✅ Signal loaded: {len(signal)} samples")
        
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

elif "signal_data" in st.session_state and st.session_state.test_case_loaded:
    idx = st.session_state.signal_idx
    signal = st.session_state.signal_data
    signal_loaded = True
    st.info("📌 Using Test Case 2 ECG Signal")

if signal_loaded and signal is not None:
    # Display signal info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Signal Length", len(signal))
    with col2:
        st.metric("Min Value", f"{min(signal):.2f}")
    with col3:
        st.metric("Max Value", f"{max(signal):.2f}")
    with col4:
        st.metric("Mean Value", f"{np.mean(signal):.2f}")
    
    # Plot original signal
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(idx, signal, linewidth=0.8)
    ax.set_xlabel('Sample Index')
    ax.set_ylabel('Amplitude')
    ax.set_title('Original ECG Signal')
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    # Filter selection
    st.subheader("Apply Filter")
    filter_method = st.radio("Select Filtering Method:", ["Direct", "Fast"], horizontal=True)
    
    if st.button("⚡ Apply Filter", key="apply_btn"):
        try:
            # Use stored filter or design new one
            if "filter_coefficients" in st.session_state:
                n = st.session_state.filter_n
                filter_coefficients = st.session_state.filter_coefficients
            else:
                st.error("⚠️ Please design a filter first!")
                st.stop()
            
            # Apply filter
            idx_filter, filtered_signal = apply_filter(
                filter_method, 
                signal, 
                idx, 
                filter_coefficients, 
                n
            )
            
            st.success(f"✅ Filter applied using {filter_method} method!")
            
            # Display filtered signal info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Output Length", len(filtered_signal))
            with col2:
                st.metric("Min Value", f"{min(filtered_signal):.2f}")
            with col3:
                st.metric("Max Value", f"{max(filtered_signal):.2f}")
            with col4:
                st.metric("Mean Value", f"{np.mean(filtered_signal):.2f}")
            
            # Plot comparison
            fig, axes = plt.subplots(2, 1, figsize=(12, 6))
            
            axes[0].plot(idx, signal, linewidth=0.8, label='Original', color='blue')
            axes[0].set_xlabel('Sample Index')
            axes[0].set_ylabel('Amplitude')
            axes[0].set_title('Original ECG Signal')
            axes[0].grid(True, alpha=0.3)
            axes[0].legend()
            
            axes[1].plot(idx_filter, filtered_signal, linewidth=0.8, label='Filtered', color='red')
            axes[1].set_xlabel('Sample Index')
            axes[1].set_ylabel('Amplitude')
            axes[1].set_title(f'Filtered Signal ({filter_method} Method)')
            axes[1].grid(True, alpha=0.3)
            axes[1].legend()
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Store filtered signal for export
            st.session_state.filtered_signal = filtered_signal
            st.session_state.filtered_idx = idx_filter
            
        except Exception as e:
            st.error(f"❌ Error applying filter: {str(e)}")
    
    # Export results
    if "filtered_signal" in st.session_state:
        st.subheader("📥 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = "Index,Value\n"
            for idx_val, sig_val in zip(st.session_state.filtered_idx, st.session_state.filtered_signal):
                csv_data += f"{idx_val},{sig_val:.6f}\n"
            
            st.download_button(
                label="📊 Download CSV",
                data=csv_data,
                file_name="filtered_signal.csv",
                mime="text/csv"
            )
        
        with col2:
            txt_data = "Filtered ECG Signal\n\n"
            txt_data += f"Total Samples: {len(st.session_state.filtered_signal)}\n\n"
            for idx_val, sig_val in zip(st.session_state.filtered_idx, st.session_state.filtered_signal):
                txt_data += f"{idx_val} {sig_val:.6f}\n"
            
            st.download_button(
                label="📄 Download TXT",
                data=txt_data,
                file_name="filtered_signal.txt",
                mime="text/plain"
            )
else:
    st.info("⚠️ Please design a filter first in the 'Filter Design' section!")

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <small>DSP Task 8 - FIR Filter Design & Application | Built with Streamlit</small><br>
    <small>Default Values: Test Case 1 & Test Case 2</small>
</div>
""", unsafe_allow_html=True)
