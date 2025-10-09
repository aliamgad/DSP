import numpy as np

def generate_signal(signal_type="Sine", A=1, theta=0, f=5, fs=50, duration=1):
    """
    Generate both continuous and discrete sine/cosine signals.

    If fs < 2*f (violating the sampling theorem), the discrete signal is returned empty.

    Parameters:
        signal_type : "Sine" or "Cosine"
        A           : Amplitude
        theta       : Phase shift (radians)
        f           : Analog frequency (Hz)
        fs          : Sampling frequency (Hz)
        duration    : Time length (seconds)

    Returns:
        (t_cont, x_cont, t_disc, x_disc)
    """

    # --- Adaptive high-resolution continuous time base ---
    num_points = max(1000, int(50 * f * duration))
    t_cont = np.linspace(0, duration, num_points)

    # Continuous signal
    if signal_type.lower() == "sine":
        x_cont = A * np.sin(2 * np.pi * f * t_cont + theta)
    else:
        x_cont = A * np.cos(2 * np.pi * f * t_cont + theta)

    # --- Discrete-time signal ---
    if fs >= 2 * f:  # ✅ Nyquist criterion satisfied
        t_disc = np.arange(0, duration, 1/fs)
        if signal_type.lower() == "sine":
            x_disc = A * np.sin(2 * np.pi * f * t_disc + theta)
        else:
            x_disc = A * np.cos(2 * np.pi * f * t_disc + theta)
    else:
        # ❌ fs too low — violates sampling theorem
        t_disc = np.array([])
        x_disc = np.array([])

    return t_cont, x_cont, t_disc, x_disc
