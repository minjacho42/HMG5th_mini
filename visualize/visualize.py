import matplotlib.pyplot as plt
import pandas as pd
import argparse
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

VISUALIZED_IMAGE_DIR = os.getenv("VISUALIZED_IMAGE_DIR")

colors = ['#66b3ff', '#ff9999', '#99ff99']
# Blue, Red, Green

def connect_db():
    """ PostgreSQL 연결 및 테이블 생성 """
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
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

def visualize_sentiment_pie(comments_df, threshold):
    comments_df['label'] = comments_df['sentiment_score'].apply(
        lambda x: 'Positive' if x >= threshold else ('Neutral' if x >= -1 * threshold else 'Negative')
    )
    readers_comment_df = comments_df.groupby('reader_loyalty')['label'].value_counts(normalize=True)
    loyalty_reader = readers_comment_df['일반 독자']
    non_loyalty_reader = readers_comment_df['충성 독자']
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].pie(loyalty_reader, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 12}, labels=loyalty_reader.index, colors=colors)
    ax[1].pie(non_loyalty_reader, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 12}, labels=non_loyalty_reader.index, colors=colors)
    ax[0].set_title('Loyalty Reader')
    ax[1].set_title('Non-Loyalty Reader')
    return fig

def visualize_trend(trend_df):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].plot(trend_df.index, trend_df["rating"], marker='o', linestyle='-', label="Rating")
    ax[0].set_xlabel("Trend ID")
    ax[0].set_ylabel("Rating")
    ax[0].set_ylim(0, 10)
    ax[0].set_title("Rating Trend")

    ax[1].plot(trend_df.index, trend_df["negative_comment_ratio"], marker='s', linestyle='--', label="Negative Comment Ratio")
    ax[1].set_xlabel("Trend ID")
    ax[1].set_ylabel("Value")
    ax[1].set_ylim(0, 100)
    ax[1].set_title("Rating and Negative Comment Ratio Trend")
    fig.suptitle("Trend Analysis")
    return fig

def load_trend_and_comments_from_db(title, episode_num):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT trend ,comments FROM webtoon_episodes 
        WHERE webtoon = '{title}' 
        AND episode = {episode_num};
    """)
    data = cursor.fetchall()
    trend, comments = data[0]
    return trend, comments

def visualize(title, episode_num):
    """ 전체 시각화 실행 함수 """
    trend, comments = load_trend_and_comments_from_db(title, episode_num)
    if trend is None or comments is None:
        print(f"[ERROR] {title} {episode_num}화 데이터가 존재하지 않습니다.")
        return

    # 트렌드 데이터 변환
    trend_df = pd.DataFrame(trend).T
    trend_df.index.name = 'Episode'
    trend_df['rating'] = trend_df['rating'].astype(float)
    trend_df['negative_comment_ratio'] = trend_df['negative_comment_ratio'].replace('N/A', 0).astype(float, errors='ignore')

    # 시각화 실행
    trend_fig = visualize_trend(trend_df)
    comments_df = pd.DataFrame(comments)
    sentiment_fig = visualize_sentiment_pie(comments_df, 0.6)

    # 결과 저장
    output_dir = VISUALIZED_IMAGE_DIR
    os.makedirs(output_dir, exist_ok=True)
    trend_fig.savefig(f"{output_dir}/{title}_{episode_num}_trend.png")
    sentiment_fig.savefig(f"{output_dir}/{title}_{episode_num}_sentiment.png")

    print(f"[INFO] 시각화 결과 저장 완료: {output_dir}")

def main():
    """ 단독 실행 시 기본 실행 함수 """
    title = '김부장'
    episode = 167
    visualize(title, episode)

if __name__ == "__main__":
    main()