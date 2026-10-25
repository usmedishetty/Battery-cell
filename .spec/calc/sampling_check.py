#!/usr/bin/env python3
"""
CellCheck PulsePod - INA226 TD-EIS Sampling & Time-Skew Verification Script
Simulates a Randles equivalent circuit cell under INA226 conversion timing, sequential
shunt/bus time-skew, quantization, and DFT extraction.

THIS IS A NUMERICAL SIMULATION, NOT A PHYSICAL LABORATORY MEASUREMENT.
All cell equivalent circuit values are ASSUMED parameters for validation.
"""

import math
import cmath

def run_simulation():
    # -------------------------------------------------------------------------
    # 1. ASSUMED Randles Cell Equivalent Circuit Parameters
    # -------------------------------------------------------------------------
    R0 = 0.035        # Ohms (35.0 mOhm nominal Ohmic resistance) [ASSUMED]
    Rct = 0.025       # Ohms (25.0 mOhm charge-transfer resistance) [ASSUMED]
    Cdl = 1.00        # Farads (1.00 F electrical double-layer capacitance) [ASSUMED]

    # -------------------------------------------------------------------------
    # 2. Real INA226 Hardware Conversion & Bus Timing
    # -------------------------------------------------------------------------
    # Datasheet: 140 us Shunt conversion time, 140 us Bus conversion time
    # Mode: Continuous Shunt + Bus conversion
    # Case N_avg = 1: T_frame = 140 us + 140 us = 280 us -> fs = 3571.43 Hz
    # Sequential conversion skew: Bus is sampled 140 us after Shunt
    tau_skew = 140.0e-6    # Seconds (140.0 us delay between current and voltage)
    T_frame = 280.0e-6     # Seconds (280.0 us frame period)
    fs = 1.0 / T_frame     # Sampling frequency: 3571.43 Hz

    # Quantization parameters
    LSB_vbus = 0.00125     # Volts (1.25 mV/bit fixed INA226 bus voltage LSB)
    LSB_shunt = 2.5e-6     # Volts (2.5 uV/bit INA226 shunt differential LSB)
    R_shunt = 0.050        # Ohms (Vishay WSLP2512 50 mOhm current shunt)
    LSB_current = LSB_shunt / R_shunt  # Amperes (50.0 uA/bit current resolution)

    print("=" * 102)
    print("CELLCHECK PULSEPOD: TD-EIS INA226 SAMPLING & TIME-SKEW SIMULATION")
    print("NOTE: THIS IS A NUMERICAL SIMULATION, NOT A PHYSICAL MEASUREMENT.")
    print("=" * 102)
    print(f"Assumed Cell Model:     R0 = {R0*1000:.1f} mOhm, Rct = {Rct*1000:.1f} mOhm, Cdl = {Cdl:.2f} F [ASSUMED]")
    print(f"INA226 Timing (N_avg=1): T_frame = {T_frame*1e6:.1f} us (fs = {fs:.2f} Hz), Sequential Skew tau = {tau_skew*1e6:.1f} us")
    print(f"Quantization LSB:       V_bus LSB = {LSB_vbus*1000:.2f} mV, Current LSB = {LSB_current*1e6:.1f} uA")
    print("-" * 102)

    # Test frequencies to evaluate
    tones = [10.0, 100.0, 500.0, 1000.0]

    print(f"{'Tone':<8} | {'True Impedance':<20} | {'Uncorrected Meas':<22} | {'Corrected (Rotated)':<22} | {'Residual Error':<18}")
    print(f"{'(Hz)':<8} | {'Zp - j*Zpp (mOhm)':<20} | {'Zp - j*Zpp (mOhm)':<22} | {'Zp - j*Zpp (mOhm)':<22} | {'dZp, dZpp (mOhm)':<18}")
    print("-" * 102)

    for f in tones:
        omega = 2.0 * math.pi * f
        # Analytical Randles impedance: Z(s) = R0 + Rct / (1 + j*omega*Rct*Cdl)
        denom = 1.0 + 1j * omega * Rct * Cdl
        Z_true = R0 + (Rct / denom)
        z_true_re = Z_true.real * 1000.0
        z_true_im = Z_true.imag * 1000.0

        # Simulate integer number of full signal cycles for coherent DFT
        n_cycles = 10 if f >= 50.0 else 2
        duration = n_cycles / f
        N_samples = int(round(duration * fs))
        # Ensure integer number of samples
        dt = duration / N_samples

        # Excitation parameters: Square-wave current perturbation between 0 and 0.755 A
        I_dc = 0.3775
        I_peak = 0.3775

        # Discrete sample buffers
        i_sampled = []
        v_sampled = []

        for n in range(N_samples):
            t_curr = n * dt
            t_volt = t_curr + tau_skew  # Sequential time skew

            # Fourier sum of square wave harmonics (odd harmonics 1 to 29)
            i_val = I_dc
            v_drop = I_dc * (R0 + Rct)

            for k in range(1, 31, 2):
                w_k = k * omega
                if w_k > 2.0 * math.pi * 15000.0:
                    break
                # Harmonic amplitude of square wave
                I_k = (4.0 * I_peak / (math.pi * k))
                Z_k = R0 + (Rct / (1.0 + 1j * w_k * Rct * Cdl))
                mag_Z_k = abs(Z_k)
                phase_Z_k = cmath.phase(Z_k)

                i_val += I_k * math.sin(w_k * t_curr)
                v_drop += I_k * mag_Z_k * math.sin(w_k * t_volt + phase_Z_k)

            v_val = 3.800 - v_drop

            # Apply hardware quantization
            i_quant = round(i_val / LSB_current) * LSB_current
            v_quant = round(v_val / LSB_vbus) * LSB_vbus

            i_sampled.append(i_quant)
            v_sampled.append(v_quant)

        # Single-bin Discrete Fourier Transform at fundamental frequency f
        I_fourier = 0.0 + 0.0j
        V_drop_fourier = 0.0 + 0.0j

        for n in range(N_samples):
            angle = -omega * (n * dt)
            rot = cmath.exp(1j * angle)
            I_fourier += (i_sampled[n] - I_dc) * rot
            # Drop is Vocv - v_val
            V_drop_fourier += (3.800 - v_sampled[n]) * rot

        I_fourier *= (2.0 / N_samples)
        V_drop_fourier *= (2.0 / N_samples)

        Z_uncorr = V_drop_fourier / I_fourier
        z_unc_re = Z_uncorr.real * 1000.0
        z_unc_im = Z_uncorr.imag * 1000.0

        # Phase Skew Correction: rotate by +omega * tau_skew
        phase_corr = cmath.exp(1j * (omega * tau_skew))
        Z_corr = Z_uncorr * phase_corr
        z_cor_re = Z_corr.real * 1000.0
        z_cor_im = Z_corr.imag * 1000.0

        err_re = z_cor_re - z_true_re
        err_im = z_cor_im - z_true_im

        true_str = f"{z_true_re:6.2f} - j{abs(z_true_im):5.2f}"
        unc_str = f"{z_unc_re:6.2f} - j{abs(z_unc_im):5.2f}"
        cor_str = f"{z_cor_re:6.2f} - j{abs(z_cor_im):5.2f}"
        err_str = f"dZp={err_re:+5.2f}, dZpp={err_im:+5.2f}"

        print(f"{f:<8.1f} | {true_str:<20} | {unc_str:<22} | {cor_str:<22} | {err_str:<18}")

    print("-" * 102)

    # -------------------------------------------------------------------------
    # 3. Square-Wave Harmonic Aliasing Matrix (Harmonics 3 to 11)
    # -------------------------------------------------------------------------
    print("\nTABLE: Odd Harmonic Aliasing Matrix at fs = 3571.43 Hz (Nyquist = 1785.71 Hz)")
    print(f"{'Tone f0':<10} | {'Harmonic k=3':<16} | {'Harmonic k=5':<16} | {'Harmonic k=7':<16} | {'Harmonic k=9':<16} | {'Harmonic k=11':<16}")
    print("-" * 96)

    for f0 in [10.0, 100.0, 500.0, 1000.0]:
        row = [f"{f0:.0f} Hz"]
        for k in [3, 5, 7, 9, 11]:
            fk = k * f0
            # Compute alias frequency: |fk - round(fk / fs) * fs|
            m = round(fk / fs)
            f_alias = abs(fk - m * fs)
            alias_flag = " (ALIAS)" if fk > (fs / 2.0) else ""
            row.append(f"{f_alias:.1f} Hz{alias_flag}")
        print(f"{row[0]:<10} | {row[1]:<16} | {row[2]:<16} | {row[3]:<16} | {row[4]:<16} | {row[5]:<16}")

    print("-" * 96)

if __name__ == "__main__":
    run_simulation()
