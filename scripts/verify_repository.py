#!/usr/bin/env python3
"""Verify public-repository metadata and forbid game, save, secret, and local-path leaks."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "STATUS.json"
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
FORBIDDEN_EXTENSIONS = {
    ".iso",
    ".cso",
    ".pbp",
    ".bin",
    ".gba",
    ".nds",
    ".3ds",
    ".cia",
    ".nsp",
    ".xci",
    ".sav",
    ".srm",
    ".state",
    ".ss0",
    ".ss1",
    ".ppst",
    ".elf",
    ".prx",
    ".key",
    ".keys",
}
FORBIDDEN_FILENAMES = {
    ".env",
    "credentials.json",
    "secrets.json",
    "id_rsa",
    "id_ed25519",
}
REQUIRED_FILES = {
    "README.md",
    "INSTALL_KO.md",
    "COMPATIBILITY_KO.md",
    "TROUBLESHOOTING_KO.md",
    "SUPPORT_KO.md",
    "NOTICE.md",
    "PATCH_FORMAT.md",
    "RELEASE_NOTES.md",
    "RELEASE_DRAFT.md",
    "RELEASE_CHECKLIST.md",
    "SHA256SUMS.txt",
    "STATUS.json",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/repository-integrity.yml",
    "scripts/apply_patch.py",
    "scripts/verify_repository.py",
}
ALLOWED_RELEASE_STATES = {
    "LOCAL_PREPARED",
    "OWNER_APPROVED_PUBLICATION",
    "PUBLIC_REPOSITORY_CREATED",
    "PUBLISHED",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def repository_files() -> list[Path]:
    files: list[Path] = []
    for directory, names, filenames in os.walk(ROOT):
        names[:] = [name for name in names if name not in SKIP_DIRS]
        for filename in filenames:
            files.append(Path(directory, filename))
    return files


def main() -> None:
    errors: list[str] = []
    try:
        status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FAIL: STATUS.json을 읽을 수 없습니다: {exc}") from exc

    if status.get("release_state") not in ALLOWED_RELEASE_STATES:
        errors.append("invalid release_state")
    patch_metadata = status.get("patch") or {}
    patch_relative = Path(str(patch_metadata.get("path") or ""))
    if patch_relative.parent != Path(".") or patch_relative.suffix.lower() != ".xdelta":
        errors.append("patch must be a root .xdelta file")
    patch = ROOT / patch_relative
    if not patch.is_file():
        errors.append(f"missing patch: {patch_relative}")
    else:
        if patch.stat().st_size != patch_metadata.get("size"):
            errors.append("patch size mismatch")
        if sha256_file(patch) != patch_metadata.get("sha256"):
            errors.append("patch SHA-256 mismatch")

    missing = sorted(name for name in REQUIRED_FILES if not (ROOT / name).is_file())
    if missing:
        errors.append("missing required files: " + ", ".join(missing))

    files = repository_files()
    xdelta_files = [path for path in files if path.suffix.lower() == ".xdelta"]
    if xdelta_files != [patch]:
        errors.append("repository must contain exactly the STATUS.json root patch")

    forbidden: list[str] = []
    oversized: list[str] = []
    symlinks: list[str] = []
    local_path_leaks: list[str] = []
    credential_leaks: list[str] = []
    workspace_markers = [
        b"C:" + b"\\" + b"shin",
        b"C:" + b"/" + b"shin",
        b"/" + b"home" + b"/",
    ]
    credential_markers = [
        b"gh" + b"p_",
        b"github" + b"_pat_",
        b"OPENAI" + b"_API_KEY=",
    ]
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        if path.is_symlink():
            symlinks.append(relative)
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS or path.name.lower() in FORBIDDEN_FILENAMES:
            forbidden.append(relative)
        if path.stat().st_size > 95 * 1024 * 1024:
            oversized.append(relative)
        data = path.read_bytes()
        if any(marker.lower() in data.lower() for marker in workspace_markers):
            local_path_leaks.append(relative)
        if any(marker.lower() in data.lower() for marker in credential_markers):
            credential_leaks.append(relative)

    if forbidden:
        errors.append("forbidden game/save/secret files: " + ", ".join(forbidden))
    if oversized:
        errors.append("files over 95 MiB: " + ", ".join(oversized))
    if symlinks:
        errors.append("symlinks are not allowed: " + ", ".join(symlinks))
    if local_path_leaks:
        errors.append("local absolute paths found: " + ", ".join(local_path_leaks))
    if credential_leaks:
        errors.append("credential-like text found: " + ", ".join(credential_leaks))

    checksum_text = (ROOT / "SHA256SUMS.txt").read_text(encoding="utf-8")
    patch_checksum_line = f'{patch_metadata.get("sha256")}  {patch_relative.as_posix()}'
    if patch_checksum_line not in checksum_text.splitlines():
        errors.append("SHA256SUMS.txt does not bind the root patch")
    for key in ("sha256",):
        for section in ("source", "patch", "target"):
            value = str((status.get(section) or {}).get(key) or "")
            if re.fullmatch(r"[0-9a-f]{64}", value) is None:
                errors.append(f"invalid {section}.{key}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "release_state": status.get("release_state"),
        "files": len(files),
        "patch": patch_relative.as_posix(),
        "patch_size": patch.stat().st_size if patch.is_file() else None,
        "patch_sha256": sha256_file(patch) if patch.is_file() else None,
        "forbidden": forbidden,
        "oversized": oversized,
        "symlinks": symlinks,
        "local_path_leaks": local_path_leaks,
        "credential_leaks": credential_leaks,
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
