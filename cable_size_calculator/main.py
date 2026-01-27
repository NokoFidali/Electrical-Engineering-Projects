import math
import tkinter as tk
from tkinter import ttk, messagebox

# LV Cables: ampacity in A, R in Ω/km, Thermal withstand (kA for 1 sec)
LV_CABLES = {
    16: {"ampacity": 76, "R": 1.15, "thermal_withstand": 5.0},
    25: {"ampacity": 101, "R": 0.727, "thermal_withstand": 7.5},
    35: {"ampacity": 125, "R": 0.524, "thermal_withstand": 10.0},
    50: {"ampacity": 150, "R": 0.387, "thermal_withstand": 13.0},
    70: {"ampacity": 195, "R": 0.268, "thermal_withstand": 18.0},
}

# MV Cables: ampacity in A, R in Ω/km, Thermal withstand (kA for 1 sec)
MV_CABLES = {
    50:  {"ampacity": 150, "R": 0.39, "thermal_withstand": 10.0},
    95:  {"ampacity": 240, "R": 0.193, "thermal_withstand": 15.0},
    185: {"ampacity": 355, "R": 0.099, "thermal_withstand": 22.0},
    300: {"ampacity": 460, "R": 0.060, "thermal_withstand": 30.0},
}

def size_cable(power_mw, voltage, pf, length_m, system_type, short_circuit_current_ka=None):
    """Calculate cable size based on ampacity, voltage drop, and thermal withstand.
    
    Args:
        power_mw: Power in MW
        voltage: Voltage in Volts
        pf: Power factor
        length_m: Cable length in meters
        system_type: "LV" or "MV"
        short_circuit_current_ka: Short-circuit current in kA (optional)
    
    Returns:
        Dict with cable specifications or error message
    """
    # Calculate operating current
    current = (power_mw * 1_000_000) / (math.sqrt(3) * voltage * pf)
    length_km = length_m / 1000

    # Select system parameters
    if system_type.upper() == "LV":
        cables = LV_CABLES
        vd_limit = 5
    else:
        cables = MV_CABLES
        vd_limit = 3

    # Cable selection loop
    for size, data in cables.items():
        # Check ampacity
        if data["ampacity"] < current:
            continue
        
        # Check voltage drop
        vd = math.sqrt(3) * current * data["R"] * length_km
        vd_percent = (vd / voltage) * 100
        
        if vd_percent > vd_limit:
            continue
        
        # Check thermal withstand if short-circuit current provided
        thermal_ok = True
        thermal_margin = None
        if short_circuit_current_ka is not None:
            thermal_withstand = data["thermal_withstand"]
            if short_circuit_current_ka > thermal_withstand:
                thermal_ok = False
            else:
                thermal_margin = round((thermal_withstand / short_circuit_current_ka) * 100 - 100, 1)
        
        if thermal_ok:
            result = {
                "System": system_type,
                "Power (MW)": power_mw,
                "Voltage (V)": voltage,
                "Operating Current (A)": round(current, 2),
                "Cable Size (mm²)": size,
                "Voltage Drop (%)": round(vd_percent, 2),
                "Thermal Withstand (kA)": data["thermal_withstand"],
            }
            
            if short_circuit_current_ka is not None:
                result["Short-Circuit Current (kA)"] = short_circuit_current_ka
                result["Thermal Margin (%)"] = thermal_margin
            
            return result

    return "❌ No suitable cable found — revise inputs or apply parallel cables"


class CableSizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cable Sizing Calculator")
        self.root.geometry("500x500")
        self.root.resizable(True, True)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
        
        # Title
        title = ttk.Label(main_frame, text="Cable Sizing Calculator", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Power input
        ttk.Label(main_frame, text="Power (MW):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.power_var = tk.DoubleVar(value=0.1)
        ttk.Entry(main_frame, textvariable=self.power_var, width=20).grid(row=1, column=1, sticky=tk.W)
        
        # Voltage input
        ttk.Label(main_frame, text="Voltage (V):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.voltage_var = tk.DoubleVar(value=10000)
        ttk.Entry(main_frame, textvariable=self.voltage_var, width=20).grid(row=2, column=1, sticky=tk.W)
        
        # Power Factor input
        ttk.Label(main_frame, text="Power Factor:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.pf_var = tk.DoubleVar(value=0.95)
        ttk.Entry(main_frame, textvariable=self.pf_var, width=20).grid(row=3, column=1, sticky=tk.W)
        
        # Length input
        ttk.Label(main_frame, text="Length (m):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.length_var = tk.DoubleVar(value=1000)
        ttk.Entry(main_frame, textvariable=self.length_var, width=20).grid(row=4, column=1, sticky=tk.W)
        
        # System Type
        ttk.Label(main_frame, text="System Type:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.system_var = tk.StringVar(value="MV")
        system_combo = ttk.Combobox(main_frame, textvariable=self.system_var, 
                                     values=["LV", "MV"], state="readonly", width=17)
        system_combo.grid(row=5, column=1, sticky=tk.W)
        
        # Short-Circuit Current input
        ttk.Label(main_frame, text="Short-Circuit Current (kA):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.sc_current_var = tk.DoubleVar(value=0)
        ttk.Entry(main_frame, textvariable=self.sc_current_var, width=20).grid(row=6, column=1, sticky=tk.W)
        ttk.Label(main_frame, text="(Leave 0 to skip)", font=("Arial", 8)).grid(row=6, column=1, sticky=tk.E, padx=5)
        
        # Calculate button
        ttk.Button(main_frame, text="Calculate", command=self.calculate).grid(row=7, column=0, columnspan=2, pady=20)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.result_text = tk.Text(results_frame, height=6, width=50, state=tk.DISABLED)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def calculate(self):
        try:
            power = self.power_var.get()
            voltage = self.voltage_var.get()
            pf = self.pf_var.get()
            length = self.length_var.get()
            system = self.system_var.get()
            sc_current = self.sc_current_var.get()
            
            # Only pass short-circuit current if > 0
            sc_current = sc_current if sc_current > 0 else None
            
            result = size_cable(power, voltage, pf, length, system, sc_current)
            
            # Display results
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            
            if isinstance(result, dict):
                self.result_text.insert(tk.END, "✓ Cable Selection Result:\n\n")
                for key, value in result.items():
                    self.result_text.insert(tk.END, f"{key}: {value}\n")
            else:
                self.result_text.insert(tk.END, result)
            
            self.result_text.config(state=tk.DISABLED)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CableSizerGUI(root)
    root.mainloop()
