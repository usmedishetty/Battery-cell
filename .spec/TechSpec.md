# Technical Specification (TechSpec)
**Document ID:** `CC-SPEC-TECH-v4.0`  
**System Name:** CellCheck PulsePod  
**Standard Compliance:** ASD-STE100, FreeRTOS Real-Time Kernel, IEEE 802.15.1 (BLE 4.2), NIST FIPS 186-4 (Ed25519)  

---

## 1. Embedded Runtime Stack & Firmware Allocation

The instrumentation architecture runs on an Espressif ESP32-WROOM-32 microcontroller (dual-core Xtensa 32-bit LX6 running at $240\text{ MHz}$, $520\text{ KB}$ internal SRAM, $4\text{ MB}$ SPI flash). The firmware executes under FreeRTOS with strict asymmetric core task binding.

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      ESP32 FREERTOS DUAL-CORE TASK EXECUTION MATRIX                    │
├──────┬────────────────────────┬──────────┬───────────┬─────────────────────────────────┤
│ CORE │ TASK IDENTIFIER        │ PRIORITY │ STACK     │ FUNCTIONAL RESPONSIBILITY       │
├──────┼────────────────────────┼──────────┼───────────┼─────────────────────────────────┤
│ 0    │ `Task_DSP_Acquisition` │ 24 (Max) │ 8,192 B   │ Synchronous INA226 ADC DMA read │
│      │                        │          │           │ and on-chip TD-EIS DFT math.    │
│ 0    │ `Task_Thermal_Safety`  │ 22       │ 4,096 B   │ MLX90614 IR poll (100 Hz);      │
│      │                        │          │           │ hardware safety interrupter ISR.│
│ 0    │ `Task_Ultrasonic_Echo` │ 18       │ 4,096 B   │ 40 kHz transducer burst drive   │
│      │                        │          │           │ and envelope peak detection.    │
│ 1    │ `Task_Display_OLED`    │ 5        │ 4,096 B   │ SH1106 30 FPS Nyquist rendering │
│      │                        │          │           │ and live voltage sag curve.     │
│ 1    │ `Task_Audio_Glissando` │ 4        │ 2,048 B   │ Hardware LEDC PWM frequency     │
│      │                        │          │           │ synthesis for sound profile.    │
│ 1    │ `Task_BLE_Telemetry`   │ 3        │ 12,288 B  │ BLE GATT server and packed      │
│      │                        │          │           │ binary serial frame stream.     │
│ 1    │ `Task_Crypto_Sign`     │ 2        │ 6,144 B   │ Ed25519 digital signature and   │
│      │                        │          │           │ W3C passport credential mint.   │
└──────┴────────────────────────┴──────────┴───────────┴─────────────────────────────────┘
```

### 1.1 Inter-Core Data Synchronization
1. Core 0 and Core 1 communicate via a thread-safe, lock-free circular ring buffer (`RingBuffer_ADC`, 512-frame capacity).
2. Core 0 writes digitized engineering units ($v_{\text{cell}}, i_{\text{shunt}}, T_{\text{vent}}$) into `RingBuffer_ADC` at $100\text{ Hz}$.
3. Core 1 reads from `RingBuffer_ADC` asynchronously. If `RingBuffer_ADC` overflows, the firmware asserts a buffer-overrun flag and halts the test.
4. Maximum interrupt service routine (ISR) latency on Core 0 is constrained below $12\ \mu\text{s}$.

---

## 2. Complete COTS Bill of Materials & Cost Reconcile

The production instrument uses commercial-off-the-shelf (COTS) components sourced via standard electronics distribution (DigiKey, Mouser, LCSC).

```text
┌────┬───────────────────────┬──────────────────────────────┬──────────┬─────┬───────────┐
│ #  │ SUBSYSTEM             │ COMPONENT PART NUMBER        │ PACKAGE  │ QTY │ COST ($)  │
├────┼───────────────────────┼──────────────────────────────┼──────────┼─────┼───────────┤
│ 1  │ Controller MCU        │ ESP32 DevKit V1 (30-pin)     │ DIP-30   │ 1   │ 4.20      │
│ 2  │ High-Precision ADC    │ TI INA226 (I2C address 0x40) │ MSOP-10  │ 1   │ 2.80      │
│ 3  │ Current Shunt Resistor│ Vishay WSLP2512 (0.05Ω 0.5%) │ 2512     │ 1   │ 1.10      │
│ 4  │ Primary Load Switch   │ Infineon IRLZ44N Logic N-FET │ TO-220   │ 1   │ 0.75      │
│ 5  │ Power Load Resistor   │ Ohmite 850 5.0Ω 1% 10W Alum  │ Chassis  │ 1   │ 1.35      │
│ 6  │ Contactless IR Sensor │ Melexis MLX90614ESF-BAA      │ TO-39    │ 1   │ 4.50      │
│ 7  │ Ultrasonic Pair       │ 40 kHz Piezo Ceramic Disc    │ 16mm     │ 1   │ 1.80      │
│ 8  │ True Kelvin Clamp Jaws│ Isolated Dual-Contact Spring │ Custom   │ 1   │ 2.40      │
│ 9  │ Reverse Polarity Gate │ Vishay IRF9540 P-MOSFET      │ TO-220   │ 1   │ 0.60      │
│ 10 │ Galvanic Fuse         │ Littelfuse 218 2.5A Fast Cart│ 5x20mm   │ 1   │ 0.35      │
│ 11 │ Waveform Display      │ 1.3" I2C OLED (SH1106 128x64)│ Module   │ 1   │ 2.50      │
│ 12 │ Master Arm Switch     │ Aircraft Toggle w/ Red Guard │ Panel    │ 1   │ 1.60      │
│ 13 │ Emergency Stop        │ 22mm Latching Mushroom E-Stop│ Industrial│ 1  │ 1.90      │
│ 14 │ Trigger Button        │ Sanwa-Style 30mm Arcade PB   │ Snap-In  │ 1   │ 0.85      │
│ 15 │ Status Indicator      │ 5mm RGB Common-Cathode LED   │ Through  │ 1   │ 0.25      │
│ 16 │ Piezo Buzzer          │ 5V Magnetic Buzzer / Piezo   │ Module   │ 1   │ 0.45      │
│ 17 │ Enclosure & Screws    │ Laser-Cut Acrylic + Spacers  │ Chassis  │ 1   │ 3.50      │
├────┴───────────────────────┴──────────────────────────────┴──────────┴─────┼───────────┤
│    TOTAL PRODUCTION INSTRUMENT BOM COST                                    │ $30.10    │
└────────────────────────────────────────────────────────────────────────────┴───────────┘
```

> **BOM Cost Reconciliation:**  
> The headline figure of $\$15\text{ to }\$16$ represents a minimal bare-board DC pulse discharger ($16.85\text{ USD}$ BOM) without acoustic diagnostics, contactless IR, or aircraft safety interlocks. The complete competition-grade, auditable instrument specified here costs $\$30.10\text{ USD}$ in 1,000-unit production lots.

---

## 3. Four-Wire Kelvin Interface & Sensing Circuitry

```text
                  4-WIRE KELVIN ISOLATED VOLTAGE SENSING TOPOLOGY

        [ HIGH-CURRENT FORCE CIRCUIT ]             [ HIGH-IMPEDANCE SENSE CIRCUIT ]
        18 AWG Multi-Strand Copper Wire            28 AWG Teflon-Insulated Gold Needle
        Carries 0.75A Discharge Current            Input Impedance > 10 Megohms; I < 40 nA
                     │                                             │
                     ▼                                             ▼
        ┌─────────────────────────┐                   ┌─────────────────────────┐
        │ Outer Copper Clamp Jaw  │                   │ Inner Gold Pogo Needle  │
        └────────────┬────────────┘                   └────────────┬────────────┘
                     │                                             │
                     ▼                                             ▼
        ═════════════════════════════════════════════════════════════════════════
                              CYLINDRICAL CELL TERMINAL CAP
        ═════════════════════════════════════════════════════════════════════════
```

### 3.1 Contact Resistance Suppression Proof
1. The force circuit carries the load current ($I_{\text{pulse}} \approx 0.75\text{ A}$). Contact resistance between the clamp jaw and cell terminal ranges from $R_{\text{contact}} = 10\text{ m}\Omega\text{ to }80\text{ m}\Omega$.
2. The sense circuit connects to the differential inputs of the Texas Instruments INA226 ADC. The input bias current of the INA226 is $I_{\text{bias}} \le 40\text{ nA}$.
3. The measurement voltage error across the sense interface is:
   $$V_{\text{error}} = I_{\text{bias}} \times R_{\text{contact}} \le (40 \times 10^{-9}\text{ A}) \times (80 \times 10^{-3}\ \Omega) = 3.20\ \text{nV}$$
4. This error is four orders of magnitude below the INA226 ADC least significant bit ($85\ \mu\text{V}$). Contact resistance variance is mathematically eliminated.

### 3.2 ADC Configuration & Signal Bus
- **Sensor:** Texas Instruments INA226 Bi-Directional Current/Power Monitor.
- **Bus Speed:** I2C Fast-mode running at $400\text{ kHz}$ with hardware pull-up resistors ($2.2\text{ k}\Omega$).
- **Configuration Registers:**
  - Shunt conversion time: $140\ \mu\text{s}$.
  - Bus voltage conversion time: $140\ \mu\text{s}$.
  - Averaging mode: 4 samples per conversion cycle.
  - Total measurement conversion duration: $560\ \mu\text{s}$ per frame (effective continuous rate: $1.78\text{ kHz}$).
- **Quantization Step:** $85\ \mu\text{V}$ LSB on bus voltage; $2.5\ \mu\text{V}$ LSB on shunt differential voltage (with $0.05\Omega$ shunt, current resolution is $50\ \mu\text{A}$).
- **Voltage Noise Floor:** $V_{\text{noise, RMS}} < 120\ \mu\text{V}$.

---

## 4. Multi-Domain Physical Instrumentation

### 4.1 Contactless Infrared Vent-Cap Thermopile (MLX90614)
- **Sensor:** Melexis MLX90614ESF-BAA non-contact infrared thermometer ($90^\circ$ FOV, factory-calibrated for $-40^\circ\text{C}$ to $+85^\circ\text{C}$ ambient, $-70^\circ\text{C}$ to $+380^\circ\text{C}$ object).
- **Physical Mounting:** Housed in a 3D-printed shroud focused onto the cell positive terminal crimp seal / PTC safety disc.
- **Refresh Rate:** Interrogated over I2C at $100\text{ Hz}$ ($10\text{ ms}$ interval).
- **Thermal Response Latency:** Detects localized crimp Ohmic dissipation ($\Delta T \ge +0.8^\circ\text{C}$) within $180\text{ ms}$. This replaces glued NTC thermistors that suffer $5\text{ to }10\text{-second}$ thermal packaging lag.

### 4.2 Ultrasonic Transducer Array & Silicone Coupler Pad
- **Acoustic Transducers:** $40.0\text{ kHz} \pm 1.0\text{ kHz}$ piezoelectric ceramic disc elements mounted on opposing V-groove clamp jaws.
- **Acoustic Coupling:** Standard bare dry contact against steel casing introduces $>40\text{ dB}$ air-gap mismatch attenuation. The clamp integrates a compliant $1.5\text{ mm}$ silicone acoustic coupler elastomer pad (Shore A 30).
- **Drive Signal:** Core 0 drives a 5-cycle square-wave burst at $40\text{ kHz}$ via GPIO19 (LEDC Channel 1).
- **Detection:** The opposing transducer output passes through a passive envelope detector into ADC1 Channel 6 (GPIO34). Attenuation $> 20.0\text{ dB}$ indicates interior delamination, dry-out, or internal gas pocket formation.

---

## 5. Mathematical Zero-Hazard Thermal & Joulean Proof

```text
               THERMAL BALANCE ACROSS A 60-SECOND TEST CYCLE
 
  Peak Discharge Current:     I_pulse  = 0.755 A
  Discharge Duration:         t_pulse  = 5.000 s
  Internal Ohmic Resistance:  R_0      = 0.035 Ω (Healthy Cell)
  Total Energy Dissipation:   E_pulse  = 0.0997 Joules
  18650 Cell Thermal Mass:    m · C_p  = 37.35 J / °C
  Core Temperature Rise:      ΔT_core  = 0.00267 °C
```

### 5.1 Proof of Thermal Runaway Impossibility
1. Thermal runaway in standard lithium-ion cells initiates only when internal core temperatures exceed separator shutdown and breakdown limits ($T_{\text{runaway}} \ge 135^\circ\text{C}\text{ to }160^\circ\text{C}$).
2. The total electrical energy injected into the cell core during Phase 1 is:
   $$E_{\text{core}} = \int_{0}^{5} I^2(t) R_0 \, dt = (0.755\text{ A})^2 \times 0.035\ \Omega \times 5.0\text{ s} = 0.0997\text{ Joules}$$
3. Assuming zero heat dissipation to the ambient air (perfect adiabatic conditions), the core temperature rise of a $45.0\text{ g}$ cylindrical cell ($C_p = 830\text{ J}/(\text{kg}\cdot^\circ\text{C})$) is:
   $$\Delta T_{\text{core}} = \frac{E_{\text{core}}}{m \cdot C_p} = \frac{0.0997\text{ J}}{0.045\text{ kg} \times 830\text{ J}/(\text{kg}\cdot^\circ\text{C})} = \mathbf{0.00267^\circ\text{C}}$$
4. For an abusive, severely damaged cell with internal resistance 10 times higher ($R_0 = 0.350\ \Omega$):
   $$\Delta T_{\text{core, abusive}} = \frac{(0.755\text{ A})^2 \times 0.350\ \Omega \times 5.0\text{ s}}{37.35\text{ J}/^\circ\text{C}} = \mathbf{0.0267^\circ\text{C}}$$
5. Even under extreme degradation, the core temperature rise remains below $0.03^\circ\text{C}$. The 60-second test cannot induce thermal runaway.

### 5.2 Load Resistor Thermal Margin
- Peak power dissipation in load resistor during pulse:
  $$P_{\text{load}} = I^2 R_{\text{load}} = (0.755\text{ A})^2 \times 5.0\ \Omega = 2.85\text{ Watts}$$
- Resistor continuous rating: Ohmite 850 aluminum-housed wirewound resistor rated at $10.0\text{ Watts}$.
- Safety Operating Margin:
  $$\text{Margin} = \frac{10.0\text{ W}}{2.85\text{ W}} = 3.51\times\quad (351\%\text{ safe derating headroom})$$
- Average continuous power across the 60-second cycle:
  $$P_{\text{avg}} = \frac{2.85\text{ W} \times 5.0\text{ s}}{60.0\text{ s}} = 0.238\text{ Watts}$$
- Convection cooling through ambient chassis venting is sufficient. No active cooling fan is required.

---

## 6. Machine Learning Pipeline & Statistical Formulation

```text
 8-Dimensional Input Tensor x in R^8
                │
                ▼
 ┌──────────────────────────────┐
 │ MONOTONIC XGBOOST CLASSIFIER │ ──► Strictly enforces dDegradation/df1 >= 0
 └──────────────┬───────────────┘
                │
                ▼
 ┌──────────────────────────────┐
 │ ISOTONIC CALIBRATION ENGINE  │ ──► Maps raw tree margins to true Bayesian posteriors
 └──────────────┬───────────────┘
                │
                ▼
 ┌──────────────────────────────┐
 │ CONFORMAL PREDICTION GATE    │ ──► Enforces 95% finite-sample coverage guarantee
 └──────────────┬───────────────┘
                │
        ┌───────┴───────┐
        ▼               ▼
 [ |C(x)| == 1 ]  [ |C(x)| != 1 ]
  Unambiguous      Epistemic Noise / Ambiguity
  Grade Assigned   Model Refuses to Guess: "RETEST"
```

### 6.1 The 8-Dimensional Feature Tensor Formulation
The feature engine extracts the vector $\mathbf{x} = [f_1, f_2, f_3, f_4, f_5, f_6, f_7, f_8]^T \in \mathbb{R}^8$:

1. **Feature 1 ($f_1$): Instantaneous Normalized Ohmic Drop Ratio ($R_0$)**
   $$f_1 = \frac{\bar{V}_{\text{P0}} - V(t_{\text{pulse}} + 20\text{ ms})}{\bar{V}_{\text{P0}}} \times 100 \quad [\%]$$
   Isolates pure electrolyte and collector resistance independent of cell state-of-charge.

2. **Feature 2 ($f_2$): Double-Layer Relaxation Gradient**
   $$f_2 = \left( \left. \frac{dV}{dt} \right|_{t=11\text{ s}}^{t=15\text{ s}} \right) \cdot \frac{1}{\bar{V}_{\text{P0}}} \times 10^3 \quad \left[\frac{\text{mV}}{\text{s}\cdot\text{V}}\right]$$
   Measures charge-transfer kinetics across the solid-electrolyte interphase (SEI) film.

3. **Feature 3 ($f_3$): TD-EIS Imaginary-to-Real Impedance Ratio**
   $$f_3 = \frac{-Z''(100\text{ Hz})}{Z'(100\text{ Hz})} = \tan(\theta_{\text{impedance}})$$
   Measures capacitive double-layer phase displacement under dynamic multi-tone perturbation.

4. **Feature 4 ($f_4$): Normalized Vent-Cap Infrared Thermal Rise**
   $$f_4 = \frac{T_{\text{IR, max}}(0..60) - T_{\text{ambient, P0}}}{\max(T_{\text{ambient, P0}}, 15.0^\circ\text{C})} \times 100 \quad [\%]$$
   Identifies micro-corrosion, weld detachment, and localized current crowding on safety vents.

5. **Feature 5 ($f_5$): Ultrasonic Casing Attenuation**
   $$f_5 = 20 \log_{10} \left( \frac{V_{\text{acoustic, received}}}{V_{\text{acoustic, reference}}} \right) \quad [\text{dB}]$$
   Quantifies internal jellyroll mechanical separation, delamination, and gas formation.

6. **Feature 6 ($f_6$): Dynamic Current Ripple Stability Index**
   $$f_6 = \frac{\sqrt{\frac{1}{M}\sum_{m=1}^M \left( I(t_m) - \bar{I}_{\text{P1}} \right)^2}}{\bar{I}_{\text{P1}}} \quad [\text{dimensionless}]$$
   Flags micro-dendritic flashover events and intermittent contact micro-arcing.

7. **Feature 7 ($f_7$): Micro-Charge Polarization Rate**
   $$f_7 = \left( \left. \frac{dV}{dt} \right|_{t=40\text{ s}}^{t=55\text{ s}} \right) \cdot \frac{1}{I_{\text{charge}}} \quad \left[\frac{\text{mV}}{\text{s}\cdot\text{A}}\right]$$
   Measures active lithium-ion insertion kinetics into the graphite host structure.

8. **Feature 8 ($f_8$): Chemistry & Capacity Normalization Prior**
   $$f_8 = \frac{C_{\text{rated, OCR}}}{3500\text{ mAh}} \times \kappa_{\text{chem}}$$
   Where $\kappa_{\text{NMC}} = 1.00$, $\kappa_{\text{LCO}} = 0.92$, $\kappa_{\text{LFP}} = 0.78$, $\kappa_{\text{NCA}} = 0.98$.

### 6.2 Split Conformal Prediction Mathematics
To avoid uncalibrated overconfident errors, the system outputs prediction sets $\mathcal{C}(\mathbf{x})$:
1. Divide reference data into a training set ($80\%$) and an independent calibration set $\{( \mathbf{x}_i, y_i )\}_{i=1}^n$ ($20\%$).
2. Fit monotonic XGBoost and isotonic calibration on the training set to produce posterior probability estimator $\hat{P}(Y = c \mid \mathbf{x})$.
3. Compute non-conformity scores on calibration samples:
   $$s_i = 1 - \hat{P}(Y = y_i \mid \mathbf{x}_i)$$
4. Given significance level $\alpha = 0.05$ (guaranteeing $95\%$ coverage), compute the empirical critical quantile:
   $$\hat{q} = \text{Quantile}\left( s_1, \ldots, s_n;\ \frac{\lceil (n+1)(1-\alpha) \rceil}{n} \right)$$
5. For an unseen query cell with feature vector $\mathbf{x}_{\text{new}}$, form the prediction set:
   $$\mathcal{C}(\mathbf{x}_{\text{new}}) = \left\{ c \in \{\text{Tier A, Tier B, Tier C}\} \mid 1 - \hat{P}(Y = c \mid \mathbf{x}_{\text{new}}) \le \hat{q} \right\}$$
6. **Decision Logic:**
   - If $\mathcal{C}(\mathbf{x}_{\text{new}}) = \{ \text{Tier A} \}$, output certified Tier A.
   - If $\mathcal{C}(\mathbf{x}_{\text{new}}) = \{ \text{Tier B} \}$, output certified Tier B.
   - If $\mathcal{C}(\mathbf{x}_{\text{new}}) = \{ \text{Tier C} \}$, output certified Tier C (Recycle).
   - If $|\mathcal{C}(\mathbf{x}_{\text{new}})| > 1$ or $|\mathcal{C}(\mathbf{x}_{\text{new}})| = 0$, output `RETEST / INCONCLUSIVE`.
