# CheckInternetSpeed-CLI

## Introduction
Check your Wifi connection and speed. And then recommand to download file type. If load's speed is low speed, recommned to connect your mobile hotspot.

## How to use

```
## python3 ./{Assignment number directory}/CheckInternetSpeed.py connect --ip {IP : str or address} --port {port : int}
python3 ./no.1/CheckInternetSpeed.py connect --ip 8.8.8.8 --port 80
python3 ./no.2/CheckInternetSpeed.py connect --ip naver.com --port 443 
  
```

## Using Third-party library

speedtest-cli : for testing speed
```
import speedtest

## call speedtest
st = speedtest.Speedtest()
## allocate speedtest best server for load test
st.get_best_server()

##(sync func) calculate download speed
st.download()
##(sync func) calculate upload speed
st.upload()
```

## "no.1" vs "no.2"
"no.1"'s funcs are executed in order. Therefore `st.upload()` is waiting until `st.download()`'s status is end. But I apply to ayncio and thread on "no.2". Since `st.upload()` and `st.download()` are sync func, multithreading was applied to this section by using `loop.run_in_executor()`. By implementing it this way, "no.2" is faster than "no. 1".

