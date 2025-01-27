import json
import os
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 전역 변수 설정
INPUT_DIR = 'comments_processed_data'
OUTPUT_DIR = 'wordcloud_output'
STOPWORDS = {"너무", "진짜", "그냥", "좀", "더", "이건", "이게", "ㅋㅋ"}
FONT_PATH = 'fonts/NanumGothic.ttf'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_comments(title, episode):
    """지정된 웹툰과 에피소드의 댓글 데이터를 불러오기"""
    file_path = os.path.join(INPUT_DIR, f"{title}_{episode}_processed.json")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 독자 유형별 댓글 분류
    general_comments = [comment['text'] for comment in data['comments'] if comment['reader_loyalty'] == '일반 독자']
    loyal_comments = [comment['text'] for comment in data['comments'] if comment['reader_loyalty'] == '충성 독자']

    return general_comments, loyal_comments

def preprocess_text(comments):
    """댓글 텍스트 전처리 및 불용어 제거"""
    all_text = ' '.join(comments)
    words = all_text.split()
    filtered_words = [word for word in words if word not in STOPWORDS]
    return filtered_words

def generate_combined_wordcloud(title, episode):
    """일반 독자와 충성 독자의 워드 클라우드를 하나의 이미지로 결합"""

    # 댓글 데이터 로드 및 전처리
    general_comments, loyal_comments = load_comments(title, episode)
    general_words = preprocess_text(general_comments)
    loyal_words = preprocess_text(loyal_comments)
    
    # 일반 독자 워드클라우드 생성
    general_word_counts = Counter(general_words)
    general_wordcloud = WordCloud(
        width=600, 
        height=600, 
        background_color='white',
        font_path=FONT_PATH
    ).generate_from_frequencies(general_word_counts)

    # 충성 독자 워드클라우드 생성
    loyal_word_counts = Counter(loyal_words)
    loyal_wordcloud = WordCloud(
        width=600, 
        height=600, 
        background_color='white',
        font_path=FONT_PATH
    ).generate_from_frequencies(loyal_word_counts)

    # 플롯 설정
    plt.figure(figsize=(14, 7))

    # 일반 독자 워드클라우드
    plt.subplot(1, 2, 1)
    plt.imshow(general_wordcloud, interpolation='bilinear')
    plt.title('General Reader Word Cloud')
    plt.axis('off')

    # 충성 독자 워드클라우드
    plt.subplot(1, 2, 2)
    plt.imshow(loyal_wordcloud, interpolation='bilinear')
    plt.title('Loyal Reader Word Cloud')
    plt.axis('off')

    # 저장 및 출력
    output_file = os.path.join(OUTPUT_DIR, f"{title}_{episode}_combined_wordcloud.png")
    plt.savefig(output_file)
    plt.show()
    print(f"워드 클라우드가 {output_file}로 저장되었습니다.")

def main():
    title = '김부장'
    episode = 167

    # 워드 클라우드 생성 및 저장
    generate_combined_wordcloud(title, episode)

if __name__ == '__main__':
    main()