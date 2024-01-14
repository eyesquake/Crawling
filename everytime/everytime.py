from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', None)  # 출력 너비 설정
pd.set_option('display.max_colwidth', None)  # 각 열의 최대 너비 설정

#########################[에브라타임 로그인]#########################
webdriver_service = Service('/Users/gachonswacademyo7/Documents/KAKAO/아이디어톤/셀레니움/chromedriver-mac-x64/chromedriver')
options = Options()
driver = webdriver.Chrome(service=webdriver_service, options=options)

driver.get('https://everytime.kr/login')

driver.find_element(By.NAME, 'id').send_keys('jinii915')  # 아이디 입력
driver.find_element(By.NAME, 'password').send_keys('Everytime1!')  # 비밀번호 입력

driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

time.sleep(10)

#########################[소프트웨어학과 정보 공유 페이지]#########################
link = driver.find_element(By.LINK_TEXT, '소프트웨어학과 정보 공유')
link.click()

#########################[검색]#########################
search_box = driver.find_element(By.NAME, 'keyword')  # 검색창 선택
search_box.send_keys('카엔프')  # 검색창에 "엔터프라이즈" 입력
search_box.send_keys(Keys.RETURN)  # Enter 키 입력

time.sleep(10)

#########################[검색결과 수집]#########################
data = pd.DataFrame(columns=['제목', '내용', '댓글', '대댓글'])  # 데이터를 저장할 DataFrame 생성

post_link_list = [post.get_attribute('href') for post in
                  driver.find_elements(By.CSS_SELECTOR, 'article.list a.article')][:5]

for post_link in post_link_list:
    # 각 게시물에 접근
    driver.get(post_link)
    time.sleep(5)

    # 제목, 내용
    title = driver.find_element(By.CSS_SELECTOR, 'h2.large').text
    content = driver.find_element(By.CSS_SELECTOR, 'p.large').text

    # 댓글
    ## 댓글 리스트 수집
    comment_list = driver.find_elements(By.CSS_SELECTOR, 'article')
    for comment in comment_list:
        if "parent" in comment.get_attribute("class"):
            parent_comment = comment.find_element(By.CSS_SELECTOR, 'p.large').text

            # 새로운 행 생성
            new_row = pd.DataFrame({
                '제목': [title],
                '내용': [content],
                '댓글': [parent_comment],
                '대댓글': ['']  # 대댓글 데이터 추가
            })

            # 기존 DataFrame에 새로운 행 추가
            data = pd.concat([data, new_row], ignore_index=True)

        elif "child" in comment.get_attribute("class"):
            child_comment_content = comment.find_element(By.CSS_SELECTOR, 'p.large').text

            # 새로운 행 생성
            new_row = pd.DataFrame({
                '제목': [title],
                '내용': [content],
                '댓글': [''],
                '대댓글': [child_comment_content]  # 대댓글 데이터 추가
            })

            # 기존 DataFrame에 새로운 행 추가
            data = pd.concat([data, new_row], ignore_index=True)

    # 뒤로 가기를 실행하여 게시물 리스트 페이지로 돌아가기
    driver.back()
    time.sleep(10)

print(data)
# 엑셀 파일로 저장
data.to_excel('data.xlsx', index=False)
