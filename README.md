# SIH26155 — AI-Driven Multi-Vendor Network Security Compliance Auditor

> **Smart India Hackathon 2026 · SIH26155 · NTRO · Blockchain & Cybersecurity**

An AI-augmented, vendor-agnostic security compliance engine for heterogeneous network infrastructure.

The platform transforms proprietary network-device configurations into a **common Security Baseline Model (SBM)**, evaluates that model against security frameworks, identifies previously unseen configuration semantics through a human-in-the-loop AI workflow, and produces evidence-backed, vendor-specific remediation and reports.

---

## Why this exists

Enterprise networks are heterogeneous by design: firewalls, routers, switches, SASE platforms, white-box networking, and cloud-native controls may all use different configuration languages and structures.

Traditional auditing approaches tend to become either:

- manual, checklist-heavy processes, or
- vendor-specific tooling that becomes difficult to extend across new devices, operating-system versions, and configuration formats.

**SIH26155 asks us to bridge that gap.**

Our core idea is to separate **vendor syntax** from **security meaning**.

```text
Vendor Configuration
        │
        ▼
  Vendor Detection
        │
        ▼
  Vendor Parser / AI Semantic Resolver
        │
        ▼
 Facts + Evidence
        │
        ▼
 Security Baseline Model (SBM)
        │
        ├───────────────┐
        ▼               ▼
 Compliance Engine    AI Learning Loop
        │               │
        └───────┬───────┘
                ▼
             Findings
                │
                ▼
        Validated Remediation
                │
          ┌─────┴─────┐
          ▼           ▼
      Dashboard      Reports
```

---

## Core architectural principle

### **AI understands. Policy decides. Evidence proves.**

The system does **not** hand an entire configuration to an LLM and ask whether it is secure.

Instead:

1. Deterministic parsers extract known configuration semantics.
2. Unknown syntax can be sent through an AI-assisted semantic resolution workflow.
3. Both paths converge into the same **Security Baseline Model**.
4. A deterministic compliance engine evaluates that model against policies.
5. Findings retain the original configuration evidence.
6. Remediation comes from validated vendor/platform-specific mappings.

This keeps the system extensible, auditable, and resistant to AI hallucination in security decisions.

---

## What we are building

### 1. Unified ingestion

Accept configuration exports individually or in batches.

Planned inputs include:

- Cisco IOS / IOS-XE
- Juniper JunOS
- Palo Alto PAN-OS
- future vendor adapters
- future live collection through network management protocols/APIs

### 2. Vendor-aware parsing

Convert vendor-specific syntax into structured semantic facts.

Example:

```text
Cisco:
    ip ssh version 2

Juniper:
    set system services ssh protocol-version v2
```

Both should become the same semantic representation:

```text
management.ssh.version = 2
```

### 3. Security Baseline Model (SBM)

The central vendor-neutral representation of security state.

Initial domains include:

```text
device
management
authentication
access_control
logging
monitoring
time
cryptography
```

The SBM is the main contract between ingestion, parsers, AI, compliance, remediation, and presentation.

### 4. AI-assisted semantic adaptation

When the system encounters unknown configuration syntax:

```text
Unknown configuration
        │
        ▼
AI semantic interpretation
        │
        ▼
Candidate field + value + confidence
        │
        ▼
Human confirmation / edit / rejection
        │
        ▼
Persisted mapping
        │
        ▼
Future recognition
```

The goal is **adaptive onboarding of new configuration semantics without rewriting the core compliance engine**.

### 5. Multi-framework compliance

The compliance engine evaluates the normalized SBM against policy packs.

Initial framework architecture:

```text
Security Baseline Model
        │
        ├── CIS
        ├── NIST
        └── STIG
```

Framework rules remain separate from vendor parsers.

### 6. Evidence-backed findings

Every finding should be traceable to:

- control ID
- expected state
- observed state
- severity
- source configuration
- source line / evidence
- parser or AI provenance
- confidence where applicable

Example:

```text
Control:       MGMT-HTTP-001
Status:        FAIL
Severity:      HIGH
Observed:      HTTP management enabled
Evidence:      ip http server
Source line:   17
Expected:      HTTP management disabled
```

### 7. Validated remediation

Remediation is selected using:

```text
Finding
   +
Vendor
   +
Platform / OS
   +
Version
        │
        ▼
Validated remediation mapping
```

AI may explain a remediation, but production commands should come from a controlled remediation registry rather than being freely invented by a model.

### 8. Reporting and dashboard

The platform will provide:

- compliance score
- findings by severity
- evidence drill-down
- remediation guidance
- AI confidence / semantic confidence where applicable
- executive report
- technical report
- interactive training workflow

---

# Repository architecture

```text
sih26155/
│
├── docs/
│   ├── architecture/
│   ├── vendors/
│   ├── compliance/
│   └── demo/
│
├── data/
│   ├── configs/
│   ├── policies/
│   ├── mappings/
│   ├── remediation/
│   └── schemas/
│
├── backend/
│   └── src/
│       └── sih26155/
│           ├── core/
│           ├── ingestion/
│           ├── parsers/
│           ├── ai/
│           ├── compliance/
│           ├── remediation/
│           ├── reporting/
│           ├── storage/
│           └── api/
│
├── frontend/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
│
└── scripts/
```

### Module boundaries

| Module | Responsibility |
|---|---|
| `core/` | Canonical models, facts, evidence, interfaces, pipeline contracts |
| `ingestion/` | File loading, vendor detection, future live collection |
| `parsers/` | Vendor-specific configuration interpretation |
| `ai/` | Unknown syntax resolution, retrieval, confidence, learning |
| `compliance/` | Policy packs, evaluation, risk and severity |
| `remediation/` | Validated vendor-specific corrective actions |
| `reporting/` | Executive and technical reports |
| `storage/` | Persistence and repositories |
| `api/` | Backend API surface |
| `frontend/` | User-facing dashboard and training interface |
| `tests/` | Unit, integration, and end-to-end validation |

---

# End-to-end flow

## Known configuration

```text
.config / CLI export
       │
       ▼
    Ingest
       │
       ▼
Vendor detection
       │
       ▼
Vendor parser
       │
       ▼
Facts + Evidence
       │
       ▼
Security Baseline Model
       │
       ▼
Compliance evaluation
       │
       ▼
Findings + Risk
       │
       ▼
Validated remediation
       │
       ├──────────────► Dashboard
       │
       └──────────────► PDF report
```

## Unknown configuration

```text
Unknown syntax
       │
       ▼
Context extraction
       │
       ▼
AI semantic resolver
       │
       ▼
Candidate mapping
(field + value + confidence)
       │
       ▼
Human confirmation
       │
       ▼
Learned mapping store
       │
       ▼
Security Baseline Model
       │
       ▼
Normal compliance pipeline
```

---

# Initial MVP

The first vertical slice intentionally stays small.

### Vendors

- Cisco
- Juniper
- Palo Alto

### Initial security controls

- SSH version
- Telnet / remote-access exposure
- HTTP management
- login protection / administrative timeout
- logging

### Initial product flow

```text
Upload configuration
        ↓
Detect vendor
        ↓
Normalize
        ↓
Build SBM
        ↓
Run compliance rules
        ↓
Show PASS / FAIL
        ↓
Display exact evidence
        ↓
Generate remediation
        ↓
Generate report
```

### Adaptive-learning demonstration

```text
Unknown vendor syntax
        ↓
AI candidate interpretation
        ↓
Confidence score
        ↓
Human approval
        ↓
Mapping stored
        ↓
Re-run
        ↓
Command recognized
```

The MVP demonstrates the architecture; it does not claim exhaustive support for every vendor or every control in the statement.

---

# Engineering rules

### 1. Parsers do not contain compliance policy

```text
Vendor syntax
    ↓
Semantic facts / SBM
    ↓
Compliance engine
```

Never:

```text
Cisco parser
    ↓
Cisco-specific CIS decision
```

### 2. AI does not directly decide compliance

```text
Unknown syntax
    ↓
AI candidate mapping
    ↓
SBM
    ↓
Policy evaluation
    ↓
Finding
```

### 3. Preserve evidence

Every important semantic fact should remain traceable to its source configuration.

### 4. Keep vendor knowledge modular

Adding a vendor should primarily mean adding an adapter/mapping layer, not rewriting the compliance engine.

### 5. Remediation must be controlled

Do not execute or present unverified model-generated configuration commands as authoritative remediation.

### 6. Security comes before UI

The backend semantics, evidence chain, compliance correctness, and E2E reliability take priority over visual polish.

---

# Development workflow

Use short-lived branches and integrate frequently.

```text
main
  │
  ├── feature/core-sbm
  ├── feature/cisco-parser
  ├── feature/juniper-parser
  ├── feature/ai-semantic-mapping
  ├── feature/compliance-engine
  └── feature/dashboard
```

Before merging:

```text
unit tests
   ↓
integration tests
   ↓
E2E pipeline
   ↓
review
```

No module should silently change the canonical SBM contract.

---

# Data & security

This is a cybersecurity project.

**Never commit:**

- real customer configurations
- passwords
- private keys
- API credentials
- device backups
- live network captures
- internal IP inventories
- confidential logs
- secrets in `.env`

Only sanitized, public, synthetic, or explicitly approved demo data belongs in `data/`.

---

# Current status

### Architecture

**LOCKED**

### Repository structure

**LOCKED**

### Team

**6 members**

### Immediate objective

Build and validate the first end-to-end vertical slice before expanding module depth.

### Target demonstration

**Multi-vendor normalization + deterministic compliance + evidence + validated remediation + AI-assisted unknown-command learning.**

---

# Long-term direction

The architecture is intentionally extensible toward:

```text
More vendors
      ↓
More device / OS versions
      ↓
More security controls
      ↓
More frameworks
      ↓
Live device collection
      ↓
Continuous compliance monitoring
      ↓
Change / drift detection
      ↓
Security posture management
```

The core remains the same:

> **Convert vendor-specific configuration syntax into a trustworthy, vendor-neutral representation of security state.**

---

## Problem statement

**SIH26155 — AI-Driven Multi-Vendor Network Security Compliance Auditor**

**Organization:** National Technical Research Organisation (NTRO)

**Category:** Software · Blockchain & Cybersecurity

Built for **Smart India Hackathon 2026**.

---

## Team

Six-member engineering team.

Ownership is documented in:

`docs/architecture/module-boundaries.md`

---

## License

Add the team's chosen license before public release.
