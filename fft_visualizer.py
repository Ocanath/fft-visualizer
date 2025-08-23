import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import sympy as sp
import scipy.fft

class FFTVisualizer:
    def __init__(self):
        # Parameters
        self.fs = 3000  # Sampling frequency (Hz)
        self.T = 1.0    # Duration (seconds)
        self.N = int(self.fs * self.T)  # Number of samples
        self.n_periods = 2  # Number of periods to show in time domain
        
        # Create time array
        self.t = np.linspace(0, self.T, self.N, endpoint=False)
        
        # Default expression
        self.default_expr = "sin(t*2*pi*10)"
        
        # Setup the plot
        self.setup_plot()
        
        # Initial plot
        self.update_plot(self.default_expr)
    
    def setup_plot(self):
        # Create figure and subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 10))
        plt.subplots_adjust(bottom=0.15)  # Make room for widgets
        
        # Setup axes
        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Amplitude')
        self.ax1.set_title('Time Domain Signal')
        self.ax1.grid(True)
        
        self.ax2.set_xlabel('Frequency (Hz)')
        self.ax2.set_ylabel('Magnitude')
        self.ax2.set_title('FFT Magnitude Spectrum')
        self.ax2.grid(True)
        
        # Create text box for expression input
        ax_textbox = plt.axes([0.15, 0.05, 0.6, 0.04])
        self.textbox = TextBox(ax_textbox, 'Expression: ', initial=self.default_expr)
        self.textbox.on_submit(self.on_text_submit)
        
        # Create update button
        ax_button = plt.axes([0.8, 0.05, 0.1, 0.04])
        self.button = Button(ax_button, 'Update')
        self.button.on_clicked(self.on_button_click)
        
        # Initialize plot lines
        self.line1, = self.ax1.plot([], [], 'b-', linewidth=2)
        self.line2, = self.ax2.plot([], [], 'r-', linewidth=2)
    
    def parse_expression(self, expr_text):
        """Parse symbolic expression using SymPy"""
        try:
            # Define symbolic variable
            t_sym = sp.Symbol('t')
            
            # Parse the expression
            expr = sp.sympify(expr_text)
            
            # Convert to numpy function
            func = sp.lambdify(t_sym, expr, ['numpy', 'scipy'])
            
            # Evaluate the function
            signal = func(self.t)
            
            return np.real(signal)  # Take real part in case of complex results
            
        except Exception as e:
            print(f"Error parsing expression '{expr_text}': {e}")
            # Return default signal on error
            return np.sin(2 * np.pi * 10 * self.t)
    
    def compute_fft(self, signal):
        """Compute FFT and return frequencies and magnitudes"""
        # Compute FFT
        fft_values = scipy.fft.fft(signal)
        fft_freq = scipy.fft.fftfreq(self.N, 1/self.fs)
        
        # Take only positive frequencies
        positive_freq_idx = fft_freq > 0
        fft_magnitude = np.abs(fft_values) * 2 / self.N  # Normalize
        
        return fft_freq[positive_freq_idx], fft_magnitude[positive_freq_idx]
    
    def find_max_frequency(self, freq, magnitude):
        """Find the frequency with maximum magnitude"""
        if len(magnitude) == 0:
            return 10  # Default frequency
        
        # Find frequency with maximum magnitude (ignore DC component)
        non_dc_idx = freq > 1  # Ignore frequencies below 1 Hz
        if np.any(non_dc_idx):
            max_idx = np.argmax(magnitude[non_dc_idx])
            max_freq = freq[non_dc_idx][max_idx]
        else:
            max_freq = freq[np.argmax(magnitude)] if len(freq) > 0 else 10
        
        return max(max_freq, 1)  # Ensure minimum frequency of 1 Hz
    
    def update_plot(self, expr_text):
        """Update both time and frequency domain plots"""
        # Parse expression and generate signal
        signal = self.parse_expression(expr_text)
        
        # Compute FFT
        freq, magnitude = self.compute_fft(signal)
        
        # Find maximum frequency and calculate time window
        max_freq = self.find_max_frequency(freq, magnitude)
        time_window = self.n_periods / max_freq  # Show n periods of max frequency
        
        # Update time domain plot with limited time window
        time_mask = self.t <= time_window
        self.line1.set_data(self.t[time_mask], signal[time_mask])
        self.ax1.set_xlim(0, time_window)
        self.ax1.relim()
        self.ax1.autoscale_view(scalex=False)  # Don't autoscale x-axis
        
        # Update frequency domain plot
        self.line2.set_data(freq, magnitude)
        self.ax2.relim()
        self.ax2.autoscale_view()
        # self.ax2.set_xlim(0, min(100, max(freq)))  # Focus on relevant frequencies
        
        # Update title with current expression
        self.ax1.set_title(f'Time Domain Signal: {expr_text}')
        
        # Redraw
        self.fig.canvas.draw()
    
    def on_text_submit(self, text):
        """Handle text box submission"""
        self.update_plot(text)
    
    def on_button_click(self, event):
        """Handle button click"""
        current_text = self.textbox.text
        self.update_plot(current_text)
    
    def show(self):
        """Display the interactive plot"""
        plt.show()

def main():
    print("FFT Visualizer - Interactive Signal Analysis")
    print("Enter expressions using 't' as the time variable")
    print("Examples:")
    print("  sin(t*2*pi*10)")
    print("  sin(t*2*pi*10) + sin(t*2*pi*5)")
    print("  cos(t*2*pi*15) + 0.5*sin(t*2*pi*25)")
    print("  exp(-t*2)*sin(t*2*pi*20)")
    print("\nAvailable functions: sin, cos, exp, log, sqrt, etc.")
    print("Use 'pi' for π")
    
    visualizer = FFTVisualizer()
    visualizer.show()

if __name__ == "__main__":
    main()