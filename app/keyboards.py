from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.config import MAX_PLAYERS, MIN_PLAYERS, CATEGORIES

def get_mode_keyboard():
    builder = InlineKeyboardBuilder()
    for key, cat in CATEGORIES.items():
        builder.button(text=cat["label"], callback_data=key)
    builder.adjust(2)
    return builder.as_markup()

def get_players_keyboard():
    buttons = []
    for i in range(MIN_PLAYERS, MAX_PLAYERS+1):
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
