간단한 개인프로젝트

이 프로젝트의 목표는
notion과 상당히 유사한 기능을 하는 메모장 프로젝트이다.
Django와 AWS, 배포까지의 과정을 체험해보고 기록으로 남기기 위해 진행하는 프로젝트이다



AI 활용 ( GPT PLUS (GPT 5.2) ) 

notebook 은 AI를 사용하기도 했지만 거의 웬만해서는 직접 타이핑하고 일부 모르는 함수를 제외하면 직접 코드를 짰다
html의 js, style부분은 AI를 썼다( 너무 어렵다... )

account 같은 경우는 온전히 AI를 사용했고 주석은 AI에게 묻지 않고 직접 생각해서 타이핑 후 AI에게 확인받았다.



현재까지 진행도

기본적인 노트북, 포스트의 CRUD, 로그인 완성, AWS S3 연결 후 이미지, 동영상 업로드 확인 완료
모든 UI 개선 완료

이제 해야할건 인덱스 페이지, notebook detail, post update, post create 에서 카드(블록)들의 위치 자유자제로 움직이기

추가적으로 해보고싶은건 개인 메모 뿐만 아닌 공개형 메모(게시판 느낌), 찜하기


설치된 lib
django, ipython, boto3, storages
