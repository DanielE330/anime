import telebot
from telebot import types
from DB import db

bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')  

ANIME_DATA = db.ANIME_DATA

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    for genre_name in ANIME_DATA.keys():
        btn = types.InlineKeyboardButton(
            genre_name.capitalize(), 
            callback_data=f'genre_{genre_name}'
        )
        keyboard.add(btn)
    
    bot.send_message(
        message.chat.id,
        "🎬 Выберите жанр аниме:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('genre_'))
def show_anime_list(call):
    genre = call.data.split('_')[1]
    
    keyboard = types.InlineKeyboardMarkup()
    
    for idx, anime in enumerate(ANIME_DATA[genre]):
        btn = types.InlineKeyboardButton(
            anime['title'],  
            callback_data=f'anime_{genre}_{idx}'  
            )
        keyboard.add(btn)
    
    keyboard.add(types.InlineKeyboardButton("🔙 Назад", callback_data='back_to_start'))
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"📚 Топ-4 в жанре {genre.capitalize()}:",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('anime_'))
def show_anime_details(call):
    _, genre, idx = call.data.split('_')
    idx = int(idx)
    
    anime = ANIME_DATA[genre][idx]
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(        types.InlineKeyboardButton("Сменить жанр", callback_data='back_to_start')
    )
    
    try:
        bot.send_photo(
            call.message.chat.id,
            photo=anime['img'],
            caption=f"<b>{anime['title']}</b>\n\n{anime['desc']}",
            parse_mode='HTML',
            reply_markup=keyboard
        )
    except:
        bot.send_message(
            call.message.chat.id,
            f"<b>{anime['title']}</b>\n\n{anime['desc']}",
            parse_mode='HTML',
            reply_markup=keyboard
        )

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_start')
def back_to_main_menu(call):
    start(call.message)

bot.polling(none_stop=True)