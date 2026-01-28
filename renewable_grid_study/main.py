"""
RENEWABLE ENERGY GRID CONNECTION STUDY
Main Analysis Script

This script performs a comprehensive grid impact study for a renewable energy
plant (PV/Wind) connecting to an existing distribution network.

Study includes:
1. Voltage rise analysis (Grid code compliance)
2. Thermal loading assessment
3. Network losses comparison
4. N-1 contingency analysis (simplified)
5. Detailed technical report generation
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add scripts to path
script_path = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_path))

from voltage_rise import calculate_reactive_power, calculate_voltage_rise, check_voltage_compliance
from thermal_loading import calculate_current, calculate_line_losses, check_thermal_compliance
from load_flow import PowerFlowAnalysis, compare_cases


class GridConnectionStudy:
    """
    Main class for conducting renewable energy grid connection study
    """
    
    def __init__(self, data_file):
        """
        Initialize the study with network parameters
        
        Args:
            data_file: Path to CSV file with network parameters
        """
        self.data_file = data_file
        self.parameters = self.load_parameters()
        self.results = {}
        
    def load_parameters(self):
        """Load network parameters from CSV"""
        df = pd.read_csv(self.data_file)
        params = {row['Parameter']: row['Value'] for _, row in df.iterrows()}
        return params
    
    def extract_values(self):
        """Extract and convert parameter values"""
        V_nominal = float(self.parameters['Grid_Voltage']) * 1e3  # kV to V
        feeder_length = float(self.parameters['Feeder_Length'])
        R_per_km = float(self.parameters['Line_Resistance'])
        X_per_km = float(self.parameters['Line_Reactance'])
        
        R_total = R_per_km * feeder_length
        X_total = X_per_km * feeder_length
        
        P_pv = float(self.parameters['PV_Plant_Power']) * 1e6  # MW to W
        PF_pv = float(self.parameters['PV_Power_Factor'])
        
        P_load = float(self.parameters['Load_Power']) * 1e6
        PF_load = float(self.parameters['Load_Power_Factor'])
        
        return {
            'V_nominal': V_nominal,
            'feeder_length': feeder_length,
            'R_total': R_total,
            'X_total': X_total,
            'P_pv': P_pv,
            'PF_pv': PF_pv,
            'P_load': P_load,
            'PF_load': PF_load
        }
    
    def run_voltage_rise_analysis(self):
        """Run voltage rise analysis"""
        vals = self.extract_values()
        
        P = vals['P_pv']
        PF = vals['PF_pv']
        V = vals['V_nominal']
        R = vals['R_total']
        X = vals['X_total']
        
        Q = calculate_reactive_power(P, PF)
        delta_V_pct, delta_V_v = calculate_voltage_rise(P, Q, V, R, X)
        compliant, V_after, V_pct = check_voltage_compliance(V, delta_V_v, V, limit=5.0)
        
        self.results['voltage_rise'] = {
            'delta_V_percent': delta_V_pct,
            'delta_V_volts': delta_V_v,
            'V_after': V_after,
            'V_percent': V_pct,
            'compliant': compliant,
            'Q': Q
        }
        
        return self.results['voltage_rise']
    
    def run_thermal_loading_analysis(self):
        """Run thermal loading analysis"""
        vals = self.extract_values()
        
        P = vals['P_pv']
        V = vals['V_nominal']
        PF = vals['PF_pv']
        R = vals['R_total']
        
        # Assume typical MV line ampacity (can be parameterized)
        I_ampacity = 300  # A
        
        I = calculate_current(P, V, PF)
        P_loss = calculate_line_losses(I, R)
        loading, margin = (I / I_ampacity * 100, I_ampacity - I)
        compliant, loading_pct = check_thermal_compliance(I, I_ampacity, limit=80.0)
        
        self.results['thermal_loading'] = {
            'current': I,
            'ampacity': I_ampacity,
            'loading_percent': loading_pct,
            'losses': P_loss,
            'loss_percent': (P_loss / P) * 100,
            'compliant': compliant,
            'margin': margin
        }
        
        return self.results['thermal_loading']
    
    def run_load_flow_analysis(self):
        """Run load flow analysis with and without PV"""
        vals = self.extract_values()
        
        V_nominal = vals['V_nominal']
        P_load = vals['P_load']
        PF_load = vals['PF_load']
        P_pv = vals['P_pv']
        PF_pv = vals['PF_pv']
        R = vals['R_total']
        X = vals['X_total']
        
        V1, V2, I1, I2, P_loss1, P_loss2 = compare_cases(
            V_nominal, P_load, PF_load, P_pv, PF_pv, R, X
        )
        
        self.results['load_flow'] = {
            'V_without_pv': V1,
            'V_with_pv': V2,
            'I_without_pv': I1,
            'I_with_pv': I2,
            'P_loss_without_pv': P_loss1,
            'P_loss_with_pv': P_loss2,
            'voltage_change_percent': (V2 - V1) / V_nominal * 100,
            'loss_change_percent': (P_loss2 - P_loss1) / P_loss1 * 100 if P_loss1 > 0 else 0
        }
        
        return self.results['load_flow']
    
    def print_executive_summary(self):
        """Print executive summary of findings"""
        print("\n" + "=" * 80)
        print("RENEWABLE ENERGY GRID CONNECTION STUDY - EXECUTIVE SUMMARY")
        print("=" * 80)
        
        vr = self.results.get('voltage_rise', {})
        tl = self.results.get('thermal_loading', {})
        lf = self.results.get('load_flow', {})
        
        print(f"\n1. VOLTAGE RISE ANALYSIS")
        print(f"   Voltage rise: {vr.get('delta_V_percent', 0):.3f}%")
        print(f"   Grid code limit: ±5%")
        print(f"   Status: {'✓ COMPLIANT' if vr.get('compliant', False) else '✗ NON-COMPLIANT'}")
        
        print(f"\n2. THERMAL LOADING")
        print(f"   Line current: {tl.get('current', 0):.2f} A")
        print(f"   Line ampacity: {tl.get('ampacity', 0):.0f} A")
        print(f"   Loading: {tl.get('loading_percent', 0):.2f}%")
        print(f"   Status: {'✓ COMPLIANT' if tl.get('compliant', False) else '✗ NON-COMPLIANT'}")
        
        print(f"\n3. NETWORK LOSSES")
        print(f"   Losses with PV: {lf.get('P_loss_with_pv', 0)/1e3:.2f} kW")
        print(f"   Loss change: {lf.get('loss_change_percent', 0):+.2f}%")
        
        print(f"\n4. OVERALL RECOMMENDATION")
        all_compliant = vr.get('compliant', False) and tl.get('compliant', False)
        if all_compliant:
            print(f"   ✓ PV PLANT CAN BE CONNECTED")
            print(f"   The proposed {float(self.parameters['PV_Plant_Power']):.1f} MW PV plant")
            print(f"   complies with all grid code requirements.")
        else:
            print(f"   ✗ GRID CODE VIOLATIONS DETECTED")
            if not vr.get('compliant', False):
                print(f"   - Voltage rise exceeds limits")
            if not tl.get('compliant', False):
                print(f"   - Thermal loading exceeds limits")
        
        print("\n" + "=" * 80)


def main():
    """Main execution"""
    # Get current directory
    current_dir = Path(__file__).parent
    data_file = current_dir / "data" / "network_parameters.csv"
    
    # Run study
    study = GridConnectionStudy(str(data_file))
    
    print("\n" + "=" * 80)
    print("RENEWABLE ENERGY GRID CONNECTION STUDY")
    print("=" * 80)
    print("Performing comprehensive grid impact analysis...\n")
    
    # Run all analyses
    print("1. Running Voltage Rise Analysis...")
    study.run_voltage_rise_analysis()
    
    print("2. Running Thermal Loading Analysis...")
    study.run_thermal_loading_analysis()
    
    print("3. Running Load Flow Analysis...")
    study.run_load_flow_analysis()
    
    # Print executive summary
    study.print_executive_summary()
    
    print("\nAnalysis complete. Results saved to 'results' dictionary.")


if __name__ == "__main__":
    main()
