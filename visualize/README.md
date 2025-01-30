# 감정 분석 파이 차트 시각화

## 개요
이 스크립트는 감정 점수를 기반으로 댓글의 감정 분포를 파이 차트로 시각화합니다.<br>
주어진 임계값을 기준으로 댓글을 `긍정`, `중립`, `부정`으로 분류하며, <br>
`일반 독자`와 `충성 독자`를 구분하여 보여줍니다.

## 사용법
JSON 파일과 감정 점수 임계값을 지정하여 스크립트를 실행합니다:

```sh
python visualize_sentiment_pie.py --input comments.json --threshold 0.2 --output figure.png
```

### 인자 설명
- `--input` : 댓글 데이터를 포함한 JSON 파일 경로
- `--threshold` : 감정을 분류하는 기준이 되는 감정 점수 임계값
- `--output` : 다 그려진 플롯을 저장할 파일명.

## 입력 데이터 형식
JSON 파일은 `sentiment_score`(감정 점수)와 `reader_loyalty`(독자 충성도) 속성을 포함한 배열이어야 합니다. 예제:

```json
[
  {
    "nickname": "<nickname>",
    "text": "<comment>",
    "recomm": "<count of recommended>",
    "unrecomm": "<count of unrecommended>",
    "date": "YYYY-MM-DDTHH:MM:SS+0900",
    "sentiment_score": "<sentiment score value>",
    "reader_loyalty": "<충성 독자 or 일반 독자>"
  },
  {
    "nickname": "<nickname>",
    "text": "<comment>",
    "recomm": "<count of recommended>",
    "unrecomm": "<count of unrecommended>",
    "date": "YYYY-MM-DDTHH:MM:SS+0900",
    "sentiment_score": "<sentiment score value>",
    "reader_loyalty": "<충성 독자 or 일반 독자>"
  }
]
```

## 출력
스크립트는 다음과 같은 두 개의 파이 차트를 생성합니다:
1. **일반 독자 감정 분포**
2. **충성 독자 감정 분포**

각 차트는 `긍정`, `중립`, `부정` 댓글의 비율을 표시합니다.

## 예제
```sh
python visualize_sentiment_pie.py --input sample_comments.json --threshold 0.4 --output comment_fig.png
```
이 명령어는 `sample_comments.json` 파일을 읽고 `0.2` 임계값을 기준으로 감정을 분류하여 감정 분포 파이 차트를 생성합니다.
