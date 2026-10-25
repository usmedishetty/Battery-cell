# Milestones & Verification Checklist (Tracker)
**Document ID:** `CC-SPEC-TRCK-v4.0`  
**System Name:** CellCheck PulsePod  
**Standard Compliance:** ASD-STE100, IEEE 1012-2016 (System Verification and Validation)  

---

## 1. Phased Implementation Roadmap

```text
┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│ PHASE 1: BENCH CALIBRATION      │ PHASE 2: EMBEDDED INTEGRATION   │ PHASE 3: ML RIGOR & CONFORMAL   │
│ Duration: Weeks 1 - 3           │ Duration: Weeks 4 - 6           │ Duration: Weeks 7 - 9           │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ • Build 4-wire test bench on    │ • Flash dual-core FreeRTOS tasks│ • Implement GroupKFold pipeline │
│   breadboard using COTS parts.  │   onto ESP32 hardware.          │   on NASA, Oxford, CALCE CSVs.  │
│ • Cross-validate INA226 voltage │ • Establish lock-free ring      │ • Fit monotonic XGBoost models. │
│   and current with Fluke 87V DMM│   buffer between Core 0 and 1.  │ • Calibrate conformal quantile  │
│ • Characterize Ohmite 5Ω power  │ • Calibrate MLX90614 interrupt  │   q_hat on n=480 holdout cells. │
│   load resistor thermal drift.  │   latency to < 12 µs.           │ • Build isomorphic vectorizer.  │
└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
                                                  │
                                                  ▼
                                  ┌─────────────────────────────────┐
                                  │ PHASE 4: AUDIT & CERTIFICATION  │
                                  │ Duration: Weeks 10 - 12         │
                                  ├─────────────────────────────────┤
                                  │ • Embed Ed25519 eFuse keys.     │
                                  │ • Implement offline Wasm engine.│
                                  │ • Deploy thermal label printer. │
                                  │ • Execute 500-cell blind trial. │
                                  │ • Finalize production tooling.  │
                                  └─────────────────────────────────┘
```

---

## 2. Deterministic Claim-to-Verification Acceptance Matrix

Every functional and performance claim made in the project documentation maps to a testable laboratory verification procedure:

```text
┌────┬─────────────────────────────┬───────────────────────────┬────────────────────────────────┐
│ ID │ NARRATIVE CLAIM             │ TEST PROCEDURE            │ PASS / FAIL ACCEPTANCE CRITERIA│
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V1 │ 93% Triage Agreement Rate   │ Run 5-fold cell-wise      │ Macro-F1 score ≥ 0.930. 95%    │
│    │                             │ GroupKFold cross-val on   │ Wilson confidence interval     │
│    │                             │ 1,240 cycles from NASA    │ [0.908, 0.952]. Zero cell-row  │
│    │                             │ Ames and Oxford datasets. │ leakage between train and test.│
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V2 │ 60-Second Cycle Duration    │ Measure elapsed duration  │ Test cycle duration equals     │
│    │                             │ using a digital logic     │ 60.0 ± 0.20 seconds from arcade│
│    │                             │ analyzer on GPIO18 & GPIO5│ trigger to QR render interrupt.│
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V3 │ Hardware BOM Cost < $31     │ Audit certified vendor    │ Total 1,000-unit production    │
│    │                             │ invoices from DigiKey,    │ BOM invoice price equals       │
│    │                             │ Mouser, and LCSC.         │ $30.10 USD. Zero custom ASICs. │
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V4 │ Bounded Test Energy Thermal │ Drill thermocouple well   │ Internal core temperature rise │
│    │ Rise (Core ΔT < 0.05°C)     │ into dummy cell core;     │ ΔT_core ≤ 0.050°C. Resistor    │
│    │                             │ execute 5-second pulse.   │ surface temp remains < 45.0°C. │
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V5 │ Contact Resistance          │ Insert 0.050Ω reference;  │ Extracted Ohmic resistance     │
│    │ Elimination (< 1.2 µV error)│ vary clamp contact force  │ varies by < 0.5% despite clamp │
│    │                             │ from 2.0 N to 15.0 N.     │ resistance swinging 10 to 80mΩ.│
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V6 │ Vent-Cap Thermal Plume      │ Test dendrite-shorted cell│ MLX90614 registers localized   │
│    │ Detection (< 200 ms)        │ at 500 mA load; measure   │ thermal delta (+1.2°C) in      │
│    │                             │ I2C response latency.     │ under 200 milliseconds.        │
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V7 │ Conformal Coverage          │ Test 200 physical aged    │ Conformal prediction set C(x)  │
│    │ Guarantee (≥ 95% Coverage)  │ cells against 4-hour CC-CV│ contains true benchmark health │
│    │                             │ laboratory benchmarks.    │ tier in ≥ 95.0% of cases.      │
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V8 │ Offline Wasm Verification   │ Cut external internet;    │ Smartphone browser validates   │
│    │ Without Cloud Dependency    │ scan printed thermal QR   │ Ed25519 signature and renders  │
│    │                             │ label on phone browser.   │ SVG curve in < 500 ms offline. │
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V9 │ Thermal Budget Verification │ Execute and review        │ Script outputs match Bernardi  │
│    │ Script Output               │ .spec/calc/               │ overpotential equations; core  │
│    │                             │ thermal_budget.py         │ dT remains < 0.05°C (degraded).│
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V10│ Galvanic Fuse Time-Current  │ Test Littelfuse 216 2.5A  │ Fuse clears under short-circuit│
│    │ and I^2t Response           │ (021602.5MXP) at 16A, 28A,│ faults (16A to 45A) in 1.4 ms  │
│    │                             │ and 45A fault currents.   │ to 50 ms; holds at 0.755A pulse│
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V11│ IR Emissivity Calibration   │ Calibrate MLX90614 on bare│ Temperature error ≤ 0.5°C with │
│    │ on Crimp Vent Surface       │ nickel vs matte black dot │ matte dot (ε ≥ 0.95); verifies │
│    │                             │ (ε ≥ 0.95) target.        │ low-emissivity offset fix.     │
├────┼─────────────────────────────┼───────────────────────────┼────────────────────────────────┤
│ V12│ Phase 3 Micro-Charge        │ Inject fault flags during │ GPIO27 charge enable line stays│
│    │ Anomaly Interlock Gating    │ Phases 0, 1, or 2 (Vocv,  │ LOW (0.00 mA current injected) │
│    │                             │ dV/dt, acoustic, temp).   │ when any anomaly flag is set.  │
└────┴─────────────────────────────┴───────────────────────────┴────────────────────────────────┘
```

---

## 3. Engineering Sign-Off Checklist

- [x] Phase 1 breadboard schematics verified against electrical safety derating rules.
- [x] FreeRTOS task priority hierarchy audited for priority inversion and deadlocks.
- [x] GroupKFold cross-validation scripts audited to confirm zero cell leakage.
- [x] Non-conformity score quantile function audited against textbook split conformal definitions.
- [x] W3C Verifiable Credential schema validated against EU Battery Directive 2023/1542.
- [x] Thermal label barcode dimensions verified for scanner legibility at $203\text{ DPI}$.
- [x] Thermal budget calculation script (`.spec/calc/thermal_budget.py`) reviewed and verified.
- [x] TD-EIS sampling rate, time skew rotation, and aliasing numerical simulation (`.spec/calc/sampling_check.py`) reviewed and verified.
- [ ] Galvanic fuse time-current curve and $I^2 t$ clearing characteristics bench-tested under fault loads.
- [ ] MLX90614 emissivity calibration and matte-dot target application validated.
- [ ] Phase 3 micro-charge interlock gating logic verified under fault injection testing.
- [ ] Oscilloscope verification of IRLZ44N gate drive switching waveform, slew rate, and fall times.
- [ ] Known-resistor benchmark calibration ($50\text{ m}\Omega$ and $100\text{ m}\Omega$ precision non-inductive resistors) at 10 Hz, 100 Hz, and 500 Hz.
- [ ] Sequential conversion time skew calibration ($\tau_{\text{skew}} = 140.0\ \mu\text{s}$) and phase rotation validation.

---

## 4. Open Engineering Issues & Technical Debt

```text
┌──────────┬─────────────────────────────┬────────────────────────────────────────────────────────┐
│ ISSUE ID │ TITLE                       │ TECHNICAL DESCRIPTION & RESOLUTION PLAN                │
├──────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ OPEN-01  │ INA226 ADC Nyquist Sampling │ Status: Resolved in spec - hardware verification       │
│          │ & Skew in TD-EIS Chirp      │ pending.                                               │
│          │                             │ INA226 timing re-derived: T_frame = 1120 µs (Navg=4)   │
│          │                             │ and 280 µs (Navg=1, fs = 3.57 kHz). 400 kHz I2C wire   │
│          │                             │ budget is 225 µs (94.6% load at 3.57 kHz); conversion- │
│          │                             │ ready ALERT interrupt specified; invalid I2C DMA claim │
│          │                             │ removed. Tones bounded to Option A (10, 100, 500 Hz);   │
│          │                             │ feature f3 preserved at 100 Hz; 1 kHz deferred to v2.  │
│          │                             │ Sequential skew (140 µs, 50.4 deg at 1 kHz) compensated│
│          │                             │ via Z_corr = Z_meas * exp(j*omega*tau).                │
├──────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ OPEN-02  │ INA226 Bus Voltage LSB      │ TechSpec 3.2 previously stated a bus voltage LSB of    │
│          │ Resolution Mismatch for     │ 85 µV. Per TI INA226 datasheet, bus voltage register   │
│          │ 1 mOhm Resistance Target    │ LSB is fixed at 1.25 mV (16-bit register scaling to    │
│          │                             │ 40.96 V). At I = 0.755 A, resolving 1.0 mOhm requires  │
│          │                             │ delta_V = 0.755 A * 1.0 mOhm = 755 µV, which is < 1 LSB│
│          │                             │ (effective bus resolution is 1.25 mV / 0.755 A =       │
│          │                             │ 1.66 mOhm/LSB). Section 3.1 contact resistance proof   │
│          │                             │ and Section 3.2 claims depending on 85 µV bus LSB must │
│          │                             │ be re-evaluated using shunt differential channel or    │
│          │                             │ multi-sample oversampling.                             │
├──────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ OPEN-03  │ Vishay IRF9540 P-MOSFET     │ The reverse-polarity protection P-MOSFET (IRF9540) has │
│          │ Sub-Threshold Conduction    │ its gate tied to GND. For a 3.0 V to 4.2 V 18650 cell, │
│          │ at Low Cell Voltage         │ |V_GS| is only 3.0 V to 4.2 V. The IRF9540 datasheet   │
│          │                             │ specifies V_GS(th) = -2.0 V to -4.0 V and rates        │
│          │                             │ R_DS(on) (0.20 Ohm) exclusively at V_GS = -10 V. Near  │
│          │                             │ 3.0 V cutoff, the device operates sub-threshold or     │
│          │                             │ conducts via the internal body diode (~0.7 V drop).    │
│          │                             │ Must replace with logic-level P-FET rated at -2.5 V    │
│          │                             │ V_GS (e.g., AO3401A or FDN340P).                       │
├──────────┼─────────────────────────────┼────────────────────────────────────────────────────────┤
│ OPEN-04  │ Kelvin Differential Sense   │ In README.md Section 2 ASCII schematic, the Kelvin     │
│          │ Tap Point Downstream of     │ voltage sense lead is tapped at BAT_VCC, downstream of │
│          │ Fuse & P-FET in Schematic   │ the galvanic fuse, P-MOSFET, and current shunt. Sense  │
│          │                             │ must be tapped directly at the cell terminal clamps,   │
│          │                             │ upstream of the fuse, P-MOSFET, and shunt, so that     │
│          │                             │ fuse resistance (~58 mOhm) and FET R_DS(on) do not     │
│          │                             │ distort R0 measurements. Schematic requires re-drafting│
│          │                             │ in next formal revision.                               │
└──────────┴─────────────────────────────┴────────────────────────────────────────────────────────┘
```
