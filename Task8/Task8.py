import numpy as np
import math
import cmath
import os
from CompareSignal import Compare_Signals

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

def Convolution(signal1, signal2):
    S1 = signal1.tolist()
    S2 = signal2.tolist()

    minidx = 0
    maxidx = (len(S1) - 1) + (len(S2) - 1)
    Idx = np.arange(minidx, maxidx + 1)
    
    S = np.zeros(len(Idx))
    for i in range(len(Idx)):
        sum_val = 0
        for j in range(len(S1)):
            k = Idx[i] - 0 - (0 + j)
            if k >= 0 and k < len(S2):
                sum_val += S1[j] * S2[k]
        S[i] = sum_val

    return S.tolist()

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

def filter_design(method,FilterType, FS, StopBandAttenuation, FC, TransitionBand):
    window, n = window_function(StopBandAttenuation, TransitionBand, FS)
    impulse_func = impulse_response(FilterType, FC, n, FS, TransitionBand)

    if method == "Direct":
        filter_coefficients = impulse_func * window

    elif method == "Fast":
        impulse_fft = FourierTransform(impulse_func.tolist(), IDFT=False)
        window_fft = FourierTransform(window.tolist(), IDFT=False)
        
        product_fft = np.array(impulse_fft) * np.array(window_fft)
                
        result = FourierTransform(product_fft, IDFT=True)
        filter_coefficients = np.array([x.real for x in result])

    filter_coefficients = np.concatenate((filter_coefficients[-1:0:-1], filter_coefficients))
    filter_coefficients = np.round(filter_coefficients, 10)
    n = np.concatenate((-n[-1:0:-1], n))
    return n, filter_coefficients

if __name__ == "__main__":
    n, filter_coefficients = filter_design("Direct","lowpass", 8000, 50, [1500], 500)
    #Compare_Signals("Task8\FIR test cases\Testcase 1\LPFCoefficients.txt", n.tolist(), filter_coefficients.tolist())
    
    n, filter_coefficients = filter_design("Fast","lowpass", 8000, 50, [1500], 500)
    Compare_Signals("Task8\FIR test cases\Testcase 1\LPFCoefficients.txt", n.tolist(), filter_coefficients.tolist())
    print(filter_coefficients)
    
    
    