import json

class DataHandlerError(Exception):
	def __init__(self,text):
		self.text = text



class data:
	def __init__(self,path):
		self.path = path

	def get(self):
		with open(self.path) as file:
			data = json.load(file)
			return data

	def set(self,data):
		previous_data = self.get()
		new_data = previous_data.copy()
		for key, value in data.items():
			new_data[key] = value

		with open(self.path,'w') as file:
			json.dump(new_data,file)

	def process(self,c_data):
		s_data = self.get() #s_data - server_data(dict)
		if c_data["type"] not in tuple(s_data.keys()): #c_data - client_data(dict)
			raise DataHandlerError("DataType not found")

		if c_data["type"] == "simple":
			return s_data["simple"][c_data["data"]]

if __name__ == "__main__":
	d = data("data.json")
	print(d.process({"type":"simple","data":"key"}))