# Anti-Slop & Agent Directives (Rules)
**Document ID:** `CC-SPEC-RULE-v4.0`  
**System Name:** CellCheck PulsePod  
**Standard Compliance:** ASD-STE100 (Simplified Technical English), ISO/IEC/IEEE 29148:2018  

---

## 1. ASD-STE100 Simplified Technical English Constraints

All documentation, technical specifications, and user-facing copy must adhere to ASD-STE100 principles:

1. **Sentence Structure:**
   - Write one instruction or thought per sentence.
   - Limit sentence length to a maximum of 20 words in procedural text and 25 words in descriptive text.
   - Use the active voice. Identify the actor in every operational statement.
   - *Prohibited:* "The load is disconnected by the safety task when the temperature rises."
   - *Mandatory:* "The safety task disconnects the load if the temperature rises."

2. **Grammar & Lexicon Rules:**
   - Use only words that are approved in the ASD-STE100 lexicon or explicitly defined in the project glossary.
   - Do not use verbs as nouns or nouns as verbs. (Do not write: "To solution this problem..." Write: "To solve this problem...")
   - State the condition before the action. (Write: "If the voltage is below 2.5V, stop the test." Do not write: "Stop the test if the voltage is below 2.5V.")
   - Avoid ambiguous modal verbs. Use "shall" for mandatory requirements, "must" for physical constraints, and "may" for optional allowances. Never use "should".

3. **Anti-Slop Directives (Marketing Terminology Prohibition):**
   - Eliminate marketing adjectives, subjective superlatives, and buzzwords.
   - The following words are permanently banned from specification text:
     `revolutionary`, `game-changing`, `miraculous`, `lightning-fast`, `groundbreaking`, `unrivaled`, `world-first`, `disruptive`, `masterpiece`.
   - **Banned Absolute Safety Terms:** Never use absolute safety claims. The following terms are permanently banned from safety statements:
     `impossible`, `zero-hazard`, `zero hazard`, `cannot fail`, `cannot trigger`, `cannot induce`, `guaranteed`.
   - Replace absolute statements with bounded operating limits, model assumptions, order-of-magnitude margins, and explicit residual risk disclosures.
   - Replace subjective claims with quantitative metrics, test conditions, and statistical boundaries.

---

## 2. Hard Non-Negotiable Engineering Directives

The CellCheck architecture enforces the following invariants:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        NON-NEGOTIABLE ARCHITECTURAL DIRECTIVES                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ RULE 1: Never claim a 93% triage agreement rate without citing the specific validation  │
│         partition, sample size (n), confidence interval, and cycler protocol.          │
│ RULE 2: Never omit the two-point affine calibration step in the TD-EIS protocol. Every │
│         minted passport must embed an immutable CAL_HASH verified against NVS flash.   │
│ RULE 3: Never execute a discharge pulse if baseline open-circuit voltage is below      │
│         2.50V. Over-discharged cells create copper dissolution and internal fire risks.│
│ RULE 4: Never issue a single-tier classification guess when conformal prediction set   │
│         size |C(x)| != 1. The instrument must output "RETEST / INCONCLUSIVE".          │
│ RULE 5: Never use 2-wire sensing for Ohmic resistance extraction. Current force leads  │
│         and voltage sense leads must maintain physical isolation to the terminal cap.  │
│ RULE 6: Never execute blocking wait loops inside FreeRTOS Core 0 tasks. All ADC and    │
│         sensor polling must utilize hardware timers and non-blocking state flags.      │
│ RULE 7: Never store unencrypted private signing keys in companion software. Hardware   │
│         attestation signatures must originate inside the ESP32 secure eFuse subsystem. │
│ RULE 8: Never make absolute safety claims (such as "zero-hazard" or "impossible to     │
│         trigger thermal runaway"). Safety cases must state model assumptions, thermal  │
│         margins to self-heating onset, and residual risk from internal cell defects.   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Agent Bootstrapping & Contribution Protocol

Any artificial intelligence agent or human software engineer contributing code to this repository must follow this bootstrapping sequence:

### Step 1: Sequential Specification Ingestion
Do not write code before completing this sequence. Read the 8 foundational specification files in this exact order:
1. `.spec/PRD.md` $\rightarrow$ Understand personas, boundaries, and acceptance criteria.
2. `.spec/TechSpec.md` $\rightarrow$ Understand hardware constraints, sampling rates, and ML formulas.
3. `.spec/Architecture.md` $\rightarrow$ Understand compute boundaries, pin mappings, and trust flows.
4. `.spec/AppFlow.md` $\rightarrow$ Understand state machine transitions and recovery actions.
5. `.spec/Design.md` $\rightarrow$ Understand display tokens, label geometry, and audio formulas.
6. `.spec/Rules.md` $\rightarrow$ Understand ASD-STE100 writing constraints and non-negotiable invariants.
7. `.spec/Schema.md` $\rightarrow$ Bind all data structures to declared JSON and binary schemas.
8. `.spec/Tracker.md` $\rightarrow$ Map every implementation commit to a testable acceptance criterion.

### Step 2: Implementation Invariants
1. **Schema Compliance:** Every data payload generated by edge firmware, companion software, or cloud APIs must validate against the schemas declared in `.spec/Schema.md`.
2. **Firmware Hygiene:** Firmware code targeting the ESP32 must compile with zero compiler warnings under `-Wall -Werror -Wextra`.
3. **Machine Learning Integrity:** Training scripts must enforce cell-wise `GroupKFold` partitioning. Shuffling cycle rows across training and validation partitions will cause immediate PR rejection.
4. **Test-Driven Acceptance:** No PR shall be merged without unit tests verifying that all modified routines maintain the quantitative thresholds specified in `.spec/Tracker.md`.
