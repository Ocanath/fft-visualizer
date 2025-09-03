import numpy as np
import matplotlib.pyplot as plt
#from scipy.fft import fft, fftfreq
import scipy as scipy
import scipy.io

def main():
    # Load .mat file
    mat_data = scipy.io.loadmat('SDS814X_HD_Matlab_C1_17.mat')
    
    # Extract time and signal data (keys are zero-padded)
    time_key = [k for k in mat_data.keys() if k.rstrip('\x00') == 'C1_time'][0]
    data_key = [k for k in mat_data.keys() if k.rstrip('\x00') == 'C1_data'][0]
    
    t = mat_data[time_key].flatten()
    signal = mat_data[data_key].flatten()
    
    # Calculate N and sampling frequency from the data
    N = len(signal)
    T_total = t[-1] - t[0]  # Total time duration
    fs = (N - 1) / T_total  # Sampling frequency
    
    print(f"N (number of samples): {N}")
    print(f"Total duration: {T_total:.6f} s")
    print(f"Sampling frequency: {fs:.2f} Hz")
    
    # Compute FFT
    fft_values = scipy.fft.fft(signal)
    fft_freq = scipy.fft.fftfreq(N, 1/fs)
    
    # Take only positive frequencies
    positive_freq_idx = fft_freq > 0 
    fft_magnitude = np.abs(fft_values) * 2 / N  #absolute value, and scale to volts
    
    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot original signal
    ax1.plot(t, signal)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('TDS')
    ax1.grid(True)
    
    # Plot FFT magnitude spectrum
    ax2.plot(fft_freq[positive_freq_idx], fft_magnitude[positive_freq_idx])
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude (Volts)')
    ax2.set_title('FFT Magnitude Spectrum')
    ax2.grid(True)
    # ax2.set_xlim(0, 50)  # Focus on low frequencies
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()