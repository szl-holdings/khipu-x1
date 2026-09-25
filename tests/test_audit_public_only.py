"""Committed audit inventories must list public repositories only."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"


def _inventory_repositories():
    inventory = json.loads((AUDIT / "repo_inventory.json").read_text(encoding="utf-8"))
    return inventory["repositories"]


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


def test_inventory_repository_names_are_unique():
    full_names = [repo["full_name"] for repo in _inventory_repositories()]
    assert len(full_names) == len(set(full_names))


def test_source_lock_covers_exactly_the_inventory():
    lock = json.loads((AUDIT / "source_lock.json").read_text(encoding="utf-8"))
    full_names = [repo["full_name"] for repo in _inventory_repositories()]
    assert sorted(lock) == sorted(full_names)


def test_chip_readiness_matrix_covers_exactly_the_inventory():
    with (AUDIT / "chip_readiness_matrix.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    names = [repo["name"] for repo in _inventory_repositories()]
    assert [row["name"] for row in rows] == names


def test_gap_report_matches_the_inventory():
    report = (AUDIT / "gap_report.md").read_text(encoding="utf-8")
    repositories = _inventory_repositories()
    full_names = {repo["full_name"] for repo in repositories}
    observed = re.findall(r"^Repositories observed: \*\*(\d+)\*\*", report, re.MULTILINE)
    assert observed == [str(len(repositories))]
    listed = re.findall(r"^\| `([^`]+)` \|", report, re.MULTILINE)
    assert listed
    assert set(listed) <= full_names


def test_payload_run_summary_matches_the_inventory():
    summary = json.loads((ROOT / "PAYLOAD_RUN_SUMMARY.json").read_text(encoding="utf-8"))
    audit = summary.get("audit")
    if isinstance(audit, dict) and "repositories" in audit:
        assert audit["repositories"] == len(_inventory_repositories())
