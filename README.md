# 기동전사 건담 신 기렌의 야망 한국어 패치

> **v0.2.0 공개 릴리스 — `PUBLISHED`**

PSP 일본판 `機動戦士ガンダム 新ギレンの野望` 1.01용 비공식 한국어 현지화 패치 배포 저장소입니다.
소유자 공개 승인을 거쳐 GitHub 공개 저장소와 불변 Release 게시를 완료했습니다.

- 플랫폼: PlayStation Portable
- 게임 ID: `NPJH50441`
- 지원 버전: `1.01`
- 원본 크기: `1,667,629,056 bytes`
- 원본 SHA-256: `5c23bbf4bb0415edb04b00b3cadbcfa9c1d6fd776a5ef838408ccda682f44cc5`
- 최신 태그: `v0.2.0`
- 예정 저장소: `TeamLimRyan/KIDOU_SENSHI_GUNDAM_SHIN_GIHREN_NO_YABOU_KOREAN_LOCALIZATION_RELEASE`

## 반영 범위

- 현재 구조적으로 발견·검증된 번역 대상 텍스트 필드 `3,803/3,803`
- 한글 글리프 443자: 1바이트 37자 + 2바이트 406자 하이브리드 인코딩
- 최종 이미지 적용 대상 9,051개: 변경 8,817개, 승인된 원본 유지 234개
- 특별 계획 효과·설명 패널 137개 추가 현지화
- 기체명 필드가 한계 퍼센트 바이트를 덮어써 전 기체가 0%로 표시되던 회귀 수정
- 이벤트 캡션 156개와 보이스 캡션 5,529개 저장·표시 왕복 검증
- 보이스 캡션 런타임 제어 7,424개 발생 위치 검증
- 전략 메뉴 및 특별 계획의 런타임 이미지 라벨 반영
- 원문과 번역문의 행 길이 차이에 맞춘 이벤트·보이스 캡션 배열 재구성

수치는 서로 단위가 다른 텍스트 필드와 이미지 적용 대상을 합산하지 않습니다. 텍스트 수치는 발견된
필드 범위의 완료율이며 ISO 전체에서 존재 가능한 모든 문자열의 발견을 보증하는 표현이 아닙니다.

## 패치 파일

- 파일: `Shin_Gihren_no_Yabou_KO.xdelta`
- 크기: `45,466,271 bytes`
- SHA-256: `dd827e4845a4c208738cedd65525305e6235378cd377ad4b425188e44ef0a701`

최신 안정판은 [GitHub Releases의 v0.2.0](https://github.com/TeamLimRyan/KIDOU_SENSHI_GUNDAM_SHIN_GIHREN_NO_YABOU_KOREAN_LOCALIZATION_RELEASE/releases/tag/v0.2.0)에서
xdelta 패치를 받을 수 있습니다. 저장소와 릴리스에는 원본 ISO, 완성 ISO, BIOS, 펌웨어, 키,
세이브 또는 에뮬레이터 상태 파일을 포함하지 않습니다.

## 설치

Python 3과 `xdelta3`가 준비되어 있으면 저장소 루트에서 다음 명령으로 원본 검증, 패치 적용,
결과 검증을 한 번에 수행할 수 있습니다.

```powershell
python scripts/apply_patch.py "Kidou Senshi Gundam Shin Gihren no Yabou (1.01).iso"
```

직접 적용할 때는 다음 명령을 사용합니다.

```powershell
xdelta3 -d -s "Kidou Senshi Gundam Shin Gihren no Yabou (1.01).iso" `
  "Shin_Gihren_no_Yabou_KO.xdelta" `
  "Shin_Gihren_no_Yabou_KO_v0.2.0.iso"
```

자세한 절차는 [설치 안내](INSTALL_KO.md), 지원 범위는 [호환성 및 검증 범위](COMPATIBILITY_KO.md)를
확인하십시오.

## 결과 무결성

정상 적용 결과는 다음과 같습니다.

- 결과 크기: `1,667,629,056 bytes`
- 결과 SHA-256: `29daf7a10554d6d6f37770481271bc641d531410b78542677173c90cbff5890f`

배포 xdelta를 깨끗한 원본에 적용한 결과가 최종 검수 ISO와 SHA-256 및 전체 바이트 비교에서
정확히 일치함을 확인했습니다. 전체 값은 [SHA256SUMS.txt](SHA256SUMS.txt)에 있습니다.

## 런타임 검증과 공개된 한계

- v0.1.0 기준으로 PPSSPP v1.20.4에서 새로 부팅하여 경고 화면, 타이틀, NEW GAME, 시나리오·난이도·지원팀,
  이벤트·보이스 캡션, 전략 메인, 특별 계획 메뉴까지 진행했습니다.
- 위 경로에서 크래시, 캡션 배열 깨짐 및 확인 화면의 일본어 잔존이 없음을 검증했습니다.
- v0.2.0 변경분은 정적 역추출·픽셀·xdelta 왕복 검증을 완료했으며 별도 에뮬레이터 재검증은 하지 않았습니다.
- 전체 시나리오를 처음부터 끝까지 플레이한 장기 검증과 실제 PSP 하드웨어 검증은 아직 하지 않았습니다.
- 소유자의 원본 유지 결정에 따라 타이틀 로고는 일본어 원본 에셋을 사용합니다.

과거 PPSSPP 세이브스테이트는 이전 VRAM 텍스처를 보존할 수 있으므로 표시 검증은 새로 부팅해
진행하십시오. 자세한 내용은 [문제 해결](TROUBLESHOOTING_KO.md)을 확인하십시오.

## 오류 제보

[지원 안내](SUPPORT_KO.md)에 따라 패치 버전, 원본·패치·결과 해시, xdelta 버전, 운영체제,
PPSSPP 버전과 설정, 재현 순서 및 개인정보를 가린 스크린샷을 Issues에 남겨 주십시오.
ISO, BIOS, 키, 세이브 또는 에뮬레이터 상태 파일은 첨부하지 마십시오.

## 배포 및 권리

이 프로젝트는 비공식 팬메이드 한국어 패치입니다. 게임, 캐릭터, 상표, 로고와 원본 데이터의
권리는 각 권리자에게 있습니다. 이 저장소는 원본 게임을 제공하거나 대체하지 않으며, 사용자는
정당하게 보유한 지원 대상 일본판 ISO를 직접 준비해야 합니다. 자세한 고지는 [NOTICE.md](NOTICE.md)에 있습니다.
