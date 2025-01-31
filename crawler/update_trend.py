import json
import os
from dotenv import load_dotenv

load_dotenv()

PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR")  # 댓글 JSON 데이터가 있는 폴더
EPISODE_DATA_DIR = os.getenv("EPISODE_DATA_DIR")  # 별점 정보가 있는 폴더


def log(message):
    print(f"[LOG] {message}")


def load_json(filepath):
    """ JSON 파일 로드 함수 """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filepath, data):
    """ JSON 파일 저장 함수 """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_recent_ratings(webtoon_name, current_episode):
    """ 최근 5화의 별점 데이터를 가져옴 """
    episode_file = os.path.join(EPISODE_DATA_DIR, f"{webtoon_name}.json")
    episode_data = load_json(episode_file)

    # 최근 5화 찾기 (현재 화 포함)
    recent_episodes = {str(ep["episode"]): ep["rating"] for ep in episode_data["episodes"]}
    recent_ratings = {
        ep: recent_episodes[ep]
        for ep in sorted(recent_episodes.keys(), key=int, reverse=True)
        if int(ep) >= current_episode - 4 and int(ep) <= current_episode
    }

    return recent_ratings

def get_recent_negative_comment_ratios(webtoon_name, current_episode):
    """ 최근 5화의 부정적 댓글 비율을 가져옴 """
    negative_ratios = {}

    for ep in range(current_episode - 4, current_episode + 1):
        file_path = os.path.join(PROCESSED_DATA_DIR, f"{webtoon_name}_{ep}_processed.json")

        if not os.path.exists(file_path):
            log(f"파일 없음: {file_path}")
            continue    # 해당 화의 데이터가 없으면 건너뜀

        data = load_json(file_path)
        comments = data.get("comments", [])

        if not comments:
            negative_ratios[str(ep)] = 0    # 댓글이 없으면 부정 비율 0%
            continue

        # sentiment_score -0.5 이하인 댓글 수 계산
        negative_comments = sum(1 for c in comments if c.get("sentiment_score", 0) <= -0.5)
        total_comments = len(comments)

        # 부정 댓글 비율 계산 (소수점 둘째 자리까지)
        negative_ratios[str(ep)] = round(negative_comments / total_comments * 100, 2) if total_comments > 0 else 0

    return negative_ratios

def update_comments_with_trend(webtoon_name, episode):
    """ 댓글 JSON 파일을 업데이트하여 trend(추이) 필드 추가 """
    processed_file = os.path.join(PROCESSED_DATA_DIR, f"{webtoon_name}_{episode}_processed.json")

    # 댓글 JSON 파일 로드
    if not os.path.exists(processed_file):
        log(f"파일 없음: {processed_file}")
        return

    data = load_json(processed_file)

    # 최근 5화 별점 및 부정 댓글 비율 가져오기
    recent_ratings = get_recent_ratings(webtoon_name, episode)
    recent_negative_ratios = get_recent_negative_comment_ratios(webtoon_name, episode)

    # trend 필드 추가
    data["trend"] = {
        ep: {
            "rating": recent_ratings.get(ep, "N/A"),
            "negative_comment_ratio": recent_negative_ratios.get(ep, "N/A")
        }
        for ep in recent_ratings.keys()
    }

    # 업데이트된 JSON 저장
    save_json(processed_file, data)
    log(f"업데이트 완료: {processed_file}")


if __name__ == "__main__":
    # 예제 실행
    webtoon_name = "퀘스트지상주의"
    episode = 152
    update_comments_with_trend(webtoon_name, episode)