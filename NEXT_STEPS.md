# Next Steps

1. Review `MASTER_BUILD_PAYLOAD.md`, `docs/CLAIMS_LEDGER.md`, and the audit output.
2. Create a Python 3.11 virtual environment.
3. Run `python -m pip install -e ".[dev]"`.
4. Run `pytest -q`.
5. Run `khipu-x1 demo --out demo-output`.
6. Confirm the demo reports hardware status `UNAVAILABLE` and leaves physical
   outcome verification as open Reality Debt.
7. Reconcile the live GitHub audit with the seed source map; do not copy code
   until license and source lineage are reviewed.
8. Select an FPGA development platform with the hardware partner before adding
   vendor-specific RTL or driver code.
9. Open a reviewed PR only after local tests and claims review. Do not push
   generated scaffolding directly to protected `main`.

Local workspace: `/home/user/workspace/khipu-x1-workspace`
