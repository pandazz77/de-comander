from dic import dictionary

class data:
	@staticmethod
	def process(c_data):
		if c_data["type"] not in dictionary.keys():
			return False
		return True

if __name__ == "__main__":
	d = data()
	print(d.process({"type":"check"}))