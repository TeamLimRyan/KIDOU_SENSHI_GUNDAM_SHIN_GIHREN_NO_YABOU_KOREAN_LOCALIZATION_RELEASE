# 패치 형식

- 형식: VCDIFF/xdelta3
- 생성기: xdelta3 3.2.0
- 패치 파일: `Shin_Gihren_no_Yabou_KO.xdelta`
- 패치 크기: `45,466,271 bytes`
- 패치 SHA-256: `dd827e4845a4c208738cedd65525305e6235378cd377ad4b425188e44ef0a701`
- 애플리케이션 헤더: 비활성화 (`-A`)
- 보조 압축: LZMA
- 로컬 절대 경로 포함: 없음
- 원본·완성 ISO 포함: 없음

생성에 사용한 옵션:

```text
xdelta3 -f -e -A -s SOURCE.iso TARGET.iso PATCH.xdelta
```

복호화 검증 명령:

```text
xdelta3 -d -s SOURCE.iso PATCH.xdelta ROUNDTRIP.iso
```

`ROUNDTRIP.iso`의 크기와 SHA-256을 최종 검수 ISO와 비교한 뒤 `fc /b` 전체 바이트 비교도 수행했습니다.

```text
복호화 결과 크기     1,667,629,056 bytes
복호화 결과 SHA-256  29daf7a10554d6d6f37770481271bc641d531410b78542677173c90cbff5890f
전체 바이트 비교     PASS
```
