import numpy as np


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


def TestSignal(OutputFile, Your_indices, Your_samples):
    expected_indices, expected_samples = ReadSignalFile(OutputFile)
    if (len(expected_samples) != len(Your_samples)) and (
        len(expected_indices) != len(Your_indices)
    ):
        print(
            "   Test case failed, your signal have different length from the expected one"
        )
        return
    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            print(
                "   Test case failed, your signal have different indicies from the expected one"
            )
            return
    print("    Test case passed successfully")


def Convolution(signal1path, signal2path):
    Idx1, S1 = ReadSignalFile(signal1path)
    Idx2, S2 = ReadSignalFile(signal2path)

    minidx = Idx1[0] + Idx2[0]
    maxidx = Idx1[-1] + Idx2[-1]
    Idx = np.arange(minidx, maxidx + 1)

    S = np.convolve(S1, S2)
    # for i in range(len(Idx)):
    #     sum = 0
    #     for j in range(len(S1)):
    #         k = Idx[i] - Idx1[0] - (Idx2[0] + j)
    #         if k >= 0 and k < len(S2):
    #             sum += S1[j] * S2[k]
    #     S[i] = sum

    return Idx.tolist(), S.tolist()


def Derivative(signalpath, degree):
    Idx1, S1 = ReadSignalFile(signalpath)
    S = []
    if degree == 1:
        for n in range(1, len(Idx1)):
            S.append(S1[n] - S1[n - 1])
        Idx = list(range(len(S)))
    elif degree == 2:
        for n in range(1, len(Idx1) - 1):
            S.append(S1[n + 1] - 2 * S1[n] + S1[n - 1])
        Idx = list(range(len(S)))

    return Idx, S


def MovingAvg(signalpath, window):
    _, S1 = ReadSignalFile(signalpath)
    S = np.convolve(S1, np.ones(window) / window, mode="valid")
    Idx = np.arange(0, len(S))
    return Idx, S.tolist()


if __name__ == "__main__":
    # Convolution Test
    Your_indices, Your_samples = Convolution(
        "Task5\\testcases\Convolution testcases\Signal 1.txt",
        "Task5\\testcases\Convolution testcases\Signal 2.txt",
    )
    print("Convolution Test:")
    TestSignal(
        "Task5\\testcases\Convolution testcases\Conv_output.txt",
        Your_indices,
        Your_samples,
    )

    # Derivative Tests
    Your_indices, Your_samples = Derivative(
        "Task5\\testcases\Derivative testcases\Derivative_input.txt", degree=1
    )
    print("1st Derivative Test:")
    TestSignal(
        "Task5\\testcases\Derivative testcases\\1st_derivative_out.txt",
        Your_indices,
        Your_samples,
    )
    Your_indices, Your_samples = Derivative(
        "Task5\\testcases\Derivative testcases\Derivative_input.txt", degree=2
    )
    print("2nd Derivative Test:")
    TestSignal(
        "Task5\\testcases\Derivative testcases\\2nd_derivative_out.txt",
        Your_indices,
        Your_samples,
    )
    # Moving Average Tests
    Your_indices, Your_samples = MovingAvg(
        "Task5\\testcases\Moving Average testcases\MovingAvg_input.txt", window=3
    )
    print("Moving Average Test with Window 3")
    TestSignal(
        "Task5\\testcases\Moving Average testcases\MovingAvg_out1.txt",
        Your_indices,
        Your_samples,
    )

    Your_indices, Your_samples = MovingAvg(
        "Task5\\testcases\Moving Average testcases\MovingAvg_input.txt", window=5
    )
    print("Moving Average Test with Window 5")
    TestSignal(
        "Task5\\testcases\Moving Average testcases\MovingAvg_out2.txt",
        Your_indices,
        Your_samples,
    )
