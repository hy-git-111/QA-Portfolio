from google_sheets.connector import GoogleSheetConnector

class DataFetcher:
    # 워크시트 이름을 가져오는 함수 > 추후 수정 필요
    @staticmethod
    def get_worksheet_name():
        try:
            worksheets = GoogleSheetConnector.get_worksheet_list()
            return [ws.title for ws in worksheets]
        except Exception as e:
            print(f"워크시트 이름을 가져오는 중 오류 발생: {e}")
            return []
    
    # 워크시트 데이터(TC)를 가져오는 함수
    @staticmethod
    def get_worksheet_data():   # 데이터 읽기
        worksheets = GoogleSheetConnector.get_worksheet_list()
        all_data = []
        
        for worksheet in worksheets[1:]:
            try:
                # 헤더가 9번째 행에 있다고 가정
                header_row = worksheet.row_values(9)
                if not header_row:
                    continue  # 헤더가 없는 경우 건너뛰기
                
                # 데이터가 있는 헤더만 선택 (빈 헤더 제외)
                valid_headers = [header for header in header_row if header]
                
                # 헤더 중복 체크
                if len(valid_headers) != len(set(valid_headers)):
                    print(f"워크시트 '{worksheet.title}'에 중복된 헤더가 있습니다.")
                    # 중복 헤더 처리: 고유한 헤더만 유지
                    unique_headers = []
                    seen_headers = set()
                    for header in valid_headers:
                        if header not in seen_headers:
                            seen_headers.add(header)
                            unique_headers.append(header)
                    valid_headers = unique_headers
                
                # 헤더 기반으로 모든 데이터 가져오기 (유효한 헤더만)
                records = worksheet.get_all_records(head=9, expected_headers=valid_headers)
                    
                # "구분" 컬럼이 "자동화"인 행만 필터링
                filtered_records = [row for row in records if row.get("구분") == "자동화"]
                
                # 워크시트 이름과 함께 데이터 저장
                for record in filtered_records:
                    record["worksheet_name"] = worksheet.title
                    all_data.append(record)
                    
            except Exception as e:
                print(f"워크시트 '{worksheet.title}'에서 데이터 추출 중 오류 발생: {e}")
                continue
                
        return all_data  # 리스트-딕셔너리 형태로 반환
