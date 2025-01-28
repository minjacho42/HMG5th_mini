from crawler.extract_comments import scrape_recent_episodes, scrape_webtoon_comments
from crawler.transform_comments import load_comments_json, classify_reader, get_threshold_time, save_transformed_data
from sentiment.sentiment_predictor import get_sentiment_score, get_sentiment_classifier
import argparse
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

RAW_DATA_DIR = os.getenv('RAW_DATA_DIR')
PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')
LOCAL_MODEL_PATH = os.getenv('LOCAL_MODEL_PATH')

def log(message):
    print(f"[LOG] {message}")

def transform(title, episode):
    log("웹툰 데이터 변환 시작")
    log(f"웹툰 댓글 데이터 로드 중: {RAW_DATA_DIR}/{title}_{episode}.json")
    data = load_comments_json(title, episode)
    comments = data["comments"]
    log(f"총 {len(comments)}개의 댓글 분석 중")
    threshold_time = get_threshold_time(comments)
    log(f"충성 독자 구분 시간: {threshold_time}")
    log(f"Sentiment Classifier 로딩 중")
    classifier = get_sentiment_classifier(LOCAL_MODEL_PATH)
    log(f"Sentiment Classifier Load 완료")
    for comment in tqdm(comments):
        comment["sentiment_score"] = get_sentiment_score(comment["text"], classifier)
        comment["reader_loyalty"] = classify_reader(comment, threshold_time)
    save_transformed_data(title, episode, data)
    log("웹툰 데이터 변환 완료")
    log(f"업데이트된 파일이 저장되었습니다: {PROCESSED_DATA_DIR}/{title}_{episode}_processed.json")


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', required=True, help='Webtoon title')
    parser.add_argument('--episode', type=int, required=True, help='Episode number')
    args = parser.parse_args()

    scrape_recent_episodes(args.title)
    scrape_webtoon_comments(args.title, args.episode)
    transform(args.title, args.episode)


