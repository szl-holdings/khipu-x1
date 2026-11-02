"""Archive integrity must not admit missing or malformed package contracts."""
from __future__ import annotations

import copy
import hashlib
import json
import zipfile

import numpy as np
import pytest

from khipu_x1 import KhipuPackageError, build_package, verify_package


GRAPH = b'{"ops":[{"op":"nop"}]}'


def manifest(files=None):
    files = {"graph.json": GRAPH} if files is None else files
    return {
        "format": "khipu-package",
        "schema_version": "0.1",
        "kids_version": "0.1",
        "execution_claim": "SOFTWARE_REFERENCE_ONLY",
        "metadata": {},
        "files": {name: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                  for name, data in files.items()},
    }


def write_package(tmp_path, contract, files=None):
    path = tmp_path / "case.khipu"
    files = {"graph.json": GRAPH} if files is None else files
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("manifest.json", json.dumps(contract))
        for name, data in files.items():
            archive.writestr(name, data)
    return path


def test_manifest_only_archive_is_not_a_verified_package(tmp_path):
    path = write_package(tmp_path, manifest({}), {})
    with pytest.raises(KhipuPackageError, match="graph.json"):
        verify_package(path)


def test_weights_cannot_replace_required_graph(tmp_path):
    files = {"weights/w.npy": b"synthetic bytes"}
    path = write_package(tmp_path, manifest(files), files)
    with pytest.raises(KhipuPackageError, match="graph.json"):
        verify_package(path)


@pytest.mark.parametrize("contract", [None, [], "manifest", 7, True])
def test_manifest_must_be_an_object(tmp_path, contract):
    with pytest.raises(KhipuPackageError, match="manifest"):
        verify_package(write_package(tmp_path, contract))


@pytest.mark.parametrize("version", [None, "9.9", 0.1, [], {}])
def test_unsupported_kids_version_is_rejected(tmp_path, version):
    contract = manifest()
    contract["kids_version"] = version
    with pytest.raises(KhipuPackageError, match="KIDS"):
        verify_package(write_package(tmp_path, contract))


def test_missing_kids_version_is_a_package_error(tmp_path):
    contract = manifest()
    del contract["kids_version"]
    with pytest.raises(KhipuPackageError, match="KIDS"):
        verify_package(write_package(tmp_path, contract))


@pytest.mark.parametrize("claim", [None, "FPGA_MEASURED", "ASIC_MEASURED", True, []])
def test_unsupported_execution_claim_is_rejected(tmp_path, claim):
    contract = manifest()
    contract["execution_claim"] = claim
    with pytest.raises(KhipuPackageError, match="execution claim"):
        verify_package(write_package(tmp_path, contract))


@pytest.mark.parametrize("record", [None, [], "record", 7, True])
def test_file_records_must_be_objects(tmp_path, record):
    contract = manifest()
    contract["files"]["graph.json"] = record
    with pytest.raises(KhipuPackageError, match="file record"):
        verify_package(write_package(tmp_path, contract))


@pytest.mark.parametrize("size", [str(len(GRAPH)), float(len(GRAPH)), None, True, -1, []])
def test_file_size_is_an_exact_nonnegative_integer(tmp_path, size):
    contract = manifest()
    contract["files"]["graph.json"]["size"] = size
    with pytest.raises(KhipuPackageError, match="size"):
        verify_package(write_package(tmp_path, contract))


@pytest.mark.parametrize("graph", [b"[]", b"null", b'"graph"', b"bad JSON", b"\xff"])
def test_graph_member_must_contain_a_json_object(tmp_path, graph):
    files = {"graph.json": graph}
    with pytest.raises(KhipuPackageError, match="graph.json"):
        verify_package(write_package(tmp_path, manifest(files), files))


@pytest.mark.parametrize("token", [b"NaN", b"Infinity", b"-Infinity", b"1e999"])
def test_graph_numbers_follow_the_builders_finite_json_contract(tmp_path, token):
    files = {"graph.json": b'{"value":' + token + b'}'}
    with pytest.raises(KhipuPackageError, match="graph.json"):
        verify_package(write_package(tmp_path, manifest(files), files))


def test_manifest_metadata_must_follow_finite_json_contract(tmp_path):
    contract = manifest()
    contract["metadata"] = {"value": float("nan")}
    with pytest.raises(KhipuPackageError, match="manifest"):
        verify_package(write_package(tmp_path, contract))


@pytest.mark.parametrize("weights", [{}, {"w": np.ones((2, 2), dtype=np.int8)}])
def test_builder_round_trip_preserves_optional_weights(tmp_path, weights):
    graph = {"ops": [{"op": "nop"}]}
    path = build_package(tmp_path / "valid.khipu", graph, weights)
    result = verify_package(path)
    assert result["verified"] is True
    assert result["kids_version"] == "0.1"
    assert result["execution_claim"] == "SOFTWARE_REFERENCE_ONLY"
    assert result["package_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert set(result["files"]) == {"graph.json", *(f"weights/{name}.npy" for name in weights)}


def test_tampered_content_still_fails_integrity_verification(tmp_path):
    contract = copy.deepcopy(manifest())
    with pytest.raises(KhipuPackageError, match="hash mismatch"):
        verify_package(write_package(tmp_path, contract, {"graph.json": b"{}"}))


def test_package_digest_binds_inspected_bytes_when_path_is_replaced(tmp_path, monkeypatch):
    path = write_package(tmp_path, manifest())
    inspected_bytes = path.read_bytes()
    replacement = tmp_path / "replacement"
    replacement_bytes = b"NOT A KHIPU ARCHIVE"
    replacement.write_bytes(replacement_bytes)
    original_read = zipfile.ZipFile.read
    swapped = False

    def replace_after_graph_read(archive, name, *args, **kwargs):
        nonlocal swapped
        data = original_read(archive, name, *args, **kwargs)
        if name == "graph.json" and not swapped:
            replacement.replace(path)
            swapped = True
        return data

    monkeypatch.setattr(zipfile.ZipFile, "read", replace_after_graph_read)
    result = verify_package(path)

    assert swapped
    assert path.read_bytes() == replacement_bytes
    assert result["verified"] is True
    assert result["files"]["graph.json"]["sha256"] == hashlib.sha256(GRAPH).hexdigest()
    assert result["package_sha256"] == hashlib.sha256(inspected_bytes).hexdigest()
    assert result["package_sha256"] != hashlib.sha256(replacement_bytes).hexdigest()
