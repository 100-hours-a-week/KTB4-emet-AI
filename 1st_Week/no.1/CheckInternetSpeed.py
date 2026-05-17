import os
import socket
import speedtest
import argparse
from dataclasses import dataclass

@dataclass
class IP_Info:
   ip :str
   port: int
   download_speed : float
   upload_speed : float

   def recommand(self):
       if self.download_speed >= 300:
          print("This Wifi has high speed, recommand to download 4k viedeos or play high spec game that need to internet.") 
       elif self.download_speed >= 100 and self.download_speed < 300:
          print("This Wifi is recommand to self.download big size file.")
       elif self.download_speed >= 10 and self.download_speed < 100:
          print("This Wifi is recommand to download middle size file.")  
       elif self.download_speed >= 3 and self.download_speed < 10:
          print("This Wifi is recommand to download small size file.") 
       else :
          print("Please dont't connect this Wifi. I recommand to use your Mobile Hotspot.") 


##Check to Internet Connection
def check_connection(args):
    ip = args.ip
    port = args.port
    try:
      ##socket.create_connection((ip, port),timeout=3)
      ##print(f"ip:{ip}, port:{port}")
      return True
    except OSError:
      return False

def check_speed():
    try:
       print("Calculating speed. Please wait for second!")	
       st = speedtest.Speedtest()
       st.get_best_server()
    
       download_speed = round(st.download()/1024/1024, 2)
       upload_speed = round(st.upload()/1024/1024, 2)

       print("------ Internet Speed Status -----")	
       print(f"download speed: {download_speed} Mbps")
       print(f"upload speed: {upload_speed} Mbps")
       
       ip1 = IP_Info(args.ip, args.port, download_speed, upload_speed)
       ip1.recommand()

    except OSError:
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
         check_speed()
      else:
         print("Internet is not connected.")
