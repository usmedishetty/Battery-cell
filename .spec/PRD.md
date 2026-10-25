# Product Requirements Document (PRD)
**Document ID:** `CC-SPEC-PRD-v4.0`  
**System Name:** CellCheck PulsePod  
**Standard Compliance:** ASD-STE100, EU Battery Directive (EU 2023/1542), IEC 61960-3, IEC 62660-2  
**Target Architecture:** ESP32 Dual-Core Edge Instrument + Conformal ML Inference + W3C QR Battery Passport  

---

## 1. Executive Problem Definition & Research Index Validation

Testing retired lithium-ion cells currently creates an economic bottleneck. The certification of a single retired cell using conventional laboratory cyclers costs more than the secondary asset market value.

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FIRECRAWL RESEARCH INDEX & PRIMARY BENCHMARKS                   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Laboratory Cycler Capital Cost: $5,000 to $50,000 per bench.                         │
│    • BioLogic BCS-800 series, Maccor Series 4000, Arbin LBT: list at $1,200 to $3,500   │
│      per channel. Complete 8-to-16 channel laboratory installations cost $15,000 to    │
│      $52,000. Source: NREL Battery Testing Laboratory Baseline Study (2023).           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. Characterization Duration: 3.5 to 5.0 hours for CC-CV cycle.                        │
│    • IEC 61960-3 Clause 7.3.1 mandates 0.2C CC discharge. Standard industrial refurbish │
│      triage uses 0.5C CC discharge to 2.50V, followed by 0.5C CV recharge to 4.20V with │
│      a C/20 cutoff. Total cycle duration spans 210 to 290 minutes.                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 3. Scrap / Shred Rate: 70%+ of healthy retired cells shredded prematurely.             │
│    • Circular Energy Storage (CES) Global Recycler Report (2024): 72.4% of end-of-life │
│      and post-industrial EV cells undergo direct pyrometallurgical shredding into      │
│      "black mass" because per-cell testing costs exceed salvage margins.                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 4. Labor Cost per Cell: $25.00 to $50.00 loaded technician time.                       │
│    • Loaded labor rates for clean-room battery technicians average $25.00 to $35.00/hr. │
│      Handling, socket loading, thermal stabilizing, and chamber management total        │
│      40 to 60 minutes of active human involvement across a multi-hour cycle.           │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 5. Secondary Asset Market Realized Value: $6.00 to $12.00 per 18650/21700 cell.        │
│    • Graded 2.5 Ah to 5.0 Ah Tier-A cells resell at $6.00 to $12.00 on secondary       │
│      marketplaces (e.g., Battery Hookup, eBay Refurbished, Jag35). Shred scrap value is│
│      $0.35 to $0.50 per cell.                                                          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

The CellCheck PulsePod resolves this discrepancy. It replaces 4-hour bulk energy depletion with a deterministic 60.0-second Time-Domain Electrochemical Relaxation and Impedance Perturbation (TD-EIS) protocol on an edge instrument.

---

## 2. Goals & Non-Goals

### 2.1 Goals
1. The system shall evaluate the functional health and safety status of cylindrical lithium-ion cells within 60.0 seconds.
2. The system shall support 18650, 20700, 21700, and 26650 cylindrical mechanical form factors.
3. The system shall extract five physical parameters: bulk Ohmic resistance ($R_0$), charge-transfer resistance ($R_{\text{ct}}$), double-layer capacitance ($C_{\text{dl}}$), positive terminal crimp thermal delta ($\Delta T_{\text{IR}}$), and ultrasonic casing attenuation.
4. The system shall calculate split conformal prediction confidence intervals that achieve $\ge 95\%$ coverage on unseen cell test distributions.
5. The system shall output an offline-verifiable, cryptographically signed W3C Verifiable Credential conforming to EU Battery Regulation 2023/1542.
6. The system shall keep total bill-of-materials (BOM) cost below $\$31.00\text{ USD}$ using off-the-shelf COTS electronic components.
7. The system shall bound test-induced adiabatic cell heating under $0.05^\circ\text{C}$ throughout the 60-second test sequence for nominal cells.

### 2.2 Non-Goals
1. The system shall not predict historical cycle counts. The device measures current electrochemical health and safety properties only.
2. The system shall not identify specific cathode chemical stoichiometry (e.g., distinguishing NMC 622 from NMC 811) using transient DC pulses alone.
3. The system shall not replace legal IEC 61960-3 warranty capacity certification cycles. The device functions as a high-speed pre-certification and triage sorting instrument.
4. The system shall not charge depleted cells to full rated capacity. The instrument injects only low-current ($200\text{ mA}$) polarization pulses during Phase 3.

---

## 3. User Personas & Operational Scenarios

### Persona 1: Battery Refurbishment Operator
- **Context:** Operates in a high-throughput battery pack decommissioning and salvage workshop.
- **Goal:** Sort 1,000 to 2,000 recovered power-tool and EV cells per shift into secondary application tiers (Tier A: Stationary Storage, Tier B: Solar Reserve, Tier C: Materials Recycling).
- **Pain Points:** Incumbent cyclers create multi-day inventory delays and consume excessive facility power.
- **Required Workflow:** Insert cell into clamp $\rightarrow$ depress arcade button $\rightarrow$ observe Cole-Cole arc $\rightarrow$ apply printed thermal passport label.

### Persona 2: Warehouse Safety Compliance Officer
- **Context:** Manages bulk storage facilities containing 50,000+ retired lithium-ion battery modules awaiting qualification.
- **Goal:** Intercept latent dendrites, internal micro-shorts, and thermal runaway hazards prior to long-term storage or air/sea transport.
- **Pain Points:** Multimeters measure rest voltage but cannot detect latent internal shorts or high localized interfacial resistance.
- **Required Workflow:** Connect clip $\rightarrow$ monitor vent-cap thermal rise and acoustic damping $\rightarrow$ trigger automatic lockout if safety boundaries are exceeded.

### Persona 3: European Union Circular Economy Auditor
- **Context:** Inspects second-life battery packs sold or leased across EU jurisdictions.
- **Goal:** Verify compliance with EU Regulation 2023/1542, including state-of-health disclosures, carbon footprint offsets, and supply chain provenance.
- **Pain Points:** Paper certificates and central database links are prone to tampering, link rot, and counterfeiting.
- **Required Workflow:** Scan physical QR code with any smartphone $\rightarrow$ verify Ed25519 cryptographic signature offline via WebAssembly $\rightarrow$ review embedded electrochemical impedance curves.

---

## 4. Functional Scope

### 4.1 60-Second 4-Phase Protocol Specification
The instrument operates according to a strict four-phase timeline:

```text
  0s            5s                     10s                                    35s                                   60s
  ┌─────────────┬──────────────────────┬──────────────────────────────────────┬──────────────────────────────────────┐
  │ PHASE 0     │ PHASE 1              │ PHASE 2                              │ PHASE 3                              │
  │ Baseline &  │ Dynamic Load Pulse   │ Open-Circuit Voltage Relaxation      │ Micro-Charge Polarization            │
  │ Pre-Screen  │ & TD-EIS Chirp       │ & Ultrasonic Attenuation             │ & Passport Minting                   │
  └─────────────┴──────────────────────┴──────────────────────────────────────┴──────────────────────────────────────┘
```

1. **Phase 0: Baseline & Safety Pre-Screen ($0.0\text{ s} \le t < 5.0\text{ s}$)**
   - The analog-to-digital converter (ADC) samples open-circuit voltage ($V_{\text{ocv}}$) at $100\text{ Hz}$.
   - The infrared thermopile records baseline ambient temperature ($T_{\text{amb}}$).
   - If $V_{\text{ocv}} < 2.50\text{ V}$, the system locks out and aborts the test (copper shunting hazard).
   - If $V_{\text{ocv}} > 4.25\text{ V}$, the system locks out and aborts the test (overcharge hazard).

2. **Phase 1: Dynamic Load Pulse & TD-EIS Chirp ($5.0\text{ s} \le t < 10.0\text{ s}$)**
   - At $t = 5.000\text{ s}$, the gate driver saturates the logic-level N-MOSFET.
   - A $0.75\text{ A}$ current pulse discharges through the $5.0\Omega$ non-inductive aluminum resistor.
   - At $t = 5.020\text{ s}$, the ADC computes the instantaneous Ohmic drop ratio ($f_1$).
   - From $t = 7.000\text{ s}$ to $t = 8.500\text{ s}$, the hardware timer modulates the gate with a Pseudo-Random Binary Sequence (PRBS) multi-tone chirp ($10\text{ Hz}, 100\text{ Hz}, 1\text{ kHz}$).
   - On-chip discrete Fourier transformation computes real ($Z'$) and imaginary ($Z''$) impedance.

3. **Phase 2: Open-Circuit Voltage Relaxation & Ultrasonic Testing ($10.0\text{ s} \le t < 35.0\text{ s}$)**
   - At $t = 10.000\text{ s}$, the MOSFET turns off.
   - The ADC captures the voltage relaxation curve at $100\text{ Hz}$ across a $25.0\text{-second}$ window.
   - Non-linear least-squares fitting extracts the charge-transfer resistance ($R_{\text{ct}}$) and double-layer capacitance ($C_{\text{dl}}$).
   - The audio buzzer synthesizes the voltage relaxation into an audible frequency sweep ($300\text{ Hz}$ to $1500\text{ Hz}$).
   - A $40\text{ kHz}$ ultrasonic transmitter drives a $5\text{-cycle}$ burst across the cell diameter; the receiver measures attenuation ($f_5$).

4. **Phase 3: Micro-Charge Polarization & Passport Minting ($35.0\text{ s} \le t \le 60.0\text{ s}$)**
   - **Phase 3 Anomaly Interlock Gate:** The charge management switch enables $200\text{ mA}$ injection only if Phases 0, 1, and 2 complete with zero anomaly flags. If voltage is out of bounds, Ohmic drop exceeds $0.350\ \Omega$, vent temperature rises $> 0.8^\circ\text{C}$, or acoustic damping exceeds $20.0\text{ dB}$, firmware locks out Phase 3. The system skips micro-charge injection to prevent stimulating defect growth in compromised cells.
   - If gated PASS, the ADC computes the polarization slope ($dV/dt$) to determine active lithium acceptance ($f_7$).
   - The ML inference engine evaluates the 8-dimensional feature vector $\mathbf{x} \in \mathbb{R}^8$.
   - Conformal uncertainty bounds determine the classification tier (`TIER_A`, `TIER_B`, `TIER_C_RECYCLE`, or `RETEST`).
   - The ESP32 signs the payload with its Ed25519 hardware key and outputs the W3C QR Battery Passport.

### 4.2 Operational Containment & Safety Procedure
1. **Fireproof Bench Setup:** Operators shall position the instrument inside or on top of a non-combustible, sand-lined or vermiculite-filled catch tray.
2. **Operator Stance & PPE:** Operators must wear ANSI Z87.1 approved safety glasses and maintain a minimum safe standoff distance of 1.0 meter during active testing.
3. **Immediate Defect Quarantine:** If a cell fails pre-screen ($V_{\text{ocv}} < 2.50\text{ V}$ or $> 4.25\text{ V}$) or exhibits thermal rise ($\Delta T \ge +0.8^\circ\text{C}$):
   - The operator shall not re-arm or re-trigger the instrument.
   - The operator shall extract the cell using insulated tongs and immediately deposit it into a heavy-gauge steel quarantine bucket filled with dry coarse sand.

---

## 5. Success Metrics & Quantitative Confidence Intervals

| Metric Description | Target Threshold | Baseline Benchmark | Verification Method |
|---|---|---|---|
| **Macro-F1 Triage Agreement Rate** | $\ge 0.930$ (93.0%) | 0.81 (DC IR heuristic) | 5-fold cell-wise GroupKFold on 1,240 cycles (NASA/Oxford). |
| **Agreement 95% Confidence Interval** | $[0.908, 0.952]$ | Unbounded in literature | Wilson score interval across held-out physical cells. |
| **False-Pass Rate on Micro-Shorts** | $< 0.10\%$ | $8.5\%$ in simple DMM triage | Abusive testing of dendrite-seeded cells ($n=200$). |
| **False Reject Rate (Type I Error)** | $\le 4.5\%$ | $18.0\%$ in conservative triage | Testing pristine Samsung 25R and Panasonic B cells ($n=500$). |
| **Conformal Coverage Guarantee** | $\ge 95.0\%$ | N/A (Standard models lack coverage) | Split conformal prediction coverage on calibration set ($n=480$). |
| **Ambiguous Retest Rejection Rate** | $\le 6.0\%$ of fleet volume | $0\%$ (Incumbents force arbitrary guesses) | Ambiguous boundary cells where $|\mathcal{C}(\mathbf{x})| > 1$. |
| **Cycle Duration Determinism** | $60.0 \pm 0.2\text{ s}$ | $210\text{ to }290\text{ minutes}$ | Oscilloscope trigger measurement from button to QR output. |
| **Hardware BOM Unit Cost** | $\le \$30.10\text{ USD}$ | $\$5,000\text{ to }\$50,000$ (Lab cyclers) | Verified 1,000-unit volume COTS distributor invoices. |
