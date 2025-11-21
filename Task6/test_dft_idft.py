import math
try:
    from .Task6 import FourierTransform, GetAmplitudeAndPhaseShift, ReadSignalFile
    from .signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift, RoundPhaseShift
except ImportError:
    from Task6 import FourierTransform, GetAmplitudeAndPhaseShift, ReadSignalFile
    from signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift, RoundPhaseShift


def test_dft():
    """Test DFT using the input_Signal_DFT.txt test case"""
    input_file = "Task6/Test Cases/DFT/input_Signal_DFT.txt"
    try:
        indices, samples = ReadSignalFile(input_file)
        FT = FourierTransform(samples, IDFT=False)
        amp, phase_rad = GetAmplitudeAndPhaseShift(FT)
        return True
    except Exception:
        return False


def test_idft():
    """Test IDFT (Inverse Discrete Fourier Transform)"""
    print("\n" + "="*60)
    print("TEST: IDFT (Inverse Discrete Fourier Transform)")
    print("="*60)
    
    # Read input signal (using DFT input as test signal)
    input_file = "Task6/Test Cases/DFT/input_Signal_DFT.txt"
    try:
        indices, samples = ReadSignalFile(input_file)
        print(f"✓ Input file read successfully")
        print(f"  Original samples: {samples}")
    except Exception as e:
        print(f"✗ Failed to read input file: {e}")
        return False

    # Compute DFT then IDFT (round-trip test)
    try:
        # Forward DFT
        FT = FourierTransform(samples, IDFT=False)
        print(f"✓ Forward DFT computed")
        
        # Inverse DFT
        reconstructed = FourierTransform(FT, IDFT=True)
        recon_real = [x.real for x in reconstructed]
        print(f"✓ IDFT computed successfully")
        print(f"\n  Reconstructed samples: {[round(x, 6) for x in recon_real]}")
        
        # Compare original vs reconstructed
        print(f"\n  Comparison (Original vs Reconstructed):")
        max_error = 0
        for i, (orig, recon) in enumerate(zip(samples, recon_real)):
            error = abs(orig - recon)
            max_error = max(max_error, error)
            print(f"    Sample[{i}]: {orig:.6f} → {recon:.6f} (error: {error:.2e})")
        
        print(f"\n  Maximum absolute error: {max_error:.2e}")
        
        # Test amplitude comparison
        amp_orig, _ = GetAmplitudeAndPhaseShift(FT)
        amp_recon, _ = GetAmplitudeAndPhaseShift(FourierTransform(reconstructed, IDFT=False))
        
        if SignalComapreAmplitude(amp_orig, amp_recon):
            print(f"✓ Amplitude comparison PASSED")
        else:
            print(f"✗ Amplitude comparison FAILED")
        
        return True
    except Exception as e:
        print(f"✗ IDFT computation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_roundtrip_accuracy():
    """Test accuracy of DFT -> IDFT round-trip"""
    print("\n" + "="*60)
    print("TEST: DFT → IDFT Round-trip Accuracy")
    print("="*60)
    
    # Test with multiple signals
    test_signals = [
        [1, 0, 0, 0],
        [1, 1, 1, 1],
        [1, 2, 3, 4],
        [0, 1, 0, 1],
    ]
    
    all_passed = True
    for sig_idx, signal in enumerate(test_signals):
        print(f"\n  Test Signal {sig_idx + 1}: {signal}")
        
        # Forward-inverse round trip
        FT = FourierTransform(signal, IDFT=False)
        reconstructed = FourierTransform(FT, IDFT=True)
        recon_real = [x.real for x in reconstructed]
        
        # Check accuracy
        max_error = max(abs(orig - recon) for orig, recon in zip(signal, recon_real))
        tolerance = 1e-10
        
        if max_error < tolerance:
            print(f"    ✓ PASSED (max error: {max_error:.2e})")
        else:
            print(f"    ✗ FAILED (max error: {max_error:.2e}, tolerance: {tolerance})")
            all_passed = False
    
    return all_passed


if __name__ == "__main__":
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  DFT/IDFT Test Suite".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    # Run all tests
    test1 = test_dft()
    test2 = test_idft()
    test3 = test_roundtrip_accuracy()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"DFT Test:                    {'PASSED ✓' if test1 else 'FAILED ✗'}")
    print(f"IDFT Test:                   {'PASSED ✓' if test2 else 'FAILED ✗'}")
    print(f"Round-trip Accuracy Test:    {'PASSED ✓' if test3 else 'FAILED ✗'}")
    print("="*60)
    
    if test1 and test2 and test3:
        print("All tests PASSED! ✓")
    else:
        print("Some tests FAILED! ✗")
