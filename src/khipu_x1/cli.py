"""KHIPU-X1 reference CLI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .package import verify_package


def main() -> int:
    parser = argparse.ArgumentParser(prog="khipu-x1")
    sub = parser.add_subparsers(dest="command", required=True)

    demo = sub.add_parser("demo", help="run the offline software-reference demo")
    demo.add_argument("--out", default="demo-output")

    verify = sub.add_parser("verify-package", help="verify a .khipu package")
    verify.add_argument("package")

    args = parser.parse_args()
    if args.command == "demo":
        from scripts.demo import run_demo
        summary = run_demo(Path(args.out))
        print(json.dumps(summary, indent=2, sort_keys=True))
        return 0
    if args.command == "verify-package":
        print(json.dumps(verify_package(args.package), indent=2, sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
