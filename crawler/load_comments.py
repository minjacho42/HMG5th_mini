import json
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR")  # 댓글 JSON 데이터가 있는 폴더

def log(message):
    """로그 출력 함수"""
    print(f"[LOG] {message}")

def load_json(filepath):
    """ JSON 파일 로드 함수 """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        log(f"파일 없음: {filepath}")
        return None  # 파일이 없으면 None 반환
    

def connect_db():
    """ PostgreSQL 연결 및 테이블 생성 """
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # ✅ 테이블이 없으면 자동 생성
    create_table_query = """
    CREATE TABLE IF NOT EXISTS webtoon_episodes (
        id SERIAL PRIMARY KEY,
        webtoon VARCHAR(255) NOT NULL,
        episode INT NOT NULL,
        interest_count INT,
        like_count INT,
        rating FLOAT,
        trend JSONB,  -- 최근 5화의 별점 & 부정 댓글 비율 저장
        comments JSONB, -- 댓글 전체를 JSON 형태로 저장
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (webtoon, episode)  -- 중복 방지
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

    return conn

def insert_episode_data(webtoon_name, episode):
    """웹툰 회차 데이터를 DB에 적재"""
    conn = connect_db()
    cursor = conn.cursor()

    # 파일 경로 정의
    processed_file = os.path.join(PROCESSED_DATA_DIR, f"{webtoon_name}_{episode}_processed.json")

    # JSON 데이터 로드
    processed_data = load_json(processed_file)

    if processed_data is None:
        log(f"데이터 없음: {webtoon_name} {episode}")
        return

    # 기본 필드 추출
    interest_count = int(processed_data.get("interest_count", "0").replace(",", ""))
    like_count = int(processed_data.get("like_count", "0").replace(",", ""))
    rating = float(processed_data.get("rating", "0"))
    comments = json.dumps(processed_data.get("comments", []), ensure_ascii=False)

    # trend 필드 추출
    trend = processed_data.get("trend", {})
    trend_json = json.dumps(trend, ensure_ascii=False)

    # SQL INSERT 수행
    query = """
        INSERT INTO webtoon_episodes (webtoon, episode, interest_count, like_count, rating, trend, comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (webtoon, episode) DO UPDATE 
        SET interest_count = EXCLUDED.interest_count,
            like_count = EXCLUDED.like_count,
            rating = EXCLUDED.rating,
            trend = EXCLUDED.trend,
            comments = EXCLUDED.comments;
    """
    cursor.execute(query, (webtoon_name, episode, interest_count, like_count, rating, trend_json, comments))

    conn.commit()
    cursor.close()
    conn.close()
    log(f"DB 저장 완료: {webtoon_name} {episode}")

def main():
    """ 실행 함수 """
    title = "퀘스트지상주의"
    episode = 169
    insert_episode_data(title, episode)

if __name__ == "__main__":
    main()