import os
import socket
import speedtest
import argparse
import asyncio


async def recommend_download(speed):
   if speed >= 300:
      print("This Wifi has high speed, recommend to download 4k viedeos or play high spec game that need to internet.") 
   elif speed >= 100 and speed < 300:
      print("This Wifi is recommend to self.download big size file.")
   elif speed >= 10 and speed < 100:
      print("This Wifi is recommend to download middle size file.")  
   elif speed >= 3 and speed < 10:
      print("This Wifi is recommend to download small size file.") 
   else :
      print("Please dont't connect this Wifi. I recommend to use your Mobile Hotspot.") 

async def recommend_upload(speed):
   if speed >= 300:
      print("This Wifi has high upload speed, recommend to upload 4k viedeos.") 
   elif speed >= 100 and speed < 300:
      print("This Wifi is recommend to upload big size file.")
   elif speed >= 10 and speed < 100:
      print("This Wifi is recommend to upload middle size file.")  
   elif speed >= 3 and speed < 10:
      print("This Wifi is recommend to upload small size file.") 
   else :
      print("Please dont't connect this Wifi. I recommend to use your Mobile Hotspot.") 


##Check to Internet Connection
def check_connection(args):
    ip = args.ip
    port = int(args.port)
    try:
      socket.create_connection((ip, port),timeout=3)
      print(f"ip:{ip}, port:{port}")
      return True
    except Exception as e:
      print(e)
      return False


async def calcluate_speed(st, load):
   ## getattr() -> attribut process as str
   func_attribute = getattr(st, load)

   ## get async envet loop that is processing
   loop = asyncio.get_running_loop()
   
   ## I/O process(st.download() & st.upload())is sync func
   ## sync func allocate another thread
   speed = await loop.run_in_executor(None, func_attribute)

   speed = round(speed/1024/1024, 2)
   print(f"{load} speed: {speed} Mbps")
   
   await globals()[f"recommend_{load}"](speed)
   return speed

async def check_speed():
    try:
       print("Calculating speed. Please wait for second!")	
       st = speedtest.Speedtest()
       st.get_best_server()
       
       print("------ Internet Speed Status -----")

       download_task = calcluate_speed(st, "download")
       upload_task = calcluate_speed(st, "upload")
       download_speed, upload_speed =  await asyncio.gather(download_task, upload_task)

    except Exception as e:
      print(e)
      return False

parser = argparse.ArgumentParser(description = "recomand to Internet Connection") 
sub_parser = parser.add_subparsers(dest="command")
socket_parser = sub_parser.add_parser("connect", help="ip and port connect test")
socket_parser.add_argument("--ip", default = "8.8.8.8")
socket_parser.add_argument("--port", default = 80)
socket_parser.set_defaults(func=check_connection)

if __name__ == "__main__":
   args = parser.parse_args() 
   if args.command:
      if args.func(args):
         print("Internet is connected.")
         asyncio.run(check_speed())
      else:
         print("Internet is not connected.check your Wifi, ip and port.")
