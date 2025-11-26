from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def make_options_keyboard(options):
    keyboard = []
    for opt in options:
        keyboard.append([InlineKeyboardButton(text=opt, callback_data=opt)])
    return InlineKeyboardMarkup(keyboard)
