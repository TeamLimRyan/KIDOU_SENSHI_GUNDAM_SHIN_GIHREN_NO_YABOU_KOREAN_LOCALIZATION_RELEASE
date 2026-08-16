# 패치 형식

- 형식: VCDIFF/xdelta3
- 생성기: xdelta3 3.2.0
- 패치 파일: `Shin_Gihren_no_Yabou_KO.xdelta`
- 패치 크기: `43,691,745 bytes`
- 패치 SHA-256: `fc5e0c50d425b5a2f475c2cf2d0164dd66ba57d3effe6f4ea26c17a95d411587`
- 애플리케이션 헤더: 비활성화 (`-A`)
- 보조 압축: Static Huffman (`djw`)
- 로컬 절대 경로 포함: 없음
- 원본·완성 ISO 포함: 없음

생성에 사용한 옵션:

```text
xdelta3 -9 -S djw -A -a -G -e -s SOURCE.iso TARGET.iso PATCH.xdelta
```

복호화 검증 명령:

```text
xdelta3 -d -s SOURCE.iso PATCH.xdelta ROUNDTRIP.iso
```

`ROUNDTRIP.iso`의 크기와 SHA-256을 최종 검수 ISO와 비교한 뒤 `fc /b` 전체 바이트 비교도 수행했습니다.

```text
복호화 결과 크기     1,667,629,056 bytes
복호화 결과 SHA-256  f64044662f58e7e46df4a75c83ba88f82bae93386d7ef7713c7aef8574ca715b
전체 바이트 비교     PASS
```
