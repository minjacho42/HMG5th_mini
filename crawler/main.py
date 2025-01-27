import os
import argparse
from extract_comments import scrape_recent_episodes, scrape_webtoon_comments
from transform_comments import classify_readers
from make_wordcloud import generate_combined_wordcloud

def main(title, episode):
    print(f"웹툰 '{title}'의 에피소드 {episode} 처리 시작")

    # 1. 댓글 수집
    print("댓글 수집 중...")
    scrape_recent_episodes(title)
    scrape_webtoon_comments(title, episode)

    # 2. 댓글 전처리
    print("댓글 전처리 중...")
    classify_readers(title, episode)

    # 3. 워드 클라우드 생성
    print("워드 클라우드 생성 중...")
    generate_combined_wordcloud(title, episode)

    print(f"웹툰 '{title}'의 에피소드 {episode} 처리 완료.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="웹툰 댓글 수집 및 분석 파이프라인")
    parser.add_argument("--title", required=True, help="웹툰 제목")
    parser.add_argument("--episode", type=int, required=True, help="에피소드 번호")
    
    args = parser.parse_args()
    main(args.title, args.episode)