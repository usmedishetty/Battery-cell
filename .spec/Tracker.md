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
│ V4 │ Zero Thermal Runaway Hazard │ Drill thermocouple well   │ Internal core temperature rise │
│    │ (Core ΔT < 0.03°C)          │ into dummy cell core;     │ ΔT_core ≤ 0.050°C. Resistor    │
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
