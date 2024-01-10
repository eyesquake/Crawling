from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# ChromeDriver 경로 설정
webdriver_service = Service('/Users/gachonswacademyo7/Documents/KAKAO/아이디어톤/chromedriver-mac-x64/chromedriver')

# ChromeOptions 객체 생성
options = Options()

# WebDriver 객체 생성
driver = webdriver.Chrome(service=webdriver_service, options=options)

# 에브리타임 로그인 페이지 열기
driver.get('https://everytime.kr/login')

# 로그인 정보 입력 (아이디와 비밀번호를 교체해야 합니다)
driver.find_element(By.NAME, 'id').send_keys('your_id')  # 아이디 입력
driver.find_element(By.NAME, 'password').send_keys('your_password')  # 비밀번호 입력

# 로그인 버튼 클릭
driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

# 키 누르기 전까지 창 띄우도록
input("클릭")