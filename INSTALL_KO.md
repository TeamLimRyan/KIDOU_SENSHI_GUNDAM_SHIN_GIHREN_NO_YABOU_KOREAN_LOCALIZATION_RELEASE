# 설치 안내

## 1. 준비물

- 정당하게 보유한 일본판 `機動戦士ガンダム 新ギレンの野望` 1.01 ISO
- `xdelta3`
- 이 저장소 루트의 `Shin_Gihren_no_Yabou_KO.xdelta`
- 패치 결과를 저장할 약 2 GB의 추가 여유 공간

원본 또는 패치된 ISO는 이 저장소에서 제공하지 않습니다.

## 2. 원본 확인

지원 원본:

```text
파일명 예시  Kidou Senshi Gundam Shin Gihren no Yabou (1.01).iso
게임 ID      NPJH50441
버전         1.01
크기         1,667,629,056 bytes
SHA-256      5c23bbf4bb0415edb04b00b3cadbcfa9c1d6fd776a5ef838408ccda682f44cc5
```

Windows PowerShell:

```powershell
Get-FileHash "Kidou Senshi Gundam Shin Gihren no Yabou (1.01).iso" -Algorithm SHA256
```

Linux 또는 macOS:

```bash
sha256sum "Kidou Senshi Gundam Shin Gihren no Yabou (1.01).iso"
```

파일명보다 크기와 SHA-256이 기준입니다. 값이 다르면 적용하지 마십시오.

## 3. 자동 적용과 검증

Python 3과 `xdelta3`가 PATH에 등록되어 있다면 저장소 루트에서 실행합니다.

```powershell
python scripts/apply_patch.py "Kidou Senshi Gundam Shin Gihren no Yabou (1.01).iso"
```

기본 출력 파일은 `Shin_Gihren_no_Yabou_KO_v0.1.0.iso`입니다. 다른 위치를 지정하려면 두 번째
인수를 사용합니다.

```powershell
python scripts/apply_patch.py "원본.iso" "D:\Games\Shin_Gihren_KO.iso"
```

`xdelta3`가 PATH에 없다면 실행 파일 경로를 지정할 수 있습니다.

```powershell
python scripts/apply_patch.py "원본.iso" --xdelta "C:\Tools\xdelta3.exe"
```

스크립트는 원본과 패치의 크기·SHA-256을 먼저 검사하고 임시 파일에 적용합니다. 결과 해시가
정확히 일치할 때만 최종 출력 파일명으로 바꿉니다.

## 4. 직접 적용

```powershell
xdelta3 -d -s "Kidou Senshi Gundam Shin Gihren no Yabou (1.01).iso" `
  "Shin_Gihren_no_Yabou_KO.xdelta" `
  "Shin_Gihren_no_Yabou_KO_v0.1.0.iso"
```

## 5. 결과 확인

```powershell
Get-FileHash "Shin_Gihren_no_Yabou_KO_v0.1.0.iso" -Algorithm SHA256
```

정상 결과:

```text
크기     1,667,629,056 bytes
SHA-256  f64044662f58e7e46df4a75c83ba88f82bae93386d7ef7713c7aef8574ca715b
```

## 6. 실행

검증에는 PPSSPP v1.20.4를 사용했습니다. 일본판 또는 이전 패치의 세이브스테이트를 불러오면
과거 VRAM 텍스처가 남아 표시가 다르게 보일 수 있으므로, 첫 확인은 반드시 ISO를 새로 부팅해
진행하십시오. 일반 저장 데이터를 사용하기 전에는 별도 백업을 권장합니다.
