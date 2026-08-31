# SZL / A11oy / KHIPU-X1 Master Build Payload

**Version:** 1.0.0  
**Program:** One owner prototype; FPGA-first; no ASIC tapeout  
**Canonical objective:** Turn the existing SZL governed-AI software estate into
an executable, measured, fail-closed reference stack for a future custom LLM
accelerator and its first humanitarian/offline integration.

## 1. Mission

Build one coherent program around three layers:

1. **A11oy Beacon / PHYS-1** — offline-first secure edge appliance.
2. **RC1** — independent authorization/safety controller for privileged outputs.
3. **KHIPU-X1** — FPGA-first governed LLM inference accelerator reference.

The system must preserve the distinction:

> **Intent is not Action. Action is not Outcome.**

No software response, driver completion code, or actuator command may be
reported as a verified real-world outcome without separate witness evidence.

## 2. Non-negotiable truth boundaries

- This program starts with a **software reference and FPGA prototype**, not a
  fabricated custom ASIC.
- Do not claim a speedup, energy advantage, safety certification, production
  readiness, proof of trust, or novelty without measured evidence.
- Lambda remains an advisory conjecture where the existing estate says it is
  open. Never promote an open conjecture to a theorem.
- Energy is `UNAVAILABLE` when no calibrated measurement is present. Never
  substitute estimates while labeling them measured.
- A receipt proves integrity, ordering and provenance within its stated scope;
  it does not prove semantic correctness or truth by itself.
- No private key, token, credential, model secret, customer data or personal
  humanitarian record may be committed.
- Do not create or push a remote repository from this payload. Produce a local
  reviewable workspace and evidence first.
- Preserve upstream licenses, copyright notices and source attribution. Verify
  file-level licenses before copying implementation code.

## 3. Canonical repository strategy

Do **not** create seven new repositories at the beginning. For a solo build,
create one canonical monorepo named `khipu-x1` with stable internal boundaries:

```text
khipu-x1/
  spec/          KIDS descriptor/ABI, registers, package and receipt contracts
  src/           simulator, compiler reference, runtime and RC1 emulator
  rtl/           FPGA RTL/HLS only after the target platform is selected
  firmware/      RC1 and board-management firmware contracts
  driver/        Linux driver design and later source
  conformance/   golden vectors, differential tests, fuzz/fault tests
  docs/          Beacon integration, ASIC gap analysis, Minewing handoff
  evidence/      source locks, test receipts and measured benchmark outputs
```

Split components into independent repositories only after interfaces are stable,
release cadence requires it, and duplication risk is demonstrably lower.

## 4. Existing estate to map, not duplicate

Audit every organization repository, then deeply map at least:

- `a11oy`
- `szl-substrate`
- `szl-khipu`
- `szl-receipt-attn`
- `YARQA-ATTN`
- `szl-kernels`
- `szl-block-kv`
- `szl-maskmod`
- `szl-govsign`
- `szl-provctl`
- `szl-blocked`
- `szl-invariants`
- `governance-as-code`
- `szl-energy-attest`
- `szl-gpu-bridge`
- `szl-forge`
- `lutar-lean`

For each repository capture default-branch revision, license, language, active or
archived state, relevant files, tests, generated artifacts, duplicate code,
claim boundaries and what should become a dependency, adapter, reference, or
retired duplicate.

## 5. Deliverable A — KIDS v0.1

Define the **KHIPU Instruction and Descriptor Specification** with:

- versioned descriptor header and canonical byte encoding;
- monotonic sequence number and anti-replay nonce;
- model, policy, bitstream and firmware digests;
- buffer handles, shapes, strides, dtypes and quantization metadata;
- queue submission/completion semantics;
- timeout, abort, reset and zeroization behavior;
- explicit error/status codes;
- deterministic receipt-event encoding;
- forward/backward compatibility rules;
- endianness, alignment and maximum-size constraints.

Initial logical operations:

`NOP`, `LOAD`, `STORE`, `GEMM_INT8`, `GEMM_BF16`, `RMSNORM`, `ROPE`,
`ATTN_CAUSAL`, `ATTN_YARQA`, `KV_GATHER`, `KV_SCATTER`, `SHA3_COMMIT`,
`RECEIPT_EMIT`, `BARRIER`, `ZEROIZE`, `ABORT`.

Only `NOP`, `GEMM_INT8`, `RMSNORM`, `SHA3_COMMIT`, `BARRIER` and `ABORT`
need executable software support in the first payload scaffold. Remaining
operations are reserved and must return `UNIMPLEMENTED`, never silently fall
back while claiming hardware execution.

## 6. Deliverable B — deterministic golden simulator

Implement a NumPy reference that:

- validates every descriptor before execution;
- executes supported operations deterministically;
- rejects sequence replay, malformed shapes, unsupported dtypes and invalid
  buffer references;
- records input/output commitments and an ordered SHA3-256 receipt chain;
- emits a machine-readable execution trace;
- differentiates software-emulated, FPGA and unavailable execution paths;
- provides golden vectors for future RTL and driver differential testing.

## 7. Deliverable C — compiler/reference lowering

Start with a small explicit KHIPU graph JSON format. Lower it into KIDS
commands. Then add, in this order:

1. manually-authored graph support;
2. PyTorch FX/export adapter;
3. ONNX import subset;
4. KHIPU IR or MLIR dialect only when the operation/shape contracts stabilize;
5. quantization, fusion and memory planning;
6. target-specific scheduling.

The first executable graph is a tiny inference fragment:

`INT8 GEMM -> RMSNorm -> SHA3 output commitment`.

Do not call the initial JSON lowering a complete compiler.

## 8. Deliverable D — `.khipu` package and runtime

Define a safe archive format binding:

- manifest and schema version;
- graph;
- weight files;
- model digest;
- required KIDS/driver/bitstream/firmware ABI;
- quantization metadata;
- policy digest;
- file hashes and optional signature envelope;
- declared limitations and measured qualification evidence.

The loader must reject path traversal, duplicate archive entries, missing files,
unknown required features and hash mismatch.

Implement a Python emulator runtime first. `libkhipu`, a Linux driver and a
PyTorch backend remain explicit later milestones.

## 9. Deliverable E — RC1 emulator and firmware contract

The RC1 emulator is not production cryptography. It exists to prove state and
protocol behavior before hardware selection. It must:

- validate target identity, channel, requested state, counter, time window,
  policy digest and message authentication;
- reject replay, expiry, malformed commands and wrong target;
- default every output to a safe state after reset or failure;
- create an independent actuation receipt;
- distinguish authorization from physical outcome witness evidence.

The production design should use a secure element or public-key signature
verification, protected monotonic state, signed firmware and anti-rollback.

## 10. Deliverable F — FPGA v0.1

Do not begin RTL until the FPGA family, development board, toolchain license,
memory topology and Minewing/partner responsibilities are selected.

Recommended first synthesizable slice:

- descriptor parser and queue;
- monotonic counter and hardware timestamps;
- DMA loopback/test engine;
- INT8 GEMV/GEMM tile;
- RMSNorm or fixed supported normalization datapath;
- SHA3-256 commitment/receipt block;
- error/status registers and interrupt;
- board power/energy telemetry ingestion.

YARQA attention, full causal attention, KV paging and BF16 are phase-two targets
unless the selected FPGA has sufficient resources and engineering budget.

## 11. Deliverable G — Beacon integration

Build a safe bench demonstration only:

1. create a structured need or equipment state;
2. make a bounded local proposal;
3. require explicit human authorization;
4. pass an authenticated command to RC1 emulator or hardware;
5. switch only a low-voltage LED/fan/relay test load;
6. receive an independent sensor or switch witness;
7. close the Outcome Receipt only when witness evidence matches;
8. keep conflicting or missing evidence as open Reality Debt;
9. run without internet;
10. reconcile signed records after connectivity returns.

No life-safety, medical-treatment, access-control, high-energy, vehicle-control
or industrial control target is permitted in Rev A.

## 12. Conformance and evidence

Required tests:

- descriptor canonicalization and validation;
- NumPy differential output tests;
- malformed shape/dtype/buffer rejection;
- receipt-chain tamper detection;
- replay and stale-counter rejection;
- `.khipu` path-traversal, duplicate-entry and hash-mismatch rejection;
- deterministic build/source lock;
- bitstream/firmware identity reporting when hardware exists;
- fault-injection and reset-to-safe-state tests;
- measured latency, bandwidth, receipt overhead and energy only on real hardware.

Every report must distinguish `PLANNED`, `SCAFFOLDED`, `SOFTWARE_EMULATED`,
`FPGA_MEASURED`, `BLOCKED`, and `UNAVAILABLE`.

## 13. Minewing handoff

Request a normal commercial quote first, separately identifying:

- Phase 0 architecture/feasibility;
- FPGA engineering, internal or disclosed partner;
- electrical schematic/PCB design;
- power, thermal and RF engineering;
- RC1/secure-element integration;
- enclosure and mechanical work;
- BSP/board-management firmware;
- assembly, bring-up, validation and shipping;
- total all-in cost for exactly one owner prototype.

Require delivery of project-specific schematics, PCB source/Gerbers, BOM/AVL,
mechanical CAD, test procedures/results, firmware source created for SZL,
FPGA source/constraints/build scripts created for SZL, and reproducibility notes,
subject only to clearly disclosed background IP and third-party licenses.

No production tooling, volume order, exclusivity, publicity right, equity,
software transfer, model transfer, patent transfer or ASIC tapeout is authorized.

## 14. ASIC gate

An ASIC is not approved until the FPGA program demonstrates:

- correct and stable operation contracts;
- a workload benefit worth hardening;
- feasible on-chip/external memory architecture;
- usable compiler/runtime/driver flow;
- measured power and thermal envelope;
- verification coverage and reproducible builds;
- credible unit-volume/business case;
- funding for RTL verification, physical design, DFT, packaging, masks,
  fabrication, bring-up and production test.

Additional ASIC software still required includes boot ROM, HAL/BSP, production
firmware, production driver, manufacturing test software, post-silicon
characterization, microcode/update strategy, errata handling and long-term ABI
compatibility.

## 15. Definition of done for this payload

This payload is complete when it produces:

- full organization inventory and source locks;
- chip-readiness/gap matrix;
- canonical one-repository scaffold;
- KIDS v0.1 draft;
- deterministic simulator;
- minimal graph lowering;
- safe `.khipu` package builder/verifier;
- RC1 behavior emulator;
- conformance tests;
- Beacon and Minewing handoff documents;
- explicit next-step plan;
- no false hardware or ASIC claim.
