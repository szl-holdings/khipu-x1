# KHIPU-X1 — Build Status (payload closeout)

**Closed out:** 2026-09-02 · Doctrine v11 · additive record; supersedes nothing.

## What the 2026-08-31 master build payload produced

Evidence: `PAYLOAD_RUN_SUMMARY.json`, `MASTER_BUILD_PAYLOAD.md`, `audit/`.

- 101-repo estate audit with source locks (`audit/gap_report.md`, `audit/chip_readiness_matrix.csv`, `audit/seed_upstream_map.json`).
- KIDS v0.1 instruction/descriptor spec (`spec/KIDS_v0.1.md`) — DRAFT / SOFTWARE-REFERENCE ONLY.
- `khipu-x1` 0.1.0 software reference package: explicit graph lowering, `.khipu` package builder/verifier, SHA3-256 receipt chain, RC1 authorization emulator, simulator, CLI.
- Conformance and tests: PASS at generation time (`PAYLOAD_RUN_SUMMARY.json`, returncode 0).

## Post-payload repairs (merged)

- #1 — workflow actions pinned to full-length commit SHAs (org runner policy).
- #2 — `khipu-x1 demo --out` packaged loader fix; the CI demo step passes.

## NEXT_STEPS.md disposition

- Install/test/demo steps run in CI on every push and pull request (`.github/workflows/ci.yml`); the demo crash that blocked step 5 was repaired in #2.
- Step 6 (hardware reports `UNAVAILABLE`) holds by design: `docs/CLAIMS_LEDGER.md` keeps every hardware claim `UNAVAILABLE` and the simulator stays `SOFTWARE_EMULATED`. No FPGA/ASIC exists or is claimed.

## Remaining work — hardware-gated, out of software scope

Every `UNAVAILABLE` row in `docs/CLAIMS_LEDGER.md` requires physical FPGA/MCU hardware, bench telemetry, or a signed promotion flow. None of that is assertable from this repository and none is claimed here. See `docs/ASIC_GAP_CHECKLIST.md` for the honest gap list.

## Known metadata gap

The GitHub repository description was never set by the payload. Suggested text:
`KHIPU-X1 — FPGA-first governed LLM accelerator software reference (SOFTWARE_EMULATED; no hardware claimed). Doctrine v11.`
Setting it requires repo-settings access; recorded here so it is not lost.
