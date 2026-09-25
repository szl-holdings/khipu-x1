"""Committed audit inventories must list public repositories only."""

from __future__ import annotations

import csv
import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1] / "audit"


def test_repo_inventory_lists_public_repositories_only():
    inventory = json.loads((AUDIT / "repo_inventory.json").read_text(encoding="utf-8"))
    repositories = inventory["repositories"]
    assert repositories
    assert all(repo.get("private") is False for repo in repositories)
    assert inventory["repository_count"] == len(repositories)


def test_source_lock_lists_public_repositories_only():
    lock = json.loads((AUDIT / "source_lock.json").read_text(encoding="utf-8"))
    assert lock
    assert all(entry.get("private") is False for entry in lock.values())


def test_chip_readiness_matrix_lists_public_repositories_only():
    with (AUDIT / "chip_readiness_matrix.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    assert all(row["private"] == "False" for row in rows)
