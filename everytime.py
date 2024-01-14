from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

#########################[에브라타임 로그인]#########################
# ChromeDriver 경로 설정
webdriver_service = Service('/Users/gachonswacademy02/Desktop/Selenium/chromedriver-mac-x64/chromedriver')

# ChromeOptions 객체 생성
options = Options()

# WebDriver 객체 생성
driver = webdriver.Chrome(service=webdriver_service, options=options)

# 에브리타임 로그인 페이지 열기
driver.get('https://everytime.kr/login')

# 로그인 정보 입력 (아이디git rev-parse --show-toplevel와 비밀번호를 교체해야 합니다)
driver.find_element(By.NAME, 'id').send_keys('your_id')  # 아이디 입력
driver.find_element(By.NAME, 'password').send_keys('your_password')  # 비밀번호 입력

# 로그인 버튼 클릭
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

time.sleep(10)

#########################[소프트웨어학과 정보 공유 페이지]#########################
# '소프트웨어학과 정보 공유' 링크 클릭
link = driver.find_element(By.LINK_TEXT, '소프트웨어학과 정보 공유')
link.click()

#########################[검색]#########################
# 검색창에 "엔터프라이즈" 입력
search_box = driver.find_element(By.NAME, 'keyword')  # 검색창 선택
search_box.send_keys('카엔프')  # 검색창에 "엔터프라이즈" 입력

# 검색 실행(Enter 키 입력)
from selenium.webdriver.common.keys import Keys
search_box.send_keys(Keys.RETURN)  # Enter 키 입력

time.sleep(10)
#########################[검색결과 수집]#########################
# 모든 페이지를 순회하도록 while문 실행
while True:
    print("페이지 전환")
    # 게시글 링크 리스트 수집
    post_link_list = [post.get_attribute('href') for post in driver.find_elements(By.CSS_SELECTOR, 'article.list a.article')]

    for post_link in post_link_list:
        # 각 게시물에 접근
        driver.get(post_link)
        time.sleep(5)

        # 제목, 내용
        title = driver.find_element(By.CSS_SELECTOR, 'h2.large')
        content = driver.find_element(By.CSS_SELECTOR, 'p.large')
        print("제목: ", title.text)
        print("내용: ", content.text)

        # 댓글
        ## 댓글 리스트 수집
        comment_list = driver.find_elements(By.CSS_SELECTOR, 'article')
        # parent_comment = ""
        for comment in comment_list:
            if "parent" in comment.get_attribute("class"):
                parent_comment = comment.find_element(By.CSS_SELECTOR, 'p.large').text
                print("댓글: ", parent_comment)

            elif "child" in comment.get_attribute("class"):
                child_comment_content = comment.find_element(By.CSS_SELECTOR, 'p.large').text
                print("대댓글: ", child_comment_content)


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
        break

# 키 누르기 전까지 창 띄우도록
# input("클릭")


