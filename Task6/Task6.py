import cmath
try:
    from .signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift, RoundPhaseShift
except ImportError:
    from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift, RoundPhaseShift
import math

def ReadSignalFile(file_name):
    indices = []
    samples = []
    with open(file_name, "r") as f:
        for _ in range(3):
            f.readline()

        for line in f:
            parts = [p for p in line.strip().split() if p]
            if len(parts) < 2:
                continue

            v1 = float(parts[0].rstrip("f"))
            v2 = float(parts[1].rstrip("f"))

            indices.append(v1)
            samples.append(v2)

    return indices, samples

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

def ConvertComplexToAmpPhase(signal):
    amplitudes = []
    phases = []
    for x in signal:
        amplitudes.append(abs(x))
        raw_phase = math.atan2(x.imag, x.real)
        wrapped_phase = RoundPhaseShift(raw_phase)

        phases.append(wrapped_phase)

    return amplitudes, phases

def ComplexFromAmpPhase(amplitudes, phases):
    return [A * cmath.exp(1j * RoundPhaseShift(P)) for A, P in zip(amplitudes, phases)]


if __name__ == "__main__":
    DFT_Input_file = "Task6/Test Cases/DFT/input_Signal_DFT.txt"
    _, DFT_signal = ReadSignalFile(DFT_Input_file)
    dft_complex = FourierTransform(DFT_signal, IDFT=False)
    
    dft_amp, dft_phase = ConvertComplexToAmpPhase(dft_complex)

    DFT_Output_file = "Task6/Test Cases/DFT/Output_Signal_DFT_A,Phase.txt"
    expected_amp, expected_phase = ReadSignalFile(DFT_Output_file)
    expected_phase = [RoundPhaseShift(p) for p in expected_phase]
    
    rounded_amp = [round(a, 12) for a in dft_amp]
    rounded_expected_amp = [round(a, 12) for a in expected_amp]

    print("DFT Amplitude Match:", SignalComapreAmplitude(rounded_amp, rounded_expected_amp))
    print("DFT Phase Match:", SignalComaprePhaseShift(dft_phase, expected_phase))
    
    IDFT_Input_file = "Task6/Test Cases/IDFT/Input_Signal_DFT_A,Phase.txt" 
    IDFT_Output_file = "Task6/Test Cases/IDFT/output_Signal_IDFT.txt" 

    amplitudes, phases = ReadSignalFile(IDFT_Input_file)
    dft_complex = ComplexFromAmpPhase(amplitudes, phases)
    reconstructed = FourierTransform(dft_complex, IDFT=True)
    reconstructed_real = [x.real for x in reconstructed]
    _, original_signal = ReadSignalFile(IDFT_Output_file)

    rounded_original = [round(x, 12) for x in original_signal]
    rounded_reconstructed = [round(x, 12) for x in reconstructed_real]

    print("IDFT Amplitude Match:", SignalComapreAmplitude(rounded_reconstructed, rounded_original))
