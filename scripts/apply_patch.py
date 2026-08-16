#!/usr/bin/env python3
"""Apply the supported Shin Gihren xdelta patch and verify every file hash."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATCH = ROOT / "Shin_Gihren_no_Yabou_KO.xdelta"
SOURCE_SIZE = 1_667_629_056
SOURCE_SHA256 = "5c23bbf4bb0415edb04b00b3cadbcfa9c1d6fd776a5ef838408ccda682f44cc5"
PATCH_SIZE = 43_691_745
PATCH_SHA256 = "fc5e0c50d425b5a2f475c2cf2d0164dd66ba57d3effe6f4ea26c17a95d411587"
TARGET_SIZE = 1_667_629_056
TARGET_SHA256 = "f64044662f58e7e46df4a75c83ba88f82bae93386d7ef7713c7aef8574ca715b"
DEFAULT_OUTPUT = Path("Shin_Gihren_no_Yabou_KO_v0.1.0.iso")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_file(path: Path, size: int, digest: str, label: str) -> None:
    if not path.is_file():
        raise SystemExit(f"{label} 파일이 없습니다: {path}")
    actual_size = path.stat().st_size
    actual_digest = sha256_file(path)
    if actual_size != size or actual_digest != digest:
        raise SystemExit(
            f"{label} 검증 실패\n"
            f"  경로: {path}\n"
            f"  크기: {actual_size} (예상 {size})\n"
            f"  SHA-256: {actual_digest}\n"
            f"  예상값: {digest}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="신 기렌의 야망 한국어 xdelta 적용기")
    parser.add_argument("source", type=Path, help="지원 대상 일본판 1.01 원본 ISO")
    parser.add_argument("output", type=Path, nargs="?", default=DEFAULT_OUTPUT)
    parser.add_argument("--xdelta", default="xdelta3", help="xdelta3 실행 파일 또는 경로")
    parser.add_argument("--force", action="store_true", help="기존 출력 파일 덮어쓰기")
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    patch = PATCH.resolve()
    if output == source:
        raise SystemExit("원본 ISO와 출력 파일은 같은 경로일 수 없습니다.")
    if output == patch:
        raise SystemExit("xdelta 패치 파일을 출력 경로로 사용할 수 없습니다.")
    xdelta = shutil.which(args.xdelta)
    if xdelta is None and Path(args.xdelta).is_file():
        xdelta = str(Path(args.xdelta).resolve())
    if xdelta is None:
        raise SystemExit("xdelta3를 찾을 수 없습니다. PATH에 추가하거나 --xdelta로 경로를 지정하십시오.")
    if output.exists() and not args.force:
        raise SystemExit(f"출력 파일이 이미 있습니다: {output}\n덮어쓰려면 --force를 사용하십시오.")

    require_file(source, SOURCE_SIZE, SOURCE_SHA256, "원본 ISO")
    require_file(patch, PATCH_SIZE, PATCH_SHA256, "xdelta 패치")
    output.parent.mkdir(parents=True, exist_ok=True)

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=output.name + ".",
            suffix=".tmp",
            dir=output.parent,
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
        subprocess.run(
            [xdelta, "-f", "-d", "-s", str(source), str(patch), str(temp_path)],
            check=True,
        )
        require_file(temp_path, TARGET_SIZE, TARGET_SHA256, "패치 결과")
        os.replace(temp_path, output)
        temp_path = None
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"xdelta3 적용 실패: 종료 코드 {exc.returncode}") from exc
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)

    print(f"PASS: {output}")
    print(f"SIZE: {TARGET_SIZE}")
    print(f"SHA-256: {TARGET_SHA256}")


if __name__ == "__main__":
    main()
