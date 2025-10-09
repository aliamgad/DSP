import numpy as np

def generate_signal(signal_type="Sine", A=1, theta=0, f=5, fs=50, duration=1):

    num_points = max(1000, int(50 * f * duration))
    t_cont = np.linspace(0, duration, num_points)

    if signal_type.lower() == "sine":
        x_cont = A * np.sin(2 * np.pi * f * t_cont + theta)
    else:
        x_cont = A * np.cos(2 * np.pi * f * t_cont + theta)

    if fs >= 2 * f:
        t_disc = np.arange(0, duration, 1/fs)
        if signal_type.lower() == "sine":
            x_disc = A * np.sin(2 * np.pi * f * t_disc + theta)
        else:
            x_disc = A * np.cos(2 * np.pi * f * t_disc + theta)
    else:
        t_disc = np.array([])
        x_disc = np.array([])

    return t_cont, x_cont, t_disc, x_disc
