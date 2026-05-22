
[공식문서](https://docs.astral.sh/uv/)

- 설치
```
## macOS & Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
## Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
- 가상환경 생성 및 파이썬 설치
```
## 가상환경(.venv)만들고 python 자동설치
uv init
## 가상환경이 존재하는 확인하고 없으면 (.venv)만들고 python 자동설치
uv run
```

- 가상환경진입(이후 명령어는 가상환경안에서의 명령어)
```
## 기존 가상환경 진입과 동일
source .venv/bin/activate
```

- 설치된 패키지 정보 리스트 출력
```
##tree 구조 출력
uv pip tree
##단순 구조 출력
uv pip list
```

- 패키지 추가
```
## uv 가상환경에서 패키지 추가
uv add {package}
## uvicorn 설치
uv add uvicorn
## fastapi 설치
uv add fastapi
```

