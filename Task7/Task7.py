try:
    from .CompareSignal import *
except ImportError:
    from CompareSignal import *
import numpy as np
import math


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


def Corrlation(S1, S2):

    normalized_factor = (1 / len(S1)) * math.sqrt(
        sum(a**2 for a in S1) * sum(b**2 for b in S2)
    )
    
    results = []
    shifted = S2.copy()
    for _ in range(len(S1)):

        results.append(
            round(float((1 / len(S1) * np.dot(S1, shifted)) / normalized_factor), 8)
        )
        shifted = np.roll(shifted, -1)
 
    return results


def TimeDelay(S1, S2, fs):
    corrlation_values = Corrlation(S1, S2)
    max_index = corrlation_values.index(max(corrlation_values))
    delay = max_index / fs
    return delay


if __name__ == "__main__":

    indx, signal1 = ReadSignalFile("Task7\Point1 Correlation\Corr_input signal1.txt")
    _, signal2 = ReadSignalFile("Task7\Point1 Correlation\Corr_input signal2.txt")
    results = Corrlation(signal1, signal2)

    Compare_Signals("Task7\Point1 Correlation\CorrOutput.txt", indx, results)

    _, signal1 = ReadSignalFile("Task7\Point2 Time analysis\TD_input signal1.txt")
    _, signal2 = ReadSignalFile("Task7\Point2 Time analysis\TD_input signal2.txt")

    print("Time Delay Output:", TimeDelay(signal1, signal2, 100))
