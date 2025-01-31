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

# OpenAI API 설정
API_KEY = os.getenv("OPENAI_API_KEY")
GPT_MODEL = "gpt-4o"  # 또는 "gpt-3.5-turbo"

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=API_KEY)

# 보고서 저장 경로
PROMPT_FILE = os.getenv("PROMPT_FILE_PATH")
REPORTS_DIR = os.getenv("REPORTS_DIR")

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
        SELECT webtoon, episode, interest_count, like_count, rating, trend, comments, created_at 
        FROM webtoon_episodes 
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
    """GPT API 요청을 위한 프롬프트 생성"""
    prompt_text = load_prompt()
    if not prompt_text:
        return None
    
    webtoon_data = fetch_webtoon_row(title, episode)
    if not webtoon_data:
        return None

    webtoon, episode, interest_count, like_count, rating, trend, comments, created_at = webtoon_data

    prompt = f"{prompt_text}\n\n"
    prompt += f"### {webtoon} {episode}화 독자 반응 데이터\n"
    prompt += f"- 관심 수: {interest_count}\n"
    prompt += f"- 좋아요 수: {like_count}\n"
    prompt += f"- 평점: {rating}\n"
    prompt += f"- 트렌드 분석 데이터: {trend}\n"
    prompt += f"- 데이터 기록 시간: {created_at}\n\n"

    # JSON 파싱 예외 처리
    try:
        if isinstance(comments, str):
            comment_list = json.loads(comments)  # 문자열이면 JSON 변환
        elif isinstance(comments, list):
            comment_list = comments  # 이미 리스트라면 그대로 사용
        else:
            raise ValueError("comments 데이터가 JSON 변환 불가한 형식입니다.")
        

    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"[ERROR] {episode}화 댓글 데이터 로드 실패: {e}")
        comment_list = []

    # 부정적 댓글만 추출
    negative_comments = [c["text"] for c in comment_list if isinstance(c, dict) and c.get("sentiment_score", 0) <= -0.5]

    if negative_comments:
        prompt += "- 대표적인 독자 피드백: \n"
        for comment in negative_comments[:5]:  # 최대 5개 샘플링
            prompt += f"  - {comment}\n"
    else:
        prompt += "- 부정적인 댓글이 거의 없습니다.\n"

    return prompt

def gpt_analyze(prompt):
    """GPT API를 호출하여 웹툰 분석 수행"""
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a professional data analyst specializing in user feedback analysis."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def save_report(title, episode, content):
    """분석 결과를 보고서 파일로 저장"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_filename = os.path.join(REPORTS_DIR, f"{title}_{episode}_gpt_report.md")

    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(content)


def gpt_report(title, episode):
    """웹툰 데이터를 가져와 GPT 분석 후 저장"""
    prompt = generate_prompt(title, episode)
    if not prompt:
        return

    analysis_result = gpt_analyze(prompt)
    save_report(title, episode, analysis_result)

def main():
    """ 실행 함수 """
    title = "김부장"
    episode = 170
    gpt_report(title, episode)


if __name__ == "__main__":
    main()