# HTTP
---
고차원(이미지,링크,비디오 등)으로 구조화된 텍스트를 전송하기 위해 사용되는 통신 규약

사용이유: 웹 서버와 클라이언트가 서로 정해진 규칙에 따라 파일을 주고받기 위해서

- Text: HTML,CSS,jS
    
- Binary: Image(jpg,png)
    
- multimedia: jpg,png,HTML,CSS,audio,link
    

## HTTP Message
---
HTTP 통신의 기본 단위  
종류: **request, response**  
브라우저(browser):대표적인 HTTP의 클라이언트  
구성

- 시작줄(Start Line): request 와 response를 구분
    
- 헤더(Header): 헤더의 집합, 메시지 바디 요약
    
- 빈줄(Empty Line): 헤더와 바디를 구분하는 공백(\r\n\r\n)
    
- 바디(Body): 실제 주고받을려는 데이터
    

HTTP URL

스키마(프로토콜종류), 도메인(주소), 포트(생략가능), 리소스경로, 매개변수(없을 수 있음) 구성됨

ex) https://exp.goorm.io/education/TESIiAqKYZ88RcfzuJ/dashboard/posts/write은 스키마,도메인,리소스경로로 구성됨

https: // exp.goorm.io / education/TESIiAqKYZ88RcfzuJ/dashboard/posts/write

### HTTP request method
---
웹 서버에게 구체적인 작업(정보 요청, 제출 ,삭제 등)을 요청하는 메소드

- **GET**
    

클라이언트가 **데이터 조회 요청**을 목적으로 서버에게 요청하는 메소드  
본문에 들어나지않는 상태(본문X)

서버는 URL에 포함된 경로 매개변수(path value)와 질의 매개변수(query string)의 처리 후, 요청한 데이터를 응답으로 클라이언트에게 보냄  
ex) 웹페이지 요청, 데이터 조회, 검색 결과 요청

- **POST**
    

클라이언트가 **데이터 생성 또는 최신화**를 목적으로 서버에게 요청하는 메소드  
본문이 들어나는 형태(본문O)

서버는 요청 바디를 파싱하고, 파싱한 데이터를 기반으로 데이터 처리 후, 응답을 클라이언트에게 보냄  
ex) 게시글 작성, 제품 등록

- **PUT**
    

클라이언트가 **데이터 전체를 최신화하는 목적**으로 서버에게 요청하는 메소드  
본문이 들어나는 형태(본문O)

서버는 요청 바디를 파싱하고, 파싱한 데이터를 기반으로 데이터를 최신화함  
ex) 프로필 이미지 변경

- PATCH
    

클라이언트가 **서버의 데이터를 부분적으로 수정 또는 최신화**를 목적으로 서버에게 요청하는 메소드

서버는 요청 바디를 파싱하고, 파싱한 데이터와 일치한 서버의 데이터(리소스)를 수정 또는 최신화함  
ex) 사용자 정보 변경(비밀번호, 이메일, 개인정보)

- DELETE
    

클라이언트가 **서버의 데이터(리소스)를 삭제**를 목적으로 서버에게 요청하는 메소드

서버는 URL에서 리소스를 식별해서 삭제함  
ex) 게시글 삭제, 사용자 정보 삭제

### **HTTP 상태코드**
---
|Status Pre-code|Status Code|Desciption|
|---------------|-----------|---|------|
|1xx||정보 메세지|
|2xx||성공|  
||201|요청수신하고, 처리 완료|  
||202|요청수신했지만, 처리불가능|  
||204|헤더는 유효하지만, 요청에 대한 정보처리 불가능|
|3xx||리다이렉션(도착 주소 재지정)|
|4xx||클라이언트측 오류(Bad Request)|  
||401|불법적인 요청(로그인하지 않고 정보 조회)|  
||403|허락되지 않은 요청(일반회원이 관리자 페이지 조회)| 
||404|없는 페이지 요청(삭제된 페이지)|  
||429|일정시간동안 너무 많은 요청(잘못된 비밀번호입력)|
|5xx||서버측 오류(Internal Server Error)|  
||500|서버가 요청 처리 방법을 모름|  
||501|요청 방법이 올바르지않음(미지원 방식 요청)|  
||503|서버가 일시적으로 요청 처리 불가능(트래픽 몰림)|
    

# FastAPI
---
python으로 빠르고 쉽게 API 서버를 만들 수 있는 웹 프레임워크

사용이유: 빠른성능과 API 제작 용이

웹앱: 서버에서 동작하는 웹 HTTP 앱  
web app framework(Django, Plask) vs web app server  
Django server - Apacher server, Nginx  
Web server - Apache web server

WSGI(Web Server Gateway Interface)는 파이썬 웹 서버, 프레임워크, 애플리케이션 간의 **동기** 표준 인터페이스

ASGI(Asynchronous Server Gateway Interface)는 파이썬 웹 서버, 프레임워크, 애플리케이션 간의 **비동기** 표준 인터페이스

```plaintext
from fastapi import FastAPI
## 객체 생성(FastAPI는 class)
app = FastAPI()
## 함수를 부르는 데코레이터 , "/"는 루트로 읽음
@app.get("/")
def read_root():
	return {"Hello": "World"}	
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
	return {"item_id": item_id,"q": q}
```

  
**uv**

파이썬을 전반적으로 관리해주는 툴(pip이상의 기능)

```plaintext
## uv 설치한 상태에서 파이썬 설치 명령어
uv init --python 3.14.5
```

**uvicorn**

Python 애플리케이션을 실행하기 위한 경량 ASGI 서버  
동작순서

```plaintext
## uv 설치한 상태에서 uvicorn 설치 명령어
## 명령어 동작 순서: 자동으로 python 설치 -> 자동으로 .venv 생성 -> uvicorn 설치
uv add uvicorn
## uvicorn으로 실행할때는 .venv activate하고 실행하기!
```

**starlette**  
ASGI을 좀더 간결하게 코드 작성도와주는 프레임워크(uvicorn으로 짜는 코드보다 더 짧음)

공식홈:[https://starlette.dev](https://starlette.dev/)

**JSON(JavaScript Object Notation)**

"자바스크립트 객체 문법으로 구조화한 일종의 설계 데이터"를 표현한 표준 텍스트 포맷(과거에는 XML을 사용함)

사용이유: 데이터의 형태가 교환을 목적으로 경량화 및 구조화했음

형태

키-밸류 형태 ({}로 구분)  
배열 지원([ ]로 배염범위 구분,로 요소 구분)

```plaintext
[ 
   { 
      "이름": "웨인", 
      "나이": 25 
   }, 
   { 
      "이름": "야로", 
      "나이": 30 
   } 
]
```

## REST API(Representational State Transfer API)
---
URI(리소스)와 HTTP 메서드(행동)를 사용해 클라이언트와 서버가 서로 데이터(대체로 JSON)를 교환하는 설계 방식

사용이유: 개발자 간의 일관된 통신 규칙으로 업무 효율을 높이고, 단순한 URL구조로 목적을 쉽게 이해하기위해  
일부 사용방법

- URI는 정보의 자원을 표현(동사가 아닌 명사를 사용)-
    
- 자원의 행위는 HTTP method로 사용
    
- 슬래시(`/`)는 계층 관계 표현에 사용
    
- 소문자 사용
    
- 밑줄(`_`)대신 하이폰(`-`) 사용
    
- 확장자(.txt, .png, etc)를 사용하지 않는다