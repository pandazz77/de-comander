import telebot
from keyboards import *
from server import handler

admins = (8888888888,)
token = "token"
bot = telebot.TeleBot(token)
users_choice = {}

@bot.message_handler(commands=['start'])
def start_message(message):
	if message.from_user.id in admins:
		bot.send_message(message.chat.id,"Админ-панель:",reply_markup=admin_panel)
	else:
		bot.send_message(message.chat.id,"Нет доступа.")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	global users_choice
	print(call.data)
	jsonCallData = json.loads(call.data)
	if jsonCallData["type"] == "menu":
		bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Админ-панель:",reply_markup=admin_panel)
	elif jsonCallData["type"] == "connections":
		try:
			connections = handler.getClients().keys()
		except AttributeError:
			connections = None
		if connections is None: bot.send_message(call.message.chat.id,"Нет активных соединений")
		else: 
			try: 
				bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Активные соединения:",reply_markup=genConnectionsKeyboard(connections))
			except Exception as e:
				print("\n"+str(e)+"\n")
	elif jsonCallData["type"] == "select_connection":
		connection = jsonCallData["connection"]
		bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Выберите действие:",reply_markup=connection_panel)
	elif jsonCallData["type"] == "command":
		users_choice[call.message.chat.id] = "input_command"
		bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Напишите команду:")
	elif jsonCallData["type"] == "to_connections":
		bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Админ-панель:",reply_markup=admin_panel)

@bot.message_handler(content_types=['text'])
def send_text(message):
	if users_choice[message.chat.id] == "input_command":
		bot.send_message(message.chat.id, "Исполнено"+message.text)

def start():
	print("Бот запущен")
	bot.polling()

if __name__ == "__main__":
	bot.polling()
