# Arisu_Visiter_Record
	아리수정수센터 출입자관리시스템



	현재 버전: 0.4.3

	버전 0 : 베타테스트

	사용 언어: Microsoft Excel




------------------------------------------------------------------------------------------------------------------------------------



# 2019-07-27 : Build 0.4.3

    출입자기록부
    
        * 이제 인수인계를 한 교대자의 이름이 자동으로 현재 근무자 칸에 기입됩니다.



    출입자DB
    
        * 데이터 보존 기간을 1달에서 3달로 변경하였습니다.
        
        
        버그수정
            1. 기간을 지난 데이터가 지워졌을 때 간헐적으로 업데이트가 더이상 불가능해지는 현상을 수정했습니다.




# 2019-07-01 : Build 0.4.2
 
    통합
    
        * "이전 기록부들" 폴더가 삭제되었습니다.
          
        버그수정
            1. 기록부와 DB 양쪽의 파일을 서로 참조할 때 발생하는 메모리 누수를 일부 해결했습니다.


    
    출입자기록부
    
        * 자동 스크롤 기능(나가다 버튼, 들어오다 버튼의 왼쪽 버튼)에 여백을 두었습니다.
          앞으로는 스크롤이 4칸의 여백을 두고 진행됩니다.
        * 이전 기록부 가져오기 기능을 추가했습니다.
          
        버그수정
            1. 75번째 행의 서식 오류를 수정했습니다.
            2. "나가다" 데이터에서 출입증번호 란의 서식이 유지되지 않는 점을 수정했습니다.
            3. 인수인계시 고유번호에 적용된 서식(빗금)이 지워지지 않는 점을 수정했습니다.




# 2019-07-01 : Build 0.4.1a
    핫픽스
    
    출입자기록부
        1. 셀 잠금을 조금 더 명확히 확인할 수 있도록 UI를 업데이트 하였습니다.




# 2019-07-01 : Build 0.4.1

    ** 확인된 문제점
        1. 출입자기록부를 켜둔 상태에서 출입자DB 파일을 종료시 메모리 부족 현상으로 출입자기록부가 강제종료되는 현상이 
	   가끔 발생합니다. 원인을 확인 중에 있으며, 사용 시에는 출입자기록부가 자동저장이 되므로 큰 문제는 발생하지 않습니다.


    
    통합
    
        * 셀의 수식값 등의 원치 않은 변경을 막기 위해 시트보호가 적용되었습니다. 
          암호는 존재하지 않기에 자유롭게 해제할 수 있지만, 그로 인해 변경된 셀값에 의해 프로그램이 예상치 못한 동작을 
	  할 수 있습니다.
          
        버그수정
            1. 예기치 못한 원인으로 프로그램이 종료된 후 다시 실행 시, 프로그램의 코드 상에서 문제가 발생하여 디버그하는 
	       문제를 수정했습니다.


    
    출입자기록부
    
        * 현재 근무자 매크로가 삭제되었습니다.
        * 시간, 근무자, 수식값에 기본적으로 셀 잠금이 적용됩니다. 
          이는 "들어오다" 버튼을 통해서만 시간과 근무자, 수식값을 입력하게 하기 위함입니다.
        * "나가다" 버튼을 누르면 해당 나간 인원의 기록으로 스크롤이 자동 이동합니다.
        * "들어오다" 버튼 왼쪽에, 현재 작성할 기록의 위치를 자동으로 찾아가는 버튼이 추가되었습니다. 
          해당 버튼의 바로가기 키 도입은 미정이며, 실 사용 후 결정될 예정입니다.
        
    
    
    출입자DB
    
        * UI를 소폭 개선하였습니다.
        * 이전버전 DB의 이름을 적는 셀에서 확장자를 생략하도록 변경했습니다.
        * 틀 고정이 적용되었습니다.
        
        
        버그수정
            1. 인수인계가 DB에 잘못 기록되는 현상을 수정했습니다.
            2. 업데이트할 파일이 켜져있지 않은 상태에서 업데이트를 시도할 때, 프로그램이 간헐적으로 종료되는 현상이 존재합니다.
               해당 부분의 원인을 찾지 못해 임시로, 파일이 켜져있지 않을 때 연결을 시도시 에러 창이 발생하게 하였습니다.




# 2019-06-27 : Build 0.4.0

	출입자기록부

		* 이제 비고가 뒤쪽으로 옮겨집니다! 사용시 편의를 위해 작성하는 열의 순서를 변경했습니다.
	
		버그수정
		    1. 76번째 행 텍스트의 굵기와 정렬이 다른 행들과 다른 것을 수정했습니다.
		    2. 기록부 시트에서 정문, 후문, 취수장을 변경할 시, '데이터를 새 파일로 내보내기'에서 생성되는 파일에도 
		       변경 내용이 적용되도록 수정했습니다.
		    3. 기록부의 첫 기록 내용이 인수인계일시, 나가다 버튼을 누르면 프로그램이 멈추는 문제를 수정했습니다.
		    4. 인수인계시 기입되는 식별번호를 "제외"에서 "인수인계"로 수정했습니다.
		    5. 검색목록상자의 너비와 높이가 프로그램 시작시 간헐적으로 길이가 조금씩 달라지는 현상을 수정했습니다.



	출입자DB

		* 출입자기록부의 열 순서 변경에 맞춰, 기록부에서 데이터를 가져오는 코드를 수정했습니다.



	통합

		버그수정
		   1. 출입자기록부와 출입자DB가 자동으로 숨겨져서 열리는 현상을 수정했습니다. 
		      앞으로는 둘 중 하나라도 열려있지 않은 상태에서 다른 파일의 데이터를 필요로 할 경우 
		      그 파일을 '숨겨지지 않은 상태'로 열어서 사용합니다.



# 2019-06-23 : Build 0.3  
	베타테스트 시작
