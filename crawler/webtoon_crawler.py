import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 전역 변수 설정
WEBTOON_INFO_FILE = 'mapping_data/webtoon_info.json'
SAVE_DIR = 'comments_data'
HEADERS = {'User-agent': 'Mozilla/5.0'}

def log(message):
    print(f"[LOG] {message}")

def load_webtoon_info(file_path=WEBTOON_INFO_FILE):
    log(f"웹툰 정보 로드 중: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def scrape_webtoon_comments(title, episode):
    log(f"웹툰 '{title}'의 에피소드 {episode} 댓글 수집 시작")
    webtoon_info = load_webtoon_info()
    if title not in webtoon_info:
        print(f"웹툰 '{title}' 정보를 찾을 수 없습니다.")
        return
    
    webtoon_id = webtoon_info[title]['id']
    url = f"https://comic.naver.com/webtoon/detail?titleId={webtoon_id}&no={episode}"
    log(f"웹툰 URL 접근 중: {url}")
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        log("페이지 요청 실패")
        return
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    log("페이지 로드 완료")
    time.sleep(3)
    
    # 관심웹툰 등록자수
    interest_count = driver.find_element(By.CLASS_NAME, 'UserAction__count--jk3vo').text
    log(f"관심웹툰 등록자수 수집 완료: {interest_count}")
    
    # 좋아요 수
    like_count = driver.find_element(By.CLASS_NAME, 'u_cnt._count').text
    log(f"좋아요 수 수집 완료: {like_count}")
    
    # 별점
    rating = driver.find_element(By.CLASS_NAME, 'UserAction__score--sP1ha').text
    log(f"별점 수집 완료: {rating}")
    
    # 전체 댓글 보기 버튼 클릭
    try:
        view_comments_btn = driver.find_element(By.CLASS_NAME, 'u_cbox_btn_view_comment')
        view_comments_btn.click()
        log("전체 댓글 보기 버튼 클릭")
        time.sleep(2)
    except:
        log("전체 댓글 보기 버튼이 없습니다.")
    
    # 더보기 버튼 클릭 (끝까지)
    log("댓글 로드 시작")
    while True:
        try:
            more_btn = driver.find_element(By.CLASS_NAME, 'u_cbox_paginate')
            more_btn.click()
            time.sleep(1)
        except:
            break
    
    comments_data = []
    comments = driver.find_elements(By.CLASS_NAME, 'u_cbox_comment_box')
    log(f"총 {len(comments)}개의 댓글을 수집 중")
    for comment in comments:
        try:
            text = comment.find_element(By.CLASS_NAME, 'u_cbox_contents').text
            recomm = comment.find_element(By.CLASS_NAME, 'u_cbox_cnt_recomm').text
            unrecomm = comment.find_element(By.CLASS_NAME, 'u_cbox_cnt_unrecomm').text
            comments_data.append({
                "text": text,
                "recomm": recomm,
                "unrecomm": unrecomm
            })
        except NoSuchElementException:
            continue
    log("댓글 수집 완료")
    
    driver.quit()
    
    # JSON 파일로 저장
    os.makedirs('comments_data', exist_ok=True)
    save_path = os.path.join(SAVE_DIR, f"{title}_{episode}.json")
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump({
            "webtoon": title,
            "episode": episode,
            "interest_count": interest_count,
            "like_count": like_count,
            "rating": rating,
            "comments": comments_data
        }, f, ensure_ascii=False, indent=4)
    
    log(f"{len(comments_data)}개의 댓글이 {save_path}에 저장되었습니다.")

def main():
    title = '퀘스트지상주의'
    episode = 157
    scrape_webtoon_comments(title, episode)

if __name__ == "__main__":
    main()



