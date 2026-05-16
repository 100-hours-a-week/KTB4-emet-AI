import os
import socket
import speedtest

google = "8.8.8.8"
port = 53

def check_connection():
    try:
      socket.create_connection((google,port),timeout=3)
      return True
    except OSError:
      return False


def check_speed():
    print("Calculating Speed")	
    st = speedtest.Speedtest()
    st.get_best_server()
    
    download_speed = round(st.download()/1024/1024, 2)
    upload_speed = round(st.upload()/1024/1024, 2)
    ping = round(st.results.ping, 2)

    print("------ Internet Speed Status -----")	
    print(f"download speed: {download_speed} Mbps")
    print(f"upload speed: {upload_speed} Mbps")
    print(f"ping: {ping} ms")
   ##파서로 현재 다운가능한 데이터 추천하기 
   ## 고용량 게임및 4k영상: x > 500Mbps
   ## FHD: 100Mbps < x < 500Mbps 
   ## 일반문서: x < 100Mbps    
   ## 너무 느리면 핫스팟 추천하기

if __name__ == "__main__":
   if check_connection():
       print("Internet is connected.")
       check_speed()
   else:
       print("Internet is not connected.")
    

