import numpy as np
import matplotlib.pyplot as plt
#from scipy.fft import fft, fftfreq
import scipy as scipy

def main():
    # Parameters
    fs = 1000  # Sampling frequency (Hz)
    T = 1.0    # Duration (seconds)
    N = int(fs * T)  # Number of samples
    
    # Create time array
    t = np.linspace(0, T, N, endpoint=False)
    
    # Create signal: sin(10*2*pi*t)
    frequency = 10  # Hz
    signal = np.sin(10 * 2 * np.pi * t)
    
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
    ax1.set_title('Original Signal: sin(10*2*π*t)')
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