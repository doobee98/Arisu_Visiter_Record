# Arisu_Visiter_Record
	아리수정수센터 출입자관리시스템



	현재 버전: 0.4.0

	버전 0 : 베타테스트

	사용 언어: Microsoft Excel




------------------------------------------------------------------------------------------------------------------------------------

# 2019-06-27 : Build 0.4.0

	출입자기록부

		* 이제 차량번호가 앞쪽으로, 비고가 뒤쪽으로 옮겨집니다! 사용시 편의를 위해 작성하는 열의 순서를 변경했습니다.
	
		버그수정
		    1. 76번째 행 텍스트의 굵기와 정렬이 다른 행들과 다른 것을 수정했습니다.
		    2. 기록부 시트에서 정문, 후문, 취수장을 변경할 시, '데이터를 새 파일로 내보내기'에서 생성되는 파일에도 
		       변경 내용이 적용되도록 수정했습니다.
		    3. 기록부의 첫 기록 내용이 인수인계일시, 나가다 버튼을 누르면 프로그램이 멈추는 문제를 수정했습니다.
		    4. 인수인계시 기입되는 식별번호를 "제외"에서 "인수인계"로 수정했습니다.
		    5. 검색목록상자의 너비와 높이가 프로그램 시작시 간헐적으로 길이가 조금씩 달라지는 현상을 수정했습니다.



	출입자DB

		* 출입자기록부의 순서 변경에 맞춰, 기록부에서 데이터를 가져오는 코드를 수정했습니다.



	통합

		버그수정
		   1. 출입자기록부와 출입자DB가 자동으로 숨겨져서 열리는 현상을 수정했습니다. 
		      앞으로는 둘 중 하나라도 열려있지 않은 상태에서 다른 파일의 데이터를 필요로 할 경우 
		      그 파일을 '숨겨지지 않은 상태'로 열어서 사용합니다.



# 2019-06-23 : Build 0.3  
	베타테스트 시작
