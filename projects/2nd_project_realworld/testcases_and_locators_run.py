# -*- coding: utf-8 -*-
from ai_generate.claude_generate import generate_with_claude
from file_manage import read_file, save_data_append, save_data_overwrite
from google_sheets.fetcher import DataFetcher
from google_sheets.converter import GoogleSheetsConverter
from html_crawler.crawling import capture_page
from html_crawler.html_locators import CRAWLING_LOCATORS
from prompts.locator import LOCATOR_PROMPT
import time
import re

# api 응답에서 python 태그를 제거하는 함수
def remove_python_tags(content: str) -> str:
    content = content.strip()
    content = re.sub(r"^```python\s*", "", content, flags=re.IGNORECASE|re.MULTILINE)
    content = re.sub(r"\s*```$", "", content, flags=re.MULTILINE)
    return content.lstrip("\n")

def run():
        # 로케이터 자동 생성
    for locator in CRAWLING_LOCATORS:
        # HTML 파일 생성 및 저장
        capture_page(*locator)  # DB 연결시 사용 가능, 임시 주석처리함

        # LLM로 로케이터 추출 및 저장
        html_path = f"html_data/{locator[0]}.html" 
        llm_payload = read_file(html_path)
        page_locators = generate_with_claude(LOCATOR_PROMPT, llm_payload)

        locator_path = "qa-realworld-automation/locators"
        locator_filename = f"{locator[0]}_locators.py"
        formatted_locators = remove_python_tags(page_locators)
        save_data_append(formatted_locators, locator_path, locator_filename)
        time.sleep(2)   # api 속도 제한을 위해 추가

    # 테스트케이스 데이터 추출하여 저장
    test_cases = DataFetcher.get_worksheet_data()
    results = []
    for test_case in test_cases:
        result = GoogleSheetsConverter.convert_worksheet_data_to_json(test_case)
        results.append(result)
    """
    테스트케이스 데이터 직접 사용 시 이런 식으로 사용해야함
    text_content = formatted_payload["content"][0]["text"]
    result = generate_with_claude(prompt, text_content)
    """
    save_data_overwrite(results, "json_data", "testcase.json")

if __name__ == "__main__":
    run()


    
