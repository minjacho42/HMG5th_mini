import sys
import os
import json
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import argparse
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()


def get_sentiment_score(text: str, pipeline: TextClassificationPipeline):
    """
    주어진 text를 local model으로 감성 점수를 평가한다.
    1에 가까울수록 positive, -1에 가까울수록 negative 감성을 의미한다.

    :param text: The input text whose sentiment is to be analyzed.
    :type text: str
    :param pipeline: The sentiment classifier pipeline.
    :type pipeline: TextClassificationPipeline
    :return: The computed sentiment score. Positive score indicates
        positive sentiment, while a negative score indicates negative.
    :rtype: float
    """
    pred = pipeline(text)
    pred = pred[0]
    return round((int(pred['label']) * 2 - 1) * pred['score'], 2)

def get_sentiment_classifier(model_path: str):
    """
    사전 학습된 분류기 모델을 model_path에서 가져온다.

    :param model_path: Path to the directory containing the pre-trained model
        and tokenizer files.
        Type: str
    :return: TextClassificationPipeline object initialized with the specified
        pre-trained model and tokenizer.
        Type: TextClassificationPipeline
    """
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    return TextClassificationPipeline(tokenizer=tokenizer, model=model)

def set_sentiment_column(infile: str, outfile: str, model_path: str):
    """
    JSON 파일 내부의 comments 필드를 DataFrame으로 전환한다.
    DataFrame 내에 'label'이라는 column을 추가하고, 해당 column에 감성 점수를 넣는다.
    이후, DataFrame을 CSV 파일로 저장한다.

    :param infile: Path to the input JSON file containing comments.
    :type infile: str
    :param outfile: Path to save the resulting output CSV file.
    :type outfile: str
    :param model_path: Path to the directory containing the pretrained model.
    :type model_path: str
    :return: A pandas DataFrame containing the comments and their sentiment scores.
    :rtype: pandas.DataFrame
    :raises FileExistsError: If the output file already exists.
    :raises FileNotFoundError: If the input file does not exist.
    """

    # 사전 학습된 모델과 토크나이저 로드
    sentiment_classifier = get_sentiment_classifier(model_path)

    if os.path.exists(outfile):
        print("File already exists. Please choose another name.", file=sys.stderr)
        raise FileExistsError
    if not os.path.isfile(infile):
        print("Input file does not exist.", file=sys.stderr)
        raise FileNotFoundError

    with open(infile, 'r', encoding='utf-8') as f:
        comments_json = json.load(f)

    # DataFrame 생성 후 'label' 열 추가
    comment_df = pd.DataFrame(comments_json['comments'])
    # apply를 사용해 각 텍스트에 `get_sentiment` 호출
    comment_df['label'] = comment_df['text'].progress_apply(lambda text: get_sentiment_score(text, sentiment_classifier))
    # 결과 저장
    comment_df.to_csv(outfile, index=False)

    return comment_df

def main():
    tqdm.pandas()
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=True, help='Input JSON file with comments')
    parser.add_argument('--outfile', required=True, help='Output CSV file path')
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    set_sentiment_column(infile, outfile, os.getenv('LOCAL_MODEL_PATH'))

if __name__ == '__main__':
    main()