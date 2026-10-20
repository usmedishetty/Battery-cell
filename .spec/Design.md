# Design Contract (Design)
**Document ID:** `CC-SPEC-DSGN-v4.0`  
**System Name:** CellCheck PulsePod  
**Standard Compliance:** ASD-STE100, OpenDesign Tokens, IEC 60073 (Colors of Indicators and Actuators)  

---

## 1. OpenDesign System Design Tokens

```text
┌──────────────────────┬──────────┬──────────────────────────────────────────────────────────────┐
│ TOKEN IDENTIFIER     │ VALUE    │ FUNCTIONAL DESIGN APPLICATION                                │
├──────────────────────┼──────────┼──────────────────────────────────────────────────────────────┤
│ `--color-bg-base`    │ `#0B0F19`│ Primary background for companion dashboard & OLED display    │
│ `--color-surface`    │ `#161F30`│ Card background, chart panels, and front panel acrylic finish│
│ `--color-tier-a`     │ `#10B981`│ Tier A indicator (Emerald Green): EV / High-Drain Second Life│
│ `--color-tier-b`     │ `#F59E0B`│ Tier B indicator (Amber Yellow): Solar Energy Reserve Storage│
│ `--color-tier-c`     │ `#EF4444`│ Tier C indicator (Ruby Red): Immediate Pyrometallurgical Scrap│
│ `--color-retest`     │ `#EC4899`│ Retest indicator (Magenta Pink): Conformal Uncertainty Gate  │
│ `--color-accent-blue`│ `#3B82F6`│ Active pulse status indicator and dynamic Nyquist trace line │
│ `--color-text-main`  │ `#F9FAFB`│ Primary high-contrast tabular numeric readouts & headings    │
│ `--color-text-muted` │ `#9CA3AF`│ Secondary units, parameter labels, and W3C DID timestamps    │
└──────────────────────┴──────────┴──────────────────────────────────────────────────────────────┘
```

---

## 2. Enclosure & Physical Ergonomics Contract

1. **Chassis Dimensions & Materials:**
   - Outer Envelope: $160\text{ mm (Width)} \times 110\text{ mm (Depth)} \times 55\text{ mm (Height)}$.
   - Chassis Body: $3.0\text{ mm}$ optical-grade transparent PMMA acrylic.
   - Base Plate: $3.0\text{ mm}$ matte-black extruded acrylic with four non-slip silicone feet ($12\text{ mm}$ diameter, Shore A 50) to absorb clamping torque.
   - Mechanical Fasteners: M3 $\times 12\text{ mm}$ stainless steel hex standoffs and black nylon washers.

2. **Operator Interface Layout:**
   - **Left Zone:** Universal Delrin 4-wire Kelvin V-groove clamp with knurled aluminum tension adjustment thumbscrew ($M6 \times 20\text{ mm}$).
   - **Center Zone:** $1.3\text{-inch}$ monochrome I2C OLED display (SH1106 controller) protected by a $2.0\text{ mm}$ flush-mounted scratch-resistant acrylic window.
   - **Right Zone (Actuation & Safety):**
     - Aircraft Master Arm toggle switch equipped with an anodized red spring-loaded flip safety guard (APEM A01 series equivalent).
     - Sanwa-style $30\text{ mm}$ arcade pushbutton (Red dome, low-friction microswitch, snap-action actuation).
     - Industrial $22\text{ mm}$ mushroom latching Emergency Stop switch (Twist-to-release, NC contacts mechanically wired in series with the MOSFET gate resistor).

3. **Sensor Alignment Mechanical Shroud:**
   - A 3D-printed shroud (black PETG, $0.15\text{ mm}$ layer height) suspends the Melexis MLX90614 infrared thermopile $8.0\text{ mm} \pm 0.5\text{ mm}$ directly above the positive cell terminal cap.
   - The shroud limits peripheral thermal field-of-view (FOV) to a $12\text{ mm}$ circular spot centered on the PTC crimp seal.

---

## 3. Visual Display & Oscilloscope Specifications

### 3.1 1.3-Inch Local OLED Display Layout ($128 \times 64$ Pixels)
```text
 ┌──────────────────────────────────────────────────────────┐
 │ NMC 18650  |  Vocv: 3.820V  |  T: 24.8°C  [ARMED]        │ ◄── Header Row (8 px)
 ├────────────────────────────┬─────────────────────────────┤
 │ -Z'' (mΩ)                  │ R0:    24.8 mΩ              │
 │   12 ┼       *             │ R_ct:  18.2 mΩ              │
 │    8 ┼    *     *          │ C_dl:  1.45 F               │
 │    4 ┼  *         *        │ Phase: 0.16 rad             │
 │    0 ┴──┴─────────┴──► Z'  │                             │
 │         24        43       │ GRADE: [ TIER A ]           │
 ├────────────────────────────┴─────────────────────────────┤
 │ PROGRESS: [████████████████████████████████] 60.0s (DONE)│ ◄── Progress Bar (6 px)
 └──────────────────────────────────────────────────────────┘
```
- **Left Panel ($64 \times 50\text{ px}$):** Live Cole-Cole Nyquist arc rendered at $30\text{ FPS}$. Real impedance ($Z'$) maps to horizontal pixels; negative imaginary impedance ($-Z''$) maps to vertical pixels.
- **Right Panel ($64 \times 50\text{ px}$):** Real-time tabular readout displaying computed $R_0$, $R_{\text{ct}}$, $C_{\text{dl}}$, and the conformal classification verdict.

### 3.2 Client-Side Offline SVG Oscilloscope (Phone Browser)
When an auditor scans the QR passport:
1. The browser launches a self-contained WebAssembly page (`cellcheck.id/verify`).
2. The page parses the Base64-encoded W3C credential and renders an interactive vector SVG chart.
3. The horizontal axis represents elapsed test time ($0.0\text{ to }60.0\text{ s}$). The vertical axis represents terminal voltage ($2.50\text{ to }4.25\text{ V}$).
4. The user can touch-scrub across the curve to inspect:
   - Instantaneous Ohmic voltage step ($\Delta V_0$) at $t = 5.020\text{ s}$.
   - Double-layer exponential relaxation tangent between $t = 10.0\text{ s}$ and $t = 35.0\text{ s}$.
   - Reference envelope overlays showing $95\%$ confidence corridors derived from the NASA Ames PCoE database.

### 3.3 Physical Thermal Passport Sticker Geometry
```text
 ┌──────────────────────────────────────────────────────────┐
 │  ┌─────────────────────────┐  CELLCHECK BATTERY PASSPORT │
 │  │ █▀▀▀▀▀█ ▄ █▄█ █▀▀▀▀▀█   │  ========================== │
 │  │ █ ███ █ ▄█▄ ▄ █ ███ █   │  SERIAL: INR18650-25R-9041A │
 │  │ █ ▀▀▀ █ █ ▄ █ █ ▀▀▀ █   │  GRADE:  [ TIER A - EV ]    │
 │  │ ▀▀▀▀▀▀▀ ▀ █ ▀ ▀▀▀▀▀▀▀   │  HEALTH: 92.4% SoH (95% CI) │
 │  │ █ ▄▄█▀▀▄█▀▄ █▄█▄▄█▄▄█   │  VALUATION: $7.80 USD       │
 │  │ █▀ █ ▀▄▀▀▄ ▄█▄ ▀▄ ▄▄█   │  R0: 24.8 mΩ | R_ct: 18.2mΩ │
 │  │ █▀▀▀▀▀█ █ ▄█▄ █ ▀ █▄█   │  CAL_HASH: b47e2a91f0c3a812 │
 │  │ █ ███ █ █▄▄ ▄▄█▀█▀▄ █   │  -------------------------- │
 │  │ █ ▀▀▀ █ ▄█ ▄▀▄█▄▀█▀▄█   │  ED25519 VERIFIED PASSPORT  │
 │  │ ▀▀▀▀▀▀▀ ▀▀  ▀ ▀▀  ▀▀▀   │  EU REGULATION 2023/1542    │
 │  └─────────────────────────┘  SCAN FOR LIVE FORENSIC PLOT│
 └──────────────────────────────────────────────────────────┘
```
- **Label Dimensions:** $57.0\text{ mm (Width)} \times 32.0\text{ mm (Height)}$ standard direct thermal peel-and-stick stock.
- **QR Geometry:** $25.0\text{ mm} \times 25.0\text{ mm}$ square matrix (Version 6, $41 \times 41$ modules, Error Correction Level M: $15\%$ recovery).

---

## 4. Acoustic Sonification & Sound Profile Contract

The instrument sonifies electrochemical kinetics to provide operators with immediate acoustic feedback:

1. **Relaxation Glissando Formula:**
   $$f(t) = f_{\text{min}} + \left( \frac{V(t) - V_{\text{trough}}}{V_{\text{baseline}} - V_{\text{trough}}} \right)^2 \times (f_{\text{max}} - f_{\text{min}})$$
   - Minimum frequency: $f_{\text{min}} = 300\text{ Hz}$.
   - Maximum frequency: $f_{\text{max}} = 1500\text{ Hz}$.
   - Duty cycle: $50\%$ square wave generated via ESP32 LEDC PWM timer.

2. **Auditory Diagnostic Signatures:**
   - **Tier A (Pristine Kinetics):** Voltage rebounds rapidly. The buzzer outputs a crisp, ascending glissando sweeping from $300\text{ Hz}$ to $1500\text{ Hz}$ in under $1.2\text{ seconds}$.
   - **Tier B (Aged Kinetics):** Moderate SEI resistance slows recovery. The frequency rises steadily from $300\text{ Hz}$ to $950\text{ Hz}$ over $6.0\text{ seconds}$.
   - **Tier C (Degraded / Hazard):** Severe internal resistance and electrolyte dry-out. The buzzer emits a flat, sluggish drone rising from $300\text{ Hz}$ to only $420\text{ Hz}$ over $15\text{ seconds}$.

3. **Auditory Status Cues:**
   - **System Arm:** Single $80\text{ ms}$ chirp at $880\text{ Hz}$ (A5).
   - **Test Complete (Valid Pass):** Ascending major third chime: $523\text{ Hz}$ (C5) for $100\text{ ms}$, followed by $659\text{ Hz}$ (E5) for $150\text{ ms}$.
   - **Safety Abort / Thermal Trip:** Continuous rapid pulsing tone at $220\text{ Hz}$ at $4\text{ Hz}$ repetition rate until manually reset.
