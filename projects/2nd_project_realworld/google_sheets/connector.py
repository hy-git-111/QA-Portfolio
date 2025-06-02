import gspread, os
from google.oauth2.service_account import Credentials

class GoogleSheetConnector:
    # 워크시트 리스트를 반환하는 함수
    @staticmethod
    def get_worksheet_list():
        try:
            SHEET_NAME = "엘리스_2차_3조_팀프로젝트"
            SCOPES = [
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly"
            ]

            base_dir = os.getcwd()
            creds_file = os.path.join(base_dir, "credentials.json")

            if not creds_file:
                raise ValueError("GOOGLE_APPLICATION_CREDENTIALS 환경 변수가 설정되지 않았습니다.")

            # 서비스 계정 키 파일로 자격 증명 객체 생성
            creds = Credentials.from_service_account_file(
                creds_file,
                scopes=SCOPES
            )
            client = gspread.authorize(creds)   # gspread 클라이언트 초기화

            # 스프레드시트 열기
            spreadsheet = client.open(SHEET_NAME)   # 구글 드라이브의 스프레드시트 이름
            worksheets = spreadsheet.worksheets()   # [Worksheet, Worksheet, ...]
                                        
            return worksheets
        except Exception as e:
            print(f"워크시트 목록을 가져오는 중 오류 발생: {e}")
            return []