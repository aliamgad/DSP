try:
    from .QuanTest1 import *
    from .QuanTest2 import *
except ImportError:
    from QuanTest1 import *
    from QuanTest2 import *
import numpy as np

def ReadSignalFile(file_name):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices,expected_samples

def quantizeSignal(file_name, num_levels, IsBits):
    
    _, signal = ReadSignalFile(file_name)
    
    if IsBits:
        num_levels = 2 ** num_levels

    min_val = np.min(signal)
    max_val = np.max(signal)

    edges = np.linspace(min_val, max_val, num_levels + 1)

    levels = (edges[:-1] + edges[1:]) / 2

    indices = np.digitize(signal, edges, right=False)
    indices = np.clip(indices, 1, num_levels)

    q_signal = levels[indices - 1]

    error = q_signal - signal

    bits = int(np.ceil(np.log2(num_levels)))
    codes = [format(i - 1, f'0{bits}b') for i in indices]

    return indices.tolist(), codes, q_signal.tolist(), error.tolist()

if __name__ == "__main__":
    # === Test 1 ===
    indices, codes, q_signal, error = quantizeSignal("Task3/Quan1_input.txt", 3, True)
    QuantizationTest1("Task3/Quan1_Out.txt", codes, q_signal)

    # === Test 2 ===
    indices, codes, q_signal, error = quantizeSignal("Task3/Quan2_input.txt", 4, False)
    QuantizationTest2("Task3/Quan2_Out.txt", indices, codes, q_signal, error)