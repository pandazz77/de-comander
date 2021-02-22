import socket
import sys
import json
import threading
import time
from dataHandler import data


class ClientsManager:
	def __init__(self):
		self.clients_dict = {}

	def append(self,ClientThread):
		self.clients_dict[ClientThread.getAddress()] = ClientThread

	def pop(self,ClientThread):
		self.clients_dict.pop(ClientThread.getAddress())

	def getClients(self):
		for addr, client in self.clients_dict.copy().items():
			if client.alive is False:
				self.pop(client)
			return self.clients_dict

	def control(self, ClientAddress, **kwargs):
		typ = kwargs["type"]
		if typ == "os_system":
			cmd = kwargs["cmd"]
			r_data = self.clients_dict[ClientAddress].s2r({"type":"os_system","cmd":cmd})
			return r_data


handler = ClientsManager()

class Server:
	global handler
	def __init__(self,ip,port):
		self.connections = []
		self.ip = ip
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((self.ip,self.port))
		self.s.listen(0)
		threading.Thread(target=self.connect_handler).start()
		print(f'Сервер запущен на {ip}:{port}')
		inp = InputManager(handler)
		inp.start()

	def connect_handler(self):
		while True:
			client, address = self.s.accept()
			self.connections.append(client)
			thread = ClientThread(client)
			handler.append(thread)
			thread.start()
			#threading.Thread(target=self.client_handler, args=(client,)).start()
			time.sleep(1)

	def client_handler(self,client):
		pass
	'''
		while True:
			r_data = client.recv(1024)
			if r_data != b'':
				print(r_data)
				r_data = json.loads(r_data)
				print(r_data)
				new_data = self.data_handler(r_data)
				s_data = json.dumps(new_data)
				client.send(s_data.encode())
			time.sleep(1)
	'''
	def s2r(self,client,s_data): #s2r - send to receive - функция отправляющая запрос на клиент, чтобы получить определенный ответ
		s_data = json.dumps(s_data)
		self.s.send(s_data.encode())
		r_data = self.s.recv(1024)
		r_data = json.loads(r_data)
		return r_data


	def data_handler(self,r_data):
		return(data.process(r_data))


class ClientThread(threading.Thread, Server):
	def __init__(self, args):
		threading.Thread.__init__(self,args=((args,)))
		self.client = args
		self.alive = True
		self.address = self.client.getpeername()[0]

	def run(self):
		#print("New client")
		while True:
			try:
				r_data = self.client.recv(1024)
				if r_data != b'':
					print(r_data)
					r_data = json.loads(r_data)
					print(r_data)
					new_data = self.data_handler(r_data)
					s_data = json.dumps(new_data)
					self.client.send(s_data.encode())
				time.sleep(1)
			except ConnectionResetError:
				self.alive = False
				sys.exit(0)

	def s2r(self,s_data): #s2r - send to receive - функция отправляющая запрос на клиент, чтобы получить определенный ответ
		s_data = json.dumps(s_data) # send data
		self.client.send(s_data.encode())
		r_data = self.client.recv(1024) #receive data
		r_data = json.loads(r_data)
		return r_data

	def data_handler(self,r_data):
		return(data.process(r_data))

	def getAddress(self):
		return self.address


class InputManager(threading.Thread, Server):
	def __init__(self,handler):
		self.handler = handler
		threading.Thread.__init__(self)

	def wrapper(self,cmd):
		if cmd == "clients": print(self.handler.getClients())

	def run(self):
		while True:
			user_input = input()
			self.wrapper(user_input)


def start():
	server_data = data('data.json')
	server = Server('192.168.1.231',7777)

if __name__ == "__main__":
	server_data = data('data.json')
	server = Server('192.168.1.231',7777)