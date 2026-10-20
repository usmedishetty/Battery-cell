# Protocol & Data Schemas (Schema)
**Document ID:** `CC-SPEC-SCHM-v4.0`  
**System Name:** CellCheck PulsePod  
**Standard Compliance:** JSON Schema Draft 2020-12, W3C Verifiable Credentials 1.1, OpenViking Spec v2.1  

---

## 1. W3C Battery Passport Credential JSON Schema (EU 2023/1542)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://cellcheck.id/schemas/v4/battery-passport.json",
  "title": "CellCheckBatteryPassport",
  "description": "Cryptographically signed W3C Verifiable Credential conforming to EU Battery Directive (EU 2023/1542)",
  "type": "object",
  "required": [
    "@context",
    "id",
    "type",
    "issuer",
    "issuanceDate",
    "credentialSubject",
    "proof"
  ],
  "properties": {
    "@context": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 2
    },
    "id": {
      "type": "string",
      "format": "uri"
    },
    "type": {
      "type": "array",
      "items": { "type": "string" },
      "contains": { "const": "BatteryPassCredential" }
    },
    "issuer": {
      "type": "string",
      "pattern": "^did:cellcheck:CP-ESP32-[A-Fa-f0-9]{4}-[A-Fa-f0-9]{4}$"
    },
    "issuanceDate": {
      "type": "string",
      "format": "date-time"
    },
    "credentialSubject": {
      "type": "object",
      "required": [
        "cellSerial",
        "formFactor",
        "chemistry",
        "ratedCapacityAh",
        "measuredStateOfHealth",
        "conformalTier",
        "conformalCoverage",
        "electrochemicalMetrics",
        "circularityValuation"
      ],
      "properties": {
        "cellSerial": { "type": "string" },
        "formFactor": { "enum": ["18650", "20700", "21700", "26650", "POUCH_CUSTOM"] },
        "chemistry": { "enum": ["NMC", "LFP", "LCO", "NCA"] },
        "ratedCapacityAh": { "type": "number", "minimum": 0.5, "maximum": 20.0 },
        "measuredStateOfHealth": { "type": "number", "minimum": 0.0, "maximum": 120.0 },
        "conformalTier": { "enum": ["TIER_A", "TIER_B", "TIER_C_RECYCLE", "RETEST"] },
        "conformalCoverage": { "type": "number", "minimum": 0.80, "maximum": 1.00 },
        "electrochemicalMetrics": {
          "type": "object",
          "required": [
            "r0_ohmic_mohm",
            "r_ct_charge_transfer_mohm",
            "c_dl_capacitance_farad",
            "crimp_thermal_rise_c",
            "acoustic_attenuation_db",
            "current_ripple_variance"
          ],
          "properties": {
            "r0_ohmic_mohm": { "type": "number", "minimum": 5.0, "maximum": 500.0 },
            "r_ct_charge_transfer_mohm": { "type": "number", "minimum": 2.0, "maximum": 500.0 },
            "c_dl_capacitance_farad": { "type": "number", "minimum": 0.05, "maximum": 25.0 },
            "crimp_thermal_rise_c": { "type": "number", "minimum": -2.0, "maximum": 20.0 },
            "acoustic_attenuation_db": { "type": "number", "minimum": -60.0, "maximum": 5.0 },
            "current_ripple_variance": { "type": "number", "minimum": 0.0 }
          }
        },
        "circularityValuation": {
          "type": "object",
          "required": [
            "fairMarketResaleUSD",
            "avoidedCarbonFootprintKgCO2e",
            "scrapRecycleValueUSD",
            "recommendedSecondLife"
          ],
          "properties": {
            "fairMarketResaleUSD": { "type": "number", "minimum": 0.0 },
            "avoidedCarbonFootprintKgCO2e": { "type": "number", "minimum": 0.0 },
            "scrapRecycleValueUSD": { "type": "number", "minimum": 0.0 },
            "recommendedSecondLife": { "type": "string" }
          }
        }
      }
    },
    "proof": {
      "type": "object",
      "required": [
        "type",
        "created",
        "verificationMethod",
        "proofPurpose",
        "proofValue",
        "calibrationHash"
      ],
      "properties": {
        "type": { "const": "Ed25519Signature2020" },
        "created": { "type": "string", "format": "date-time" },
        "verificationMethod": { "type": "string" },
        "proofPurpose": { "const": "assertionMethod" },
        "proofValue": { "type": "string" },
        "calibrationHash": { "type": "string", "minLength": 16, "maxLength": 16 }
      }
    }
  }
}
```

---

## 2. Edge Binary Telemetry Stream Frame Specification

Core 0 serializes telemetry records into packed 20-byte binary frames sent over USB CDC and BLE GATT:

```c
#include <stdint.h>

/**
 * @brief Packed 20-byte telemetry frame streamed at 100 Hz by ESP32 Core 0.
 * Endianness: Little-Endian (Standard Xtensa / ARM byte order).
 */
typedef struct __attribute__((__packed__)) {
    uint32_t timestamp_ms;        // Byte 0-3:   Elapsed time from trigger actuation (ms)
    uint16_t voltage_mv;          // Byte 4-5:   Cell terminal voltage (0 - 5000 mV)
    int16_t  current_ma;          // Byte 6-7:   Shunt current (-3000 mA to +3000 mA)
    int16_t  vent_temp_c_x100;    // Byte 8-9:   MLX90614 temperature (e.g. 2480 = 24.80 °C)
    int16_t  real_z_mohm;         // Byte 10-11: Extracted real impedance Z' (mΩ)
    int16_t  imag_z_mohm;         // Byte 12-13: Extracted imaginary impedance Z'' (mΩ)
    int16_t  acoustic_amp_mv;     // Byte 14-15: 40 kHz ultrasonic envelope peak (mV)
    uint8_t  phase_state;         // Byte 16:    0=P0, 1=P1, 2=P2, 3=P3, 4=MINT, 5=TRIP
    uint8_t  reserved_pad;        // Byte 17:    Alignment pad / future expansion
    uint8_t  crc8_checksum;       // Byte 18:    CRC-8/MAXIM calculated over bytes 0-17
    uint8_t  frame_delimiter;     // Byte 19:    Constant frame tail: 0xAA
} TelemetryFrame_t;

_Static_assert(sizeof(TelemetryFrame_t) == 20, "TelemetryFrame_t must be exactly 20 bytes");
```

---

## 3. OpenViking (`viking://`) ML Registry Schema

The OpenViking specification defines the deployment packaging for the monotonic model and conformal calibration set:

```yaml
viking_format_version: "2.1.0"
model_identifier: "viking://models/cellcheck/triage-monotonic-xgb:v4.0"
model_metadata:
  model_name: "CellCheck Monotonic Triage Classifier"
  release_date: "2026-10-20T07:00:00Z"
  framework: "XGBoost"
  framework_version: "2.0.3"
  model_sha256: "9e5c7a3f814b62d8e0f91a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d"

hyperparameters:
  booster: "gbtree"
  n_estimators: 120
  max_depth: 4
  learning_rate: 0.05
  monotone_constraints: "(1, -1, 1, 1, -1, 1, 1, 0)"
  objective: "multi:softprob"
  num_class: 3

training_manifest:
  datasets:
    - repository: "NASA_Ames_Prognostics_Center_of_Excellence"
      collection: "Li-ion Battery Aging Datasets B0005, B0006, B0007, B0018, B0056"
      cell_count: 34
    - repository: "Oxford_University_Battery_Intelligence_Lab"
      collection: "Oxford Battery Degradation Dataset 1"
      cell_count: 8
    - repository: "CALCE_Battery_Research_Group"
      collection: "CS2 Series Cylindrical & Prismatic Life Profiles"
      cell_count: 12
  validation_strategy: "Strict_Cell_Wise_GroupKFold"
  k_splits: 5
  zero_leakage_verified: true

conformal_calibration:
  method: "Split_Conformal_Prediction"
  coverage_target_1_minus_alpha: 0.950
  calibration_sample_size: 480
  conformal_quantile_q_hat: 0.8412
  nonconformity_metric: "one_minus_softmax_probability"
  rejection_behavior: "OUTPUT_RETEST_ON_AMBIGUOUS_SET"
```
