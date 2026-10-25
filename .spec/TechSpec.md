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
│ 10 │ Galvanic Fuse         │ Littelfuse 216 2.5A (021602.5MXP)│ 5x20mm│ 1   │ 0.35 [TO VERIFY]│
│ 11 │ Waveform Display      │ 1.3" I2C OLED (SH1106 128x64)│ Module   │ 1   │ 2.50      │
│ 12 │ Master Arm Switch     │ Aircraft Toggle w/ Red Guard │ Panel    │ 1   │ 1.60      │
│ 13 │ Emergency Stop        │ 22mm Latching Mushroom E-Stop│ Industrial│ 1  │ 1.90      │
│ 14 │ Trigger Button        │ Sanwa-Style 30mm Arcade PB   │ Snap-In  │ 1   │ 0.85      │
│ 15 │ Status Indicator      │ 5mm RGB Common-Cathode LED   │ Through  │ 1   │ 0.25      │
│ 16 │ Piezo Buzzer          │ 5V Magnetic Buzzer / Piezo   │ Module   │ 1   │ 0.45      │
│ 17 │ Micro-Charge Module   │ TP4056 1A Linear Li-Ion (0.2A)│ Module   │ 1   │ 0.45      │
│ 18 │ Enclosure & Screws    │ Laser-Cut Acrylic + Spacers  │ Chassis  │ 1   │ 3.05      │
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

### 3.2 ADC Configuration, Timing Derivation & Nyquist Dynamics
- **Sensor:** Texas Instruments INA226 Bi-Directional Current/Power Monitor.
- **Physical Interface:** I2C Fast-mode running at $400\text{ kHz}$ with external hardware pull-up resistors ($2.2\text{ k}\Omega$).
- **Conversion Timing Derivation:**
  The INA226 datasheet defines the frame conversion duration as the sum of shunt and bus conversion times multiplied by the sample average count:
  $$T_{\text{frame}} = (T_{\text{shunt}} + T_{\text{bus}}) \times N_{\text{avg}}$$
  - **4-Sample Averaging Mode ($N_{\text{avg}} = 4$):**
    $$T_{\text{frame}} = (140\ \mu\text{s} + 140\ \mu\text{s}) \times 4 = 1120\ \mu\text{s} \implies f_s = \frac{1}{1120\ \mu\text{s}} \approx 892.86\text{ Hz}$$
    *(Note: The earlier specification claim of $560\ \mu\text{s}$ / $1.78\text{ kHz}$ was an error that omitted multiplying by $N_{\text{avg}}$ across both conversion phases).*
  - **Single-Sample Mode ($N_{\text{avg}} = 1$):**
    $$T_{\text{frame}} = (140\ \mu\text{s} + 140\ \mu\text{s}) \times 1 = 280\ \mu\text{s} \implies f_s = \frac{1}{280\ \mu\text{s}} \approx 3571.43\text{ Hz}$$
- **Quantization Step:**
  - Shunt differential voltage LSB: $2.5\ \mu\text{V}$. With a $0.05\ \Omega$ shunt resistor, current resolution is:
    $$\Delta I_{\text{LSB}} = \frac{2.5\ \mu\text{V}}{0.05\ \Omega} = 50.0\ \mu\text{A}$$
  - Bus voltage LSB: $1.25\text{ mV}$ (fixed internal architecture of the TI INA226). *(Note: The earlier specification claim of $85\ \mu\text{V}$ is incorrect and is tracked as OPEN-02).*
  - Voltage noise floor: $V_{\text{noise, RMS}} < 120\ \mu\text{V}$.

#### A. I2C Bus Timing Budget & Polling Architecture
At $400\text{ kHz}$ Fast-Mode ($T_{\text{clk}} = 2.50\ \mu\text{s}$), reading the two 16-bit measurement registers (Shunt Voltage register `0x01` and Bus Voltage register `0x02`):
1. **Clock Cycle Budget per Register Read:**
   - START condition + 7-bit Slave Address + Write bit + ACK = 9 clocks.
   - 8-bit Register Pointer + ACK = 9 clocks.
   - REPEATED START + 7-bit Slave Address + Read bit + ACK = 9 clocks.
   - Data Byte High + ACK = 9 clocks.
   - Data Byte Low + NACK + STOP = 9 clocks.
   - Total per register = 45 clock cycles.
2. **Total Wire Time for Two Registers:**
   $$T_{\text{wire}} = 2 \times 45\ \text{cycles} \times 2.50\ \mu\text{s} = 225.0\ \mu\text{s}$$
3. **Driver Execution Overhead:**
   ESP-IDF FreeRTOS context switching, I2C command descriptor link, and ISR dispatch introduce an assumed $30\ \mu\text{s}\text{ to }50\ \mu\text{s}$ [ASSUMED]. Total read turnaround time:
   $$T_{\text{read}} \approx 225.0\ \mu\text{s} + 40.0\ \mu\text{s} = 265.0\ \mu\text{s}$$
4. **Bus Margin Comparison:**
   - In 4-sample averaging mode ($T_{\text{frame}} = 1120\ \mu\text{s}$), bus utilization is $265 / 1120 = 23.7\%$, leaving ample processing headroom.
   - In single-sample mode ($T_{\text{frame}} = 280\ \mu\text{s}$), bus utilization is $265 / 280 = 94.6\%$. Software polling at $3.57\text{ kHz}$ risks bus congestion and dropped frames.
   - **Mitigation:** Route the INA226 ALERT pin to ESP32 GPIO to assert on Conversion Ready (`CVRF`). The MCU services data synchronously on hardware interrupt instead of spinning.
   - **DMA Architectural Status:** The ESP32 does not support Direct Memory Access (DMA) on the I2C peripheral interface. DMA on the ESP32 is restricted to SPI and I2S hardware. All I2C telemetry operates via interrupt-driven FIFO transfers.

#### B. Sequential Conversion Time Skew
The INA226 does not sample shunt and bus voltages simultaneously. It samples them sequentially through an internal multiplexer:
- Sequential conversion offset: $\tau_{\text{skew}} = 140.0\ \mu\text{s}$.
- The voltage sample $v[n]$ lags the current sample $i[n]$ by $\tau_{\text{skew}}$.
- Induced phase error at frequency $\omega = 2\pi f$:
  $$\Delta \theta_{\text{skew}} = \omega \cdot \tau_{\text{skew}} = 2\pi \cdot f \cdot (140.0 \times 10^{-6}\text{ s})$$
  - At $10\text{ Hz}$: $\Delta \theta = 0.50^\circ$ ($0.0088\text{ rad}$).
  - At $100\text{ Hz}$: $\Delta \theta = 5.04^\circ$ ($0.0880\text{ rad}$).
  - At $500\text{ Hz}$: $\Delta \theta = 25.20^\circ$ ($0.4398\text{ rad}$).
  - At $1000\text{ Hz}$: $\Delta \theta = 50.40^\circ$ ($0.8796\text{ rad}$).
- At $1000\text{ Hz}$, $50.4^\circ$ skew rotates real resistive impedance into imaginary reactive impedance, producing invalid Nyquist arcs.
- **Phase Rotation Correction:**
  To correct the measurement vector, the firmware rotates the uncompensated impedance by the calibrated sequential delay:
  $$Z_{\text{corr}}(\omega) = Z_{\text{meas}}(\omega) \cdot e^{j \omega \tau_{\text{skew}}}$$
  Where $\tau_{\text{skew}} = 140.0\ \mu\text{s}$ is a calibrated system constant.

#### C. Square-Wave Harmonic Aliasing
The IRLZ44N load switch drives square-wave current pulses. Square waves contain odd harmonics $k \cdot f_0$ ($k = 3, 5, 7, 9, 11$) with relative amplitudes $1/k$.
In single-sample mode ($f_s = 3571.43\text{ Hz}$), the Nyquist fold limit is $f_{\text{Nyq}} = 1785.71\text{ Hz}$. Harmonics above $1785.71\text{ Hz}$ alias into the baseband:
$$f_{\text{alias}} = |k \cdot f_0 - m \cdot f_s|$$

| Tone ($f_0$) | Harmonic $k=3$ | Harmonic $k=5$ | Harmonic $k=7$ | Harmonic $k=9$ | Harmonic $k=11$ | Aliasing Status |
|---|---|---|---|---|---|---|
| **10 Hz** | 30.0 Hz | 50.0 Hz | 70.0 Hz | 90.0 Hz | 110.0 Hz | **No aliasing** (all $k \le 11$ below Nyquist) |
| **100 Hz** | 300.0 Hz | 500.0 Hz | 700.0 Hz | 900.0 Hz | 1100.0 Hz | **No aliasing** (all $k \le 11$ below Nyquist) |
| **500 Hz** | 1500.0 Hz | 1071.4 Hz (ALIAS) | 71.4 Hz (ALIAS) | 928.6 Hz (ALIAS) | 1642.9 Hz (ALIAS) | Harmonics $k \ge 5$ fold into band |
| **1000 Hz** | 571.4 Hz (ALIAS) | 1428.6 Hz (ALIAS) | 142.9 Hz (ALIAS) | 1714.3 Hz (ALIAS) | 285.7 Hz (ALIAS) | Harmonics $k \ge 3$ fold into band |

**Harmonic Mitigations:**
1. **Coherent Sampling:** Synchronize sampling such that $f_s = M \cdot f_0$, placing harmonic energy exactly on orthogonal DFT bin boundaries.
2. **Single-Tone Bursts:** Drive discrete single-tone sinusoidal bursts rather than wideband PRBS to concentrate energy at fundamental $f_0$.
3. **Slew Rate Pre-Filtering:** Limit gate drive transition time using an RC low-pass gate filter to suppress high-order harmonics.

#### D. Decision Record: TD-EIS Tone Range Selection
Three architectural options were evaluated to address the sampling limitation:
- **Option A (INA226 Only, Bounded Tones):** Bound multi-tone excitation to frequencies resolvable by the INA226 ADC: $10\text{ Hz}$, $100\text{ Hz}$, and $500\text{ Hz}$ ($\le f_s / 7 \approx 510.2\text{ Hz}$). Machine learning feature $f_3 = \frac{-Z''(100\text{ Hz})}{Z'(100\text{ Hz})}$ depends solely on the $100\text{ Hz}$ tone. The machine learning pipeline is unaffected. Added BOM cost: $\$0.00$.
- **Option B (Add External Simultaneous ADC):** Add a dedicated 24-bit simultaneous-sampling ADC (e.g., TI ADS131M02) with true SPI DMA sampling at $\ge 32\text{ kSPS}$. Resolves $1.0\text{ kHz}$ to $10.0\text{ kHz}$ with zero sequential skew. Added BOM cost: $+\$2.50\text{ to }+\$3.50\text{ USD}$.
- **Option C (Drop AC Chirp Entirely):** Remove AC perturbation. Extract Ohmic resistance $R_0$ from the initial current step and charge-transfer resistance $R_{\text{ct}}$ from the open-circuit relaxation decay ($t = 11\text{ s to }15\text{ s}$). Added BOM cost: $\$0.00$.

**Architecture Decision:** **Option A is implemented.** The instrument operates multi-tone perturbation at $10\text{ Hz}$, $100\text{ Hz}$, and $500\text{ Hz}$. Feature $f_3$ is extracted at $100\text{ Hz}$. Support for $1.0\text{ kHz}$ AC impedance spectroscopy is retained as a PulsePod v2 product roadmap goal.

#### E. Numerical Simulation Results (`.spec/calc/sampling_check.py`)
*Note: The following table presents a numerical simulation of Randles equivalent circuit dynamics under INA226 hardware constraints. It is not an empirical laboratory measurement.*

```text
======================================================================================================
CELLCHECK PULSEPOD: TD-EIS INA226 SAMPLING & TIME-SKEW SIMULATION
NOTE: THIS IS A NUMERICAL SIMULATION, NOT A PHYSICAL MEASUREMENT.
======================================================================================================
Assumed Cell Model:     R0 = 35.0 mOhm, Rct = 25.0 mOhm, Cdl = 1.00 F [ASSUMED]
INA226 Timing (N_avg=1): T_frame = 280.0 us (fs = 3571.43 Hz), Sequential Skew tau = 140.0 us
Quantization LSB:       V_bus LSB = 1.25 mV, Current LSB = 50.0 uA
------------------------------------------------------------------------------------------------------
Tone     | True Impedance       | Uncorrected Meas       | Corrected (Rotated)    | Residual Error    
(Hz)     | Zp - j*Zpp (mOhm)    | Zp - j*Zpp (mOhm)      | Zp - j*Zpp (mOhm)      | dZp, dZpp (mOhm)  
------------------------------------------------------------------------------------------------------
10.0     |  42.21 - j11.33      |  42.31 - j10.89        |  42.41 - j10.51        | dZp=+0.20, dZpp=+0.81
100.0    |  35.10 - j 1.59      |  35.16 - j 1.45        |  34.89 - j 4.53        | dZp=-0.21, dZpp=+6.11
500.0    |  35.00 - j 0.32      |  31.94 - j14.48        |  22.74 - j26.70        | dZp=-12.27, dZpp=+27.02
1000.0   |  35.00 - j 0.16      |  22.31 - j26.58        |  -6.26 - j34.13        | dZp=-41.27, dZpp=+34.29
------------------------------------------------------------------------------------------------------
```

---

## 4. Multi-Domain Physical Instrumentation

### 4.1 Contactless Infrared Vent-Cap Thermopile (MLX90614)
- **Sensor:** Melexis MLX90614ESF-BAA non-contact infrared thermometer ($90^\circ$ FOV, factory-calibrated for $-40^\circ\text{C}$ to $+85^\circ\text{C}$ ambient, $-70^\circ\text{C}$ to $+380^\circ\text{C}$ object).
- **Physical Mounting:** Housed in a 3D-printed shroud focused onto the cell positive terminal crimp seal / PTC safety disc.
- **Refresh Rate:** Interrogated over I2C at $100\text{ Hz}$ ($10\text{ ms}$ interval).
- **Thermal Response Latency:** Detects localized crimp Ohmic dissipation ($\Delta T \ge +0.8^\circ\text{C}$) within $180\text{ ms}$. This replaces glued NTC thermistors that suffer $5\text{ to }10\text{-second}$ thermal packaging lag.
- **Emissivity Calibration on Bare Metal:** The MLX90614 factory calibration assumes blackbody emissivity ($\varepsilon = 1.00$). Bare, polished nickel-plated steel terminal caps have low emissivity ($\varepsilon \approx 0.10\text{ to }0.20$), which severely underestimates actual temperature. The operator must apply a high-emissivity matte coating or black adhesive vinyl dot ($\varepsilon \ge 0.95$) to the positive crimp inspection target before clamping, or calibrate the sensor emissivity register.

### 4.2 Ultrasonic Transducer Array & Silicone Coupler Pad
- **Acoustic Transducers:** $40.0\text{ kHz} \pm 1.0\text{ kHz}$ piezoelectric ceramic disc elements mounted on opposing V-groove clamp jaws.
- **Acoustic Coupling:** Standard bare dry contact against steel casing introduces $>40\text{ dB}$ air-gap mismatch attenuation. The clamp integrates a compliant $1.5\text{ mm}$ silicone acoustic coupler elastomer pad (Shore A 30).
- **Drive Signal:** Core 0 drives a 5-cycle square-wave burst at $40\text{ kHz}$ via GPIO19 (LEDC Channel 1).
- **Detection:** The opposing transducer output passes through a passive envelope detector into ADC1 Channel 6 (GPIO34). Attenuation $> 20.0\text{ dB}$ indicates interior delamination, dry-out, or internal gas pocket formation.

---

## 5. Bounded Thermal & Joulean Energy Analysis

### 5.1 Bounded Test-Energy Analysis

#### A. Electrochemical Heat Generation Model
Heat generation in a lithium-ion cell during electrical perturbation follows the Bernardi energy balance equation:

$$\dot{Q}_{\text{cell}} = I(t) \cdot [V_{\text{ocv}}(t) - V(t)] - I(t) \cdot T \frac{\partial V_{\text{ocv}}}{\partial T}$$

Where:
- $I(t)$ is the cell terminal current (positive for discharge, negative for charge).
- $V_{\text{ocv}}(t) - V(t)$ is total cell overpotential ($\eta_{\text{total}} = I R_0 + \eta_{\text{ct}} + \eta_{\text{diff}}$).
- The first term represents irreversible overpotential heating: $P_{\text{irrev}} = I \cdot (V_{\text{ocv}} - V) \approx I^2 \cdot (R_0 + R_{\text{ct}})$.
- The second term represents reversible entropic reaction heat: $\dot{Q}_{\text{rev}} = -I \cdot T \frac{\partial V_{\text{ocv}}}{\partial T}$.

**Model Assumptions and Boundary Conditions:**
1. **Irreversible Dominance:** Irreversible overpotential heating dominates the short 5.0 s pulse. Reversible entropic heat remains below $0.005\text{ W}$ ($|\partial V_{\text{ocv}}/\partial T| \approx 10\text{ to }30\ \mu\text{V/K}$) [TO VERIFY] and is neglected.
2. **Adiabatic Worst-Case:** The model assumes zero heat dissipation to ambient air or copper Kelvin clamps. This assumption bounds the maximum core temperature rise.
3. **Lumped Thermal Mass:** The model assumes a uniform cell core temperature. Lumped thermal capacitance is $C_{\text{th}} = m \cdot C_p = 0.045\text{ kg} \times 830\text{ J}/(\text{kg}\cdot\text{K}) = 37.35\text{ J/K}$.
4. **Defect Non-Equivalence:** Lumped models evaluate bulk heat from external current. They do NOT model localized current filaments inside damaged separators.

#### B. Self-Heating Onset vs. Separator Melt
Self-accelerating thermal runaway does not require separator melting ($135^\circ\text{C}\text{ to }160^\circ\text{C}$). Self-accelerating exotherms initiate when the Solid Electrolyte Interphase (SEI) decomposes:
- Solid Electrolyte Interphase (SEI) decomposition onset: $T_{\text{onset}} \approx 80.0^\circ\text{C}\text{ to }90.0^\circ\text{C}$ [TO VERIFY: Literature accelerating rate calorimetry (ARC) onset range for fresh and degraded cells, e.g., Feng et al. 2018].
- Nominal ambient baseline: $T_{\text{amb}} = 25.0^\circ\text{C}$.
- Available thermal headroom to self-heating onset: $\Delta T_{\text{margin}} = T_{\text{onset}} - T_{\text{amb}} = 55.0^\circ\text{C}$.

#### C. Parametric Script Simulation Output
The energy budget script (`.spec/calc/thermal_budget.py`) calculates test dissipation across Phase 1 ($0.755\text{ A}$ discharge, $5.0\text{ s}$) and Phase 3 ($0.200\text{ A}$ micro-charge, $25.0\text{ s}$):

```text
==================================================================================
CELLCHECK PULSEPOD: BOUNDED TEST-ENERGY & ADIABATIC HEATING ANALYSIS
==================================================================================
Cell Thermal Mass (m * Cp):    37.35 J/degC (m = 45.0 g, Cp = 830 J/(kg*K))
Ambient Temperature (T_amb):    25.0 degC
Self-Heating Onset (T_onset):   80.0 degC [TO VERIFY: SEI breakdown threshold]
Available Headroom to Onset:    55.0 degC
----------------------------------------------------------------------------------
TABLE 1: Scenario Breakdown Across Phase 1 Discharge and Phase 3 Micro-Charge
Scenario                     | I_p1(A) | E_p1(J)  | E_p3(J)  | E_tot(J) | dT_core(C) | Margin (x)
--------------------------------------------------------------------------------------------
Healthy Cell (Samsung 25R)   | 0.755   | 0.1566   | 0.0550   | 0.2116   | 0.00567    | 9706.4    
Aged Cell (70% SoH)          | 0.750   | 0.3371   | 0.1200   | 0.4571   | 0.01224    | 4494.5    
High-R0 Degraded Cell        | 0.710   | 1.2612   | 0.5000   | 1.7612   | 0.04716    | 1166.4    
Extreme High-Impedance Cell  | 0.633   | 2.8078   | 1.4000   | 4.2078   | 0.11266    | 488.2     
--------------------------------------------------------------------------------------------

TABLE 2: Sensitivity Table - Phase 1 Adiabatic Core Heating dT (deg C)
Fixed R_load = 5.0 Ohm (I = 3.8V / (5.0 + R0)), overpotential factor (R0 + Rct, where Rct ~ 0.5*R0)
R0 (mOhm)  | I_p1 (A) | P_p1 (W) | t = 2.0s   | t = 5.0s   | t = 10.0s  | Orders Below Onset
----------------------------------------------------------------------------------------
20.0       | 0.757    | 0.0172   | 0.00092    | 0.00230    | 0.00460    | 23900x (~4 orders)
35.0       | 0.755    | 0.0299   | 0.00160    | 0.00400    | 0.00801    | 13739x (~4 orders)
50.0       | 0.752    | 0.0425   | 0.00227    | 0.00568    | 0.01137    | 9675x (~4 orders) 
70.0       | 0.750    | 0.0590   | 0.00316    | 0.00790    | 0.01579    | 6965x (~3 orders) 
100.0      | 0.745    | 0.0833   | 0.00446    | 0.01115    | 0.02230    | 4934x (~3 orders) 
150.0      | 0.738    | 0.1225   | 0.00656    | 0.01640    | 0.03280    | 3354x (~3 orders) 
250.0      | 0.724    | 0.1965   | 0.01052    | 0.02630    | 0.05260    | 2091x (~3 orders) 
350.0      | 0.710    | 0.2649   | 0.01418    | 0.03546    | 0.07091    | 1551x (~3 orders) 
500.0      | 0.691    | 0.3580   | 0.01917    | 0.04793    | 0.09585    | 1148x (~3 orders) 
1000.0     | 0.633    | 0.6017   | 0.03222    | 0.08054    | 0.16109    | 683x (~3 orders)  
----------------------------------------------------------------------------------------

TABLE 3: Constant-Current Sensitivity Matrix for 5.0 s Pulse (dT in deg C)
R_eff (R0+Rct)   | I = 0.50 A   | I = 0.755 A  | I = 1.00 A   | I = 1.50 A   | I = 2.50 A (Fuse) 
--------------------------------------------------------------------------------------------
52.5 mOhm        | 0.00176 C    | 0.00401 C    | 0.00703 C    | 0.01581 C    | 0.04393 C         
105.0 mOhm       | 0.00351 C    | 0.00801 C    | 0.01406 C    | 0.03163 C    | 0.08785 C         
225.0 mOhm       | 0.00753 C    | 0.01717 C    | 0.03012 C    | 0.06777 C    | 0.18825 C         
525.0 mOhm       | 0.01757 C    | 0.04006 C    | 0.07028 C    | 0.15813 C    | 0.43926 C         
750.0 mOhm       | 0.02510 C    | 0.05723 C    | 0.10040 C    | 0.22590 C    | 0.62751 C         
--------------------------------------------------------------------------------------------
```

#### D. Bounded Safety Conclusion
**Under the stated assumptions, test-induced heating is 2 to 4 orders of magnitude below the self-heating onset temperature. This does not guarantee safety for cells with pre-existing internal defects.**

### 5.2 Load Resistor Thermal Margin
- Peak power dissipation in load resistor during pulse:
  $$P_{\text{load}} = I^2 R_{\text{load}} = (0.755\text{ A})^2 \times 5.0\ \Omega = 2.85\text{ Watts}$$
- Resistor continuous rating: Ohmite 850 aluminum-housed wirewound resistor rated at $10.0\text{ Watts}$.
- Safety Operating Margin:
  $$\text{Margin} = \frac{10.0\text{ W}}{2.85\text{ W}} = 3.51\times\quad (351\%\text{ safe derating headroom})$$
- Average continuous power across the 60-second cycle:
  $$P_{\text{avg}} = \frac{2.85\text{ W} \times 5.0\text{ s}}{60.0\text{ s}} = 0.238\text{ Watts}$$
- Convection cooling through ambient chassis venting is sufficient. No active cooling fan is required.

### 5.3 Residual Risk Analysis

1. **Pre-Existing Internal Defects:**
   - A standard 18650 cell stores approximately $33\text{ kJ}$ of chemical energy ($3.7\text{ V} \times 2.5\text{ Ah} \times 3600\text{ s/h}$).
   - Cells with internal defects (copper dendrites, lithium plating, damaged separator) can self-heat from internal energy.
   - The test instrument does not supply the initiation energy.
   - An abusive cell with a $0.35\ \Omega$ resistance does NOT represent an internal micro-short. An internal short creates a localized current path inside the core.

2. **Phase 3 Charge Injection Risk:**
   - Phase 3 injects $200\text{ mA}$ through the TP4056 charge management IC.
   - Charging suspect or degraded cells is the highest-risk phase.
   - Micro-charge current can stimulate dendrite growth or precipitate separator puncture.
   - Firmware must gate Phase 3. Phase 3 shall execute only if Phases 0, 1, and 2 pass with no anomaly flags.

3. **Component Failure Modes & Galvanic Fuse Behavior:**
   - **Galvanic Fuse Specification & Placement:**
     - Part: Littelfuse 216 Series fast-acting ceramic cartridge (`021602.5MXP`, 5x20 mm, 2.5 A rating).
     - Breaking capacity: 1500 A @ 250 VAC.
     - DC voltage rating: TO VERIFY (not specified in standard Littelfuse 216 datasheet).
     - Nominal cold resistance: $0.0584\ \Omega$ ($58.4\text{ m}\Omega$).
     - Nominal melting $I^2 t$: $2.70\text{ to }3.67\text{ A}^2\text{s}$ [TO VERIFY: Littelfuse 216 datasheet].
     - Physical placement: The fuse sits in a cartridge clip mounted directly adjacent to the positive clamp jaw. This placement protects the high-current wiring and instrument circuitry. The fuse protects external wiring and electronics; it does NOT protect against an internal defect inside the cell itself.
   - **Prospective Short-Circuit Current and Clearing Dynamics:**
     If the load resistor or MOSFET fails shorted, prospective short-circuit current is governed by cell voltage, cell internal resistance, and wiring resistance:
     $$I_{\text{sc}} = \frac{V_{\text{cell}}}{R_{\text{cell}} + R_{\text{wiring}}}$$
     Assuming nominal cell voltage $V_{\text{cell}} = 3.8\text{ V}$ and fresh cell resistance $R_{\text{cell}} = 0.035\ \Omega$:
     - For $R_{\text{wiring}} = 0.05\ \Omega$:
       $$R_{\text{total}} = 0.085\ \Omega \implies I_{\text{sc}} = \frac{3.8\text{ V}}{0.085\ \Omega} = 44.7\text{ A}\quad (17.9\times I_n)$$
       Melting energy clearing time $t_{\text{clear}} \approx \frac{I^2 t}{I^2} = \frac{2.70\text{ to }3.67}{44.7^2} = 1.35\text{ to }1.84\text{ ms}$. Datasheet time-current curve range: $1.4\text{ to }3.0\text{ ms}$ [TO VERIFY: Littelfuse 216 curve].
     - For $R_{\text{wiring}} = 0.10\ \Omega$:
       $$R_{\text{total}} = 0.135\ \Omega \implies I_{\text{sc}} = \frac{3.8\text{ V}}{0.135\ \Omega} = 28.1\text{ A}\quad (11.2\times I_n)$$
       Melting energy clearing time $t_{\text{clear}} \approx \frac{2.70\text{ to }3.67}{28.1^2} = 3.42\text{ to }4.65\text{ ms}$. Datasheet time-current curve range: $3.4\text{ to }6.0\text{ ms}$ [TO VERIFY: Littelfuse 216 curve].
     - For $R_{\text{wiring}} = 0.20\ \Omega$:
       $$R_{\text{total}} = 0.235\ \Omega \implies I_{\text{sc}} = \frac{3.8\text{ V}}{0.235\ \Omega} = 16.2\text{ A}\quad (6.5\times I_n)$$
       From the Littelfuse 216 time-current envelope (between $4.0 I_n = 10\text{ A}$ and $10 I_n = 25\text{ A}$), clearing time is $10\text{ to }50\text{ ms}$ [TO VERIFY: Littelfuse 216 curve].
     - The earlier specification claim of "clears in < 1.8 ms" is replaced by the bounded range: $1.4\text{ ms to }50\text{ ms}$ depending on total wiring and contact impedance.
   - **MOSFET Fails Shorted:** Current flows continuously through the $5.0\ \Omega$ load resistor ($I \approx 0.755\text{ A}$). Resistor dissipates $2.85\text{ W}$. The 2.5 A fuse does not clear at $0.755\text{ A}$. Over minutes, the load resistor overheats. Mitigation: Operator activates the manual Emergency Stop or avionics toggle to break the gate circuit physically.
   - **Load Resistor Fails Shorted:** Causes a terminal short circuit ($I_{\text{sc}} \approx 16.2\text{ A to }44.7\text{ A}$). Littelfuse 216 fuse clears in $1.4\text{ ms to }50\text{ ms}$.
   - **Load Resistor Fails Open:** Current drops to zero ($I = 0$). Test aborts with no thermal hazard.
   - **Galvanic Fuse Fails to Clear:** If a dead short occurs and the fuse fails, high fault current can vent the cell. Tested under Tracker V10.

4. **Operator Handling Errors:**
   - Operators can drop damaged cells or cause external terminal bridging during insertion.
   - Testing must occur in a dedicated fireproof tray with safety shields.

### 5.4 Failure Mode and Effects Analysis (FMEA)

| Failure Mode | Failure Effect | Detection Mechanism | Mitigation Strategy | Protection Class |
|---|---|---|---|---|
| **Cell Internal Micro-Short** | Stored energy self-heating; thermal event | MLX90614 detects crimp $\Delta T > 1.2^\circ\text{C/s}$ or $T > 45^\circ\text{C}$; INA226 detects voltage sag | Abort test; lockout Phase 3; isolate cell in fireproof sand bucket | Firmware-Dependent |
| **MOSFET Fails Short** | Continuous $0.755\text{ A}$ discharge; resistor heating | Software watchdog checks load current when gate is OFF | Open aircraft toggle; strike E-Stop; passive pulldown clamps gate | Hardware-Only (Switches) |
| **Load Resistor Short** | Direct terminal short circuit ($I > 16\text{ A}$) | INA226 current rail saturation; voltage collapse | Littelfuse 216 2.5A (021602.5MXP) fast ceramic cartridge clears circuit in 1.4 ms to 50 ms | Hardware-Only |
| **TP4056 Latch-Up** | Continuous unregulated charge current | INA226 measures negative current during rest phases | Disable GPIO27 regulator enable pin; isolate power rail | Firmware-Dependent |
| **I2C Bus Lockup** | MLX90614 and INA226 telemetry freezes | Hardware watchdog timer resets ESP32 MCU | Gate pulldown (10 kΩ) disconnects load when MCU resets | Hardware-Only (Pulldown) |
| **Low Emissivity Read** | MLX90614 under-reports crimp temperature | Operator visual check; ambient baseline cross-check | Apply high-emissivity matte dot ($\varepsilon \ge 0.95$) before clamp | Operational Procedure |

*Note: Firmware-dependent safety layers require operational MCU and bus health. They do not constitute independent safety layers under functional safety standards.*

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
