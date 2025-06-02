# # automation/merger.py

# import os
# """
# Claude의 체크리스트 평가 결과를 바탕으로 최종 병합을 수행합니다.

# - Claude와 Gemini 코드 중 하나를 선택하고, 그 이유를 코드 상단 주석에 표시합니다.
# - 선택 기준은 역할별 체크리스트와 구조적 일관성입니다.
# - 병합 결과는 camelCase 표기법과 파일 역할에 맞는 구조를 유지해야 합니다.
# - 병합 로그는 merge_logs/ 폴더에 파일명 기준으로 기록됩니다.
# """

# # ✅ Claude 응답 기반 병합 수행 함수 (카멜표기법, 구조 일관성 포함)
# def merge_outputs(
#     claudeCode: str,
#     geminiCode: str,
#     filename: str = "mergedOutput.py",
#     selectedByClaude: str = "claude",
#     reason: str = ""
# ) -> str:
#     fileName = os.path.basename(filename)

#     if claudeCode.strip() == geminiCode.strip():
#         comment = "# Claude와 Gemini 코드가 동일하여 병합 생략"
#         selectedCode = claudeCode
#     else:
#         selectedCode = claudeCode if selectedByClaude == "claude" else geminiCode

#         # 판단 이유를 줄마다 주석으로 정리
#         commentLines = [f"# Claude 선택 결과: {selectedByClaude}"]
#         for line in reason.strip().splitlines():
#             if line.strip():
#                 commentLines.append(f"# 판단 근거: {line.strip()}")
#         comment = "\n".join(commentLines)

#     # 병합 로그 저장
#     safeName = filename.replace("/", "_").replace(".py", "")
#     logPath = os.path.join("merge_logs", f"{safeName}_merge_log.txt")
#     os.makedirs("merge_logs", exist_ok=True)
#     with open(logPath, "a", encoding="utf-8") as log:
#         log.write(f"파일명: {fileName}\n{comment}\n{'='*50}\n\n")

#     return f"{comment}\n\n{selectedCode}"