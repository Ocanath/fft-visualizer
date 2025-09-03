import numpy as np
import matplotlib.pyplot as plt
#from scipy.fft import fft, fftfreq
import scipy as scipy
import scipy.io
import scipy.signal

def main():
    # Load .mat file
    mat_data = scipy.io.loadmat('SDS814X_HD_Matlab_C1_17.mat')
    
    # Extract time and signal data (keys are zero-padded)
    time_key = [k for k in mat_data.keys() if k.rstrip('\x00') == 'C1_time'][0]
    data_key = [k for k in mat_data.keys() if k.rstrip('\x00') == 'C1_data'][0]
    
    t = mat_data[time_key].flatten()
    print(f"Mint: {np.min(t)}, maxt: {np.max(t)}")
    t = t - t[0]
    print(f"Mint: {np.min(t)}, maxt: {np.max(t)}")
    signal = mat_data[data_key].flatten()
    
    #example test signal
    # t = np.linspace(0,10,100000)
    # signal = 5 + np.sin(t*2*np.pi*1000)*3


    # Calculate N and sampling frequency from the data
    N = len(signal)
    T_total = t[-1] - t[0]  # Total time duration
    fs = (N - 1) / T_total  # Sampling frequency
    
    print(f"Vppmax data: {np.max(signal) - np.min(signal)}")
    print(f"N (number of samples): {N}")
    print(f"Total duration: {T_total:.6f} s")
    print(f"Sampling frequency: {fs:.2f} Hz")
    
    # Apply Hanning window
    window = scipy.signal.windows.hann(N, False)
    windowed_signal = signal * window
    
    # Compute FFT
    fft_values = scipy.fft.fft(windowed_signal)
    fft_freq = scipy.fft.fftfreq(N, 1/fs)
    
    # Take only positive frequencies
    positive_freq_idx = fft_freq > 0 
    
    # Calculate coherent gain for Hanning window and apply correct scaling
    coherent_gain = np.mean(window)  # ~0.5 for Hanning window
    fft_magnitude = np.abs(fft_values) * 2 / (N * coherent_gain)  # Compensate for window gain
    
    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot original signal
    ax1.plot(t, signal)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('TDS')
    ax1.grid(True)
    
    # Plot FFT magnitude spectrum
    fftpos = fft_freq[positive_freq_idx]
    fftmag = fft_magnitude[positive_freq_idx]
    ax2.plot(fftpos, fftmag*1000)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude (mV)')
    ax2.set_title('FFT Magnitude Spectrum')
    ax2.set_ylim(0,30)
    ax2.set_xlim(0, 15)  # Focus on low frequencies
    ax2.grid(True)
    
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()