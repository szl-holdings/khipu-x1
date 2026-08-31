# SZL GitHub Estate — Chip Readiness Audit

Organization: `szl-holdings`  
Repositories observed: **101**  
RTL/constraint files surfaced in scanned trees: **0**  

## Honest conclusion

No synthesizable RTL or FPGA constraint file was surfaced by the scanned trees. The estate contains substantial AI/governance software references, but it is not yet a chip implementation.

## Highest-relevance repositories

| Repository | Score | Archived | RTL | Firmware | Tests | Head |
|---|---:|:---:|---:|---:|---:|---|
| `szl-holdings/a11oy` | 849 | no | 0 | 0 | 503 | `a73e734009ec` |
| `szl-holdings/szl-forge` | 183 | no | 0 | 0 | 34 | `6e0ac08533cb` |
| `szl-holdings/szl-khipu` | 112 | no | 0 | 0 | 8 | `4610f1448339` |
| `szl-holdings/szl-energy-attest` | 56 | no | 0 | 0 | 12 | `aa07e060c1eb` |
| `szl-holdings/lutar-lean` | 55 | no | 0 | 0 | 5 | `0c17b008b890` |
| `szl-holdings/szl-kernels` | 53 | no | 0 | 0 | 7 | `9b8628776afb` |
| `szl-holdings/YARQA-ATTN` | 49 | no | 0 | 0 | 8 | `373b61869278` |
| `szl-holdings/governance-as-code` | 44 | no | 0 | 0 | 1 | `b76551be2781` |
| `szl-holdings/szl-block-kv` | 44 | no | 0 | 0 | 3 | `f94ef2aa9b2c` |
| `szl-holdings/szl-blocked` | 42 | no | 0 | 0 | 2 | `d0fd834ebf6b` |
| `szl-holdings/szl-provctl` | 41 | no | 0 | 0 | 2 | `d1e562aa7b3d` |
| `szl-holdings/szl-govsign` | 40 | no | 0 | 0 | 2 | `fde27bfb7f31` |
| `szl-holdings/szl-receipt-attn` | 39 | no | 0 | 0 | 6 | `9465638440f7` |
| `szl-holdings/szl-gpu-bridge` | 37 | no | 0 | 0 | 36 | `9dc52f301c0f` |
| `szl-holdings/szl-maskmod` | 37 | no | 0 | 0 | 5 | `491ee549031b` |
| `szl-holdings/szl-invariants` | 34 | no | 0 | 0 | 4 | `513ff01e71d7` |
| `szl-holdings/szl-substrate` | 34 | no | 0 | 0 | 13 | `9c0ef8864ad4` |
| `szl-holdings/ayllu` | 33 | no | 0 | 0 | 7 | `92f952c17ddd` |
| `szl-holdings/szl-nemo` | 33 | no | 0 | 0 | 2 | `6e2f91181788` |
| `szl-holdings/anatomy` | 29 | no | 0 | 0 | 3 | `33e949086b1c` |
| `szl-holdings/a11oy-factory` | 28 | no | 0 | 0 | 10 | `294de2ff06df` |
| `szl-holdings/yarqa` | 27 | no | 0 | 0 | 14 | `0538ee2c0ed8` |
| `szl-holdings/szl-quant` | 25 | no | 0 | 0 | 14 | `0a18eea4c0ce` |
| `szl-holdings/governed-inference-meter` | 23 | yes | 0 | 0 | 6 | `aee6466ecaaa` |
| `szl-holdings/szl-serve` | 23 | no | 0 | 0 | 10 | `fa7df9222f4b` |
| `szl-holdings/immune` | 21 | no | 0 | 0 | 8 | `6d598c505e9c` |
| `szl-holdings/szl-governed-norm` | 21 | yes | 0 | 0 | 6 | `c68d06d35058` |
| `szl-holdings/governed-receipt-spec` | 19 | no | 0 | 0 | 4 | `14c35970a679` |
| `szl-holdings/szl-guardrail-receipt` | 16 | no | 0 | 0 | 5 | `e7ef3d794017` |
| `szl-holdings/a11oy-net` | 15 | no | 0 | 0 | 0 | `ed1a40e9c078` |

## Immediate gaps

1. No approved binary accelerator ABI/register/memory specification.
2. No deterministic cycle/memory simulator calibrated to a target device.
3. No complete graph compiler, quantizer, scheduler or memory planner for custom hardware.
4. No production runtime/driver/framework backend.
5. No selected FPGA target, reproducible bitstream flow or measured hardware evidence.
6. No ASIC RTL verification, physical design, DFT, packaging or post-silicon stack.

## Deep-scan limitations

Deep-scan errors: **0**. GitHub tree responses may be truncated for very large repositories. Private repositories require an authenticated token/gh session. Absence from this report is not proof of absence.
