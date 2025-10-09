import numpy as np

def generate_signal(signal_type="Sine", A=1, theta=0, f=5, fs=50, duration=1):
    """
    Generate a sine or cosine signal.
    signal_type: "Sine" or "Cosine"
    A: Amplitude
    theta: Phase shift (radians)
    f: Analog frequency (Hz)
    fs: Sampling frequency (Hz)
    duration: Time length (seconds)
    Returns: (t, x)
    """
    t = np.arange(0, duration, 1/fs)
    if signal_type.lower() == "sine":
        x = A * np.sin(2 * np.pi * f * t + theta)
    else:
        x = A * np.cos(2 * np.pi * f * t + theta)
    return t, x
