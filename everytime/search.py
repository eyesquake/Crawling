# from selenium.common import NoSuchElementException
# from selenium.webdriver.common.by import By
# import pandas as pd
# import time
#
# def search_post(driver):
#     print("검색 페이지로 이동")
#     time.sleep(30) # 페이지가 로드될 때까지 기다리기
#
#     # 빈 DataFrame 생성
#     data = pd.DataFrame(columns=['제목', '내용', '댓글'])
#
#     #########################[소프트웨어학과 정보 공유 페이지]#########################
#     # '소프트웨어학과 정보 공유' 링크 클릭
#     link = driver.find_element(By.LINK_TEXT, '소프트웨어학과 정보 공유')
#     link.click()
#
#     #########################[검색]#########################
#     # 검색창에 "카엔프" 입력
#     search_box = driver.find_element(By.NAME, 'keyword')  # 검색창 선택
#     search_box.send_keys('카엔프')  # 검색창에 "카엔프" 입력
#
#     # 검색 실행(Enter 키 입력)
#     from selenium.webdriver.common.keys import Keys
#     search_box.send_keys(Keys.RETURN)  # Enter 키 입력
#
#     time.sleep(10)
#     #########################[검색결과 수집]#########################
#     # 모든 페이지를 순회하도록 while문 실행
#     # while True:
#     #     print("페이지 전환")
#         # 게시글 링크 리스트 수집
#     post_link_list = [post.get_attribute('href') for post in
#                       driver.find_elements(By.CSS_SELECTOR, 'article.list a.article')][:2]
#
#     for post_link in post_link_list:
#         # 각 게시물에 접근
#         driver.get(post_link)
#         time.sleep(5)
#
#         # 제목, 내용
#         title = driver.find_element(By.CSS_SELECTOR, 'h2.large')
#         content = driver.find_element(By.CSS_SELECTOR, 'p.large')
#         print("제목: ", title.text)
#         print("내용: ", content.text)
#
#         # 댓글
#         ## 댓글 리스트 수집
#         comment_list = driver.find_elements(By.CSS_SELECTOR, 'article')
#         comments = []
#         for comment in comment_list:
#             if "parent" in comment.get_attribute("class"):
#                 parent_comment = comment.find_element(By.CSS_SELECTOR, 'p.large').text
#                 print("댓글: ", parent_comment)
#                 comments.append(parent_comment)
#
#             elif "child" in comment.get_attribute("class"):
#                 child_comment_content = comment.find_element(By.CSS_SELECTOR, 'p.large').text
#                 print("대댓글: ", child_comment_content)
#                 comments.append(child_comment_content)
#
#         # 새로운 행 생성
#         new_row = pd.DataFrame({'제목': [title.text], '내용': [content.text], '댓글': ['\n'.join(comments)]})
#
#         # 기존 DataFrame에 새로운 행 추가
#         data = pd.concat([data, new_row], ignore_index=True)
#         print(data)
#         # 뒤로 가기를 실행하여 게시물 리스트 페이지로 돌아가기
#         driver.back()
#         time.sleep(10)
#
#         # 다음 페이지로 이동
#         # try:
#         #     # '다음 페이지' 버튼 클릭
#         #     next_button = driver.find_element(By.CSS_SELECTOR, 'a.next')
#         #     next_button.click()
#         #     time.sleep(5)
#         # except NoSuchElementException:
#         #     print("모든 페이지 순회 완료")
#         #     break
#
#     # 결과 DataFrame 반환
#     return data
