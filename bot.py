import asyncio
import random
import signal
import sys
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile
from app.keyboards import *
from app.config import BOT_TOKEN, MUSICIANS, FOOTBALLERS, DBG, MAX_PLAYERS, MIN_PLAYERS


class GameStates(StatesGroup):
    waiting_for_mode = State()
    waiting_for_players = State()
    showing_cards = State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "добро пожаловать в игру *шпионфай*🙏🏻\n"
        "это игра, где один из игроков - шпион, который не знает секретного человека, "
        "ваша задача - вычислить шпиона, говоря факты об этом персонаже\n\n"
        "/game - для начала игры 🃏\n"
        "/help - узнать правила 📃\n",
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📜 *правила игры шпионфай*\n\n"
        f"1) выбирается количество игроков (от {MIN_PLAYERS} до {MAX_PLAYERS})\n"
        "2) каждый игрок по очереди смотрит свою карточку\n"
        "3) все карточки одинаковые, кроме одной - у шпиона (он не знает карту других игроков)\n"
        "4) игроки по очереди говорят факты о человеке\n"
        "5) шпион должен понять, о ком идет речь, и не выдать себя\n"
        "6) в конце голосование - кто шпион?\n"
        "7) если шпион отгадает персонажа - победа шпиона, иначе - поражение\n\n"
        "💡 *совет*: не показывайте свою карточку другим игрокам!",
        parse_mode="Markdown"
    )

@dp.message(Command("game"))
async def cmd_game(message: types.Message, state: FSMContext):
    await message.answer(
        "🎮 начинаем новую игру!\n"
        "выберите тематику игры ⬇️",
        reply_markup=get_mode_keyboard()
    )
    await state.set_state(GameStates.waiting_for_mode)

@dp.callback_query(GameStates.waiting_for_mode)
async def process_mode(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "теперь выберем количество игроков!\n"
        "выберите нужное число участников игры ⬇️",
        reply_markup=get_players_keyboard()
    )
    await state.update_data(mode=callback.data)
    await state.set_state(GameStates.waiting_for_players)

@dp.callback_query(GameStates.waiting_for_players, F.data.startswith("players_"))
async def process_players_count(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    mode = data["mode"]
    players_count = int(callback.data.split("_")[1])
    if mode == "music": normal_item = random.choice(MUSICIANS) 
    else: normal_item = random.choice(FOOTBALLERS)
    spy_number = random.randint(1, players_count)
    
    await state.update_data(
        players_count=players_count,
        spy_number=spy_number,
        normal_item=normal_item,
        current_player=1,
        photo_message_id=None
    )
    
    await callback.message.edit_text(
        f"🎯 игра началась!\n"
        f"количество игроков - {players_count}\n\n"
        f"игрок 1, нажмите кнопку ⬇️",
        reply_markup=get_show_card_keyboard(1)
    )
    await state.set_state(GameStates.showing_cards)
    await callback.answer()

@dp.callback_query(GameStates.showing_cards, F.data.startswith("show_"))
async def show_card(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    player_num = int(callback.data.split("_")[1])
    
    if player_num != data["current_player"]:
        await callback.answer("❌ не ваш ход!", show_alert=True)
        return
    
    normal_item = data["normal_item"]
    spy_number = data["spy_number"]
    is_spy = player_num == spy_number
    item_name = "🕵️ ШПИОН (вам нужно угадать человека)" if is_spy else normal_item["name"]
    
    if data.get("photo_message_id"):
        try:
            await bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=data["photo_message_id"]
            )
        except Exception as e:
            print(f"не удалось отправить фото: {e}")
    
    photo_message = None
    if not is_spy:
        try:
            if os.path.exists(normal_item["image"]):
                photo = FSInputFile(normal_item["image"])
                photo_message = await callback.message.answer_photo(
                    photo=photo,
                    caption=f"🎴 *карточка игрока {player_num}*\n\n"
                            f"📷 человек - *{normal_item['name']}*\n\n"
                            f"нажмите \"скрыть\", когда посмотрите",
                    parse_mode="Markdown"
                )
        except Exception as e:
            await callback.message.answer(
                f"⚠️ *ошибка загрузки изображения*\n\n"
                f"человек - *{normal_item['name']}*",
                parse_mode="Markdown"
            )
            print(f"ошибка при отправке фото: {e}")
    
    if photo_message:
        await state.update_data(photo_message_id=photo_message.message_id)
    
    await callback.message.edit_text(
        f"🎴 *карточка игрока {player_num}*\n\n"
        f"{item_name}\n\n"
        f"нажмите \"скрыть\", когда посмотрите",
        reply_markup=get_hide_card_keyboard(player_num),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(GameStates.showing_cards, F.data.startswith("hide_"))
async def hide_card(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    player_num = int(callback.data.split("_")[1])
    
    if player_num != data["current_player"]:
        await callback.answer("❌ не ваш ход!", show_alert=True)
        return
    
    photo_message_id = data.get("photo_message_id")
    if photo_message_id:
        try:
            await bot.delete_message(
                chat_id=callback.message.chat.id,
                message_id=photo_message_id
            )
        except Exception as e:
            print(f"не удалось удалить фото: {e}")
    
    players_count = data["players_count"]
    next_player = player_num + 1
    
    if next_player > players_count:
        await callback.message.edit_text(
            "✅ все игроки посмотрели свои карточки!\n\n"
            "🔍 *начинайте обсуждение!*\n"
            "задавайте вопросы, обсуждайте человека и голосуйте, кто шпион\n\n"
            "чтобы начать новую игру, используйте /game",
            parse_mode="Markdown"
        )
        await state.clear()
    else:
        await state.update_data(
            current_player=next_player,
            photo_message_id=None  # Сбрасываем ID для следующего игрока
        )
        await callback.message.edit_text(
            f"👤 игрок {player_num} готов!\n\n"
            f"игрок {next_player}, нажмите кнопку ⬇️",
            reply_markup=get_show_card_keyboard(next_player)
        )
    
    await callback.answer()

@dp.callback_query()
async def handle_other_callbacks(callback: CallbackQuery):
    await callback.answer("❌ неверное действие или не ваша очередь", show_alert=True)

async def main():
    print(f"{DBG} запуск бота 'шпионфай'")
    
    def signal_handler(sig, frame):
        print(f"\n{DBG} принудительное завершение бота!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try: await dp.start_polling(bot)
    finally:
        await bot.session.close()
        print(f"{DBG} бот остановлен успешно!")

if __name__ == "__main__":
    asyncio.run(main())
