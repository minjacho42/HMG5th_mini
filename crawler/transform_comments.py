import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
# 전역 변수 설정
RAW_DATA_DIR = os.getenv('RAW_DATA_DIR')
PROCESSED_DATA_DIR = os.getenv('PROCESSED_DATA_DIR')


def log(message):
    print(f"[LOG] {message}")

def load_comments_json(title, episode):
    file_path = os.path.join(RAW_DATA_DIR, f"{title}_{episode}.json")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def classify_reader(comment:dict, threshold_time:datetime):
    comment_time = datetime.fromisoformat(comment["date"])
    return "충성 독자" if comment_time <= threshold_time else "일반 독자"

def get_threshold_time(comments:list):
    return datetime.fromisoformat(comments[-1]["date"]) + timedelta(hours=12)

def save_transformed_data(webtoon_name, episode, data:dict):
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    output_filename = f"{PROCESSED_DATA_DIR}/{webtoon_name}_{episode}_processed.json"
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

def classify_readers(webtoon_name, episode):
    log("웹툰 데이터 변환 시작")
    filename = f"{RAW_DATA_DIR}/{webtoon_name}_{episode}.json"
    log(f"웹툰 댓글 데이터 로드 중: {filename}")
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    comments = data["comments"]
    log(f"총 {len(comments)}개의 댓글 분석 중")
    
    # Find the earliest comment (last one in the list)
    first_comment_time = datetime.fromisoformat(comments[-1]["date"])
    threshold_time = first_comment_time + timedelta(hours=12) # 충성 독자 기준 시간
    log(f"첫 댓글 시간: {first_comment_time}")
    
    # Classify comments based on posting time
    for comment in comments:
        comment_time = datetime.fromisoformat(comment["date"])
        if comment_time <= threshold_time:
            comment["reader_loyalty"] = "충성 독자"
        else:
            comment["reader_loyalty"] = "일반 독자"
    
    # Save the updated data
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    output_filename = f"{PROCESSED_DATA_DIR}/{webtoon_name}_{episode}_processed.json"
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    
    log("웹툰 데이터 변환 완료")
    log(f"업데이트된 파일이 저장되었습니다: {output_filename}")

def main():
    title = '김부장'
    episode = 167
    classify_readers(title, episode)

if __name__ == "__main__":
    main()
