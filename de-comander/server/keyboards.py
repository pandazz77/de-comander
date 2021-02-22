import telebot
import json

admin_panel = telebot.types.InlineKeyboardMarkup()

a_panel_buttons = (telebot.types.InlineKeyboardButton(text="Активные соединения", callback_data=json.dumps({"type":"connections"})),
	telebot.types.InlineKeyboardButton(text="2button",callback_data=json.dumps({"type":"2button"})),
	telebot.types.InlineKeyboardButton(text="3button",callback_data=json.dumps({"type":"3button"})),
	telebot.types.InlineKeyboardButton(text="4button",callback_data=json.dumps({"type":"4button"})))

for butt in a_panel_buttons: admin_panel.add(butt)


def genConnectionsKeyboard(connections):
	connections_keyboard = telebot.types.InlineKeyboardMarkup()
	for connection in connections: connections_keyboard.add(telebot.types.InlineKeyboardButton(text=connection ,callback_data=json.dumps({"type":"select_connection","connection":connection})))
	connections_keyboard.add(telebot.types.InlineKeyboardButton(text="Назад", callback_data=json.dumps({"type":"menu"})))
	return connections_keyboard

connection_panel = telebot.types.InlineKeyboardMarkup()

connection_panel_buttons = (telebot.types.InlineKeyboardButton(text="Исполнить команду", callback_data=json.dumps({"type":"command"})),
							telebot.types.InlineKeyboardButton(text="Назад", callback_data=json.dumps({"type":"to_connections"})))

for butt in connection_panel_buttons: connection_panel.add(butt)