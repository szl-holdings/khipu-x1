# KHIPU-X1

[![PyPI](https://img.shields.io/pypi/v/khipu-x1)](https://pypi.org/project/khipu-x1/) [![Python](https://img.shields.io/pypi/pyversions/khipu-x1)](https://pypi.org/project/khipu-x1/) [![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/szl-holdings/khipu-x1/badge)](https://scorecard.dev/viewer/?uri=github.com/szl-holdings/khipu-x1)

**FPGA-first governed LLM accelerator reference.**

This repository is a software reference and future hardware workspace. It is not
a fabricated chip and does not claim performance superiority.

Current implemented lane:

- KIDS v0.1 descriptor draft;
- deterministic NumPy simulator;
- minimal explicit graph lowering;
- safe `.khipu` package builder/verifier;
- SHA3-256 execution receipt chain;
- RC1 authorization-state emulator;
- conformance tests.

Current hardware status: **UNAVAILABLE — target FPGA not selected**.

<!-- szl:header v1 -->
<!-- Native identity: szl-brand@4309f6fce89179331b0b3ed8c99494e76c5be256; Orbit v2 icon. -->
<p>
  <a href="https://github.com/szl-holdings">
    <img src="https://raw.githubusercontent.com/szl-holdings/szl-brand/4309f6fce89179331b0b3ed8c99494e76c5be256/kit/logos/orbit-v2/suite/szl-icon-32.svg" alt="SZL Holdings — Orbit v2" width="32" height="32" />
  </a>
</p>

**Control before action. Evidence after.**

[Product](https://a-11-oy.com) · [Proof](https://a11oy.net) · [GitHub organization](https://github.com/szl-holdings)
<!-- /szl:header -->

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
khipu-x1 demo --out ./demo-output
```

Or without installing:

```bash
PYTHONPATH=src python scripts/demo.py --out ./demo-output
```

## Truth labels

- `SCAFFOLDED`: interface/document exists.
- `SOFTWARE_EMULATED`: reference code executed.
- `FPGA_MEASURED`: only after exact bitstream/device tests.
- `BLOCKED`: attempted path refused with evidence.
- `UNAVAILABLE`: capability does not exist or was not measured.

## Program boundary

One owner prototype only. No production tooling, mass-production order or ASIC
tapeout is authorized by this repository.
