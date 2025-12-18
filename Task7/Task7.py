try:
    from .CompareSignal import *
except ImportError:
    from CompareSignal import *
import numpy as np
import math
import os


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


def ReadSignalsFromPoint3(base_path="Task7\\point3 Files"):
    signals = {'Class 1': {}, 'Class 2': {}}
    
    for class_folder in ['Class 1', 'Class 2']:
        folder_path = f"{base_path}\\{class_folder}"
        for file_name in sorted(os.listdir(folder_path)):
            if file_name.endswith('.txt'):
                file_path = f"{folder_path}\\{file_name}"
                signal_name = file_name.replace('.txt', '')
                
                with open(file_path, 'r') as f:
                    signal_data = [float(line.strip()) for line in f if line.strip()]
                
                signals[class_folder][signal_name] = signal_data
    
    return signals


def ClassifyTestSignals(base_path="Task7\\point3 Files"):
    training_signals = ReadSignalsFromPoint3(base_path)
    results = {}
    
    test_path = f"{base_path}\\Test Signals"
    for file_name in sorted(os.listdir(test_path)):
        if file_name.endswith('.txt'):
            with open(f"{test_path}\\{file_name}", 'r') as f:
                test_signal = [float(line.strip()) for line in f if line.strip()]
            
            test_name = file_name.replace('.txt', '')
            
            avg_c1 = round(np.mean([max(Corrlation(test_signal, s)) for s in training_signals['Class 1'].values() ]), 8)
            avg_c2 = round(np.mean([max(Corrlation(test_signal, s)) for s in training_signals['Class 2'].values() ]), 8)
            
            results[test_name] = (avg_c1, avg_c2, 'Class 1' if avg_c1 > avg_c2 else 'Class 2')
    
    return results


if __name__ == "__main__":

    indx, signal1 = ReadSignalFile("Task7\Point1 Correlation\Corr_input signal1.txt")
    _, signal2 = ReadSignalFile("Task7\Point1 Correlation\Corr_input signal2.txt")
    results = Corrlation(signal1, signal2)

    Compare_Signals("Task7\Point1 Correlation\CorrOutput.txt", indx, results)

    _, signal1 = ReadSignalFile("Task7\Point2 Time analysis\TD_input signal1.txt")
    _, signal2 = ReadSignalFile("Task7\Point2 Time analysis\TD_input signal2.txt")

    print("Time Delay Output:", TimeDelay(signal1, signal2, 100))
    
    classification_results = ClassifyTestSignals()
    for test_name, (avg_c1, avg_c2, classified_class) in classification_results.items():
        print(f"{test_name}: Class 1 Avg: {avg_c1}, Class 2 Avg: {avg_c2}, Classified as: {classified_class}")
