import json
import tiktoken

# Load the JSON file
file_path = '/Users/admin/Downloads/%ED%80%98%EC%8A%A4%ED%8A%B8%EC%A7%80%EC%83%81%EC%A3%BC%EC%9D%98_top_100.json'  # 파일 경로를 입력하세요
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