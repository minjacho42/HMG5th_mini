import json
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

# 전역 변수 설정
WEBTOON_INFO_FILE = os.getenv('WEBTOON_INFO_FILE')
EPISODE_DATA_DIR = os.getenv('EPISODE_DATA_DIR')
RAW_DATA_DIR = os.getenv('RAW_DATA_DIR')
HEADERS = {'User-agent': 'Mozilla/5.0'}

def log(message):
    print(f"[LOG] {message}")

def load_webtoon_info(file_path=WEBTOON_INFO_FILE):
    log(f"웹툰 정보 로드 중: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def init_webdriver():
    """Selenium 웹드라이버 초기화 및 설정"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
def scrape_recent_episodes(title):
    log(f"웹툰 '{title}'의 최근 회차 정보 수집 시작")
    webtoon_info = load_webtoon_info()
    
    if title not in webtoon_info:
        print(f"웹툰 '{title}' 정보를 찾을 수 없습니다.")
        return
    
    webtoon_id = webtoon_info[title]['id']
    url = f"https://comic.naver.com/webtoon/list?titleId={webtoon_id}"
    log(f"웹툰 URL 접근 중: {url}")
    
    driver = init_webdriver()
    driver.get(url)
    log("페이지 로드 완료")
    time.sleep(3)
    
    # 최근 에피소드 목록 가져오기
    episode_elements = driver.find_elements(By.CLASS_NAME, 'EpisodeListList__item--M8zq4')
    
    episodes_data = []
    for episode in episode_elements:
        try:
            episode_title = episode.find_element(By.CLASS_NAME, 'EpisodeListList__title--lfIzU').text
            episode_num = re.search(r"no=(\d+)", episode.find_element(By.CLASS_NAME, "EpisodeListList__link--DdClU").get_attribute("href")).group(1)
            episode_rating = episode.find_element(By.CLASS_NAME, 'Rating__star_area--dFzsb').find_element(By.CLASS_NAME, 'text').text
            episode_date = episode.find_element(By.CLASS_NAME, 'EpisodeListList__meta_info--Cgquz').find_element(By.CLASS_NAME, 'date').text

            episodes_data.append({
                "title": episode_title,
                "episode": episode_num,
                "rating": episode_rating,
                "date": episode_date
            })
        except NoSuchElementException:
            continue

    log(f"총 {len(episodes_data)}개의 에피소드 정보 수집 완료")
    driver.quit()

    # JSON 파일로 저장
    os.makedirs(EPISODE_DATA_DIR, exist_ok=True)
    save_path = os.path.join(EPISODE_DATA_DIR, f"{title}.json")
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump({"webtoon": title, "episodes": episodes_data}, f, ensure_ascii=False, indent=4)
    
    log(f"{title}의 에피소드 정보가 {save_path}에 저장되었습니다.")

def scrape_webtoon_comments(title, episode):
    log(f"웹툰 '{title}'의 에피소드 {episode} 댓글 수집 시작")
    webtoon_info = load_webtoon_info()

    if title not in webtoon_info:
        log(f"웹툰 '{title}' 정보를 찾을 수 없습니다.")
        return
    
    webtoon_id = webtoon_info[title]['id']
    url = f"https://comic.naver.com/webtoon/detail?titleId={webtoon_id}&no={episode}"
    log(f"웹툰 URL 접근 중: {url}")
    
    driver = init_webdriver()
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
            nickname = comment.find_element(By.CLASS_NAME, 'u_cbox_nick').text
            text = comment.find_element(By.CLASS_NAME, 'u_cbox_contents').text
            recomm = comment.find_element(By.CLASS_NAME, 'u_cbox_cnt_recomm').text
            unrecomm = comment.find_element(By.CLASS_NAME, 'u_cbox_cnt_unrecomm').text
            date = comment.find_element(By.CLASS_NAME, 'u_cbox_date').get_attribute('data-value')
            comments_data.append({
                "nickname": nickname,
                "text": text,
                "recomm": recomm,
                "unrecomm": unrecomm,
                "date": date
            })
        except NoSuchElementException:
            continue
    log("댓글 수집 완료")
    
    driver.quit()
    
    # JSON 파일로 저장
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    save_path = os.path.join(RAW_DATA_DIR, f"{title}_{episode}.json")
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
    title = '김부장'
    episode = 167
    scrape_recent_episodes(title)
    scrape_webtoon_comments(title, episode)

if __name__ == "__main__":
    main()



