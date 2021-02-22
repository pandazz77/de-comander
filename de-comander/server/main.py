import threading
import server, bot

if __name__ == "__main__":
	threads = (threading.Thread(target=server.start),
		threading.Thread(target=bot.start))
	for thread in threads: thread.start()