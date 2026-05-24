import httpx
import json

# local에 설치된 gemma4_e4b url -> 상수
URL= "http://localhost:11434/v1/chat/completions"
AI_MODEL = "gemma4:e2b"

def content2summary(content : str):   
    payload = {
	    "model": AI_MODEL,
	    "messages": [
            {"role": "system", "content": "당신은 친절한 AI 어시스턴트입니다."
		    },
	        {"role": "user", "content": f"{content}에 대해 없앨 내용 없애고 원래 내용보다 짧게 설명해줘.단답형도 가능해, 내용 이해가 불가능거나 너무 짧으면 절대 아무말도 답변 하지마"
            }
        ],
        "stream": True
    }
    content_summary = ""
    try: 
        with httpx.Client(timeout = 60.0) as client:
            response = client.send(client.build_request("POST", URL, json = payload), stream = True )
            # response가 iterable한지 __iter__ 속성여부로 파악
            # 1줄씩 iter 진행    
            for line in response.iter_lines():
                if line and line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    if '"content":' in data_str:
                        data_json = json.loads(data_str)
                        chunk = data_json["choices"][0]["delta"]["content"]
                        #print(f"chunk: {chunk}", end = "",flush=True)
                        content_summary += chunk
    except Exception as e:
        print(e)
    
    return content_summary