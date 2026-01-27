# JIT Cable Size Calculator

A Python-based electrical engineering tool for calculating appropriate cable sizes based on JIT (Just-In-Time) standards. This project helps engineers determine the optimal cable cross-sections for low voltage (LV) and medium voltage (MV) electrical systems.

## Features

- **LV Cable Selection**: Supports cable sizes 16, 25, 35, 50, and 70 mm²
- **MV Cable Selection**: Supports cable sizes 50, 95, 185, and 300 mm²
- **Multi-Criteria Analysis**: Selects cables based on:
  - Ampacity (current carrying capacity)
  - Voltage drop limits (5% for LV, 3% for MV)
  - Thermal withstand capability
  - Short-circuit current protection
- **GUI Interface**: User-friendly Tkinter-based interface
- **Comprehensive Calculations**: Handles power, voltage, power factor, and cable length inputs

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup

1. Clone this repository
2. Navigate to the project directory:
   ```bash
   cd JIT
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the application by running `python main.py`
2. Enter the following parameters:
   - **Power (MW)**: System power in megawatts
   - **Voltage (V)**: System voltage in volts
   - **Power Factor**: Typically 0.9-1.0
   - **Cable Length (m)**: Distance the cable needs to span
   - **System Type**: Select "LV" or "MV"
   - **Short-circuit Current (kA)**: Optional, for thermal withstand checks

3. Click "Calculate" to determine the recommended cable size
4. Results show the selected cable cross-section and key parameters

## Project Structure

```
JIT/
├── main.py                    # Main application with GUI
├── cable_size_calculator/
│   └── main.py               # Core calculator functions
├── README.md                 # This file
└── .gitignore               # Git ignore file
```

## Technical Details

### LV Cables
- Supports standard European cable specifications
- Ampacity range: 76-195 A
- Voltage drop limit: 5%

### MV Cables
- Supports medium voltage applications
- Ampacity range: 150-460 A
- Voltage drop limit: 3%

### Cable Properties Included
- Ampacity (A)
- Resistance (Ω/km)
- Thermal withstand (kA for 1 second)

## Author

Created as part of electrical engineering projects portfolio.

## License

This project is open source and available for educational and professional use.

## Contributing

Feel free to fork, submit issues, and create pull requests for improvements.

---

For more information on cable sizing standards and electrical engineering best practices, refer to IEC 60364 and local electrical codes.
