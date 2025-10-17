try:
    from .DSP_Task_2_TEST_functions import *
except ImportError:
    from DSP_Task_2_TEST_functions import *
import pandas as pd
import numpy as np

signal1 = "Task1/Signal1.txt"
signal2 = "Task1/Signal2.txt"
FirstFileIndices=ReadSignalFile(signal1)
SecondFileIndices=ReadSignalFile(signal2)
    
Signals={
    "S1": pd.Series(data= FirstFileIndices[1], index=FirstFileIndices[0]),
    "S2": pd.Series(data= SecondFileIndices[1], index=SecondFileIndices[0]),
}

my_Data = pd.DataFrame(Signals)

def AddingSignals():
    addingData = my_Data.fillna(0)
    result = addingData['S1'] + addingData['S2']
    return result.index, result.values


def MultiplySignals(input):
    multiplyData = my_Data.fillna(1)
    result = multiplyData['S1'] * input
    return result.index, result.values
    
def SubSignals():
    SubData = my_Data.fillna(0)
    result = SubData['S1'] - SubData['S2']
    return result.index, result.values

def ShiftSignal(input):
    shiftData = my_Data
    result_indexes = shiftData['S1'].index - input
    result_values = shiftData['S1'].values
    
    result = pd.Series(data= result_values, index=result_indexes)
    return result.index, result.values

def Fold():
    foldData = pd.Series(my_Data['S1'].values, index=-my_Data['S1'].index).sort_index()
    return foldData.index, foldData.values

if __name__ == "__main__":
    idx, vals = AddingSignals()
    AddSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", idx, vals)

    idx, vals = MultiplySignals(5)
    MultiplySignalByConst(5, idx, vals)

    idx, vals = SubSignals()
    SubSignalSamplesAreEqual("Signal1.txt", "Signal2.txt", idx, vals)

    idx, vals = ShiftSignal(3)
    ShiftSignalByConst(3, idx, vals)

    idx, vals = ShiftSignal(-3)
    ShiftSignalByConst(-3, idx, vals)

    idx, vals = Fold()
    Folding(idx, vals)
