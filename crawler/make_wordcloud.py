import json
import os
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 전역 변수 설정
INPUT_DIR = 'comments_data'
OUTPUT_DIR = 'wordcloud_output'
STOPWORDS = {"너무", "진짜", "그냥", "좀", "더", "이건", "이게", "ㅋㅋ"}
FONT_PATH = 'fonts/NanumGothic.ttf'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_comments(title, episode):
    file_path = os.path.join(INPUT_DIR, f"{title}_{episode}.json")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    comments = [comment['text'] for comment in data['comments']]
    return comments

def preprocess_text(comments):
    all_text = ' '.join(comments)
    words = all_text.split()
    filtered_words = [word for word in words if word not in STOPWORDS]
    return filtered_words

def generate_wordcloud(words, title, episode):
    word_counts = Counter(words)
    most_common_words = dict(word_counts.most_common(100))
    
    wordcloud = WordCloud(
        width=1000, 
        height=1000, 
        background_color='white',
        font_path=FONT_PATH
    ).generate_from_frequencies(most_common_words)
    
    output_file = os.path.join(OUTPUT_DIR, f"{title}_{episode}_wordcloud.png")
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_file)
    plt.show()
    print(f"워드 클라우드가 {output_file}로 저장되었습니다.")

def main():
    title = '퀘스트지상주의'
    episode = 156
    comments = load_comments(title, episode)
    words = preprocess_text(comments)
    generate_wordcloud(words, title, episode)

if __name__ == '__main__':
    main()
