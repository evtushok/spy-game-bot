from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.config import MAX_PLAYERS, MIN_PLAYERS

def get_mode_keyboard():
    buttons = [[InlineKeyboardButton(text="футболисты ⚽️", callback_data="football")],
               [InlineKeyboardButton(text="музыканты 🎧", callback_data="music")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_players_keyboard():
    buttons = []
    for i in range(MIN_PLAYERS, MAX_PLAYERS):
        buttons.append([InlineKeyboardButton(text=str(i), callback_data=f"players_{i}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_show_card_keyboard(player_num):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👁 показать карточку", callback_data=f"show_{player_num}")]
    ])

def get_hide_card_keyboard(player_num):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🙈 скрыть карточку", callback_data=f"hide_{player_num}")]
    ])