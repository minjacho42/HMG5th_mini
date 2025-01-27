# 웹툰 댓글 크롤링 및 워드 클라우드 생성

네이버 웹툰의 특정 웹툰 특정 회차에 대한 댓글을 수집하고, 수집된 데이터를 기반으로 워드 클라우드를 생성하는 디렉토리

## 디렉토리 구조

```
crawler/
│-- comments_raw_data/   # 크롤링된 웹툰 댓글 JSON 파일 저장 디렉토리
|-- comments_processed_data/ # 전처리된 웹툰 댓글 JSON 파일 저장 디렉토리
|-- episode_data/        # 웹툰별 최근 에피소드 정보 JSON 파일 저장 디렉토리
│-- fonts/               # 워드 클라우드 제작에 사용되는 폰트 파일 저장 디렉토리
│-- mapping_data/ # 웹툰 제목, ID를 매핑한 JSON 파일 저장 디렉토리 (webtoon_info.json 포함)
│-- wordcloud_output/    # 생성된 워드 클라우드 이미지(PNG) 저장 디렉토리
│-- extract_comments.py   # 웹툰 댓글을 크롤링하는 스크립트
|-- transform_comments.py # 크롤링한 웹툰 댓글을 전처리하는 스크립트
|-- main.py                # 통합 ETL 파이프라인 실행 스크립트
│-- make_wordcloud.py    # 크롤링된 데이터를 기반으로 워드 클라우드를 생성하는 스크립트
```

## 통합 실행

**`main.py`** 실행
- `Extract` + `Transform` + `Wordcloud`
```bash
python main.py --title "퀘스트지상주의" --episode 154
```

## 개별 실행

### 사용법

1. **웹툰 댓글 + 최근 에피소드 정보 크롤링 (Extract)**
   - `extract_comments.py` 실행
   - `main` 함수 내부에서 원하는 웹툰 제목과 회차를 입력
   - 최근 에피소드 정보는 `episode_data/` 디렉토리에 JSON 형식으로 저장
   - 실행 결과는 `comments_raw_data/` 디렉토리에 JSON 형식으로 저장

   ```python
   def main():
       title = '퀘스트지상주의'
       episode = 154
       scrape_webtoon_comments(title, episode)
   
   if __name__ == '__main__':
       main()
   ```

2. **웹툰 댓글 전처리 (Transform)**
    - `transform_comments.py` 실행
    - `main` 함수 내부에서 원하는 웹툰 제목과 회차를 입력
    - 실행 결과는 `comments_processed_data/` 디렉토리에 JSON 형식으로 저장

   ```python
   def main():
       title = '퀘스트지상주의'
       episode = 154
       classify_readers(title, episode)
   
   if __name__ == '__main__':
       main()
   ```

3. **워드 클라우드 생성**
   - `make_wordcloud.py` 실행
   - `main` 함수에서 크롤링한 웹툰의 제목과 회차를 입력
   - 결과는 `wordcloud_output/` 디렉토리에 PNG 파일로 저장

   ```python
   def main():
       title = '퀘스트지상주의'
       episode = 154
       generate_wordcloud(title, episode)
   
   if __name__ == '__main__':
       main()
   ```


### 실행 순서 

1. `extract_comments.py`와 `transform_comments.py`와 `make_wordcloud.py` 코드 main 함수에 원하는 웹툰 원하는 회차 지정
2. 웹툰 댓글 크롤링: `extract_comments.py` 실행
3. 웹툰 댓글 전처리: `transform_comments.py` 실행
4. 워드 클라우드 생성: `make_wordcloud.py` 실행

### 예제 실행 (원하는 웹툰 원하는 회차 지정 후)

```bash
python extract_comments.py
python transform_comments.py
python make_wordcloud.py
```

### 파일 설명

- **`extract_comments.py`** : 네이버 웹툰에서 특정 웹툰의 특정 회차 댓글을 크롤링하여 JSON 파일로 저장합니다.
- **`transform_comments.py`** : 크롤링한 댓글 데이터를 전처리(충성/일반 독자 구분)하여 JSON 파일로 저장합니다.
- **`make_wordcloud.py`** : 저장된 댓글 데이터를 이용해 충성/일반 독자별 워드 클라우드를 생성하고 PNG 파일로 저장합니다.

## 주의 사항

- `mapping_data/webtoon_info.json` 파일이 있어야 크롤링이 정상적으로 작동합니다.
- `fonts/` 디렉토리에 워드 클라우드 생성을 위한 폰트 파일이 필요합니다.

