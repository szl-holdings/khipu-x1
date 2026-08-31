.PHONY: test demo

test:
	PYTHONPATH=src python -m pytest -q

demo:
	PYTHONPATH=src python scripts/demo.py --out demo-output
