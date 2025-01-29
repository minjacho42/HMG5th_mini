from crawler.extract_comments import scrape_recent_episodes, scrape_webtoon_comments
from crawler.transform_comments import transform
from crawler.update_trend import update_comments_with_trend
import argparse

def main(title, episode):
    print(f"웹툰 '{title}'의 에피소드 {episode} 처리 시작")

    # 1. 댓글 수집
    print("댓글 수집 중...")
    scrape_recent_episodes(title)
    scrape_webtoon_comments(title, episode)

    # 2. 댓글 전처리
    print("댓글 전처리 중...")
    transform(title, episode)
    update_comments_with_trend(title, episode)

    print(f"웹툰 '{title}'의 에피소드 {episode} 처리 완료.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="웹툰 댓글 수집 및 분석 파이프라인")
    parser.add_argument("--title", required=True, help="웹툰 제목")
    parser.add_argument("--episode", type=int, required=True, help="에피소드 번호")
    
    
    args = parser.parse_args()
    main(args.title, args.episode)