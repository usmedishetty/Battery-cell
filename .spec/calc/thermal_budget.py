"""
CellCheck PulsePod - Bounded Thermal Energy Budget & Adiabatic Heating Analysis
Author: CellCheck Safety Engineering (SYZYGY Spec-Driven Layout)
Calculates test energy injection and adiabatic temperature rise across test phases.
"""

def run_analysis():
    # -------------------------------------------------------------------------
    # Physical Constants & Cell Baseline (18650 Cylindrical Cell)
    # -------------------------------------------------------------------------
    m_cell = 0.045          # Cell mass: 45.0 grams (0.045 kg)
    Cp = 830.0              # Specific heat capacity: 830 J / (kg * K)
    C_th = m_cell * Cp      # Lumped cell thermal capacitance: 37.35 J / K
    T_amb = 25.0            # Ambient reference temperature: 25.0 deg C
    # Self-heating onset threshold: SEI decomposition starts at ~80-120 deg C.
    # We take conservative lower bound T_onset = 80.0 deg C.
    T_onset = 80.0          # deg C [TO VERIFY: ARC literature range 80-120 deg C, Feng et al. 2018]
    delta_T_margin = T_onset - T_amb  # 55.0 deg C thermal headroom

    print("=" * 82)
    print("CELLCHECK PULSEPOD: BOUNDED TEST-ENERGY & ADIABATIC HEATING ANALYSIS")
    print("=" * 82)
    print(f"Cell Thermal Mass (m * Cp):    {C_th:.2f} J/degC (m = {m_cell*1000:.1f} g, Cp = {Cp:.0f} J/(kg*K))")
    print(f"Ambient Temperature (T_amb):    {T_amb:.1f} degC")
    print(f"Self-Heating Onset (T_onset):   {T_onset:.1f} degC [TO VERIFY: SEI breakdown threshold]")
    print(f"Available Headroom to Onset:    {delta_T_margin:.1f} degC")
    print("-" * 82)

    # -------------------------------------------------------------------------
    # Scenario Modeling: Phase 1 (5s Discharge Pulse) & Phase 3 (25s Micro-Charge)
    # Model: P_irrev = I * (Vocv - V_terminal) = I^2 * (R0 + Rct)
    # -------------------------------------------------------------------------
    R_load = 5.0    # Ohmite 5.0 Ohm power load resistor
    I_ch = 0.200    # Phase 3 TP4056 micro-charge current: 200 mA
    t_p1 = 5.0      # Phase 1 pulse duration: 5.0 s
    t_p3 = 25.0     # Phase 3 charge duration: 25.0 s (35s to 60s)

    scenarios = [
        # (Name, Vocv, R0, Rct)
        ("Healthy Cell (Samsung 25R)",    3.80, 0.035, 0.020),
        ("Aged Cell (70% SoH)",           3.80, 0.070, 0.050),
        ("High-R0 Degraded Cell",         3.80, 0.350, 0.150),
        ("Extreme High-Impedance Cell",   3.80, 1.000, 0.400),
    ]

    print("TABLE 1: Scenario Breakdown Across Phase 1 Discharge and Phase 3 Micro-Charge")
    print(f"{'Scenario':<28} | {'I_p1(A)':<7} | {'E_p1(J)':<8} | {'E_p3(J)':<8} | {'E_tot(J)':<8} | {'dT_core(C)':<10} | {'Margin (x)':<10}")
    print("-" * 92)

    for name, Vocv, R0, Rct in scenarios:
        I_p1 = Vocv / (R_load + R0)
        # Phase 1 heat generation
        P_p1 = (I_p1 ** 2) * (R0 + Rct)
        E_p1 = P_p1 * t_p1

        # Phase 3 heat generation (charge overpotential)
        P_p3 = (I_ch ** 2) * (R0 + Rct)
        E_p3 = P_p3 * t_p3

        E_tot = E_p1 + E_p3
        dT_core = E_tot / C_th
        margin_factor = delta_T_margin / dT_core if dT_core > 0 else 0

        print(f"{name:<28} | {I_p1:<7.3f} | {E_p1:<8.4f} | {E_p3:<8.4f} | {E_tot:<8.4f} | {dT_core:<10.5f} | {margin_factor:<10.1f}")

    print("-" * 92)

    # -------------------------------------------------------------------------
    # TABLE 2: Sensitivity Table over R0 and Current / Pulse Duration
    # -------------------------------------------------------------------------
    print("\nTABLE 2: Sensitivity Table - Phase 1 Adiabatic Core Heating dT (deg C)")
    print("Fixed R_load = 5.0 Ohm (I = 3.8V / (5.0 + R0)), overpotential factor (R0 + Rct, where Rct ~ 0.5*R0)")
    print(f"{'R0 (mOhm)':<10} | {'I_p1 (A)':<8} | {'P_p1 (W)':<8} | {'t = 2.0s':<10} | {'t = 5.0s':<10} | {'t = 10.0s':<10} | {'Orders Below Onset':<18}")
    print("-" * 88)

    r0_sweep = [0.020, 0.035, 0.050, 0.070, 0.100, 0.150, 0.250, 0.350, 0.500, 1.000]
    for r0 in r0_sweep:
        i_pulse = 3.80 / (R_load + r0)
        r_eff = r0 * 1.5  # R0 + Rct approximation
        p_p1 = (i_pulse ** 2) * r_eff
        dt_2s = (p_p1 * 2.0) / C_th
        dt_5s = (p_p1 * 5.0) / C_th
        dt_10s = (p_p1 * 10.0) / C_th
        orders_str = f"{(delta_T_margin / dt_5s):.0f}x (~{int((delta_T_margin / dt_5s)).bit_length()//3.32:.0f} orders)"
        print(f"{r0*1000:<10.1f} | {i_pulse:<8.3f} | {p_p1:<8.4f} | {dt_2s:<10.5f} | {dt_5s:<10.5f} | {dt_10s:<10.5f} | {orders_str:<18}")

    print("-" * 88)

    # -------------------------------------------------------------------------
    # TABLE 3: Current Sensitivity Matrix (Constant Current Injection, t = 5.0 s)
    # -------------------------------------------------------------------------
    print("\nTABLE 3: Constant-Current Sensitivity Matrix for 5.0 s Pulse (dT in deg C)")
    print(f"{'R_eff (R0+Rct)':<16} | {'I = 0.50 A':<12} | {'I = 0.755 A':<12} | {'I = 1.00 A':<12} | {'I = 1.50 A':<12} | {'I = 2.50 A (Fuse)':<18}")
    print("-" * 92)
    for r0 in [0.035, 0.070, 0.150, 0.350, 0.500]:
        r_eff = r0 * 1.5
        row = [f"{r_eff*1000:.1f} mOhm"]
        for curr in [0.50, 0.755, 1.00, 1.50, 2.50]:
            p = (curr ** 2) * r_eff
            dt = (p * 5.0) / C_th
            row.append(f"{dt:.5f} C")
        print(f"{row[0]:<16} | {row[1]:<12} | {row[2]:<12} | {row[3]:<12} | {row[4]:<12} | {row[5]:<18}")
    print("-" * 92)

if __name__ == '__main__':
    run_analysis()
