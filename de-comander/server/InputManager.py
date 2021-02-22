import threading
from server import *

class InputManager(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def wrapper(self,cmd):
		if cmd == "clients": return server.handler.getClients()
		elif cmd == "os_system":
			address = input("Input address: ")
			command = input("Input command: ")
			return server.handler.control(address,type="os_system",cmd=command)

	def run(self):
		while True:
			user_input = input("Input:")
			self.wrapper(user_input)


if __name__ == "__main__":
	inp = InputManager()
	inp.start()
