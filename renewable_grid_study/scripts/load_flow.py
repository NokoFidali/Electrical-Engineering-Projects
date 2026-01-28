"""
Simplified Load Flow Analysis for Grid Connection Study
Performs basic power flow calculations without PV and with PV
"""

import numpy as np
import pandas as pd


class PowerFlowAnalysis:
    """
    Simple power flow analysis for radial distribution networks
    """
    
    def __init__(self, V_nominal, S_base=1e6):
        """
        Initialize power flow analysis
        
        Args:
            V_nominal: Nominal system voltage (V)
            S_base: Base power (VA) - default 1 MVA
        """
        self.V_nominal = V_nominal
        self.S_base = S_base
        self.Z_base = (V_nominal ** 2) / S_base
        
    def calculate_impedance(self, R, X):
        """
        Calculate impedance magnitude and angle
        
        Args:
            R: Resistance (Ohms)
            X: Reactance (Ohms)
            
        Returns:
            Z: Impedance magnitude (Ohms)
            angle: Impedance angle (radians)
        """
        Z = np.sqrt(R**2 + X**2)
        angle = np.arctan2(X, R)
        return Z, angle
    
    def case_without_pv(self, P_load, PF_load, R, X):
        """
        Calculate voltage at load bus without PV injection
        
        Args:
            P_load: Load active power (W)
            PF_load: Load power factor
            R: Line resistance (Ohms)
            X: Line reactance (Ohms)
            
        Returns:
            V_load: Voltage at load bus (V)
            I: Current magnitude (A)
            P_loss: Real power loss (W)
        """
        # Calculate load reactive power
        Q_load = P_load * np.tan(np.arccos(PF_load))
        
        # Calculate current (approximate)
        I = P_load / (np.sqrt(3) * self.V_nominal * PF_load)
        
        # Voltage drop
        Z, angle = self.calculate_impedance(R, X)
        V_drop = I * Z * np.cos(angle - np.arctan2(Q_load, P_load))
        
        # Voltage at load
        V_load = self.V_nominal - V_drop
        
        # Losses
        P_loss = 3 * (I ** 2) * R
        
        return V_load, I, P_loss
    
    def case_with_pv(self, P_load, PF_load, P_pv, PF_pv, R, X):
        """
        Calculate voltage at load bus with PV injection at load bus
        
        Args:
            P_load: Load active power (W)
            PF_load: Load power factor
            P_pv: PV active power (W)
            PF_pv: PV power factor
            R: Line resistance (Ohms)
            X: Line reactance (Ohms)
            
        Returns:
            V_load: Voltage at load bus (V)
            I_net: Net current magnitude (A)
            P_loss: Real power loss (W)
            P_injected: Net power injected to grid (W)
        """
        # Calculate reactive powers
        Q_load = P_load * np.tan(np.arccos(PF_load))
        Q_pv = P_pv * np.tan(np.arccos(PF_pv))
        
        # Net power at load bus
        P_net = P_load - P_pv  # Negative if PV > Load
        Q_net = Q_load - Q_pv
        
        # Net current (to grid)
        if P_net >= 0:
            I_net = P_net / (np.sqrt(3) * self.V_nominal * PF_load)
        else:
            # Exporting to grid (PV > Load)
            I_net = abs(P_net) / (np.sqrt(3) * self.V_nominal * PF_pv)
        
        # Voltage rise/drop
        Z, angle = self.calculate_impedance(R, X)
        V_change = I_net * Z * np.cos(angle - np.arctan2(Q_net, P_net))
        
        # Voltage at load
        V_load = self.V_nominal + V_change if P_net < 0 else self.V_nominal - V_change
        
        # Losses
        P_loss = 3 * (I_net ** 2) * R
        
        # Power injected to grid (negative = export)
        P_injected = P_pv - P_load
        
        return V_load, I_net, P_loss, P_injected


def compare_cases(V_nominal=11e3, P_load=3e6, PF_load=0.95, 
                  P_pv=5e6, PF_pv=0.98, R=1.5, X=2.0):
    """
    Compare network conditions before and after PV installation
    
    Args:
        V_nominal: Nominal voltage (V)
        P_load: Load power (W)
        PF_load: Load power factor
        P_pv: PV power (W)
        PF_pv: PV power factor
        R: Line resistance (Ohms)
        X: Line reactance (Ohms)
    """
    
    pf = PowerFlowAnalysis(V_nominal)
    
    # Case 1: Without PV
    V1, I1, P_loss1 = pf.case_without_pv(P_load, PF_load, R, X)
    
    # Case 2: With PV
    V2, I2, P_loss2, P_inj = pf.case_with_pv(P_load, PF_load, P_pv, PF_pv, R, X)
    
    # Results
    print("=" * 70)
    print("LOAD FLOW ANALYSIS - BASE CASE vs WITH PV")
    print("=" * 70)
    print(f"\nNETWORK PARAMETERS:")
    print(f"Nominal Voltage:      {V_nominal/1e3:.1f} kV")
    print(f"Line Resistance:      {R:.2f} Ω")
    print(f"Line Reactance:       {X:.2f} Ω")
    print(f"\nLOAD:")
    print(f"Active Power:         {P_load/1e6:.2f} MW")
    print(f"Power Factor:         {PF_load}")
    print(f"\nPV PLANT:")
    print(f"Rated Power:          {P_pv/1e6:.2f} MW")
    print(f"Power Factor:         {PF_pv}")
    
    print("\n" + "=" * 70)
    print("CASE 1: BASE CASE (WITHOUT PV)")
    print("=" * 70)
    print(f"Voltage at Load Bus:  {V1/1e3:.4f} kV ({(V1/V_nominal)*100:.2f}%)")
    print(f"Line Current:         {I1:.2f} A")
    print(f"Line Losses:          {P_loss1/1e3:.2f} kW ({(P_loss1/P_load)*100:.2f}%)")
    
    print("\n" + "=" * 70)
    print("CASE 2: WITH PV INJECTION")
    print("=" * 70)
    print(f"Voltage at Load Bus:  {V2/1e3:.4f} kV ({(V2/V_nominal)*100:.2f}%)")
    print(f"Net Current:          {I2:.2f} A")
    print(f"Line Losses:          {P_loss2/1e3:.2f} kW ({(P_loss2/P_load)*100:.2f}% of load)")
    print(f"Power Injected:       {P_inj/1e6:.2f} MW")
    
    print("\n" + "=" * 70)
    print("IMPACT SUMMARY")
    print("=" * 70)
    V_change = (V2 - V1) / V_nominal * 100
    I_change = ((I2 - I1) / I1) * 100
    loss_change = ((P_loss2 - P_loss1) / P_loss1) * 100
    
    print(f"Voltage Change:       {V_change:+.2f}%")
    print(f"Current Change:       {I_change:+.2f}%")
    print(f"Loss Change:          {loss_change:+.2f}%")
    
    print("=" * 70)
    
    return V1, V2, I1, I2, P_loss1, P_loss2


if __name__ == "__main__":
    compare_cases()
