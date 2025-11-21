import cmath

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

def GetAmplitudeAndPhaseShift(SignalInput):
    Amplitude = []
    PhaseShift = []
    for value in SignalInput:
        Amplitude.append(abs(value))
        PhaseShift.append(cmath.phase(value))
    return Amplitude, PhaseShift

