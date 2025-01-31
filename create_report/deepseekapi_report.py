import json
import psycopg2
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# DeepSeek API 설정
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
API_KEY = os.getenv("DEEPSEEK_API_KEY")

# OpenAI 클라이언트 초기화 (DeepSeek 사용)
client = OpenAI(api_key=API_KEY, base_url=DEEPSEEK_BASE_URL)

# 경로 설정
PROMPT_FILE = "prompt.txt"  # 사용할 프롬프트 파일
REPORTS_DIR = "reports"  # 분석 결과 저장 디렉토리

def log(message):
    """로그 출력 함수"""
    print(f"[LOG] {message}")

def load_prompt():
    """프롬프트 파일 로드"""
    if not os.path.exists(PROMPT_FILE):
        log(f"❌ 프롬프트 파일({PROMPT_FILE})이 존재하지 않습니다.")
        return None

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()


def fetch_webtoon_row(title, episode):
    """PostgreSQL에서 특정 웹툰의 특정 회차 데이터 가져오기"""
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()

    query = """
        SELECT webtoon, episode, interest_count, like_count, rating, trend, comments, created_at FROM webtoon_episodes 
        WHERE webtoon = %s AND episode = %s;
    """

    cursor.execute(query, (title, episode))
    data = cursor.fetchone()
    
    conn.close()
    
    if not data:
        log(f"❌ {title} {episode}화의 데이터를 찾을 수 없습니다.")
        return None
    
    return data

def generate_prompt(title, episode):
    """DeepSeek API 요청을 위한 프롬프트 생성"""
    prompt_text = load_prompt()
    if not prompt_text:
        return None

    webtoon_data = fetch_webtoon_row(title, episode)
    if not webtoon_data:
        return None

    webtoon, episode, interest_count, like_count, rating, trend, comments, created_at = webtoon_data

    # DeepSeek 프롬프트 구성
    prompt = f"{prompt_text}\n\n"
    prompt += f"### {webtoon} {episode}화 독자 반응 데이터\n"
    prompt += f"- 관심 수: {interest_count}\n"
    prompt += f"- 좋아요 수: {like_count}\n"
    prompt += f"- 평점: {rating}\n"
    prompt += f"- 트렌드 분석 데이터: {trend}\n"
    prompt += f"- 데이터 기록 시간: {created_at}\n\n"

    # 부정적 댓글만 추출
    try:
        comment_list = json.loads(comments)
        negative_comments = [c["text"] for c in comment_list if c["sentiment_score"] <= -0.5]
    except (json.JSONDecodeError, TypeError):
        log("❌ 댓글 데이터 로드 실패")
        negative_comments = []

    if negative_comments:
        prompt += "- 대표적인 독자 피드백: \n"
        for comment in negative_comments[:5]:  # 최대 5개 샘플링
            prompt += f"  - {comment}\n"
    else:
        prompt += "- 부정적인 댓글이 거의 없습니다.\n"

    return prompt

def deepseek_analyze(prompt):
    """DeepSeek API를 호출하여 웹툰 분석 수행"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    return response.choices[0].message.content


def save_report(title, episode, content):
    """분석 결과를 보고서 파일로 저장"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_filename = os.path.join(REPORTS_DIR, f"{title}_{episode}_report.md")

    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(content)

    log(f"📌 보고서 저장 완료: {report_filename}")

def deepseek_report(title, episode):
    """웹툰 데이터를 가져와 DeepSeek 분석 후 저장"""
    prompt = generate_prompt(title, episode)
    if not prompt:
        return

    analysis_result = deepseek_analyze(prompt)
    save_report(title, episode, analysis_result)


def main():
    """PostgreSQL 데이터를 기반으로 DeepSeek 분석 및 보고서 생성"""
    title = "퀘스트지상주의"
    episode = 169
    deepseek_report(title, episode)


if __name__ == "__main__":
    main()