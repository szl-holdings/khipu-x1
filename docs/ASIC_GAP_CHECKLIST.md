# KHIPU-X1 Chip Readiness — Missing Software and Hardware

## Software required before a useful chip

| Layer | Current payload | Still required for hardware/product |
|---|---|---|
| Architecture | KIDS logical descriptor draft | binary ABI, registers, queues, coherency and memory model |
| Simulator | deterministic NumPy functional model | calibrated cycle/memory/power simulator |
| Compiler | explicit JSON lowering | PyTorch export, ONNX subset, quantization, fusion, scheduler, memory planner |
| Runtime | Python emulator | `libkhipu`, async queues, buffer allocator, multi-stream and error recovery |
| Driver | design document only | Linux PCIe/platform driver, DMA/IOMMU, interrupts, reset, health, firmware load |
| Model packaging | `.khipu` builder/verifier | signed promotion, compatibility solver, encrypted/private package policy if needed |
| Inference engine | tiny fragment only | tokenizer, prefill/decode scheduler, sampling, batching and KV-cache manager |
| Framework | none | PyTorch custom device/backend and optional llama.cpp integration |
| Security | RC1 HMAC behavior emulator | secure-element/protected key flow, measured boot, attestation, anti-rollback |
| Observability | software elapsed time | cycles, stalls, bandwidth, temperature, voltage/current, measured joules |
| Verification | unit/conformance scaffold | RTL simulation, formal properties, coverage, fuzzing, fault injection and soak |
| SDK | Python package/CLI | C/C++ headers, bindings, profiler, debugger, docs and compatibility matrix |

## FPGA hardware still required

- selected device/development board and licensed toolchain;
- DDR/HBM topology and controller;
- PCIe/Ethernet/SoC host path;
- synthesizable descriptor queue and register block;
- DMA engines and memory protection;
- INT8 tensor tile and validated accumulation/scaling rules;
- normalization datapath;
- SHA3 receipt engine;
- clock/reset/power/thermal handling;
- RC1 MCU and secure element integration;
- board telemetry and energy measurement;
- FPGA constraints, timing closure and reproducible bitstream flow.

## Additional ASIC work after FPGA validation

- complete synthesizable RTL and microarchitecture specification;
- UVM/cocotb/formal verification, coverage closure and signoff strategy;
- SRAM compiler/macro selection and memory banking;
- clock/reset architecture and CDC/RDC verification;
- power domains, isolation, retention and UPF;
- scan, BIST, JTAG and production DFT;
- synthesis, floorplan, place/route, CTS and timing closure;
- IR-drop, electromigration, signal integrity and power integrity;
- foundry PDK, IP licensing and legal/export review;
- package, substrate, thermal solution and board reference design;
- mask, wafer, package, test and yield budget;
- boot ROM, production firmware, manufacturing test and post-silicon diagnostics;
- characterization, errata, ABI compatibility and long-term software support.

## Gate

Do not call this a custom chip until packaged silicon exists and is independently
identified. Before that, use `software reference`, `FPGA prototype`, or
`ASIC architecture/roadmap` as applicable.
