import json
import tiktoken

# Load the JSON file
file_path = 'crawler/comments_processed_data/배달왕_80_processed.json'  # 파일 경로를 입력하세요
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Convert JSON content to a string
json_string = json.dumps(data, ensure_ascii=False)

# Initialize tiktoken encoder for GPT-4
encoding = tiktoken.encoding_for_model("gpt-4")

# Count tokens in the string
tokens = encoding.encode(json_string)
token_count = len(tokens)

print(f"토큰 수: {token_count}")