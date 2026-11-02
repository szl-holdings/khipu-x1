"""Safe `.khipu` package builder and verifier."""

from __future__ import annotations

import hashlib
import io
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import numpy as np

from .kids import canonical_json_bytes


class KhipuPackageError(ValueError):
    pass


def _safe_member(name: str) -> bool:
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts and "\\" not in name


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_object(data: bytes, name: str) -> dict[str, Any]:
    try:
        value = json.loads(data)
        if not isinstance(value, dict):
            raise ValueError("expected an object")
        # Use the same finite-JSON contract as the package builder. Parsing
        # alone accepts NaN/Infinity extensions and overflowing exponents.
        canonical_json_bytes(value)
    except (ValueError, RecursionError) as exc:
        raise KhipuPackageError(f"invalid {name}") from exc
    return value


def build_package(
    output_path: str | Path,
    graph: Mapping[str, Any],
    weights: Mapping[str, np.ndarray],
    metadata: Mapping[str, Any] | None = None,
) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    files: dict[str, bytes] = {
        "graph.json": canonical_json_bytes(dict(graph)),
    }
    for name, array in sorted(weights.items()):
        if not name or "/" in name or "\\" in name:
            raise KhipuPackageError(f"unsafe weight name: {name!r}")
        buffer = io.BytesIO()
        np.save(buffer, np.ascontiguousarray(array), allow_pickle=False)
        files[f"weights/{name}.npy"] = buffer.getvalue()

    manifest = {
        "format": "khipu-package",
        "schema_version": "0.1",
        "kids_version": "0.1",
        "execution_claim": "SOFTWARE_REFERENCE_ONLY",
        "metadata": dict(metadata or {}),
        "files": {name: {"sha256": _sha256(data), "size": len(data)} for name, data in sorted(files.items())},
    }
    manifest_bytes = canonical_json_bytes(manifest)

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", manifest_bytes)
        for name, data in sorted(files.items()):
            archive.writestr(name, data)
    return output


def verify_package(path: str | Path) -> dict[str, Any]:
    """Verify one captured archive buffer and return its digest.

    The complete archive stays in memory during verification. The input path
    is a locator, not a guarantee that a later read observes the same bytes.
    """
    package_path = Path(path)
    if not package_path.is_file():
        raise KhipuPackageError(f"package not found: {package_path}")

    package_bytes = package_path.read_bytes()
    with zipfile.ZipFile(io.BytesIO(package_bytes), "r") as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise KhipuPackageError("duplicate archive entry detected")
        if any(not _safe_member(name) for name in names):
            raise KhipuPackageError("unsafe archive path detected")
        if "manifest.json" not in names:
            raise KhipuPackageError("manifest.json missing")
        manifest = _json_object(archive.read("manifest.json"), "manifest.json")
        if manifest.get("format") != "khipu-package" or manifest.get("schema_version") != "0.1":
            raise KhipuPackageError("unsupported package format/version")
        if manifest.get("kids_version") != "0.1":
            raise KhipuPackageError("unsupported or missing KIDS version")
        if manifest.get("execution_claim") != "SOFTWARE_REFERENCE_ONLY":
            raise KhipuPackageError("unsupported or missing execution claim")
        declared = manifest.get("files")
        if not isinstance(declared, dict):
            raise KhipuPackageError("manifest.files must be an object")
        if "graph.json" not in declared:
            raise KhipuPackageError("graph.json missing from manifest.files")
        if "manifest.json" in declared:
            raise KhipuPackageError("manifest.json cannot declare itself as a payload")
        expected_names = {"manifest.json", *declared.keys()}
        if set(names) != expected_names:
            raise KhipuPackageError("archive contents do not exactly match manifest")

        verified_files: dict[str, dict[str, Any]] = {}
        for name, record in sorted(declared.items()):
            if not _safe_member(name) or name not in names:
                raise KhipuPackageError(f"missing or unsafe file: {name}")
            if not isinstance(record, dict):
                raise KhipuPackageError(f"file record must be an object: {name}")
            expected_hash = record.get("sha256")
            if not isinstance(expected_hash, str) or re.fullmatch(r"[0-9a-f]{64}", expected_hash) is None:
                raise KhipuPackageError(f"invalid sha256: {name}")
            expected_size = record.get("size")
            if type(expected_size) is not int or expected_size < 0:
                raise KhipuPackageError(f"invalid size: {name}")
            data = archive.read(name)
            if _sha256(data) != expected_hash:
                raise KhipuPackageError(f"hash mismatch: {name}")
            if len(data) != expected_size:
                raise KhipuPackageError(f"size mismatch: {name}")
            if name == "graph.json":
                _json_object(data, "graph.json")
            verified_files[name] = {"sha256": expected_hash, "size": len(data)}

    return {
        "verified": True,
        "path": str(package_path),
        "package_sha256": _sha256(package_bytes),
        "schema_version": manifest["schema_version"],
        "kids_version": manifest["kids_version"],
        "execution_claim": manifest.get("execution_claim"),
        "files": verified_files,
    }
