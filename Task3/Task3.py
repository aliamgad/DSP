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
    
    # Load signal
    _, signal = ReadSignalFile(file_name)
    
    # If IsBits=True, interpret num_levels as number of bits
    if IsBits:
        num_levels = 2 ** num_levels  # compute number of levels

    min_val = np.min(signal)
    max_val = np.max(signal)

    # 1️⃣ make equally spaced interval boundaries (edges)
    edges = np.linspace(min_val, max_val, num_levels + 1)

    # 2️⃣ compute midpoints for each interval
    levels = (edges[:-1] + edges[1:]) / 2

    # 3️⃣ assign each sample to a level (find interval index)
    indices = np.digitize(signal, edges, right=False)
    indices = np.clip(indices, 1, num_levels)

    # 4️⃣ replace each sample with its corresponding midpoint
    q_signal = levels[indices - 1]

    # 5️⃣ quantization error
    error = q_signal - signal

    # 6️⃣ encoded binary representation for each index
    bits = int(np.ceil(np.log2(num_levels)))
    codes = [format(i - 1, f'0{bits}b') for i in indices]

    # ✅ return all needed lists for both tests
    return indices.tolist(), codes, q_signal.tolist(), error.tolist()

if __name__ == "__main__":
    # === Test 1 ===
    indices, codes, q_signal, error = quantizeSignal("Quan1_input.txt", 3, True)
    QuantizationTest1("Quan1_Out.txt", codes, q_signal)

    # === Test 2 ===
    indices, codes, q_signal, error = quantizeSignal("Quan2_input.txt", 4, False)
    QuantizationTest2("Quan2_Out.txt", indices, codes, q_signal, error)