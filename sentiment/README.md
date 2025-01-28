# README for sentiment

### 개요

```sentiment_predictor.py```와 ```sentiment_visualizer.py```는 텍스트 데이터를 기반으로 감성 분석을 수행하고,<br>
분석 결과를 시각화하는 도구입니다.<br>
사전 학습된 Transformer 기반 모델을 사용하여 각 텍스트의 감성 점수를 예측하며,<br>
긍정, 부정, 중립으로 분류된 데이터를 그래프로 시각화할 수 있습니다.

## 주요 기능
#### ```sentiment_predictor.py```
* Hugging Face Transformers와 같은 사전 학습된 Transformer 모델을 활용해 감성 점수를 예측.
* 입력된 JSON 파일 데이터를 읽어 데이터프레임으로 변환.
* 감성 점수에 따라 label 열을 추가하여 결과를 저장.
* 결과를 CSV 파일로 저장.

#### ```sentiment_visualizer.py```
* 감성 분석 결과를 기반으로 긍정, 부정, 중립 비율을 원형 차트(Pie Chart)로 시각화.
* 특정 임계값(threshold)을 기준으로 중립(Negative와 Positive의 중간 상태)을 설정.
* CSV 파일로 저장된 데이터를 읽어 차트를 생성.

## 사용법
1. 의존성 설치
    <br>스크립트를 실행하기 전에 필요한 라이브러리를 설치합니다.<br>
    ```
    pip install transformers tqdm pandas matplotlib
    ```
### ```sentiment_predictor.py```
2. **로컬 모델 준비**<br>
    ```./pretrained_model``` 경로에 아래와 같이 사전 학습된 감성 분석 모델을 저장합니다.
    ```
   pretrained_model/
    ├── config.json
    ├── pytorch_model.bin
    ├── tokenizer_config.json
    ├── vocab.txt
    ```

3. **스크립트 실행** <br>
   스크립트를 실행하여 JSON 데이터를 분석하고 CSV로 결과를 저장합니다. 
   ```
    python sentiment_predictor.py --infile <입력 JSON 파일 경로> --outfile <출력 CSV 파일 경로>
   ```

   * --infile: 댓글 데이터를 포함한 JSON 파일 경로 (예: comments.json).
   * --outfile: 결과를 저장할 CSV 파일 경로 (예: output.csv).

### ```sentiment_visualizer.py```

2. **스크립트 실행** <br>
    sentiment_predictor.py에서 생성된 CSV 파일을 기반으로 분석 결과를 시각화
    ```
    python sentiment_visualizer.py --csvfile <분석 결과 CSV 파일 경로> [--threshold <사용자 설정 threshold>]
    ```
    각 감성(Positive, Neutral, Negative)의 비율을 원형 차트로 보여줍니다.

    기본적으로 threshold 값은 0.6으로 설정되며, 필요에 따라 변경 가능합니다.