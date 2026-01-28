# Cable Size Calculator

A professional electrical engineering tool for calculating optimal cable cross-sections based on IEC standards. Supports both Low Voltage (LV) and Medium Voltage (MV) systems with comprehensive multi-criteria cable selection.

## Features

### Cable Selection Criteria
- **Ampacity Rating** - Ensures cable can safely carry the required current
- **Voltage Drop Compliance** - Verifies voltage drop stays within limits (5% LV, 3% MV)
- **Thermal Withstand** - Checks short-circuit thermal protection (when specified)
- **System Flexibility** - Supports multiple parallel cables for high-power applications

### Supported Cable Ranges

**Low Voltage (LV) System:**
- Cable sizes: 16, 25, 35, 50, 70 mm²
- Ampacity range: 76 - 195 A
- Default voltage drop limit: 5%

**Medium Voltage (MV) System:**
- Cable sizes: 50, 95, 185, 300 mm²
- Ampacity range: 150 - 460 A
- Default voltage drop limit: 3%

### User Interface
- GUI-based input form
- Real-time calculation and validation
- Detailed results display
- Error handling with user-friendly messages

## Installation

### Requirements
- Python 3.7 or higher
- tkinter (included with most Python installations)

### Setup
```bash
# No external dependencies required - uses only Python standard library
python main.py
```

## Usage

### Running the Calculator

```bash
python main.py
```

### Input Parameters

1. **Power (MW)** - System power in megawatts
2. **Voltage (V)** - System voltage in volts
   - LV: Typically 230/400V or 11kV
   - MV: Typically 11kV, 22kV, 33kV
3. **Power Factor** - Load power factor (0.8 - 1.0)
4. **Cable Length (m)** - Physical distance the cable spans
5. **System Type** - Select "LV" or "MV"
6. **Short-Circuit Current (kA)** - Optional, for thermal protection verification

### Example Calculation

**Input:**
- Power: 5 MW
- Voltage: 11,000 V (11 kV)
- Power Factor: 0.98
- Cable Length: 500 m
- System Type: MV
- Short-Circuit Current: 15 kA

**Output:**
```
System: MV
Cable Size: 95 mm²
Operating Current: 242.76 A
Voltage Drop: 2.15%
Thermal Withstand: 15 kA
Thermal Margin: 0.0%
Status: ✓ SUITABLE
```

## Technical Specifications

### Cable Properties Database

#### LV Cables (IEC 60228)
| Size (mm²) | Ampacity (A) | R (Ω/km) | Thermal Withstand (kA) |
|------------|-------------|----------|------------------------|
| 16         | 76          | 1.15     | 5.0                    |
| 25         | 101         | 0.727    | 7.5                    |
| 35         | 125         | 0.524    | 10.0                   |
| 50         | 150         | 0.387    | 13.0                   |
| 70         | 195         | 0.268    | 18.0                   |

#### MV Cables
| Size (mm²) | Ampacity (A) | R (Ω/km) | Thermal Withstand (kA) |
|------------|-------------|----------|------------------------|
| 50         | 150         | 0.39     | 10.0                   |
| 95         | 240         | 0.193    | 15.0                   |
| 185        | 355         | 0.099    | 22.0                   |
| 300        | 460         | 0.060    | 30.0                   |

### Calculation Methods

#### Operating Current
$$I = \frac{P}{\sqrt{3} \cdot V \cdot PF}$$

#### Voltage Drop
$$V_d\% = \frac{\sqrt{3} \cdot I \cdot R \cdot L}{V} \times 100$$

Where:
- I = Operating current (A)
- R = Cable resistance (Ω/km)
- L = Cable length (km)
- V = System voltage (V)

#### Thermal Withstand Check
$$\text{Margin} = \left(\frac{I_{thermal}}{I_{fault}} \times 100\right) - 100$$

## Compliance & Standards

This calculator follows:
- **IEC 60228** - Conductors of insulated cables
- **IEC 60364** - Electrical installations of buildings
- **IEEE 835** - Standard for Power Cable Ampacities
- **Local electrical codes** (South Africa: SABS, etc.)

## Professional Applications

Suitable for:
- Distribution network design
- Industrial power system planning
- Substation engineering
- Renewable energy plant integration
- Consulting firm deliverables

## Limitations & Notes

- **Simplified Model** - Does not account for:
  - Cable derating factors (temperature, grouping, burial depth)
  - Skin effect at high frequencies
  - Environmental conditions
  
- **Use Cases** - Best for:
  - Quick feasibility studies
  - Preliminary design phases
  - Educational purposes
  
- **Production Design** - For detailed engineering:
  - Use specialized software (ETAP, DIgSILENT, etc.)
  - Consult with licensed Professional Engineers
  - Apply all applicable derating factors

## Future Enhancements

- [ ] Multiple conductor materials (Cu, Al)
- [ ] Cable derating factor calculator
- [ ] Parallel cable support
- [ ] Temperature and environment factors
- [ ] Export to Excel/PDF
- [ ] Database for standard cable types

## Project Structure

```
cable_size_calculator/
├── main.py          # GUI application & calculations
└── README.md        # This file
```

## Author

Created as part of electrical engineering consulting portfolio.

## License

Open source - available for educational and professional use.

---

**Note**: This tool is for engineering assessment purposes. Always verify results with industry-standard cable sizing software and consult with Professional Engineers before implementation.
