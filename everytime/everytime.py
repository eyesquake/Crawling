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

#########################[에브라타임 로그인] - chromedriver 설치 주소로 바꾸기 #########################
webdriver_service = Service('/Users/gachonswacademy02/Desktop/Selenium/chromedriver-mac-x64/chromedriver')
# webdriver_service = Service('/Users/gachonswacademyo7/Documents/KAKAO/아이디어톤/셀레니움/chromedriver-mac-x64/chromedriver')
options = Options()
driver = webdriver.Chrome(service=webdriver_service, options=options)

driver.get('https://everytime.kr/login')

# 로그인 정보 입력 (아이디와 비밀번호를 교체해야 합니다)
driver.find_element(By.NAME, 'id').send_keys('yougi8')  # 아이디 입력
driver.find_element(By.NAME, 'password').send_keys('wldusWkd!')  # 비밀번호 입력

driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

time.sleep(10)

#########################[검색]#########################
# # 검색어 리스트
keywords = ['엔터프라이즈', '카엔프', 'KEA', '카카오']

#########################[검색결과 수집]#########################
data = pd.DataFrame(columns=['제목', '내용', '댓글', '대댓글'])  # 데이터를 저장할 DataFrame 생성
# 검색어 리스트에 있는 검색어 하나씩 순차검색
for search_keyword in keywords:
    #########################[소프트웨어학과 정보 공유 페이지]#########################
    # '소프트웨어학과 정보 공유' 링크 클릭
    link = driver.find_element(By.LINK_TEXT, '소프트웨어학과 정보 공유')
    link.click()

    # 검색창에 검색어 입력
    search_box = driver.find_element(By.NAME, 'keyword')  # 검색창 선택
    search_box.clear()  # 이전 검색어 삭제
    search_box.send_keys(search_keyword)  # 검색창에 검색어 입력

    # 검색 실행
    from selenium.webdriver.common.keys import Keys
    search_box.send_keys(Keys.RETURN)  # Enter 키 입력
    time.sleep(10)

    # 모든 페이지를 순회하도록 while문 실행
    while True:
        print("페이지 전환")
        # 게시글 링크 리스트 수집
        post_link_list = [post.get_attribute('href') for post in
                          driver.find_elements(By.CSS_SELECTOR, 'article.list a.article')]

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
        # 다음 페이지로 이동
        try:
            # '다음 페이지' 버튼 클릭
            next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')
            next_button.click()
            time.sleep(5)
        except NoSuchElementException:
            print("모든 페이지 순회 완료")
            time.sleep(5)
            break

print(data)
# 엑셀 파일로 저장
data.to_excel('final_data.xlsx', index=False)
