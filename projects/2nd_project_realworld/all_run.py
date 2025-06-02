# main_run.py
from pages_run import run_prompt_one_by_one as generate_page_objects
from testcases_and_locators_run import run as generate_locators_and_testcases
from tests_run import main as generate_test_files

if __name__ == "__main__":
    print("\n=== [1] 로케이터 및 테스트케이스 생성 시작 ===")
    generate_locators_and_testcases()

    print("\n=== [2] 페이지 객체 생성 시작 ===")
    generate_page_objects()

    print("\n=== [3] 테스트 파일 생성 시작 ===")
    generate_test_files()

    print("\n🎉 모든 자동화 작업 완료!")
