"""Fail-closed local consistency checks for the public release identity.

The PyPI workflow's canonical build/tag/OIDC gate remains authoritative.
These checks prevent a new tagged version from retaining an old citation or
an 'unreleased' changelog heading. They make no online publication claim.
"""

from __future__ import annotations

import datetime as dt
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _scalar(text: str, name: str) -> str:
    matches = re.findall(
        rf"^{re.escape(name)}:[ \t]*([^\r\n#]+)", text, flags=re.MULTILINE
    )
    assert len(matches) == 1, f"{name}: expected one metadata value"
    return matches[0].strip().strip("'\"")


def test_release_identity_matches_built_package_version() -> None:
    with (ROOT / "pyproject.toml").open("rb") as stream:
        project = tomllib.load(stream)["project"]
    version = project["version"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), "expected a final SemVer release"
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert _scalar(citation, "version") == version, "CITATION.cff version drift"
    release_date = dt.date.fromisoformat(_scalar(citation, "date-released"))
    first_entry = re.search(r"^##[ \t]+([^\r\n]+)$", changelog, re.MULTILINE)
    assert first_entry is not None, "CHANGELOG.md needs a release heading"
    expected = f"{version} ({release_date.isoformat()})"
    assert first_entry.group(1).strip() == expected, (
        f"top changelog entry must be {expected!r}, not {first_entry.group(1).strip()!r}"
    )
