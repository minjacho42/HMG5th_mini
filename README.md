# 웹툰 댓글 통합 ETL 파이프라인

## 통합 실행 예시

```bash
python main.py --title "퀘스트지상주의" --episode 153
```
- Extract 완료 데이터 : crawler/comments_raw_data/퀘스트지상주의_153.json
- Transform 완료 데이터 : crawler/comments_processed_data/퀘스트지상주의_153_processed.json