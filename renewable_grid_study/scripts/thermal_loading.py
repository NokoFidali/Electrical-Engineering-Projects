"""
Thermal Loading Analysis for Grid Connection Study
Calculates line currents, thermal loading, and losses
"""

import numpy as np


def calculate_current(P, V, PF=1.0):
    """
    Calculate three-phase current
    
    Args:
        P: Active power (W)
        V: Line-to-line voltage (V)
        PF: Power factor (pu)
        
    Returns:
        I: Current (A)
    """
    I = P / (np.sqrt(3) * V * PF)
    return I


def calculate_line_losses(I, R):
    """
    Calculate resistive losses in the line
    
    Args:
        I: Current (A)
        R: Line resistance (Ohms)
        
    Returns:
        P_loss: Real power loss (W)
    """
    P_loss = 3 * (I ** 2) * R  # 3 for three phases
    return P_loss


def calculate_thermal_loading(I, I_ampacity):
    """
    Calculate thermal loading percentage
    
    Args:
        I: Current (A)
        I_ampacity: Line ampacity (A)
        
    Returns:
        loading_percent: Loading as percentage
        margin: Margin to limit (A)
    """
    loading_percent = (I / I_ampacity) * 100
    margin = I_ampacity - I
    
    return loading_percent, margin


def check_thermal_compliance(I, I_ampacity, limit=100.0):
    """
    Check if thermal loading complies with grid limits
    
    Args:
        I: Current (A)
        I_ampacity: Line ampacity (A)
        limit: Loading limit (%) - default 100%
        
    Returns:
        compliant: Boolean indicating compliance
        loading: Loading percentage
    """
    loading = (I / I_ampacity) * 100
    compliant = loading <= limit
    
    return compliant, loading


if __name__ == "__main__":
    # Example calculation
    P = 5e6  # 5 MW
    V = 11e3  # 11 kV
    PF = 0.98
    R = 0.3 * 5  # 1.5 Ohms (0.3 Ohm/km * 5 km)
    I_ampacity = 300  # Typical MV line ampacity (A)
    
    I = calculate_current(P, V, PF)
    P_loss = calculate_line_losses(I, R)
    loading, margin = calculate_thermal_loading(I, I_ampacity)
    
    print("=" * 50)
    print("THERMAL LOADING ANALYSIS")
    print("=" * 50)
    print(f"Active Power (P):     {P/1e6:.2f} MW")
    print(f"Voltage:              {V/1e3:.1f} kV")
    print(f"Power Factor:         {PF}")
    print(f"\nCurrent:              {I:.2f} A")
    print(f"Line Resistance:      {R:.2f} Ω")
    print(f"Line Losses:          {P_loss/1e3:.2f} kW ({(P_loss/P)*100:.2f}%)")
    print("=" * 50)
    
    # Compliance check
    compliant, loading_pct = check_thermal_compliance(I, I_ampacity, limit=80.0)
    
    print(f"\nLine Ampacity:        {I_ampacity:.0f} A")
    print(f"Thermal Loading:      {loading_pct:.2f}%")
    print(f"Safety Margin:        {margin:.2f} A")
    print(f"Grid Code Limit:      80%")
    print(f"Compliant:            {'✓ YES' if compliant else '✗ NO'}")
    print("=" * 50)
