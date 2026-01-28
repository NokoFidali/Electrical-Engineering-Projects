# Renewable Energy Grid Connection Study

A comprehensive Python-based analysis tool for assessing the impact of connecting renewable energy sources (Solar PV/Wind) to electrical distribution networks. This project mirrors real-world grid connection studies conducted by utilities and consulting firms.

## Project Overview

This study evaluates whether a proposed renewable energy plant can be connected to an existing electrical network while maintaining compliance with grid codes and operational standards.

### Key Analyses Performed

1. **Voltage Rise Analysis** - Assesses voltage changes due to power injection
2. **Thermal Loading Assessment** - Checks cable current limits
3. **Network Losses Comparison** - Evaluates impact on system losses
4. **Load Flow Analysis** - Detailed power flow calculations
5. **Grid Code Compliance** - Verification against regulatory limits

## Technical Scope

### Network Configuration

```
GRID (Slack Bus)
     |
   Feeder (5 km)
     |
  MV Bus  —— PV Plant (5 MW)
     |
   Load (3 MW)
```

### Analysis Parameters

| Parameter | Value | Unit |
|-----------|-------|------|
| Grid Voltage | 11 | kV |
| Feeder Length | 5 | km |
| Line Resistance | 0.3 | Ω/km |
| Line Reactance | 0.4 | Ω/km |
| PV Plant Capacity | 5 | MW |
| PV Power Factor | 0.98 | pu |

### Engineering Assumptions

- Steady-state operation
- Balanced three-phase system
- Constant renewable power output at rated capacity
- Inverter-based generation with power factor control
- Unity or controlled power factor (±0.95-0.98)

## Key Calculations

### Voltage Rise
$$\Delta V \approx \frac{P R + Q X}{V}$$

Where:
- P = Active power (W)
- Q = Reactive power (VAR)
- R = Line resistance (Ω)
- X = Line reactance (Ω)
- V = Voltage (V)

### Thermal Loading
$$I = \frac{P}{\sqrt{3} \cdot V \cdot PF}$$

### Network Losses
$$P_{loss} = 3 \cdot I^2 \cdot R$$

## Grid Code Compliance Criteria

- **Voltage Limits**: ±5% of nominal (typical for distribution)
- **Power Factor**: 0.95-1.0 lagging/leading
- **Thermal Loading**: ≤80% of line ampacity
- **System Stability**: N-1 contingency assessment

## Project Structure

```
renewable_grid_study/
│
├── main.py                          # Main analysis script
│
├── data/
│   └── network_parameters.csv       # Input network data
│
├── scripts/
│   ├── voltage_rise.py             # Voltage rise calculations
│   ├── thermal_loading.py          # Thermal analysis
│   └── load_flow.py                # Load flow analysis
│
├── outputs/
│   ├── voltage_profile.png         # Voltage plots
│   └── loading_report.xlsx         # Detailed reports
│
└── report/
    └── grid_connection_study.pdf   # Final technical report
```

## Installation & Usage

### Prerequisites

- Python 3.7+
- pandas
- numpy
- matplotlib (for plotting)
- openpyxl (for Excel reports)

### Running the Analysis

```bash
# Navigate to project directory
cd renewable_grid_study

# Run main analysis
python main.py
```

### Output

The analysis produces:
- Console output with detailed results
- Compliance assessment
- Power flow comparisons
- Loss analysis

## Example Results

```
VOLTAGE RISE ANALYSIS
Voltage rise: 3.2% ✓ Compliant (limit: ±5%)

THERMAL LOADING
Line loading: 72% ✓ Compliant (limit: 80%)

NETWORK LOSSES
Loss change: -18% (PV reduces network losses)

OVERALL RECOMMENDATION
✓ PV PLANT CAN BE CONNECTED
The proposed 5 MW PV plant complies with all grid code requirements.
```

## Professional Applications

This study framework is applicable to:
- Small-scale DG connections (10-50 MW)
- Solar farms and wind projects
- Microgrid feasibility studies
- Network upgrade planning
- Utility interconnection applications

## Engineering Standards Referenced

- **IEC 60364** - Electrical installations
- **IEEE 1159** - Power quality
- **IEEE 1547** - Distributed generation interconnection
- **Local grid codes** (Eskom, municipality standards)

## Future Enhancements

- [ ] Harmonic distortion analysis
- [ ] Protection coordination study
- [ ] Dynamic stability assessment
- [ ] Multi-scenario analysis (worst-case, N-1 contingency)
- [ ] Automated report generation (PDF)
- [ ] Visualization dashboard (Plotly/Dash)
- [ ] Database integration for tracking studies

## Author

Created as a professional consulting project portfolio piece demonstrating:
- Power systems analysis
- Python engineering software
- Professional technical documentation
- Grid code compliance verification

## License

This project is available for educational and professional use.

---

**Note**: This is a simplified study tool for assessment purposes. Production studies should incorporate full load flow software (DIgSILENT PowerFactory, ETAP, etc.) and be conducted by licensed Professional Engineers.
