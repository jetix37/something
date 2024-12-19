import telebot
from telebot import types
import random

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

registred_users = {} # те, кто хочет подарить подарок

active_pool = {} # те, кто хочет получить

chosen_users = {} #те, кому подарят подарок (ru.id -> ap.name), при попадании сюда запись из ru и ap удаляются

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if (str(message.from_user.id) in chosen_users):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, "Человек, которому ты даришь подарок: " + chosen_users[str(message.from_user.id)] + " - он уже не может дождаться, когда ты его подаришь!", reply_markup=markup)
    
    elif (str(message.from_user.id) in registred_users):
        markup.row('🎅🏻 Начать игру!')
        bot.send_message(message.chat.id, "Привет! Добро пожаловать в игру 'Тайный Санта' в студсовете ФЕМИ!\n \nЧтобы узнать человека, которому ты будешь дарить подарок, нажми на кнопку ниже!", reply_markup= markup)
    else:
        message = bot.send_message(message.from_user.id, "Привет! Добро пожаловать в игру 'Тайный Санта' в студсовете ФЕМИ!\n \nЧтобы начать играть, введи, пожалуйста, свои Имя и Фамилию!", reply_markup = markup)
        bot.register_next_step_handler(message, after_registration)

def after_registration(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🎅🏻 Начать игру!')
    registred_users[str(message.from_user.id)] = message.text
    active_pool[str(message.from_user.id)] = message.text
    bot.send_message(message.chat.id, "Чтобы узнать человека, которому ты будешь дарить подарок, нажми на кнопку ниже!", reply_markup= markup)


@bot.message_handler(func=lambda message: message.text == '🎅🏻 Начать игру!')
def start_game(message):

    if (len(active_pool) <= 1):
        bot.send_message(message.chat.id, "На данный момент дарить подарок некому, если только Вы не хотите подарить подарок самому себе ❤", reply_markup=markup)
        return;
    
    markup = telebot.types.ReplyKeyboardRemove()
    
    if (str(message.from_user.id) in chosen_users):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, "Человек, которому ты даришь подарок: " + chosen_users[str(message.from_user.id)] + " - он уже не может дождаться, когда ты его подаришь! 🎉", reply_markup=markup)
        return;

    chosen_user = random.choice(list(active_pool.keys()))
    
    while (chosen_user == str(message.from_user.id)):
        chosen_user = random.choice(list(active_pool.keys()))

    chosen_users[str(message.from_user.id)] = active_pool[chosen_user]

    bot.send_message(6346628076, registred_users[str(message.from_user.id)] + " дарит " + active_pool[chosen_user])
    
    del active_pool[chosen_user]
    
    del registred_users[str(message.from_user.id)]
    
    bot.send_message(message.chat.id, "Человек, которому ты даришь подарок: " + chosen_users[str(message.from_user.id)] + " - он уже не может дождаться, когда ты его подаришь! 🎉", reply_markup=markup)


bot.polling()
