import openai
import json

# GPT API 설정
openai.api_key = "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"

# JSON 파일 로드
file_path = './crawler/comments_data/퀘스트지상주의_157_top100.json'
with open(file_path, encoding='utf-8') as file:
    data = json.load(file)

# 댓글 데이터 추출
comments = data["top_comments"]
webtoon_name = data["webtoon"]
episode_number = data["episode"]

# GPT API 요청 함수 정의
def generate_report(comments, webtoon_name, episode_number):
    prompt = f"""
웹툰 "{webtoon_name}" {episode_number}화에 대한 주요 댓글 데이터를 분석하여 A4 한 장 분량의 보고서를 작성해주세요. 보고서에는 아래 내용을 포함해주세요:
1. 주요 피드백 (독자들의 긍정적 및 부정적 반응)
2. 개선 요구 사항
3. 결론
4. 액션 플랜 (우선, 단기, 장기 전략을 구분)

데이터는 다음과 같습니다:
{comments[:20]}  # 주요 20개의 댓글만 포함
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # 또는 "gpt-4"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 보고서 생성
report = generate_report(comments, webtoon_name, episode_number)

# 보고서 출력
print("=== 보고서 ===")
print(report)

# 파일 저장
output_path = f"./feedback_data/{webtoon_name}_{episode_number}_feedback.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(report)

