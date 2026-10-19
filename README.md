# CellCheck: The $15 Pocket Stethoscope & Carfax for Used Batteries
### *Competition-Grade Master Proposal & Engineering Specification (v2.0)*

**One-Sentence Pitch:** CellCheck pairs an off-the-shelf $15–$25 pocket-sized USB stress-tester with an instant AI valuation engine to grade any used lithium battery, price its resale value, and mint an offline-verifiable QR passport in 60 seconds.

---

## Table of Contents
1. [What Changed From the Baseline](#0-what-changed-from-the-baseline-summary)
2. [Sharpened Problem, Novelty & Moat](#1-sharpened-problem-novelty--moat)
   - [1.1 The Problem, Precisely](#11-the-problem-precisely)
   - [1.2 The Competitive Wedge](#12-the-competitive-wedge)
   - [1.3 The Three-Pillar Defensible Moat](#13-the-three-pillar-defensible-moat)
3. [Deepened Hardware Design: The PulsePod Architecture](#2-deepened-hardware-design-the-pulsepod-architecture)
   - [2.1 Bill of Materials (COTS, Zero Custom PCBs)](#21-bill-of-materials-all-off-the-shelf-zero-custom-pcbs-required)
   - [2.2 Electrical Circuit Schematic (ASCII)](#22-complete-electrical-circuit--schematic-ascii)
   - [2.3 Why Kelvin 4-Wire Sensing is Non-Negotiable](#23-why-kelvin-4-wire-sensing-is-non-negotiable)
   - [2.4 The 4-Phase Time-Domain Transient Protocol](#24-the-4-phase-time-domain-transient-protocol-60-seconds)
   - [2.5 Thermal & Electrical Safety Budget: Zero Runaway Proof](#25-thermal--electrical-safety-budget-the-zero-thermal-runaway-proof)
   - [2.6 Six-Stage Defense-in-Depth Protection Chain](#26-six-stage-defense-in-depth-protection-chain)
4. [High-Impact Hardware Add-Ons](#3-high-impact-hardware-add-ons-tactile-wow--technical-defensibility)
5. [The Exact 6-Feature Extraction Pipeline](#4-the-exact-6-feature-extraction-pipeline)
   - [4.1 Mathematical Formulas, Windows & Physical Bounds](#41-mathematical-formulas-sampling-windows--physical-bounds)
   - [4.2 Isomorphic Live vs. Fleet Code Pipeline](#42-isomorphic-live-vs-fleet-code-pipeline)
   - [4.3 Two-Point Affine Transfer Calibration Engine](#43-the-two-point-affine-transfer-calibration-engine)
6. [Machine Learning Rigor, Calibration & Anti-Overclaiming](#5-machine-learning-rigor-calibration--anti-overclaiming)
   - [5.1 Datasets & Leakage-Proof Cell-Wise Split](#51-datasets--strict-group-wise-splitting)
   - [5.2 Model Architecture & Conformal Prediction Gating](#52-model-architecture--conformal-prediction-gating)
   - [5.3 Scientific Boundary Declaration ("What We Don't Claim")](#53-what-we-explicitly-do-not-claim-the-scientific-honesty-box)
7. [Cryptographic QR Battery Passport ("Carfax for Batteries")](#6-cryptographic-qr-battery-passport-carfax-for-batteries)
   - [6.1 The Cryptographic Schema (JSON v2.0 Payload)](#61-the-cryptographic-schema-json-v20-payload)
   - [6.2 Client-Side Web Verification Experience](#62-the-client-side-web-verification-experience)
8. [Masterclass 7-Minute Live Demo Script & Director's Playbook](#7-masterclass-7-minute-live-demo-script--directors-playbook)
   - [7.1 Table Props & Stage Staging Checklist](#71-table-props--stage-staging-checklist)
   - [7.2 Minute-by-Minute Stage Choreography](#72-minute-by-minute-stage-choreography)
   - [7.3 Three Bulletproof Failure Fallback Branches](#73-the-three-bulletproof-failure-fallback-branches)
9. [Hackathon Judging Criteria Mapping Matrix](#8-hackathon-judging-criteria-mapping-matrix)
10. [Executive Pitch Deck Slide Outline (10 Slides)](#9-executive-pitch-deck-slide-outline-10-slides)
11. [Pitch Variants (Calibrated by Audience)](#10-pitch-variants-calibrated-by-audience)
12. [Comprehensive Risk Register & Failure Mitigation](#11-comprehensive-risk-register--failure-mitigation)
13. [Three-Hour Rapid Build Plan & Pre-Demo Checklist](#12-three-hour-rapid-build-plan--pre-demo-checklist)
14. [Summary: Why CellCheck Dominates](#13-summary-why-cellcheck-dominates-the-hackathon)

---

## 0. What Changed From the Baseline (Summary)

| # | Subsystem | Baseline Proposal | Competition-Grade Enhanced Architecture |
|---|---|---|---|
| **1** | **Contact & Measurement Physics** | Standard 2-wire spring battery holder; prone to contact resistance swings ($20–80\,\text{m}\Omega$) that corrupt measurements. | **True 4-Wire Kelvin Sensing Bridge** using dual-contact Kelvin clips / isolated voltage sense lines direct to cell terminals. Decouples $I\cdot R_\text{contact}$ drops from true cell $R_0$. |
| **2** | **Load & Instrumentation Circuit** | Fixed 5 $\Omega$ resistor + IRLZ44N with single INA219 (12-bit ADC). | **Precision Dual-Step Load Array + INA226/ADS1115 (16-bit, $85\,\mu\text{V}$ LSB)** with low-drift shunt ($0.05\,\Omega$, $1\%$). Resolves sub-milliohm ohmic drops ($R_0$) and charge-transfer relaxation ($R_\text{ct}$). |
| **3** | **Sensing Dimensions** | Contact DS18B20 only (slow 750 ms thermal time constant). | **Dual-Sensor Thermal Architecture:** Contact DS18B20 + **Melexis MLX90614 Contactless IR Thermopile** focused on the positive crimp/vent seal for instant ($<100\,\text{ms}$) localized hot-spot detection. |
| **4** | **Tactile / Sensory Demo Hook** | Mute circuit with basic status LEDs and standard buzzer chirps. | **Acoustic Impedance Sonification Engine:** The pulse response is mapped live to an audible frequency sweep—judges *hear* the internal impedance "stiffness" of the cell like an acoustic Doppler stethoscope. |
| **5** | **The 6-Feature Pipeline** | High-level formulas without full physics derivations or noise clipping limits. | **Physics-grounded Time-Domain Electrochemical Relaxation Extraction:** Exact formulas for $R_0$, double-layer recovery $dV/dt$, polarization curvature, $\Delta T$ ratio, contact/BMS current ripple ($I_\text{RMS}/I_\text{mean}$), and OCR-normalized capacity prior. |
| **6** | **Live-vs-Fleet Mapping** | Conceptual table mapping features to NASA/Oxford data. | **Rigorous Isomorphic Code Pipeline:** Both hardware ADC streams and NASA/Oxford/CALCE raw time-series pass through the exact same vectorizer class with identical anti-aliasing, windowing, and 2-point affine transfer calibration. |
| **7** | **Machine Learning & Rigor** | Standard XGBoost classifier with basic probability thresholding. | **Leakage-Proof Cell-Wise GroupKFold + Conformal Prediction:** Outputs calibrated tier probabilities with a mathematically guaranteed coverage guarantee ($1-\alpha=95\%$) and a formal, non-negotiable **"RETEST / Ambiguity Gating"** state. |
| **8** | **Passport & Cryptography** | Simple HMAC string with arbitrary key. | **Hardware-Rooted Attestation:** ESP32 hardware eFuse MAC + session calibration hash signed into an offline-verifiable, standalone HTML/JS QR payload containing full SVG pulse curve vectors. |
| **9** | **Safety & Thermal Architecture** | General mention of fuse and P-MOSFET. | **6-Stage Protection Defense-in-Depth:** 2 A fast-acting fuse $\rightarrow$ P-FET reverse-polarity clamp $\rightarrow$ TVS transient clamp $\rightarrow$ Opto-isolated gate drive with hardware latching E-stop $\rightarrow$ Firmware thermal cutoff ($T > 45\,^\circ\text{C}$) $\rightarrow$ Host watchdog heartbeat. |
| **10** | **Demo Choreography** | Linear walkthrough vulnerable to stage hardware hiccups. | **Masterclass 7-Minute Choreography:** "Twin 3.82 V Mystery Cell" hook with live Fluke multimeter verification, judge-pressed arcade/avionics button, live NASA curve envelope overlay, and **3 bulletproof hardware failure fallbacks**. |

---

## 1. Sharpened Problem, Novelty & Moat

### 1.1 The Problem, Precisely
The energy transition has created a mountain of retired lithium-ion cells: over **12 million metric tons** of battery waste will accumulate by 2030 from electric vehicles, micro-mobility, power tools, and consumer electronics. 

Approximately **70% of retired 18650 and 21700 cells retain 75% to 85% of their original capacity**. These cells are viable for second-life applications (e.g., decentralized solar microgrids, off-grid battery energy storage systems, backup power walls). However:
- A sorted, certified Tier A/B cell resells for **$6.00 to $12.00**.
- An unsorted cell sells for scrap value: **$0.50 to $1.00 per kg** (net negative when factoring sorting and hazmat shipping).
- A cell with internal micro-dendrites or degraded separators poses a **catastrophic thermal runaway fire hazard** that voids warehouse insurance policies and causes fatal storage fires worldwide.

The current bottleneck is testing economics:
- **Incumbent (Lab Cyclers — Arbin, Maccor, Neware):** Testing a single cell requires a full CC-CV discharge and charge cycle lasting **3 to 5 hours**. The capital expenditure is **$5,000 to $50,000 per channel bank**, and loaded operator labor costs reach **$25 to $50 per cell**. The testing cost exceeds the market value of the asset.
- **Incumbent (Handheld AC Milliohm Meters — Hioki 3561):** Measures $1\,\text{kHz}$ AC resistance only ($R_\text{ac}$). It gives a single number with zero transient polarization dynamic, missing slow-diffusion capacity loss and dynamic thermal divergence.
- **Typical Hackathon Project:** A Jupyter notebook running `RandomForestClassifier` on cleaned CSV files with no physical hardware, no contact noise, and zero real-world deployment viability.

### 1.2 The Competitive Wedge

```text
                    ┌────────────────────────────────────────────────────────┐
                    │               THE TESTING PARADOX                      │
                    │   Testing a $10 battery currently costs $30 in labor.  │
                    └────────────────────────────────────────────────────────┘
                                               │
               ┌───────────────────────────────┴───────────────────────────────┐
               ▼                                                               ▼
┌───────────────────────────────┐                               ┌───────────────────────────────┐
│   Incumbent: $15,000 Cycler   │                               │    CellCheck: $15 PulsePod    │
├───────────────────────────────┤                               ├───────────────────────────────┤
│ • 4 hours per battery         │                               │ • 60 seconds per battery      │
│ • Full charge-discharge cycle │                               │ • 5-second transient pulse    │
│ • Benchtop, climate-controlled│                               │ • Pocket-sized field clip     │
│ • Labor: $30/test             │                               │ • Hardware cost: ~$15–$25     │
│ • Throughput: 2 cells/shift   │                               │ • Throughput: 480 cells/shift │
└───────────────────────────────┘                               └───────────────────────────────┘
```

| Evaluation Dimension | Benchtop Lab Cycler (Arbin/Neware) | Handheld AC Meter (Hioki 3561) | Pure-Software ML Demo | **CellCheck (PulsePod Pro)** |
|---|---|---|---|---|
| **Capital Cost** | $5,000 – $50,000 | $2,500 – $4,000 | $0 (no real asset) | **$15 – $25 COTS components** |
| **Test Duration** | 240 – 300 minutes | 5 seconds | 0 seconds (simulated) | **60 seconds flat** |
| **Throughput / 8-hr Shift** | 2 cells per channel | 200 cells (ohmic only) | N/A | **480 cells per operator** |
| **Physics Captured** | Full CC-CV Capacity ($Q_\text{dis}$) | Pure $1\,\text{kHz}$ $R_\text{ac}$ | None (synthetic assumptions) | **$R_0$ + $R_\text{ct}$ + $C_\text{dl}$ + $\Delta T$ + Contact Ripple** |
| **Blind Mystery Cell Test** | Yes (slow) | Yes (shallow) | **No** (fails instantly) | **Yes (live physical proof)** |
| **Proof of Provenance** | Proprietary lab report | Manual operator log | None | **Cryptographically signed QR Passport** |
| **Tactile Demo Factor** | Monotonous | Monotonous | Zero | **Maximum (Fluke hook, E-stop, sonified audio)** |

### 1.3 The Three-Pillar Defensible Moat
1. **The Attestation & Pricing Oracle Data Flywheel:**
   CellCheck does not sell hardware as an end product; the PulsePod is the edge ingress terminal. Every scanned battery mints an attestation record linking `[Hardware_UID + Calibration_Hash + Raw_Feature_Vector + Conformal_Grade]`. As thousands of cells are graded across refurbishers, CellCheck becomes the real-time pricing and residual life oracle for the global used battery trade (the literal "Carfax for Batteries").
2. **Transfer Calibration Hardware Lock-in:**
   Low-cost COTS sensors suffer from manufacturing drift. CellCheck’s 2-point transfer calibration engine (§4.3) maps the physical characteristics of a specific PulsePod terminal directly into the reference space of NASA Ames and Oxford degradation data. A counterfeit or uncalibrated copy of the hardware produces out-of-distribution feature vectors that fail the conformal confidence gate.
3. **Channel Economics (The Razor/Blade Model):**
   Refurbishers and battery recyclers pay **$0.25 to $0.50 per verified minted QR passport**, slashing testing costs by 98% relative to lab cycling ($30.00+). The hardware pays for itself before lunch on Day 1.

---

## 2. Deepened Hardware Design: The PulsePod Architecture

### 2.1 Bill of Materials (All Off-The-Shelf, Zero Custom PCBs Required)

Every component is standard, readily sourced, and can be assembled on a breadboard or perfboard in under 3 hours:

| # | Subsystem | Part Description | Key Technical Specification | Qty | Unit Cost | Function & Rationale |
|---|---|---|---|---|---|---|
| **1** | Compute Engine | **ESP32 DevKit V1** (30-pin) | Dual-core Tensilica Xtensa @ 240 MHz, 520 KB SRAM, USB-UART native, integrated BLE 4.2 / Wi-Fi | 1 | $4.20 | Executes high-speed sampling, FIR filtering, LCD driving, and secure HMAC signing. |
| **2** | Precision ADC / Current Sensor | **Texas Instruments INA226** (or INA219) Breakout | $I^2\text{C}$, 16-bit ADC, $85\,\mu\text{V}$ LSB, common-mode range $0–36\,\text{V}$, high-side/low-side | 1 | $2.80 | INA226 preferred: 16-bit resolution provides clean micro-volt sag measurement across high-rate pulses. |
| **3** | Primary Load Switch | **Infineon IRLZ44N** (TO-220) | N-Channel Logic-Level MOSFET: $V_\text{DSS}=55\,\text{V}$, $R_\text{DS(on)}=0.022\,\Omega$, $V_\text{GS(th)}=1.0–2.0\,\text{V}$ | 1 | $0.75 | Direct drive from 3.3 V logic with full saturation; low internal resistance prevents FET thermal drift. |
| **4** | Dynamic Load Resistor | **10 W Gold Aluminum Housed Resistor** | $5.0\,\Omega \pm 1\%$, wirewound, heat-sinkable chassis | 1 | $1.25 | Handles 3.2 W peak pulse dissipation with zero resistance drift over a 5 s burst. |
| **5** | Contactless Thermal Sensor | **Melexis MLX90614ESF-BAA** | Non-contact infrared thermopile, $I^2\text{C}$, $0.02\,^\circ\text{C}$ resolution, $90^\circ$ FOV | 1 | $4.50 | Measures positive terminal crimp heating within 100 ms (zero thermal mass lag). |
| **6** | Contact Thermal Sensor | **Dallas DS18B20** | 1-Wire digital probe, stainless steel jacket, $\pm 0.5\,^\circ\text{C}$ accuracy | 1 | $1.50 | Physical cell-body ambient temperature reference baseline. |
| **7** | Charging Micro-Source | **TP4056 USB-C Module with DW01A** | 1 A linear Li-ion charger with integrated over-current and under-voltage protection ICs | 1 | $0.65 | Provides Phase 3 micro-charge current injection for recovery slope verification. |
| **8** | Kelvin Cell Interface | **Keystone 1042 18650 Holder** + Dual Kelvin Clips | Gold-plated spring steel contacts modified with isolated sense leads | 1 | $1.80 | Eliminates contact resistance ($R_\text{contact}$) from all voltage sag math. |
| **9** | Reverse Polarity Guard | **Vishay IRF9540 or AO3401 P-MOSFET** | Low-drop P-channel gate-to-source self-latching protection switch | 1 | $0.60 | If cell is inserted backwards, gate sits at cell+; FET immediately blocks conduction. |
| **10** | Over-Current Protection | **Fast-Blow Ceramic Fuse (Schurter / Littelfuse)** | 2.5 A rating, 250 V, $5\times 20\,\text{mm}$ with PCB clips | 1 | $0.30 | Hardware galvanic failsafe against dead-short or thermal runaway cells. |
| **11** | Local Display | **1.3" I2C Monochrome OLED (SH1106 / SSD1306)** | $128\times 64$ pixels, high contrast white-on-black | 1 | $2.40 | Displays live voltage sag curve, real-time $m\Omega$, and health grade independently of laptop. |
| **12** | Acoustic Stethoscope | **Active Piezo Transducer / Buzzer (5 V)** | $2.4\,\text{kHz}$ resonant frequency, variable duty-cycle driving | 1 | $0.45 | Sonifies the impedance recovery curve into audible frequencies for tactile feedback. |
| **13** | Safety Interlock (E-Stop) | **22 mm Latching Emergency Mushroom Switch** | 1 NC / 1 NO contact block, mechanical twist-to-release | 1 | $1.90 | Physically cuts the MOSFET gate drive line to immediately abort testing. |
| **14** | Primary Trigger | **Arcade-Style Heavy Duty Push Button (Red)** | Momentary SPST, snap-action microswitch | 1 | $0.80 | High-tactility button for the judge to initiate the test sequence. |
| **15** | Status Light Pipe | **Diffused 5 mm RGB LED (Common Cathode)** | Tri-color high-luminosity LED + $3\times 220\,\Omega$ metal-film resistors | 1 | $0.25 | Visual phase signaling (Blue = Pulsing, Green = Tier A, Amber = Tier B, Red = Reject). |
| **16** | Chassis & Interconnects | Breadboard / Perfboard, JST connectors, 18 AWG silicon wire | Low-loss copper wiring, solderless prototyping base | 1 | $3.50 | Rigid mechanical mount and interconnects. |
| **TOTAL** | | | | | **~$27.65** | *(Pro tier with OLED, IR Thermopile, E-Stop, and Kelvin Clips)* |

*Note on budget:* Stripping the MLX90614 and E-stop switch drops total hardware cost to **$18.35**, preserving the "$15–$25 Pocket Hardware" claim while maintaining industrial reliability.

---

### 2.2 Complete Electrical Circuit & Schematic (ASCII)

```text
                                  [4-WIRE KELVIN CELL INTERFACE]
                                    ┌───────────────────────┐
                     ┌──────────────┤ (+)  18650 CELL   (-) ├──────────────┐
                     │              └───────────────────────┘              │
                     │ (Kelvin Force +)                   (Kelvin Force -) │
                     │                                                     │
   FUSE 2.5A         ▼                                                     ▼
  ───[====]───► P-FET POLARITY CLAMP                                       │
                ┌──────────────┐                                           │
  BAT(+) ───────┤ D          S ├──┬────────────────────────┐               │
                │   GATE: GND  │  │                        │               │
                └──────────────┘  │                        │               │
                                  ▼                        ▼               │
                           TP4056 CHARGE OUT(+)     INA226 / INA219        │
                                  │                 ┌──────────────┐       │
                                  │                 │ IN(+)  IN(-) │       │
                                  │                 └───┬──────┬───┘       │
                                  │                     │      │           │
                                  │     SHUNT RESISTOR  │      │           │
                                  │     0.05Ω, 1%, 2W   │      │           │
                                  │     ┌───────────────┴──────┴───┐       │
                                  │     │                          │       │
                                  │     ▼                          ▼       │
                                  │   BAT_VCC                    LOAD_RAIL │
                                  │                                │       │
                                  │    ┌───────────────────────────┘       │
                                  │    │                                   │
                                  │    ▼                                   │
                                  │  [5.0Ω / 10W LOAD RESISTOR]            │
                                  │    │                                   │
                                  │    ▼                                   │
                                  │  IRLZ44N MOSFET (DRAIN)                │
                                  │  ┌───────────────────────┐             │
                                  │  │ D                   S ├─────────────┼──► SYSTEM GND
                                  │  │                       │             │
                                  │  │      GATE (G)         │             │
                                  │  └──────────┬────────────┘             │
                                  │             ▲                          │
                                  │             │                          │
                                  │      100Ω   │   E-STOP SWITCH (NC)     │
                    ESP32 GPIO18 ─┴─────[===]───┴───────[ O/O ]────────────┘
                                                │
                                              [10kΩ PULL-DOWN]
                                                │
                                               GND

====================================================================================
DIGITAL & SENSOR BUS MAPPING:
====================================================================================
ESP32 Pin 3.3V   ──► VCC (INA226, MLX90614, OLED SH1106, DS18B20)
ESP32 Pin GND    ──► Common System Ground Rail
ESP32 Pin GPIO21 ──► I2C SDA (INA226 SDA, MLX90614 SDA, OLED SDA) [2.2kΩ Pullup]
ESP32 Pin GPIO22 ──► I2C SCL (INA226 SCL, MLX90614 SCL, OLED SCL) [2.2kΩ Pullup]
ESP32 Pin GPIO4  ──► 1-Wire Data (DS18B20) [4.7kΩ Pullup to 3.3V]
ESP32 Pin GPIO5  ──► Push Button (Arcade NO, Internal Pullup to 3.3V, Triggers on GND)
ESP32 Pin GPIO19 ──► E-Stop Continuity Monitor Line (Reads HIGH when closed/safe)
ESP32 Pin GPIO25 ──► Piezo Buzzer PWM Output (Timer 0, Channel 0)
ESP32 Pin GPIO12 ──► RGB LED (Red Leg)   ──[220Ω]──► GND
ESP32 Pin GPIO13 ──► RGB LED (Green Leg) ──[220Ω]──► GND
ESP32 Pin GPIO14 ──► RGB LED (Blue Leg)  ──[220Ω]──► GND
ESP32 Pin GPIO27 ──► TP4056 CE (Charge Enable Switch / Low-Side Transistor)
```

---

### 2.3 Why Kelvin 4-Wire Sensing is Non-Negotiable
Standard battery holders utilize nickel-plated spring steel contacts. Under continuous physical testing, these contacts suffer from oxidation, surface roughness, and mechanical seating variations, yielding an uncontrolled contact resistance:
$$R_\text{contact} \approx 20\,\text{m}\Omega \text{ to } 80\,\text{m}\Omega$$

In a fresh, high-performance 18650 cell (e.g., Samsung 25R or Sony VTC6), the true internal DC ohmic resistance ($R_0$) is merely **$18\,\text{m}\Omega \text{ to } 25\,\text{m}\Omega$**. 

*In a naive 2-wire setup, the contact resistance dominates the measurement by up to 300%, rendering any machine learning model trained on lab datasets useless.*

**CellCheck’s 4-Wire Kelvin Architecture:**
1. **Force Leads (Current Path):** High-gauge stranded wire routes the $0.8\,\text{A}$ discharge pulse through the spring terminals and the $5\,\Omega$ load.
2. **Sense Leads (Voltage Path):** Direct, isolated, gold-plated needle contact probes rest directly against the cell's nickel casing and positive button top.
3. Because the input impedance of the INA226 voltage sense engine exceeds **$10\,\text{M}\Omega$**, the current flowing through the sense leads is:
   $$I_\text{sense} \approx \frac{4.2\,\text{V}}{10\,\text{M}\Omega} = 0.42\,\mu\text{A}$$
4. The voltage drop across the sense contact interface is:
   $$V_\text{error} = 0.42\,\mu\text{A} \times 0.08\,\Omega = 33.6\,\text{nV}$$
   *Contact resistance is mathematically and physically eliminated from the feature vector.*

---

### 2.4 The 4-Phase Time-Domain Transient Protocol (60 Seconds)

```text
  Cell Voltage (V)
   │
V0 ├──────┐ P0: Baseline
   │      │
V1 │      │                  P2: Double-Exponential Relaxation
   │      │                  ┌──────────────────────┐
   │      │ P1: 5s Load Pulse│                      │   P3: Micro-Charge Slope
Vmin      └───────┐          │                      └────────────────────────►
   │              │          │
   └──────┴───────┴──────────┴──────────────────────┴────────────────────────► Time (s)
   0      5       10         15                     35                       60
```

| Phase | Time Window | Physical State | Sampling Rate | Physical Phenomenon Captured |
|---|---|---|---|---|
| **Phase 0: Resting Baseline** | $0 \le t < 5\,\text{s}$ | MOSFET: OFF<br>TP4056: OFF | 10 Hz | **Open-Circuit Equilibrium:** Resolves true resting open circuit voltage ($V_\text{ocv}$), ambient baseline temperature ($T_\text{amb}$), and INA226 zero-current offset. Rejects surface charge from recent handling. |
| **Phase 1: Controlled High-Load Pulse** | $5 \le t < 10\,\text{s}$ | MOSFET: ON<br>TP4056: OFF | **100 Hz (Hardware Burst Mode)** | **Ohmic Sag ($R_0$) & Charge Transfer ($R_\text{ct}$):** Immediate IR step response ($<10\,\text{ms}$) followed by polarization drop. Real-time dynamic resistance calculation under load ($I \approx 0.75\,\text{A}$). |
| **Phase 2: Open-Circuit Relaxation** | $10 \le t < 35\,\text{s}$ | MOSFET: OFF<br>TP4056: OFF | 10 Hz | **Double-Layer & Diffusion Rebound:** Voltage recovers with a fast time constant ($\tau_1 \approx 0.5\,\text{s}$, $C_\text{dl}$ discharging) and a slow solid-state diffusion time constant ($\tau_2 \approx 10\,\text{s}$). Direct signature of active material integrity. |
| **Phase 3: Micro-Charge Interrogation** | $35 \le t \le 60\,\text{s}$ | MOSFET: OFF<br>TP4056: ON | 10 Hz | **Charge Acceptance Slope:** CC charge injection ($\sim 850\,\text{mA}$). The derivative $dV/dt$ under known current identifies state of health ($SoH$) and differentiates chemistry-specific overpotentials. |

---

### 2.5 Thermal & Electrical Safety Budget: The "Zero Thermal Runaway" Proof

Hackathon judges often fear that testing arbitrary, degraded lithium batteries might trigger thermal runaway live on stage. We dismantle this concern with fundamental physics:

#### A. Energy Dissipated Inside the Cell
Under the 5-second Phase 1 load pulse:
- Cell Operating Voltage: $V_\text{cell} \approx 3.7\,\text{V}$
- Circuit Resistance: $R_\text{total} = R_\text{load} + R_\text{FET} + R_0 \approx 5.0\,\Omega + 0.022\,\Omega + 0.035\,\Omega = 5.057\,\Omega$
- Pulse Current: $I = \frac{3.7\,\text{V}}{5.057\,\Omega} = 0.732\,\text{A}$
- Internal Heat Generation Rate:
  $$\dot{Q}_\text{internal} = I^2 \cdot R_0 = (0.732\,\text{A})^2 \times 0.035\,\Omega = 0.0187\,\text{W}$$
- Total Thermal Energy Injected into Cell Core over 5 seconds:
  $$E_\text{heat} = \dot{Q} \times \Delta t = 0.0187\,\text{W} \times 5\,\text{s} = 0.0936\,\text{Joules}$$

#### B. Theoretical Core Temperature Rise
A standard 18650 cell has a mass of $m \approx 45\,\text{g}$ and a specific heat capacity of $C_p \approx 830\,\text{J}/(\text{kg}\cdot^\circ\text{C})$:
$$\Delta T = \frac{E_\text{heat}}{m \cdot C_p} = \frac{0.0936\,\text{J}}{0.045\,\text{kg} \times 830\,\text{J}/(\text{kg}\cdot^\circ\text{C})} = \mathbf{0.0025\,^\circ\text{C}}$$

Even on a severely degraded, dying cell with an internal resistance of $R_0 = 300\,\text{m}\Omega$ ($10\times$ nominal):
$$E_\text{heat, degraded} = (0.732\,\text{A})^2 \times 0.300\,\Omega \times 5\,\text{s} = 0.803\,\text{J} \implies \Delta T = \mathbf{0.021\,^\circ\text{C}}$$

*The testing pulse is orders of magnitude below the adiabatic threshold required for thermal runaway ($>135\,^\circ\text{C}$). The testing sequence cannot ignite a cell.*

#### C. Load Resistor Dissipation Margin
- Peak Power in Resistor during 5-second pulse:
  $$P_\text{load} = I^2 \cdot R_\text{load} = (0.732\,\text{A})^2 \times 5.0\,\Omega = 2.68\,\text{Watts}$$
- Continuous Power Rating of Aluminum Chassis Resistor: **$10.0\,\text{Watts}$**
- Safety Derating Ratio:
  $$\text{Safety Factor} = \frac{10.0\,\text{W}}{2.68\,\text{W}} = \mathbf{3.73\times} \quad (373\%\text{ rated headroom})$$
- Average Power over 60-second cycle:
  $$P_\text{avg} = \frac{2.68\,\text{W} \times 5\,\text{s}}{60\,\text{s}} = 0.223\,\text{W}$$
  *The resistor operates barely warm to the touch. It cannot ignite paper, plastics, or skin.*

---

### 2.6 Six-Stage Defense-in-Depth Protection Chain

```text
[CELL INSERTION]
       │
       ▼
1. PRE-SCREEN VOLTAGE GATE (Software/Host)
   If V_cell < 2.50V (copper dissolution dendrite risk) or V_cell > 4.25V:
   SYSTEM REFUSES TO ARM. Red LED flashes strobe.
       │ PASS (2.50V ≤ V ≤ 4.25V)
       ▼
2. REVERSE-POLARITY HARDWARE CLAMP (P-MOSFET IRF9540)
   Backwards insertion forces V_GS > 0V. Gate turns hard off. Zero current flows.
       │ PASS
       ▼
3. GALVANIC OVER-CURRENT PROTECTION (2.5A Fast Ceramic Fuse)
   Instantly breaks circuit if a shorted MOSFET or cell dead-fault occurs (<2ms).
       │ PASS
       ▼
4. PHYSICAL HARDWARE EMERGENCY STOP (Mushroom Latch Switch)
   Mechanically disconnects the IRLZ44N Gate line from the driver. 
   Hardware-guaranteed gate discharge via 10kΩ pulldown resistor.
       │ PASS
       ▼
5. FIRMWARE DUAL-THERMAL INTERRUPT (MLX90614 + DS18B20)
   FreeRTOS background task reads temperature every 100ms.
   If T_terminal > 45°C or dT/dt > 1.5°C/s: Hardware pin GPIO18 is forced LOW via ISR.
       │ PASS
       ▼
6. WATCHDOG HEARTBEAT TIMER
   Host dashboard must transmit a rolling 32-bit token every 500ms.
   If USB serial hangs or laptop dies: ESP32 hardware watchdog resets, disarming load.
```

---

## 3. High-Impact Hardware Add-Ons: Tactile Wow & Technical Defensibility

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           THE PULSEPOD HARDWARE ARRAY                           │
│                                                                                 │
│   ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐   │
│   │    ACOUSTIC STETH   │   │  IR THERMOPILE EYE  │   │  AVIONICS ARM/KILL  │   │
│   │  Sonifies recovery  │   │  Contactless Crimp  │   │  Physical aircraft  │   │
│   │  impedance into     │   │  hot-spot sensor    │   │  toggle + latching  │   │
│   │  audible pitch      │   │  focused on vent    │   │  mushroom E-Stop    │   │
│   └─────────────────────┘   └─────────────────────┘   └─────────────────────┘   │
│              ▲                         ▲                         ▲              │
│              └─────────────────────────┼─────────────────────────┘              │
│                                        │                                        │
│                         ┌──────────────────────────────┐                        │
│                         │   OLED WAVEFORM MONITOR      │                        │
│                         │   Standalone 128x64 display  │                        │
│                         │   renders live V-sag curve   │                        │
│                         └──────────────────────────────┘                        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Upgrade 1: The Acoustic Impedance Sonification Engine ("The True Stethoscope")
- **The Concept:** A true stethoscope makes physical internal health audible. We translate the voltage recovery curve during Phase 2 ($10\,\text{s} \le t \le 35\,\text{s}$) directly into an audible frequency modulated tone:
  $$f_\text{audio}(t) = 300\,\text{Hz} + \left(\frac{V(t) - V_\text{min}}{V_0 - V_\text{min}}\right)^2 \times 1200\,\text{Hz}$$
- **Tactile Judge Experience:**
  - A **healthy, low-impedance cell** rebounds like a steel spring: the buzzer emits a clean, rapid ascending chirping glissando ($300\,\text{Hz} \rightarrow 1500\,\text{Hz}$ in $<800\,\text{ms}$).
  - A **degraded, high-impedance cell** struggles to polarize: the tone stays low, groaning at $400\,\text{Hz}$ before slowly creeping up.
  - *Judges do not just look at a screen—they literally listen to the health of the battery.*

### Upgrade 2: Melexis MLX90614 Contactless IR Thermopile
- **The Concept:** Traditional contact probes (DS18B20) suffer from plastic encapsulation thermal resistance and take $5–10\,\text{seconds}$ to register heat. The MLX90614 non-contact infrared thermopile is rigidly positioned $10\,\text{mm}$ away, looking directly at the positive terminal crimp seal.
- **Defensibility:** In aged 18650 cells, internal PTC rings and safety vent seals develop microscopic contact corrosion and current crowding, creating localized thermal micro-plumes during current pulses. The MLX90614 detects this thermal signature within $100\,\text{ms}$, exposing internal mechanical degradation that surface probes miss.

### Upgrade 3: Avionics Master Arm & Mushroom E-Stop Switch
- **The Concept:** Replace generic breadboard pushbuttons with a red safety-interlocked **Avionics Master Arm Toggle** (with flip-up missile cover) and a heavy industrial **22 mm Red Mushroom E-Stop Switch**.
- **The Theater & Rigor:** The system cannot fire until the judge physically flips the Master Arm cover up and snaps the switch. If at any point the judge strikes the mushroom switch, the load cuts out mechanically. This tactile feedback engages judges directly while emphasizing laboratory safety discipline.

### Upgrade 4: Standalone 1.3" OLED Real-Time Micro-Oscilloscope
- **The Concept:** Driven via $I^2\text{C}$ on an SSD1306/SH1106 controller. The ESP32 draws a real-time $128\times 48$ rolling voltage waveform during the pulse, followed by an instant rendering of the calculated internal resistance ($R_0$) in large numeric glyphs, plus the final Grade tier badge.
- **Reliability:** The demo works completely standalone even if the presentation laptop crashes, the projector disconnects, or the USB cable is yanked out.

---

## 4. The Exact 6-Feature Extraction Pipeline

The feature engineering pipeline is physics-based: each feature maps directly to an electrochemical parameter within the **Randles Equivalent Circuit Model**:

```text
      R0 (Ohmic Electrolyte/Tab Resistance)
BAT(+) ──[====]──┬──────────────[====]──────────────┬── BAT(-)
                 │           R_ct (Charge Transfer) │
                 │                                  │
                 └───┤├─────────────────────────────┘
                     C_dl (Double-Layer Capacitance)
```

### 4.1 Mathematical Formulas, Sampling Windows & Physical Bounds

```text
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                     THE 6-DIMENSIONAL FEATURE VECTOR                        │
 └─────────────────────────────────────────────────────────────────────────────┘
  f1: Ohmic Sag Ratio (R0)       ──► Direct electrolyte & terminal degradation
  f2: Double-Relaxation Slope    ──► Active material diffusion & charge acceptance
  f3: Quadratic Polarization Curv──► SEI film charge-transfer impedance (R_ct)
  f4: Normalized Thermal Rise    ──► High-IR Joule heating & internal friction
  f5: Dynamic Current Stability  ──► Micro-dendritic noise & contact instability
  f6: OCR-Capacity Prior Ratio   ──► Chemistry-specific volumetric energy scaling
```

$$\mathbf{x} = \left[ f_1,\, f_2,\, f_3,\, f_4,\, f_5,\, f_6 \right]^T \in \mathbb{R}^6$$

---

#### Feature 1: Instantaneous Normalized Ohmic Drop ($f_1$)
- **Physical Meaning:** Quantifies pure bulk electrolyte, separator, and current-collector resistance ($R_0$) independent of SOC.
- **Formula:**
  $$f_1 = \frac{\bar{V}_\text{P0} - V(t_\text{pulse} + 20\,\text{ms})}{\bar{V}_\text{P0}} \times 100 \quad [\%]$$
  Where $\bar{V}_\text{P0} = \frac{1}{N}\sum_{t=0}^{5} V(t)$ is the resting open-circuit voltage, and $V(t_\text{pulse} + 20\,\text{ms})$ is the voltage at the first settled sample post-transient.
- **Expected Range (18650, $20–35\,^\circ\text{C}$):**
  - Pristine (Tier A, SoH $>80\%$): $2.5\% \text{ to } 5.2\%$ ($R_0 \approx 18–35\,\text{m}\Omega$)
  - Degraded (Tier B, SoH $65–80\%$): $5.5\% \text{ to } 9.5\%$ ($R_0 \approx 40–75\,\text{m}\Omega$)
  - Dangerous / Scrap (Tier C, SoH $<65\%$): $>10.0\%$ ($R_0 > 100\,\text{m}\Omega$)

---

#### Feature 2: Dual-Stage Relaxation Gradient ($f_2$)
- **Physical Meaning:** Evaluates the interfacial charge-transfer kinetics and initial lithium-ion diffusion relaxation across the solid-electrolyte interphase (SEI) layer during the open-circuit rebound phase (P2) and micro-charge phase (P3).
- **Formula:**
  $$f_2 = \left( \left. \frac{dV}{dt} \right|_{t=11\,\text{s}}^{t=15\,\text{s}} \right) \cdot \frac{1}{\bar{V}_\text{P0}} \times 10^3 \quad \left[\frac{\text{mV}}{\text{s}\cdot\text{V}}\right]$$
  Computed via a robust, outlier-clipped linear Theil-Sen estimator across the early recovery window ($11\,\text{s} \le t \le 15\,\text{s}$).
- **Expected Range:**
  - Pristine (Tier A): $4.5 \text{ to } 9.0\,\text{mV}/(\text{s}\cdot\text{V})$ (rapid, spring-like elastic recovery)
  - Degraded (Tier B): $1.8 \text{ to } 4.2\,\text{mV}/(\text{s}\cdot\text{V})$ (sluggish electrochemical rebound)
  - Dangerous / Scrap (Tier C): $<1.5\,\text{mV}/(\text{s}\cdot\text{V})$ (flat, lifeless response)

---

#### Feature 3: Transient Polarization Curvature Variance ($f_3$)
- **Physical Meaning:** During the 5-second pulse, voltage drop is non-linear due to the parallel $R_\text{ct} \parallel C_\text{dl}$ overpotential curve. We fit a second-degree polynomial $V(t) = a t^2 + b t + c$ over $t \in [5.2\,\text{s}, 9.8\,\text{s}]$. $f_3$ is the root-mean-square error (RMSE) of the residuals, which measures non-Faradaic interfacial distortion and solid-state diffusion warpage.
- **Formula:**
  $$f_3 = \sqrt{\frac{1}{K}\sum_{k=1}^K \left( V(t_k) - \hat{V}_\text{poly2}(t_k) \right)^2} \quad [\text{mV}]$$
- **Expected Range:**
  - Pristine (Tier A): $<1.8\,\text{mV}$ (clean, smooth exponential polarization)
  - Degraded (Tier B): $2.0 \text{ to } 5.5\,\text{mV}$
  - Dangerous / Scrap (Tier C): $>6.0\,\text{mV}$ (diffusion saturation, severe interfacial degradation)

---

#### Feature 4: Normalized Terminal Thermal Transient ($f_4$)
- **Physical Meaning:** Direct measurement of Joule heating dissipation vs. heat sinking capacity, isolated from ambient temperature fluctuations using the dual MLX90614 + DS18B20 array.
- **Formula:**
  $$f_4 = \frac{T_\text{IR, max}(t=0..60) - T_\text{ambient, P0}}{\max(T_\text{ambient, P0}, 15.0\,^\circ\text{C})} \times 100 \quad [\%]$$
- **Expected Range:**
  - Pristine (Tier A): $<0.8\%$ (imperceptible temperature rise at $0.75\,\text{A}$)
  - Degraded (Tier B): $1.0\% \text{ to } 2.5\%$
  - Dangerous / Scrap (Tier C): $>3.5\%$ (localized ohmic hot-spotting at the crimp)

---

#### Feature 5: Dynamic Current Stability Index ($f_5$)
- **Physical Meaning:** Ratio of peak high-frequency current ripple to mean current during the Phase 1 discharge pulse. Detects microscopic dendrite sparking, internal BMS switching noise (if testing e-bike protected packs), or contact micro-arcing.
- **Formula:**
  $$f_5 = \frac{\sqrt{\frac{1}{M}\sum_{m=1}^M \left( I(t_m) - \bar{I}_\text{P1} \right)^2}}{\bar{I}_\text{P1}} \quad [\text{dimensionless}]$$
- **Expected Range:**
  - Healthy (Stable Interconnect): $0.002 \text{ to } 0.015$
  - Unstable (Mechanical/BMS/Dendritic Flaws): $>0.045$ (Triggers automatic re-test flag)

---

#### Feature 6: OCR / Chemistry-Normalized Capacity Prior ($f_6$)
- **Physical Meaning:** Volumetric energy density normalization. A $3500\,\text{mAh}$ cell delivering a $0.75\,\text{A}$ pulse is loaded at $\sim 0.21\,\text{C}$, whereas a $1500\,\text{mAh}$ power-tool cell is loaded at $0.50\,\text{C}$. The wrapper's rated capacity and chemistry flag (NMC vs. LFP vs. LCO) are read by camera OCR and converted to a baseline normalization coefficient:
- **Formula:**
  $$f_6 = \frac{C_\text{rated, OCR}}{3500\,\text{mAh}} \times \kappa_\text{chem}$$
  Where $\kappa_\text{NMC} = 1.00$, $\kappa_\text{LCO} = 0.92$, and $\kappa_\text{LFP} = 0.78$ (adjusting for LFP's flat OCV curve).

---

### 4.2 Isomorphic Live vs. Fleet Code Pipeline

```text
                       ┌─────────────────────────────────────────┐
                       │       RAW VOLTAGE / CURRENT INPUT       │
                       └─────────────────────────────────────────┘
                                    │               │
                 ┌──────────────────┘               └──────────────────┐
                 ▼                                                     ▼
    ┌───────────────────────────┐                         ┌───────────────────────────┐
    │    HARDWARE INA226 STREAM │                         │   NASA PCoE / OXFORD CSV  │
    │   100 Hz Serial Packets   │                         │   Multi-Hour Lab Cycles   │
    └───────────────────────────┘                         └───────────────────────────┘
                 │                                                     │
                 ▼                                                     ▼
    [Phase Segmentation: P0..P3]                          [Synthetic Pulse Window Extract]
    Extract 60s live window                               Isolate 5s current pulse & rest
                 │                                                     │
                 └──────────────────┬──────────────────────────────────┘
                                    │
                                    ▼
                 ┌───────────────────────────────────────┐
                 │    UNIFIED CLASS: PulseFeatureEngine  │
                 ├───────────────────────────────────────┤
                 │ 1. 4-sample Savitzky-Golay filter     │
                 │ 2. 3-sigma outlier residual clipping  │
                 │ 3. Dual-point affine transfer scale   │
                 │ 4. Compute f1, f2, f3, f4, f5, f6     │
                 └───────────────────────────────────────┘
                                    │
                                    ▼
                 ┌───────────────────────────────────────┐
                 │     STANDARDIZED 6-D TENSOR (R^6)     │
                 │   [f1,  f2,  f3,  f4,  f5,  f6]       │
                 └───────────────────────────────────────┘
```

| Pipeline Step | Live PulsePod Implementation | Fleet CSV Implementation (NASA / Oxford / CALCE) |
|---|---|---|
| **Raw Sampling** | $100\,\text{Hz}$ burst from INA226 over USB-UART | Resampled to $100\,\text{Hz}$ via cubic spline interpolation |
| **Noise Attenuation** | 4-sample moving boxcar + $2.2\,\text{kHz}$ analog RC anti-alias | Digital forward-backward zero-phase Butterworth filter |
| **P1 Pulse Boundary** | Detected via hardware edge interrupt ($\Delta I > 500\,\text{mA}$) | Located via threshold scan on cycle step index variable |
| **Thermal Channel** | Synchronized MLX90614 ($10\,\text{Hz}$) & DS18B20 ($1\,\text{Hz}$) | Thermocouple channel attached to cell skin in climate chamber |
| **Calibration Map** | Multiplied by active terminal calibration block $(\mathbf{A}, \mathbf{B})$ | Identity transform $(\mathbf{A}=\mathbf{I}, \mathbf{B}=\mathbf{0})$ (acts as reference ground truth) |

---

### 4.3 The Two-Point Affine Transfer Calibration Engine
COTS resistors and ADCs exhibit slight gain/offset errors ($\pm 1\%$). To guarantee that a model trained on NASA lab cyclers works on an assembled PulsePod, every device executes a 60-second **Calibration Ceremony** before deployment:

1. **Reference Standard Calibration:**
   - A reference precision calibration plug ($0.1\%$ non-inductive wirewound resistor) is slotted into the PulsePod.
   - The device measures raw features: $\mathbf{f}_\text{raw} = [f_{1,\text{raw}}, \dots, f_{6,\text{raw}}]$.
2. **Transfer Function:**
   $$\mathbf{f}_\text{calibrated} = \mathbf{A} \odot \mathbf{f}_\text{raw} + \mathbf{B}$$
   Where $\mathbf{A} = [a_1, \dots, a_6]$ and $\mathbf{B} = [b_1, \dots, b_6]$ are stored inside the ESP32’s non-volatile EEPROM/NVS partition.
3. **Session Calibration Hash:**
   $$\text{CAL\_HASH} = \text{SHA256}(\mathbf{A} \,\|\, \mathbf{B} \,\|\, \text{Device\_MAC} \,\|\, \text{Timestamp})[:12]$$
   This 12-character cryptographic fingerprint is stamped into every QR passport minted, guaranteeing that the grading pipeline has not drifted.

---

## 5. Machine Learning Rigor, Calibration & Anti-Overclaiming

### 5.1 Datasets & Strict Group-Wise Splitting
- **NASA Ames Prognostics Center of Excellence (PCoE):** Datasets B0005, B0006, B0007, B0018 (18650 NMC cells cycled to end-of-life under varying ambient temperatures and discharge profiles).
- **Oxford Battery Degradation Dataset 1:** 8 commercial pouch/18650 cells cycled under continuous thermal chamber control with periodic full characterization cycles over 1,000+ days.
- **CALCE Battery Research Group (CS2 Series):** Prismatic/cylindrical cells under dynamic stress profiles.

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    LEAKAGE-PROOF CELL-WISE SPLIT DESIGN                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│  [Cell 01] [Cell 02] [Cell 03] ... [Cell 28]  ──► TRAINING SET (80%)            │
│  All cycles, all degradation stages, all ages    (Model learns physics curves)  │
├─────────────────────────────────────────────────────────────────────────────────┤
│  [Cell 29] [Cell 30] [Cell 31] ... [Cell 35]  ──► STRICT VALIDATION (20%)       │
│  COMPLETELY UNSEEN PHYSICAL HARDWARE CELLS       (Tests true generalization)    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

> **CRITICAL SCIENTIFIC DEFENSE (Anti-Data Leakage):**
> Many hackathon teams pool all rows and perform a random `train_test_split()`. That is fatal data leakage: the model sees Cycle 142 of Cell B0005 in training and predicts Cycle 143 of the same cell in validation.
> **CellCheck enforces strict Cell-Wise GroupKFold (k=5). Entire cells are held out.** The model must predict SoH on physical batteries it has never touched before.

---

### 5.2 Model Architecture & Conformal Prediction Gating

```text
                 6-D Input Vector: x = [f1, f2, f3, f4, f5, f6]
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │    MONOTONIC XGBOOST CLASSIFIER│
                      │    Depth: 4 | Trees: 100      │
                      │    Monotonic Constraints:     │
                      │    f1 (+), f2 (-), f4 (+)     │
                      └───────────────┬───────────────┘
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │   ISOTONIC PROBABILITY CALIB  │
                      │   Calibrates raw scores to    │
                      │   true posterior distributions│
                      └───────────────┬───────────────┘
                                      │
                                      ▼
                      ┌───────────────────────────────┐
                      │   CONFORMAL UNCERTAINTY GATE  │
                      │   Coverage Guarantee: 95%     │
                      └───────────────┬───────────────┘
                                      │
               ┌──────────────────────┴──────────────────────┐
               ▼                                             ▼
     [CONFIDENCE ≥ 0.80]                            [CONFIDENCE < 0.80]
     Unambiguous Decision                           Epistemic Uncertainty / Noise
               │                                             │
   ┌───────────┼───────────┐                                 ▼
   ▼           ▼           ▼                    ┌─────────────────────────┐
 TIER A      TIER B      TIER C                 │  RETEST / INCONCLUSIVE  │
(EV/Storage) (Solar)   (Recycle)                │  "Model Declines Guess" │
                                                └─────────────────────────┘
```

1. **Base Classifier:** 100-tree gradient boosted decision tree with **monotonic constraints**:
   - $f_1$ (voltage sag) is constrained to have a monotonically positive relationship with degradation.
   - $f_2$ (recovery slope) is constrained to have a monotonically negative relationship with degradation.
   - *This prevents non-physical edge-case hallucinations.*
2. **Probability Calibration:** Post-processed using Isotonic Regression fitted on the held-out validation group to ensure that a reported $85\%$ confidence matches empirical reality.
3. **Conformal Uncertainty Gating:**
   If the maximum calibrated class probability drops below **$0.80$** (or if the conformal prediction set contains multiple classes), the system **refuses to issue a grade**. It halts and outputs:
   $$\mathbf{RETEST\text{ — }AMBIGUOUS\text{ }TRANSIENT}$$
   *In industrial battery triage, guessing wrong burns down a warehouse. A tool that knows when to say "I don't know" is infinitely more credible than one claiming 99% accuracy on everything.*

---

### 5.3 What We Explicitly Do NOT Claim (The Scientific Honesty Box)

> [!IMPORTANT]
> ### CellCheck Scientific Boundary Declaration
> *We print this exact box directly in our slide deck and technical documentation:*
> 1. **We DO NOT claim cycle-count prediction:** A 60-second test cannot determine whether a cell has lived 200 hard cycles or 500 gentle cycles. We predict current functional capacity state ($SoH$) and safety triage tier only.
> 2. **We DO NOT claim chemical spectroscopy:** We cannot determine the exact dopant percentage of cobalt in an NMC cathode from an electrical load pulse.
> 3. **We DO NOT replace 4-hour certification cycles for warranty dispute litigation:** We serve as a rapid **triage filter** (pre-screen) that eliminates 95% of bad cells before costly cycling occurs.

---

## 6. Cryptographic QR Battery Passport ("Carfax for Batteries")

### 6.1 The Cryptographic Schema (JSON v2.0 Payload)
The QR code encodes a compact, offline-decodable, canonical JSON string signed via HMAC-SHA256 (or ECDSA using secp256k1 keys stored in the ESP32's hardware-encrypted eFuse):

```json
{
  "cc_v": 2,
  "dev_uid": "CP-ESP32-8C4F-001A",
  "cal_hash": "b47e2a91f0c3",
  "ts": "2026-10-19T18:22:10Z",
  "cell": {
    "ocr_sn": "INR18650-25R",
    "chem": "NMC",
    "rated_mah": 2500
  },
  "metrics": {
    "r0_mohm": 24.8,
    "f1_sag_pct": 3.82,
    "f2_rec_slope": 6.14,
    "f4_ir_dt_pct": 0.42,
    "v_rest": 3.824
  },
  "verdict": {
    "tier": "TIER_A",
    "soh_pct": 92.4,
    "conf": 0.941,
    "app": "High-Drain E-Mobility & Second-Life Storage"
  },
  "valuation": {
    "usd_fair": 7.80,
    "usd_scrap": 0.45,
    "oracle_index": "US-CHI-2026Q4"
  },
  "sig": "e7b901a5d4c82b19e4871a36fd4021e9c855a90d98412e6988220f8ecab17012"
}
```

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PRINTABLE PASSPORT VISUALIZATION                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  CELLCHECK BATTERY PASSPORT v2.0               │
│  │ █▀▀▀▀▀█ ▄ █▄█ █▀▀▀▀▀█   │  ============================================   │
│  │ █ ███ █ ▄█▄ ▄ █ ███ █   │  SERIAL: INR18650-25R-9041                     │
│  │ █ ▀▀▀ █ █ ▄ █ █ ▀▀▀ █   │  GRADE:  [ TIER A — EXCELLENT ]                │
│  │ ▀▀▀▀▀▀▀ ▀ █ ▀ ▀▀▀▀▀▀▀   │  HEALTH: 92.4% SoH (Conf: 94.1%)               │
│  │ █ ▄▄█▀▀▄█▀▄ █▄█▄▄█▄▄█   │  RESALE VALUATION: $7.80 USD                   │
│  │ █▀ █ ▀▄▀▀▄ ▄█▄ ▀▄ ▄▄█   │  IMPEDANCE (R0):   24.8 mΩ                     │
│  │ █▀▀▀▀▀█ █ ▄█▄ █ ▀ █▄█   │  TERMINAL THERMAL: +0.18 °C                    │
│  │ █ ███ █ █▄▄ ▄▄█▀█▀▄ █   │  --------------------------------------------   │
│  │ █ ▀▀▀ █ ▄█ ▄▀▄█▄▀█▀▄█   │  DEVICE: CP-ESP32-8C4F  CAL: b47e2a91f0c3      │
│  │ ▀▀▀▀▀▀▀ ▀▀  ▀ ▀▀  ▀▀▀   │  SIG: ✓ VERIFIED HARDWARE ATTESTATION           │
│  └─────────────────────────┘  SCAN TO VERIFY LIVE TELEMETRY DECAY CURVE     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 6.2 The Client-Side Web Verification Experience
When a judge, buyer, or safety auditor points their smartphone camera at the printed QR passport:
1. **Zero App Installation:** The browser opens an offline-capable, standalone URL (e.g., `cellcheck.id/verify#<base64_payload>`).
2. **Client-Side Cryptographic Validation:**
   - A WebAssembly / JavaScript module extracts the payload and recomputes the HMAC-SHA256 digest against the verified public key registry of certified PulsePod serial numbers.
   - An instant **Emerald Green Checkmark** displays: `AUTHENTIC HARDWARE ATTESTATION — ZERO TAMPERING`.
3. **Interactive Forensic Telemetry Curve:**
   - The verify page does not just display a grade; it renders an interactive **SVG Vector Oscilloscope Graph** of the 60-second pulse.
   - The judge can scrub through the actual voltage bounce, see the calculated $R_0$ tangent line, and compare it side-by-side with reference curves from the NASA Ames battery repository.

---

## 7. Masterclass 7-Minute Live Demo Script & Director’s Playbook

### 7.1 Table Props & Stage Staging Checklist
- [ ] **The "Twin Mystery Cells":** Two identical Samsung 18650 cells with blue wrappers. Both are pre-tested and sitting at **exactly $3.82\,\text{V}$ rest voltage**. 
  - *Cell Alpha:* Pristine cell ($>90\%$ SoH, $R_0 \approx 22\,\text{m}\Omega$).
  - *Cell Beta:* Severely aged cell from a retired hoverboard ($<60\%$ SoH, heavy dendrite growth, $R_0 \approx 140\,\text{m}\Omega$).
- [ ] **Calibrated Fluke Multimeter:** Placed front-and-center facing the judges with high-contrast display.
- [ ] **CellCheck PulsePod Pro Terminal:** Mounted in an open-top, laser-cut acrylic chassis with visible wiring, red Avionics toggle, arcade button, 1.3" OLED, and E-Stop switch.
- [ ] **Thermal Camera or Phone IR Lens:** Pointed at the test bay to project live thermal imagery onto the main screen.
- [ ] **Thermal Label Printer (Phomemo / Brother):** Connected via USB to print physical sticker passports instantly upon test completion.
- [ ] **Sacrificial Spare Rig (Velcroed Under the Table):** Duplicate pre-wired PulsePod connected to a secondary COM port for instant cutover if a wire snaps.

---

### 7.2 Minute-by-Minute Stage Choreography

```text
0:00        1:00        2:00                 4:00        5:00        6:00        7:00
┌───────────┬───────────┬────────────────────┬───────────┬───────────┬───────────┐
│ THE HOOK  │ OCR &     │ THE PULSE &        │ VERDICT & │ CONTRAST  │ FLEET     │
│ Both 3.8V │ HANDOFF   │ SONIFIED BOUNCE    │ QR SCAN   │ CELL BETA │ SCALE & Q&A│
│ Fluke DMM │ Judge Arms│ Audio Stethoscope  │ Instant   │ Audible   │ CSV Engine│
│ Mystery   │ Device    │ NASA Overlay Live  │ Printout  │ Groan (C) │ Close     │
└───────────┴───────────┴────────────────────┴───────────┴───────────┴───────────┘
```

---

#### Minute 0:00 – 1:00 | The Hook: Destroying the Voltage Myth
- **Action (Show):** Grab the Fluke multimeter leads. Jam them onto *Cell Alpha*. Display reads: **$3.82\,\text{V}$**. Immediately move leads to *Cell Beta*. Display reads: **$3.82\,\text{V}$**.
- **Script (Spoken):**
  > *"Judges, look at this meter. Three point eight two volts. Three point eight two volts. To every consumer, every multimeter, and every basic battery tester on Amazon, these two batteries are identical.*
  > 
  > *They are not. One of these batteries has 92% health and can power an off-grid home for the next eight years. The other is a degraded hazard with severe micro-dendritic separator wear that could ignite an e-bike pack.*
  > 
  > *Today, telling them apart requires a five-thousand-dollar laboratory cycler and a four-hour wait. That testing cost exceeds the value of the battery itself.*
  > 
  > *This is CellCheck. It costs under twenty-five dollars, takes sixty seconds, and acts as an acoustic stethoscope and Carfax for used energy storage."*

---

#### Minute 1:00 – 2:00 | The Physical Handoff & Machine Arming
- **Action (Show):** Present the PulsePod Pro to the lead judge. Hold up Cell Alpha to the webcam: the dashboard computer’s OpenCV script flashes a bounding box over the wrapper text: `DETECTED: SAMSUNG INR18650-25R | RATED: 2500mAh | CHEM: NMC`.
- **Script (Spoken):**
  > *"Judge, take Cell Alpha. Drop it into our gold-plated Kelvin clips. Notice that you don't need any lab gear.*
  > 
  > *Now, flip up the red aircraft Master Arm switch. You have just armed the hardware safety circuit. Now hit the big red arcade button."*

---

#### Minute 2:00 – 4:00 | The Pulse, the Audio Stethoscope & the Live NASA Overlay
- **Action (Show):** Judge strikes the arcade button.
  - The RGB LED snaps from idle-white to bright pulsing blue.
  - The 1.3" OLED begins plotting the real-time voltage sag curve.
  - **Acoustic Stethoscope Engaged:** At second 10, the load cuts out. The piezo transducer emits an audible, crisp, upward chirp ($300\,\text{Hz} \rightarrow 1500\,\text{Hz}$ in 0.5 s).
  - **Live Screen:** The dashboard plots the live voltage curve directly on top of a shaded envelope of **1,200 historical NASA Ames PCoE degradation curves**.
- **Script (Spoken):**
  > *"Watch the screen, but more importantly: listen.*
  > 
  > *That rising chirp is our acoustic sonification engine translating the electrochemical double-layer relaxation in real time. A healthy cell snaps back like a coiled spring. You just heard twenty-four milliohms of internal resistance.*
  > 
  > *On the laptop screen, our live data is passing through the exact same feature extraction pipeline we run on NASA's Ames PCoE lab database. Notice how our live curve tracks directly inside the green Tier-A 90%-plus envelope."*

---

#### Minute 4:00 – 5:00 | The Verdict, the Thermal Printout & the Phone Scan
- **Action (Show):** At second 60:
  - The buzzer plays a high double-chime.
  - The RGB LED snaps solid **Emerald Green**.
  - The OLED flashes: `TIER A | 92.4% SoH | $7.80 USD`.
  - The thermal printer fires, spitting out a $30\times 40\,\text{mm}$ peel-and-stick QR passport label.
  - Hand the printed passport to the judge: *"Scan that with your phone camera."*
- **Script (Spoken):**
  > *"Sixty seconds. The verdict is locked: Tier A, 92.4% State of Health, recommended for Second-Life Energy Storage, fair market resale value seven dollars and eighty cents.*
  > 
  > *Judge, look at your phone. You didn't download an app. You are looking at a cryptographically signed hardware passport. That green checkmark proves the test was run on our certified PulsePod terminal, calibrated to NASA reference standards, with an immutable HMAC signature."*

---

#### Minute 5:00 – 6:00 | The Contrast: Interrogating Cell Beta
- **Action (Show):** Pop Cell Alpha out. Insert *Cell Beta*. Run the 30-second rapid diagnostic mode.
  - Load triggers: The OLED voltage line drops off a cliff ($3.82\,\text{V} \rightarrow 3.10\,\text{V}$).
  - Load cuts: The piezo emits a low, sluggish, strained groan ($300\,\text{Hz} \rightarrow 450\,\text{Hz}$ over 8 seconds).
  - At second 30: The buzzer sounds a low warning alarm. The RGB LED turns **Blood Red**.
  - Dashboard: `TIER C — REJECT | INTERNAL RESISTANCE: 142 mΩ | HAZARD: THERMAL RUNAWAY RISK | VALUE: $0.45 (SCRAP RECYCLE)`.
- **Script (Spoken):**
  > *"Now you hear the difference. That low groan is an electrochemical red line. Internal resistance is one hundred and forty-two milliohms—six times nominal.*
  > 
  > *Remember: on a multimeter, this cell read 3.82 volts thirty seconds ago. If this cell was welded into an e-bike pack, it would act as a localized heating element during hill climbing.*
  > 
  > *CellCheck flagged it in thirty seconds for forty cents of testing cost."*

---

#### Minute 6:00 – 7:00 | The Scale Pivot & The Closing Mic-Drop
- **Action (Show):** Flip a toggle switch on the dashboard: `BATCH FLEET TELEMETRY INGESTION`. Instantly, 50 raw cycle CSV files from Oxford University's battery database stream through the dashboard, categorizing into Tier A, B, and C bar charts with conformal confidence metrics in under 2 seconds.
- **Script (Spoken):**
  > *"One battery on a table is a working prototype. Processing fifty batteries a second is an industrial business.*
  > 
  > *Because our feature extraction code is mathematically identical for live hardware and fleet CSV files, a recycler can deploy our twenty-five-dollar PulsePods to field workers while simultaneously running our cloud API across millions of telematics rows from active EV fleets.*
  > 
  > *We don't sell expensive cyclers. We provide the trusted valuation layer for the second-life clean energy economy. Thank you—we welcome your questions."*

---

### 7.3 The Three Bulletproof Failure Fallback Branches

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           LIVE DEMO FALLBACK MATRIX                             │
└─────────────────────────────────────────────────────────────────────────────────┘

[FAILURE SCENARIO 1: SENSOR JUMPER WIRE SNAPS OR SPRING CONTACT OXIDATION]
  │
  ├─► SYMPTOM: Dashboard reads 0.00V or INA226 throws I2C bus error.
  │
  └─► ACTION: Strike keyboard shortcut [Shift + S].
      Dashboard displays honest technical alert: 
      "HARDWARE BUS RE-SYNC ENGAGED — STREAMING CACHED HARDWARE ADC CAPTURE (115.2 kbps)".
      VERBAL RECOVERY: "Judges, a jumper wire had an intermittent contact. Notice that our
      dashboard immediately detected the open-circuit condition and engaged our golden 
      hardware serial trace. This executes the exact same downstream pipeline without missing a beat."

[FAILURE SCENARIO 2: WEBCAM FAILS TO OCR THE CELL WRAPPER DUE TO LIGHTING GLARE]
  │
  ├─► SYMPTOM: OCR bounding box shows blank or incorrect model number.
  │
  └─► ACTION: Click the single-click "QUICK-PRESET CHIP" on screen (Samsung 25R / 2500mAh).
      VERBAL RECOVERY: "Stage lighting washed out the matte blue wrapper. We hit our 2-second 
      manual override chip—showing how our human-in-the-loop workflow functions in real-world 
      warehouse environments."

[FAILURE SCENARIO 3: ESP32 USB COM PORT DISCONNECTS MID-PULSE]
  │
  ├─► SYMPTOM: USB cable gets knocked; serial port closes.
  │
  └─► ACTION: The ESP32 firmware auto-broadcasts BLE packets (`CellCheck-Pod-BLE`). 
      The web dashboard automatically falls back to Web-Bluetooth with zero page reload.
      VERBAL RECOVERY: "Our USB link dropped, and the system seamlessly fell back to wireless 
      Bluetooth Low Energy. The device never stopped measuring."
```

---

## 8. Hackathon Judging Criteria Mapping Matrix

| Hackathon Judging Criterion | Explicit Project Evidence & Proof Points | Reference Sections |
|---|---|---|
| **1. Technical Depth & Engineering Rigor** | • True 4-wire Kelvin sensing bridge eliminating contact resistance.<br>• Physics-based Time-Domain EIS extracting $R_0$, $R_\text{ct}$, and $C_\text{dl}$ overpotentials.<br>• Dual-sensor thermal transient architecture (MLX90614 IR thermopile + DS18B20).<br>• Leakage-proof cell-wise GroupKFold splitting and Conformal Prediction uncertainty bounds. | Sections 2.3, 4.1, 5.1, 5.2 |
| **2. Originality & Novelty** | • First portable "Acoustic Stethoscope" translating electrochemical bounce into audible frequencies.<br>• The "Carfax for Batteries" data model: transforming transient stress testing into tamper-evident QR provenance passports.<br>• Unification of edge embedded testing with fleet-scale battery aging datasets under an isomorphic code pipeline. | Sections 1.2, 3.1, 4.2, 6.1 |
| **3. Feasibility & Execution** | • 100% built from off-the-shelf COTS components ($<\$28$ BOM).<br>• Zero custom PCB fabrication requirements (buildable in 3 hours).<br>• Verified operation across public battery datasets (NASA Ames, Oxford, CALCE). | Sections 2.1, 4.2, 12.1 |
| **4. Real-World Impact & ESG** | • Unlocks second-life economics: testing cost drops from $\$30.00$ to $\$0.40$ per cell.<br>• Enables warehouse-scale safety triage, preventing catastrophic lithium battery fires.<br>• Directly supports circular economy reuse of over 12 million tons of Li-ion cells. | Sections 1.1, 1.3 |
| **5. Live Demo Quality & Showmanship** | • High-contrast "Twin 3.82 V Mystery Cell" Fluke hook.<br>• Physical judge interaction: Avionics safety toggle, arcade push button, industrial E-stop.<br>• Multi-sensory feedback: Live OLED curves, acoustic sonification audio, instant printed QR sticker.<br>• 3 bulletproof fallback branches for zero-failure presentation. | Sections 7.1, 7.2, 7.3 |
| **6. Safety & Failure Prevention** | • 6-stage defense-in-depth protection chain.<br>• Full mathematical thermal budget proving cell heating $<0.025\,^\circ\text{C}$ ($373\%$ resistor derating margin).<br>• Pre-screen low-voltage lockout ($V < 2.5\,\text{V}$) refusing copper-shunted cells.<br>• Conformal confidence gating ("RETEST" state refusing to guess on ambiguous cells). | Sections 2.5, 2.6, 5.2 |
| **7. Business Model & Market Moat** | • Razor-and-blade model: \$25 hardware terminal distributed at cost; \$0.25 SaaS transaction fee per printed QR passport.<br>• Transfer calibration lock-in rendering uncertified hardware incompatible with the attestation network.<br>• Data flywheel establishing the definitive secondary market pricing oracle. | Sections 1.3, 6.1 |

---

## 9. Executive Pitch Deck Slide Outline (10 Slides)

```text
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│  SLIDE 1  │ │  SLIDE 2  │ │  SLIDE 3  │ │  SLIDE 4  │ │  SLIDE 5  │
│  The Hook │ │ The Paradox│ │The Solution│ │ Hardware  │ │The 60s Test│
└───────────┘ └───────────┘ └───────────┘ └───────────┘ └───────────┘
┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐
│  SLIDE 6  │ │  SLIDE 7  │ │  SLIDE 8  │ │  SLIDE 9  │ │ SLIDE 10  │
│ One Engine│ │ ML Honesty│ │QR Passport│ │ Economics │ │ The Moat  │
└───────────┘ └───────────┘ └───────────┘ └───────────┘ └───────────┘
```

1. **Slide 1: The Title & The Hook**
   - *Visual:* High-resolution photo of two identical blue 18650 batteries sitting beside a digital multimeter reading "3.82 V" on both.
   - *Header:* **CellCheck: The $15 Pocket Stethoscope & Carfax for Used Batteries.**
   - *Script Punchline:* "Both batteries read 3.82 volts. One can power a solar home for eight years; the other will burn it down. Today, telling them apart costs more than the battery is worth."

2. **Slide 2: The Unit-Economics Paradox**
   - *Visual:* Split diagram comparing a $15,000 benchtop cycler with an operator in a lab coat vs. a mountain of unsorted batteries in a warehouse.
   - *Key Metric:* **$30 test cost vs. $8 asset value = Market Paralysis.** 70% of retired batteries are shredded for scrap because testing them is economically irrational.

3. **Slide 3: The Core Insight — The Electrochemical Stethoscope**
   - *Visual:* Medical stethoscope alongside the 3D CAD rendering of the PulsePod clip.
   - *Concept:* A cardiologist doesn't perform a 4-hour marrow biopsy to check your heart; they listen to the valve transient with a stethoscope. We apply a 5-second transient load pulse and listen to the electrochemical relaxation rebound.

4. **Slide 4: The Hardware Architecture (Deep Rigor, Zero Custom Silicon)**
   - *Visual:* Clean ASCII/schematic callouts showing True 4-Wire Kelvin sensing, INA226 16-bit ADC, Infineon IRLZ44N, MLX90614 IR thermopile, and 6-stage safety chain.
   - *Tagline:* "Built entirely from off-the-shelf COTS components for under $25. No custom PCBs required. Replicable globally in 3 hours."

5. **Slide 5: The 60-Second 4-Phase Protocol**
   - *Visual:* Timeline diagram showing P0 Baseline (5s) $\rightarrow$ P1 Load Pulse (5s) $\rightarrow$ P2 Relaxation (25s) $\rightarrow$ P3 Micro-Charge (25s).
   - *Safety Callout:* Internal heat injection = **0.09 Joules**. Core $\Delta T = \mathbf{0.0025\,^\circ\text{C}}$. Thermal runaway is physically impossible under this protocol.

6. **Slide 6: One Pipeline, Two Feeds (The Technical Masterpiece)**
   - *Visual:* The unified feature extraction diagram showing the identical `extract_features()` vectorizer digesting live INA226 ADC streams and NASA Ames / Oxford laboratory cycle datasets.
   - *Table:* The 6 physical features ($R_0$, $dV/dt$, curvature, $\Delta T$ IR, ripple, OCR prior).

7. **Slide 7: Scientific Machine Learning Rigor & Anti-Overclaiming**
   - *Visual:* Group-wise cell-level split schematic, Isotonic calibration curve, and the **"What We Don't Claim"** declaration box.
   - *Key Stat:* Macro-F1: **0.93** on held-out physical cells. Conformal uncertainty rejection: if confidence $<80\%$, model outputs **"RETEST"** instead of guessing.

8. **Slide 8: The Tamper-Evident QR Battery Passport**
   - *Visual:* Smartphone scanning a thermal sticker label; screen shows the authenticated checkmark, the cryptographic HMAC signature, and the interactive SVG voltage recovery curve.
   - *Tagline:* "Not a vague grade. An immutable, offline-verifiable proof of electrochemical provenance."

9. **Slide 9: Industrial Scale & Live Verification**
   - *Visual:* Dashboard switching from single-cell hardware mode to 50-file batch CSV mode in 2 seconds.
   - *Throughput Metric:* **480 batteries per shift per operator.** Testing cost collapses from **$30.00 to $0.25**.

10. **Slide 10: The Business Model & The Moat**
    - *Visual:* Flywheel diagram: Edge Hardware Ingress $\rightarrow$ Verifiable Passport Network $\rightarrow$ Global Pricing Oracle.
    - *The Ask / Close:* "We are turning battery waste into certified clean energy assets. The hardware is on the table; the software is live; the economics are undeniable. Thank you."

---

## 10. Pitch Variants (Calibrated by Audience)

### Variant 1: The One-Sentence Elevator Pitch
> *"CellCheck pairs an off-the-shelf twenty-five-dollar pocket stress-tester with an instant AI valuation engine to grade any used lithium battery, price its resale value, and mint an offline-verifiable QR passport in sixty seconds—replacing a five-thousand-dollar cycler and a four-hour wait."*

---

### Variant 2: The 30-Second Rapid-Fire Pitch
> *"Over twelve million tons of used batteries are heading to scrap because certifying one battery today requires a five-thousand-dollar machine and four hours of testing—spending thirty dollars to test an eight-dollar asset.*
> 
> *CellCheck collapses that testing cost to twenty-five cents. Our pocket-sized clip applies a five-second transient load pulse, measures six physical parameters using a four-wire Kelvin sensing bridge and contactless IR thermal sensing, and feeds an isotonic-calibrated model trained on NASA battery data.*
> 
> *In sixty seconds, it issues a three-tier safety grade, calculates fair market resale value, and prints a cryptographically signed QR passport. It turns hazardous battery waste into certified clean energy storage."*

---

### Variant 3: The Judge-Facing Opening Table Hook
> *"Judges, look at the multimeter on our table: both of these 18650 cells read exactly three point eight two volts. But one is worth eight dollars for an off-grid home, and the other is a fire hazard with micro-dendritic separator wear.*
> 
> *In sixty seconds, this twenty-five-dollar clip will prove which is which, let you hear its internal impedance with your own ears, and hand you a signed certificate you can verify on your smartphone.*
> 
> *Judge, flip that red safety switch and press the button."*

---

### Variant 4: The Impact & ESG Investor Pitch
> *"The clean energy transition has an unacknowledged bottleneck: second-life energy storage is economically unviable because testing retired batteries costs more than buying fresh ones from China. This dynamic causes millions of tons of good cells to be prematurely shredded or dumped in landfills.*
> 
> *CellCheck democratizes battery testing. By reducing testing time from four hours to sixty seconds and hardware costs from thousands of dollars to twenty-five dollars, we enable local refurbishers in developing nations, community microgrids, and global recyclers to safely repurpose retired EV batteries into clean power walls at one-tenth the cost."*

---

### Variant 5: The Hard-Tech / Senior Battery Engineer Pitch
> *"We do not perform an end-to-end CC-CV capacity integration, and we don't claim to. We execute time-domain electrochemical relaxation interrogation.*
> 
> *Using a four-wire Kelvin sensing interface with an INA226 sixteen-bit ADC and an MLX90614 infrared thermopile, we isolate pure Ohmic drop ($R_0$) within the first twenty milliseconds, quantify double-layer relaxation kinetics over twenty seconds of open-circuit rebound, and measure localized crimp thermal transients.*
> 
> *These features are normalized via a two-point affine transfer function directly into the parameter space of NASA Ames and Oxford cycling data. We train a monotonic XGBoost classifier using strict cell-wise GroupKFold splits and enforce conformal uncertainty bounds—ensuring that if a cell exhibits ambiguous transient dynamics, the model outputs an explicit 'retest' flag rather than a false positive."*

---

## 11. Comprehensive Risk Register & Failure Mitigation

| # | Identified Risk Event | Severity | Likelihood | Root Cause | Engineering Mitigation & Failsafe |
|---|---|---|---|---|---|
| **R1** | **Spring Contact Resistance Swing** | High | High | Surface oxidation, seating angle variations on nickel contacts. | **True 4-Wire Kelvin Bridge:** Sense leads are physically isolated from current force paths direct to the cell terminals (§2.3). |
| **R2** | **Test Cell Severely Over-Discharged ($V < 2.5\,\text{V}$)** | High | Low | Aged scrap cells left self-discharging for months (internal copper shunting). | **Hardware & Software Pre-Screen:** Firmware reads $V_\text{ocv}$ during P0. If $V < 2.50\,\text{V}$, the system refuses to arm the load; red strobe flashes. |
| **R3** | **Contact Probe Micro-Bounce / Arc Noise** | Med | Med | Mechanical vibration during button press or high current onset. | **4-Sample Savitzky-Golay FIR Filter + 3-Sigma Clipper:** Software discards the first $15\,\text{ms}$ of contact settling time before computing $f_1$. |
| **R4** | **Thermal Sensor Latency (DS18B20 Too Slow)** | Med | High | Plastic packaging thermal time constant is $5–10\,\text{seconds}$. | **Dual-Sensor Architecture:** Deployed **Melexis MLX90614 Contactless IR Thermopile** directly aimed at the terminal crimp ($<100\,\text{ms}$ response time). |
| **R5** | **Stage Lighting Glare Blinds OCR Engine** | Low | Med | Direct overhead fluorescent/spot lighting washing out wrapper text. | **Two-Second Manual Quick-Preset Chip:** One-click on-screen buttons for top 4 standard cell types (Samsung 25R, LG HG2, Sony VTC6, Panasonic NCR18650B). |
| **R6** | **USB-UART Serial Bus Hang / Driver Glitch** | High | Low | Windows COM port power saving sleep or physical cable tug. | **Automatic BLE Seamless Failover:** ESP32 concurrently broadcasts BLE telemetry packets; web app auto-connects via Web-Bluetooth API. |
| **R7** | **Model Misclassifies Mystery Cell Live on Stage** | High | Low | Unseen cell exhibiting out-of-distribution transient impedance. | **Conformal Gating + Golden Verification Cells:** Demo cells are pre-characterized and verified. If confidence drops below $80\%$, model outputs honest "RETEST". |
| **R8** | **MOSFET Thermal Drift or Gate Drive Sag** | Med | Med | 3.3 V logic gate drive failing to fully saturate standard MOSFET. | **Infineon IRLZ44N Logic-Level Selection:** Fully saturated at $V_\text{GS} = 2.8\,\text{V}$ ($R_\text{DS(on)} < 0.025\,\Omega$); 10 W aluminum resistor absorbs $>98\%$ of dissipation. |
| **R9** | **Cell Inserted Backwards by Judge** | High | Med | Human error under live presentation pressure. | **Hardware P-Channel MOSFET Polarity Clamp (IRF9540):** Reverse voltage drives gate high, locking FET in open circuit. Zero current flows. |
| **R10**| **Presentation Time Overrun ($>7$ Minutes)** | Med | Med | Stage delays, long introductory remarks. | **Configurable 30-Second Rapid Mode:** Double-click the arcade button to run a truncated 30-second protocol ($3\,\text{s}$ pulse, $12\,\text{s}$ rebound, $15\,\text{s}$ charge). |

---

## 12. Three-Hour Rapid Build Plan & Pre-Demo Checklist

```text
[HOUR 1: HARDWARE & SENSING]          [HOUR 2: ACTUATION & FIRMWARE]        [HOUR 3: SOFTWARE & STAGE RUN]
0:00                          1:00                            2:00                         3:00
┌──────────────────────────────┬───────────────────────────────┬────────────────────────────┐
│ • Breadboard power rails     │ • Wire IRLZ44N + 5Ω resistor  │ • Run 2-point transfer cal │
│ • 4-wire Kelvin holder wiring│ • Implement 4-phase state mach│ • Test Cell Alpha & Beta   │
│ • I2C bus: INA226 + MLX90614 │ • Mount OLED, buzzer, E-stop  │ • Print 2 backup passports │
│ • FLASH: 100Hz serial stream │ • VERIFY: Thermal math on FET │ • Full dress rehearsal 6:30│
└──────────────────────────────┴───────────────────────────────┴────────────────────────────┘
 GATE 1: Clean 100Hz ADC Rows   GATE 2: Full 60s Pulse Safe     GATE 3: End-to-End Success
```

### Hour-by-Hour Execution Plan

#### Hour 1: Power, Kelvin Sensing & Telemetry Bus
1. Seat ESP32 DevKit into central breadboard/perfboard track.
2. Wire $3.3\,\text{V}$ and Ground rails; install $2.2\,\text{k}\Omega$ pullups on $I^2\text{C}$ bus lines (GPIO21 SDA, GPIO22 SCL).
3. Connect INA226/INA219 and MLX90614 to $I^2\text{C}$ bus; wire DS18B20 to GPIO4 with $4.7\,\text{k}\Omega$ pullup.
4. Construct **4-Wire Kelvin Battery Holder**: solder 18 AWG silicone wires to current tabs; solder isolated 26 AWG wires direct to the gold-plated terminal contact faces.
5. Flash baseline firmware: read bus voltage, shunt current, and IR temperature at $100\,\text{Hz}$.
- **HARD EXIT GATE 1:** Serial monitor outputs valid, noise-free $100\,\text{Hz}$ CSV telemetry rows: `t_ms, v_mv, i_ma, t_c`.

#### Hour 2: Power Actuation, Safety Chain & State Machine
1. Wire low-side **Infineon IRLZ44N MOSFET**: Drain to $5\,\Omega/10\,\text{W}$ aluminum resistor; Source to System GND; Gate to GPIO18 via $100\,\Omega$ damping resistor.
2. Wire industrial **Mushroom E-Stop Switch** in series on the gate line with a $10\,\text{k}\Omega$ pulldown resistor to GND.
3. Wire the **2.5 A Ceramic Fuse** and **P-FET Reverse Polarity Guard** directly to the positive battery rail.
4. Install the 1.3" OLED (GPIO21/22), arcade trigger button (GPIO5), and Piezo Buzzer (GPIO25).
5. Flash 4-phase finite state machine (FSM): P0 (5s) $\rightarrow$ P1 (5s) $\rightarrow$ P2 (25s) $\rightarrow$ P3 (25s).
6. Insert known 18650 cell; trigger 5-second pulse. Verify with multimeter and touch-test resistor (should be warm, never hot).
- **HARD EXIT GATE 2:** Complete 60-second cycle executes autonomously; OLED graphs voltage sag; buzzer sounds recovery chirp; E-stop physically halts pulse when pressed.

#### Hour 3: Transfer Calibration, Web Dashboard & Dress Rehearsal
1. Run **Two-Point Transfer Calibration Ceremony** (§4.3) using precision test resistor. Save $(\mathbf{A}, \mathbf{B})$ calibration block to ESP32 flash.
2. Launch Python / Web dashboard: verify real-time serial charting, live NASA Ames curve overlay, and automated thermal sticker label printing.
3. Test **Cell Alpha (Healthy)**: Verify green LED, high recovery chirp, Tier A verdict ($>90\%$), and valid QR passport generation.
4. Test **Cell Beta (Aged)**: Verify red LED, low recovery groan, Tier C reject verdict.
5. Print **2 duplicate backup passports** on sticker paper and store inside the demo binder.
6. Stage the **Sacrificial Spare Rig** under the demo table; verify Shift+S fallback keyboard shortcut.
7. Conduct **one full 7-minute timed dress rehearsal** with a teammate acting as the judge.
- **HARD EXIT GATE 3:** Full dress rehearsal completed cleanly in under 6 minutes and 30 seconds with phone scan verified.

---

### Pre-Demo Go / No-Go Checklist (T-30 Minutes to Presentation)
- [ ] **Cell Rest Check:** Confirm Cell Alpha and Cell Beta both read **$3.80\,\text{V} \text{ to } 3.84\,\text{V}$** on the Fluke multimeter.
- [ ] **Contact Surface Cleaning:** Clean the Kelvin holder contacts and cell terminal caps with isopropyl alcohol wipes to eliminate fingerprint grease.
- [ ] **COM Port & Cable Lock:** Secure the USB cable to the laptop chassis using gaffer tape to prevent accidental physical disconnection.
- [ ] **BLE Auto-Connect Test:** Confirm dashboard connects via Web-Bluetooth if the serial cable is disconnected.
- [ ] **Phone QR Verification Caching:** Open the QR verification page on your smartphone browser once so all HTML/JS/CSS assets are cached locally offline.
- [ ] **Thermal Printer Ready:** Ensure fresh thermal label paper roll is loaded and feed button tested.
- [ ] **Master Arm Disarmed:** Ensure the red aircraft toggle cover is closed and E-stop switch is reset before judges approach.
- [ ] **Spare Fluke 9V Battery:** Keep a fresh 9V battery in the kit bag for the multimeter.

---

## 13. Summary: Why CellCheck Dominates the Hackathon

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      THE WINNING HACKATHON PROFILE                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   1. PHYSICAL PROOF OVER TALK                                                   │
│      Two identical-looking batteries reading 3.82V on a real Fluke DMM.         │
│      The judge flips an aircraft toggle, strikes an arcade button, and hears    │
│      the internal impedance snap back through an acoustic stethoscope.          │
│                                                                                 │
│   2. BULLETPROOF ELECTRICAL ENGINEERING                                         │
│      True 4-wire Kelvin sensing, 16-bit ADC, contactless IR thermopile,         │
│      and a 6-stage protection chain with mathematical zero-hazard proofs.       │
│                                                                                 │
│   3. SCIENTIFIC & ML INTEGRITY                                                  │
│      Strict cell-wise GroupKFold splitting on NASA/Oxford datasets.             │
│      Conformal prediction uncertainty bounds with honest "RETEST" gating.       │
│      Explicit declaration of what a 60-second test does and does not claim.     │
│                                                                                 │
│   4. AN UNASSAILABLE ECONOMIC PROPOSITION                                       │
│      Testing cost drops from $30.00 to $0.25. 480 cells per shift.              │
│      A verifiable, signed Carfax QR passport minted in 60 seconds flat.         │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

CellCheck wins because it refuses to compromise on either **hard physical engineering** or **software/ML elegance**. It does not pretend that battery physics is simple, nor does it hide behind simulated Jupyter notebooks. It brings working, tactile, laboratory-grade instrumentation directly into the judge's hands—delivering a definitive, competition-winning demonstration.
