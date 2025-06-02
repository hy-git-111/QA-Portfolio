class GoogleSheetsConverter:
    # 워크시트 데이터(TC)를 JSON으로 변환하는 함수
    @staticmethod
    def convert_worksheet_data_to_json(test_case: list):
        test_id = test_case.get("No.", "unnamed")
        title = test_case.get("Title", "")
        precondition = test_case.get("Precondition", "")
        steps = test_case.get("Steps", "")
        expected = test_case.get("Expected Result", "")

        content = f"""
테스트 ID: {test_id}
시나리오: {title}

사전 조건:
{precondition}

재현 절차:
{steps}
기대 결과:
{expected}
"""
        formatted_content = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        }
        
        return formatted_content