import json
import os
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def load_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    comments = [comment['text'] for comment in data['comments']]
    return comments

def preprocess_text(comments):
    stopwords = {"너무", "진짜", "그냥", "좀", "더", "이건", "이게", "ㅋㅋ"}
    all_text = ' '.join(comments)
    words = all_text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return filtered_words

def generate_wordcloud(words, output_file='wordcloud.png'):
    word_counts = Counter(words)
    most_common_words = dict(word_counts.most_common(100))
    
    wordcloud = WordCloud(
        width=1000, 
        height=1000, 
        background_color='white',
        font_path='NanumGothic.ttf'
    ).generate_from_frequencies(most_common_words)
    
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_file)
    plt.show()

def main():
    input_file = 'webtoon_data/퀘스트지상주의_154.json'  # 분석할 JSON 파일 지정
    comments = load_comments(input_file)
    words = preprocess_text(comments)
    generate_wordcloud(words)

if __name__ == '__main__':
    main()
