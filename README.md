# 웹툰 댓글 통합 ETL 파이프라인

## 통합 실행 예시

```bash
python main.py --title "퀘스트지상주의" --episode 153
```
- Extract 완료 데이터 : crawler/comments_raw_data/퀘스트지상주의_153.json
- Transform 완료 데이터 : crawler/comments_processed_data/퀘스트지상주의_153_processed.json
- Load 완료 데이터 : postgreSQL WEBTOON_DB에 저장

## 실행하기 전 DB 설정

### 1. psycopg2 라이브러리 설치
```bash
pip install psycopg2
```

### 2. postgresql 설치 (MacOS)
```bash
brew install postgresql
```
- Windows 사용자는 PostgreSQL 공식 사이트에서 설치 가능

### 3. postgresql 가동 (MacOS)
```bash
brew services start postgresql
```

### 4. postgres USER 생성
```bash
psql -U $(whoami) -d postgres
```
```sql
CREATE USER postgres WITH PASSWORD 'postgres';
ALTER ROLE postgres WITH SUPERUSER;
exit
```

### 5. WEBTOON_DB 생성
```bash
createdb -U $(whoami) WEBTOON_DB
```

## 통합 코드 실행 후 DB 적재 확인

### 1. WEBTOON_DB 접속
```bash
psql -U postgres -d WEBTOON_DB
```

### 2. 쿼리문 통해 확인
```sql
SELECT id, webtoon, episode FROM webtoon_episodes;
```


## 💾 저장 테이블 구조 (`webtoon_episodes`)

| 컬럼명 | 타입 | 설명 |
|--------|------|----------------------------------|
| `id` | `SERIAL PRIMARY KEY` | 자동 증가 기본 키 |
| `webtoon` | `VARCHAR(255)` | 웹툰 제목 |
| `episode` | `INT` | 회차 번호 |
| `interest_count` | `INT` | 관심 수 |
| `like_count` | `INT` | 좋아요 수 |
| `rating` | `FLOAT` | 별점 |
| `trend` | `JSONB` | 최근 5화 별점 및 부정 댓글 비율 |
| `comments` | `JSONB` | 댓글 데이터 (JSON 배열) |
| `created_at` | `TIMESTAMP` | 데이터 저장 시간 |

