import numpy as np
import math
import cmath
try:
    from .CompareSignal import *
except ImportError:
    from CompareSignal import *

def ReadSignalFile(file_name):
    expected_indices = []
    expected_samples = []
    with open(file_name, "r") as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L = line.strip()
            if len(L.split(" ")) == 2:
                L = line.split(" ")
                V1 = int(L[0])
                V2 = float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices, expected_samples

def Convolution(signal1,indx1 , signal2, indx2):
    S1 = signal1
    S2 = signal2

    minidx = indx1[0] + indx2[0]
    maxidx = indx1[-1] + indx2[-1]
    Idx = np.arange(minidx, maxidx + 1)
    
    S = np.zeros(len(Idx))
    for i in range(len(Idx)):
        sum_val = 0
        for j in range(len(S1)):
            k = Idx[i] - indx1[0] - (indx2[0] + j)
            if k >= 0 and k < len(S2):
                sum_val += S1[j] * S2[k]
        S[i] = sum_val

    return Idx,S.tolist()

def FourierTransform(SignalInput,IDFT):
    N = len(SignalInput)
    SignalOutput = []
    for k in range(N):
        sum_value = 0
        for n in range(N):
            angle = 2j * cmath.pi * k * n / N
            if IDFT:
                sum_value += SignalInput[n] * cmath.exp(angle)
            else:
                sum_value += SignalInput[n] * cmath.exp(-angle)
        if IDFT:
            sum_value /= N
        SignalOutput.append(sum_value)
    return SignalOutput

def apply_filter(method,signal,signal_idx, filter_coefficients,fileter_indxes):
    if method == "Direct":
        idx_out, filtered_signal = Convolution(signal, signal_idx, filter_coefficients,fileter_indxes)
    elif method == "Fast":
        L = len(signal) + len(filter_coefficients) - 1

        signal_pad = np.zeros(L)
        filter_pad = np.zeros(L)

        signal_pad[:len(signal)] = signal
        filter_pad[:len(filter_coefficients)] = filter_coefficients

        signal_fft = FourierTransform(signal_pad.tolist(), False)
        filter_fft = FourierTransform(filter_pad.tolist(), False)

        product_fft = np.array(signal_fft) * np.array(filter_fft)

        filtered_signal_complex = FourierTransform(product_fft.tolist(), True)
        filtered_signal = [val.real for val in filtered_signal_complex]
        
        minidx = signal_idx[0] + fileter_indxes[0]
        idx_out = np.arange(minidx, minidx + len(filtered_signal))

    return idx_out, filtered_signal

def window_function(StopBandAttenuation,TransitionBand , fs):
    if 0 < StopBandAttenuation <= 21: #Rectangular Window
        N = math.ceil(0.9 / (TransitionBand / fs))
        N = N + 1 if N % 2 == 0 else N 
        n = np.arange(((N-1)//2)+1)
        window = np.ones(((N-1)//2)+1)
        
    elif 21 < StopBandAttenuation <= 44: #Hanning Window
        N = math.ceil(3.1 / (TransitionBand / fs))
        N = N + 1 if N % 2 == 0 else N
        n = np.arange(((N-1)//2)+1)
        window = 0.5 + 0.5 * np.cos((2 * np.pi * n) /N)
        
    elif 44 < StopBandAttenuation <= 53: #Hamming Window
        N = math.ceil(3.3 / (TransitionBand / fs))
        N = N + 1 if N % 2 == 0 else N
        n = np.arange(((N-1)//2)+1)
        window = 0.54 + 0.46 * np.cos((2 * np.pi * n) / N)
        
    elif 53 < StopBandAttenuation <= 74: #Blackman Window
        N = math.ceil(5.5 / (TransitionBand / fs))
        N = N + 1 if N % 2 == 0 else N
        n = np.arange(((N-1)//2)+1)
        window = (0.42 + 0.5 * np.cos((2 * np.pi * n) / (N - 1)) +
                  0.08 * np.cos((4 * np.pi * n) / (N - 1)))
    return window, n

def impulse_response(filter_type,fc, n, fs,TransitionBand):
    if filter_type == 'lowpass':
        fc_dash = fc[0] +  (TransitionBand / 2)
        fc_norm = fc_dash / fs
        impulse_function = np.where(
            n == 0,
            2 * fc_norm,
            2 * fc_norm * np.sinc(2 * fc_norm * n)
        )
    elif filter_type == 'highpass':
        fc_dash = fc[0] - (TransitionBand / 2)
        fc_norm = fc_dash / fs
        impulse_function = np.where(
            n == 0,
            1 - 2 * fc_norm,
            -2 * fc_norm * np.sinc(2 * fc_norm * n)
        )
    elif filter_type == 'bandpass':
        fc1_dash = fc[0] - (TransitionBand / 2)
        fc2_dash = fc[1] + (TransitionBand / 2)
        fc1_norm = fc1_dash / fs
        fc2_norm = fc2_dash / fs
        impulse_function = np.where(
            n == 0,
            2 * (fc2_norm - fc1_norm),
            2 * fc2_norm * np.sinc(2 * fc2_norm * n) - 2 * fc1_norm * np.sinc(2 * fc1_norm * n)
        )
    elif filter_type == 'bandstop':
        fc1_dash = fc[0] + (TransitionBand / 2)
        fc2_dash = fc[1] - (TransitionBand / 2)
        fc1_norm = fc1_dash / fs
        fc2_norm = fc2_dash / fs
        impulse_function = np.where(
            n == 0,
            1 - 2 * (fc2_norm - fc1_norm),
            2 * fc1_norm * np.sinc(2 * fc1_norm * n) - 2 * fc2_norm * np.sinc(2 * fc2_norm * n)
        )
    return impulse_function

def filter_design(FilterType, FS, StopBandAttenuation, FC, TransitionBand):
    window, n = window_function(StopBandAttenuation, TransitionBand, FS)
    impulse_func = impulse_response(FilterType, FC, n, FS, TransitionBand)
    
    filter_coefficients = impulse_func * window
    
    filter_coefficients = np.concatenate((filter_coefficients[-1:0:-1], filter_coefficients))
    filter_coefficients = np.round(filter_coefficients, 10)
    n = np.concatenate((-n[-1:0:-1], n))
    return n, filter_coefficients

if __name__ == "__main__":
    print("=" * 60)
    print("FIR FILTER DESIGN AND APPLICATION - DSP TASK 8")
    print("=" * 60)
    
    #####################################################################################################################################
    print("\n[Test Case 1] Low Pass Filter Coefficients")
    print("-" * 60)
    n, filter_coefficients = filter_design("lowpass", 8000, 50, [1500], 500)
    Compare_Signals("Task8\FIR test cases\Testcase 1\LPFCoefficients.txt", n.tolist(), filter_coefficients.tolist())
    
    print("\n[Test Case 2] ECG Signal Low Pass Filtering")
    print("-" * 60)
    idx, signal = ReadSignalFile("Task8\FIR test cases\Testcase 2\ecg400.txt")
    
    print("\n  Method 1: Direct Method")
    idx_filter, filtered_signal = apply_filter("Direct", signal, idx, filter_coefficients, n)
    Compare_Signals("Task8\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt", idx_filter, filtered_signal)
    
    print("\n  Method 2: Fast Method")
    idx_fast, filtered_signal_fast = apply_filter("Fast", signal, idx, filter_coefficients, n)
    Compare_Signals("Task8\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt", idx_fast, filtered_signal_fast)

    #####################################################################################################################################
    print("\n[Test Case 3] High Pass Filter Coefficients")
    print("-" * 60)
    n, filter_coefficients = filter_design("highpass", 8000, 70, [1500], 500)
    Compare_Signals("Task8\FIR test cases\Testcase 3\HPFCoefficients.txt", n.tolist(), filter_coefficients.tolist())

    print("\n[Test Case 4] ECG Signal High Pass Filtering")
    print("-" * 60)
    idx, signal = ReadSignalFile("Task8\FIR test cases\Testcase 4\ecg400.txt")
    
    print("\n  Method 1: Direct Method")
    idx_filter, filtered_signal = apply_filter("Direct", signal, idx, filter_coefficients, n)
    Compare_Signals("Task8\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt", idx_filter, filtered_signal)
    
    print("\n  Method 2: Fast Method")
    idx_fast, filtered_signal_fast = apply_filter("Fast", signal, idx, filter_coefficients, n)
    Compare_Signals("Task8\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt", idx_fast, filtered_signal_fast)
    #####################################################################################################################################

    print("\n[Test Case 5] Band Pass Filter Coefficients")
    print("-" * 60)
    n, filter_coefficients = filter_design("bandpass", 1000, 60, [150,250], 50)
    Compare_Signals("Task8\FIR test cases\Testcase 5\BPFCoefficients.txt", n.tolist(), filter_coefficients.tolist())

    print("\n[Test Case 6] ECG Signal Band Pass Filtering")
    print("-" * 60)
    idx, signal = ReadSignalFile("Task8\FIR test cases\Testcase 6\ecg400.txt")
    
    print("\n  Method 1: Direct Method")
    idx_filter, filtered_signal = apply_filter("Direct", signal, idx, filter_coefficients, n)
    Compare_Signals("Task8\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt", idx_filter, filtered_signal)
    
    print("\n  Method 2: Fast Method")
    idx_fast, filtered_signal_fast = apply_filter("Fast", signal, idx, filter_coefficients, n)
    Compare_Signals("Task8\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt", idx_fast, filtered_signal_fast)
    #####################################################################################################################################

    print("\n[Test Case 7] Band Stop Filter Coefficients")
    print("-" * 60)
    n, filter_coefficients = filter_design("bandstop", 1000, 60, [150,250], 50)
    Compare_Signals("Task8\FIR test cases\Testcase 7\BSFCoefficients.txt", n.tolist(), filter_coefficients.tolist())
    
    print("\n[Test Case 8] ECG Signal Band Stop Filtering")
    print("-" * 60)
    idx, signal = ReadSignalFile("Task8\FIR test cases\Testcase 8\ecg400.txt")
    
    print("\n  Method 1: Direct Method")
    idx_filter, filtered_signal = apply_filter("Direct", signal, idx, filter_coefficients, n)
    Compare_Signals("Task8\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt", idx_filter, filtered_signal)
    
    print("\n  Method 2: Fast Method")
    idx_fast, filtered_signal_fast = apply_filter("Fast", signal, idx, filter_coefficients, n)
    Compare_Signals("Task8\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt", idx_fast, filtered_signal_fast)
    
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    
    
    