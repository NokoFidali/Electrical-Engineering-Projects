"""
Voltage Rise Calculation for Grid Connection Study
Calculates voltage rise due to renewable energy injection
"""

import numpy as np


def calculate_reactive_power(P, PF):
    """
    Calculate reactive power from active power and power factor
    
    Args:
        P: Active power (W)
        PF: Power factor (pu)
        
    Returns:
        Q: Reactive power (VAR)
    """
    if PF == 1.0:
        return 0
    angle = np.arccos(PF)
    Q = P * np.tan(angle)
    return Q


def calculate_voltage_rise(P, Q, V, R, X):
    """
    Calculate voltage rise using formula: ΔV = (P*R + Q*X) / V²
    
    Args:
        P: Active power (W)
        Q: Reactive power (VAR)
        V: Voltage (V)
        R: Line resistance (Ohms)
        X: Line reactance (Ohms)
        
    Returns:
        delta_V_percent: Voltage rise as percentage
        delta_V_volts: Voltage rise in volts
    """
    delta_V_volts = (P * R + Q * X) / V
    delta_V_percent = (delta_V_volts / V) * 100
    
    return delta_V_percent, delta_V_volts


def check_voltage_compliance(V_before, delta_V_volts, V_nominal, limit=5.0):
    """
    Check if voltage rise complies with grid code limits
    
    Args:
        V_before: Voltage before PV injection (V)
        delta_V_volts: Voltage rise (V)
        V_nominal: Nominal voltage (V)
        limit: Voltage limit (%) - default 5%
        
    Returns:
        compliant: Boolean indicating compliance
        V_after: Voltage after injection (V)
        V_percent: Voltage as % of nominal
    """
    V_after = V_before + delta_V_volts
    V_percent = (V_after / V_nominal) * 100
    
    # Check if within ±limit%
    compliant = (100 - limit) <= V_percent <= (100 + limit)
    
    return compliant, V_after, V_percent


if __name__ == "__main__":
    # Example calculation
    P = 5e6  # 5 MW
    PF = 0.98
    V = 11e3  # 11 kV
    R = 0.3 * 5  # 1.5 Ohms (0.3 Ohm/km * 5 km)
    X = 0.4 * 5  # 2.0 Ohms (0.4 Ohm/km * 5 km)
    
    Q = calculate_reactive_power(P, PF)
    delta_V_pct, delta_V_v = calculate_voltage_rise(P, Q, V, R, X)
    
    print("=" * 50)
    print("VOLTAGE RISE ANALYSIS")
    print("=" * 50)
    print(f"Active Power (P):     {P/1e6:.2f} MW")
    print(f"Reactive Power (Q):   {Q/1e6:.3f} MVAR")
    print(f"Power Factor:         {PF}")
    print(f"Line Resistance:      {R:.2f} Ω")
    print(f"Line Reactance:       {X:.2f} Ω")
    print(f"\nVoltage Rise:         {delta_V_pct:.3f} %")
    print(f"Voltage Rise (V):     {delta_V_v:.2f} V")
    print("=" * 50)
    
    # Compliance check
    V_nominal = 11e3
    V_before = 11e3  # Assuming nominal before injection
    compliant, V_after, V_pct = check_voltage_compliance(V_before, delta_V_v, V_nominal, limit=5.0)
    
    print(f"\nVoltage Before PV:    {V_before/1e3:.2f} kV ({100:.1f}%)")
    print(f"Voltage After PV:     {V_after/1e3:.4f} kV ({V_pct:.2f}%)")
    print(f"Grid Code Limit:      ±5%")
    print(f"Compliant:            {'✓ YES' if compliant else '✗ NO'}")
    print("=" * 50)
