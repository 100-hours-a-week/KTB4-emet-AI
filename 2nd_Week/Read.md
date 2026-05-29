# 2주차 회고
---
## 발생한오류들 중 시간을 가장 많이 잡은것들 

### HTTPX
(1)발생오류
`'httpx.Response' object does not support the context manager protocol (missed __exit__ method)`
(1)원인   
httpx.Response는 with을 지원안함    
(1)해결법 또는 실수   
httpx.Client에 with을 써야하는 걸 잘못된위치에 사용하고있었음 


### Ollama

(2)발생오류:
`Attempted to access streaming response content, without having called read().`
-> reddit 에서는 전체 응답 내용을 읽어오기 전(또는 스트림을 반복하기 전)에 강제로 전체 텍스트나 본문 데이터를 추출하려고 할 때 발생한다고 해서 httpx와 ollama 공식 문서와 인터넷의 다른 사람들의 코드를 비교하면서 찾아봤지만 뭐가 문제인지 찾지를 못해서 마지막으로 claude에게 부탁했다. 
그결과 내가 코드를 잘못입력했다. (최근에 카부캠 시작이후 잠을 줄이고, 개인적인 휴식 시간도 줄어서 코드 작성하는 시간에 집중을 못했는데 발생한 실수인듯하다.)
```
## delta를 data로 입력해서 실행하고았었음
## 계속 시도하던 코드
chunk = data_json["choices"][0]["data"]["content"]
## 옳게 된 코드
chunk = data_json["choices"][0]["delta"]["content"] 
```
이후에는 리소스가 부족하다는 에러를 발생시켜 모델 버전을 e4b에서 e2b로 다운그레이드했고, 그 과정에서 ollama 백그라운드 실행에 문제가있는지 꼬여서 kill process 등 완전히 ollama를 재실행해서 코드를 실행하니 정상적으로 response를 받고 원하는 질문을 받았다. 



## 최종 회고
대체적으로 시간을 잡아먹은 오류들은 논린적 오류보다는 내가 집중하지 못하고 코드를 잘못입력한 경우가 많았다. 코드를 작성할때는 되도록이면 정신이 멀쩡한 상태에서 진행하자!
아쉬운점은 이런 위의 문제들로인해 선택인 2.5를 시도못한게 아쉽다.
