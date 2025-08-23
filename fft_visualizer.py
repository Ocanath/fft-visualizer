import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import sympy as sp
import scipy.fft

class FFTVisualizer:
    def __init__(self):
        # Parameters
        self.fs = 1000  # Sampling frequency (Hz)
        self.T = 1.0    # Duration (seconds)
        self.n_periods = 2  # Number of periods to show in time domain
        
        # Calculate derived parameters
        self.update_sampling_parameters()
        
        # Default expression
        self.default_expr = "sin(t*2*pi*10)"
        
        # Setup the plot
        self.setup_plot()
        
        # Initial plot
        self.update_plot(self.default_expr)
    
    def update_sampling_parameters(self):
        """Update N and time array when fs or T changes"""
        self.N = int(self.fs * self.T)  # Number of samples
        self.t = np.linspace(0, self.T, self.N, endpoint=False)  # Time array
        # Create high-resolution time array for smooth plotting (10x upsampled)
        self.N_hires = self.N * 10
        self.t_hires = np.linspace(0, self.T, self.N_hires, endpoint=False)
    
    def setup_plot(self):
        # Create figure and subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 10))
        plt.subplots_adjust(bottom=0.25)  # Make room for more widgets
        
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
        ax_textbox = plt.axes([0.15, 0.12, 0.6, 0.04])
        self.textbox = TextBox(ax_textbox, 'Expression: ', initial=self.default_expr)
        self.textbox.on_submit(self.on_text_submit)
        
        # Create text box for sampling frequency
        ax_fs_textbox = plt.axes([0.15, 0.07, 0.25, 0.04])
        self.fs_textbox = TextBox(ax_fs_textbox, 'Fs (Hz): ', initial=str(self.fs))
        self.fs_textbox.on_submit(self.on_fs_submit)
        
        # Create text box for time duration
        ax_t_textbox = plt.axes([0.5, 0.07, 0.25, 0.04])
        self.t_textbox = TextBox(ax_t_textbox, 'T (s): ', initial=str(self.T))
        self.t_textbox.on_submit(self.on_t_submit)
        
        # Create update button
        ax_button = plt.axes([0.8, 0.07, 0.1, 0.04])
        self.button = Button(ax_button, 'Update')
        self.button.on_clicked(self.on_button_click)
        
        # Initialize plot lines
        self.line_continuous, = self.ax1.plot([], [], 'b-', linewidth=1.5, alpha=0.7, label='Continuous signal')
        self.line_samples, = self.ax1.plot([], [], 'ro', markersize=6, label='Sampled points')
        self.stems = []  # Will hold vertical line segments
        self.line2, = self.ax2.plot([], [], 'r-', linewidth=2)
        
        # Add legend to time domain plot
        self.ax1.legend(loc='upper right')
    
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
    
    def evaluate_expression_hires(self, expr_text):
        """Evaluate expression on high-resolution time array for smooth plotting"""
        try:
            # Define symbolic variable
            t_sym = sp.Symbol('t')
            
            # Parse the expression
            expr = sp.sympify(expr_text)
            
            # Convert to numpy function
            func = sp.lambdify(t_sym, expr, ['numpy', 'scipy'])
            
            # Evaluate on high-resolution time array
            signal_hires = func(self.t_hires)
            
            return np.real(signal_hires)  # Take real part in case of complex results
            
        except Exception as e:
            print(f"Error parsing expression '{expr_text}': {e}")
            # Return default signal on error
            return np.sin(2 * np.pi * 10 * self.t_hires)
    
    def update_plot(self, expr_text):
        """Update both time and frequency domain plots"""
        # Parse expression and generate sampled signal
        signal = self.parse_expression(expr_text)
        
        # Generate high-resolution signal for smooth plotting
        signal_hires = self.evaluate_expression_hires(expr_text)
        
        # Compute FFT
        freq, magnitude = self.compute_fft(signal)
        
        # Find maximum frequency and calculate time window
        max_freq = self.find_max_frequency(freq, magnitude)
        time_window = self.n_periods / max_freq  # Show n periods of max frequency
        
        # Create masks for time window
        time_mask = self.t <= time_window
        time_mask_hires = self.t_hires <= time_window
        
        # Update continuous signal line (high-resolution)
        self.line_continuous.set_data(self.t_hires[time_mask_hires], signal_hires[time_mask_hires])
        
        # Update sampled points (scatter plot)
        self.line_samples.set_data(self.t[time_mask], signal[time_mask])
        
        # Clear previous stems and create new ones
        for stem in self.stems:
            stem.remove()
        self.stems.clear()
        
        # Add vertical lines (stems) from x-axis to sample points
        t_display = self.t[time_mask]
        signal_display = signal[time_mask]
        for i in range(len(t_display)):
            stem = self.ax1.plot([t_display[i], t_display[i]], [0, signal_display[i]], 
                               'r-', alpha=0.6, linewidth=1)[0]
            self.stems.append(stem)
        
        # Set axis limits and scaling
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
        """Handle expression text box submission"""
        self.update_plot(text)
    
    def on_fs_submit(self, text):
        """Handle sampling frequency text box submission"""
        try:
            new_fs = float(text)
            if new_fs > 0:
                self.fs = new_fs
                self.update_sampling_parameters()
                current_expr = self.textbox.text
                self.update_plot(current_expr)
            else:
                print("Sampling frequency must be positive")
        except ValueError:
            print(f"Invalid sampling frequency: {text}")
    
    def on_t_submit(self, text):
        """Handle time duration text box submission"""
        try:
            new_T = float(text)
            if new_T > 0:
                self.T = new_T
                self.update_sampling_parameters()
                current_expr = self.textbox.text
                self.update_plot(current_expr)
            else:
                print("Time duration must be positive")
        except ValueError:
            print(f"Invalid time duration: {text}")
    
    def on_button_click(self, event):
        """Handle button click - update all parameters"""
        # Update fs and T from text boxes
        self.on_fs_submit(self.fs_textbox.text)
        self.on_t_submit(self.t_textbox.text)
        # Update plot with current expression
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