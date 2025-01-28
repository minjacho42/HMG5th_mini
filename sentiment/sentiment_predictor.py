import sys
import os
import json
from tqdm import tqdm
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import argparse

local_model_path = "./pretrained_model"
tqdm.pandas()

## 사전학습된 감성분석 모델 불러오기.
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
model = AutoModelForSequenceClassification.from_pretrained(local_model_path)
sentiment_classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model)


def get_sentiment(text:str):
    """
    주어진 text를 local model으로 감성 점수를 평가한다.
    1에 가까워질수록 positive -1에 가까워질수록 negative 감성을 의미한다.

    :param text: The input text whose sentiment is to be analyzed.
    :type text: str
    :return: The computed sentiment score. A positive score indicates
        positive sentiment, while a negative score indicates negative
        sentiment.
    :rtype: float
    """
    pred = sentiment_classifier(text)
    pred = pred[0]
    return round((int(pred['label']) * 2 - 1) * pred['score'], 2)


def set_sentiment_column(infile:str, outfile:str):
    """
    Json 파일 내부의 comments 필드를 DataFrame으로 전환한다.
    DataFrame내에 'label'이라는 column을 추가하고, 해당 column에 감성점수를 넣는다.
    이후, DataFrame을 csv 파일로 저장한다.

    :param infile: Path to the input JSON file containing comments.
    :type infile: str
    :param outfile: Path to save the resulting output CSV file.
    :type outfile: str
    :return: A pandas DataFrame containing the comments and their calculated sentiment labels.
    :rtype: pandas.DataFrame
    :raises FileExistsError: If the output file already exists.
    :raises FileNotFoundError: If the input file does not exist.
    """

    if os.path.exists(outfile):
        print("File already exists. Please choose another name.", file=sys.stderr)
        raise FileExistsError
    if not os.path.isfile(infile):
        print("Input file does not exist.", file=sys.stderr)
        raise FileNotFoundError

    with open(infile, 'r', encoding='utf-8') as f:
        comments_json = json.load(f)

    comment_df = pd.DataFrame(comments_json['comments'])
    comment_df['label'] = comment_df['text'].progress_apply(get_sentiment)
    comment_df.to_csv(outfile, index=False)

    return comment_df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=True, help='Input JSON file with comments')
    parser.add_argument('--outfile', required=True, help='Output CSV file path')
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    set_sentiment_column(infile, outfile)

if __name__ == '__main__':
    main()