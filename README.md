# 성적 CSV 읽기 프로그램

## ① 무엇을 하나요 (What)

성적 CSV 파일을 읽어 유효한 성적 기록과 건너뛴 행의 정보를 반환합니다.

## ② 왜 만들었나요 (Why)

[성적 파일에 빈칸이나 잘못된 점수가 섞여 있을 때 어떻게 처리해야 하는지 확인하고 싶어서 제작했다.를 위해 유효한 기록과 잘못된 기록을 구분하는 기능이 필요했다.]

## ③ 어떻게 쓰나요 (How)

Python이 설치된 상태에서 저장소를 내려받고, 터미널에서 다음 명령을 순서대로 실행합니다.

```bash
git clone https://github.com/cewlsz/ai-programming-week11.git
cd ai-programming-week11
python -m pip install pytest pytest-cov
```

다음 명령으로 예제 CSV 파일을 읽습니다.

```bash
python -c "from load_scores import load_scores; kept, skipped = load_scores('scores.csv'); print('유효한 기록:', kept); print('건너뛴 행:', skipped)"
```

## ④ 어떻게 테스트하나요

저장소 폴더의 터미널에서 다음 명령을 실행합니다.

```bash
python -m pytest test_load_scores.py
```

실제 테스트 통과 결과:

```text
[1 passed in 0.03s]
```

## ⑤ 파일 구성

| 파일 | 하는 일 |
| --- | --- |
| load_scores.py | 성적 CSV 파일을 읽고 데이터를 검증하는 함수 |
| test_load_scores.py | 정상 파일을 읽는 동작을 확인하는 테스트 |
| scores.csv | 정상 기록과 잘못된 행이 섞인 예제 데이터 |
| empty.csv | 헤더만 있는 예제 데이터 |
| weird.csv | 잘못된 점수, 빈칸 등이 포함된 예제 데이터 |
| README.md | 설치, 실행 및 테스트 방법 안내 |
| .gitignore | Git에 기록하지 않을 파일과 폴더 설정 |
| LICENSE | MIT 라이선스 내용 |

## ⑥ 만든 사람 · AI를 어디에 썼는지

- 만든 사람: 이시후 / 2026100724
- AI를 쓴 곳: 실행 오류 해결 안내, GitHub 사용 절차 안내, README 초안 작성
- 내가 직접 판단한 것: 실행 결과를 확인하고 업로드할 파일을 선택했습니다.

## 라이선스

MIT License (LICENSE 파일 참고)