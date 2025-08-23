# FFT Boilerplate & Interactive Visualizer

A collection of Python scripts for Fast Fourier Transform (FFT) analysis and visualization, designed as educational tools for understanding digital signal processing concepts.

## Contents

- `fft_example.py` - Basic FFT example with sine wave analysis
- `fft_visualizer.py` - Interactive FFT visualizer with symbolic expression input
- `requirements.txt` - Python dependencies

## Quick Start

### Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Tools

**Basic FFT Example:**
```bash
python fft_example.py
```

**Interactive FFT Visualizer:**
```bash
python fft_visualizer.py
```

## Features

### FFT Example (`fft_example.py`)
- Demonstrates FFT analysis of a 10 Hz sine wave
- Shows both time domain and frequency domain plots
- Normalized FFT magnitude for intuitive amplitude reading

### Interactive FFT Visualizer (`fft_visualizer.py`)
- **Symbolic Expression Input**: Enter mathematical expressions using `t` as time variable
- **Real-time Parameter Control**: Adjust sampling frequency and time duration
- **Advanced Time Domain Visualization**: 
  - Continuous signal (10x upsampled smooth curve)
  - Discrete samples (circles with stem plot)
  - Automatic scaling to show 2 periods of dominant frequency
- **FFT Magnitude Spectrum**: Normalized frequency domain representation

## Usage Examples

### Expression Syntax
Use standard mathematical notation with `t` as the time variable:

```
sin(t*2*pi*10)                    # 10 Hz sine wave
sin(t*2*pi*10) + sin(t*2*pi*5)    # Two frequency components
cos(t*2*pi*15) + 0.5*sin(t*2*pi*25) # Mixed amplitudes
exp(-t*2)*sin(t*2*pi*20)          # Exponentially decaying sine
sqrt(t)*cos(t*2*pi*30)            # Time-varying amplitude
```

### Available Functions
- Trigonometric: `sin`, `cos`, `tan`
- Exponential/Logarithmic: `exp`, `log`, `sqrt`
- Constants: `pi` (π), `e`
- Operations: `+`, `-`, `*`, `/`, `**` (power)

## Understanding the Visualizations

### Time Domain Plot
- **Blue Line**: Continuous mathematical function (high resolution)
- **Red Circles**: Actual sample points taken at sampling frequency
- **Red Stems**: Vertical lines showing discrete sample values
- **Auto-scaling**: Display shows 2 complete periods of the dominant frequency

### Frequency Domain Plot  
- **X-axis**: Frequency in Hz
- **Y-axis**: Magnitude (normalized to match time-domain amplitude)
- **Peaks**: Indicate frequency components present in the signal

## FFT Magnitude Scaling

The FFT magnitudes are normalized using the formula:
```
normalized_magnitude = 2 * |FFT| / N
```

This ensures that a sine wave with amplitude A in the time domain shows magnitude A in the frequency domain.

## Requirements

- Python 3.7+
- NumPy ≥ 1.21.0
- Matplotlib ≥ 3.5.0  
- SciPy ≥ 1.7.0
- SymPy ≥ 1.8.0

## Troubleshooting

- **Expression Errors**: Check syntax - use `t` for time, `pi` for π
- **Empty Plots**: Ensure sampling frequency > 0 and time duration > 0
- **Performance**: Very high sampling rates or long durations may slow rendering

## Example Session

1. Run `python fft_visualizer.py`
2. Try the default expression: `sin(t*2*pi*10)`
3. Change to: `sin(t*2*pi*10) + sin(t*2*pi*25)`
4. Adjust sampling frequency to 100 Hz
5. Observe aliasing effects when Fs < 2 × max_frequency
