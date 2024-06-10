from aiogram import Router, Bot
from aiogram.client import bot
from aiogram.types import Message, WebAppInfo, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardButton
)
import os
import json

import requests
from Tarkov_Market_bot.webApp.config import TOKEN_BOT
import Tarkov_Market_bot.Keyboards.keyboards
from Tarkov_Market_bot.Keyboards.keyboards import *
from Controllers.itemConroller import (
    _apiService,
    _itemService
)
from Services.questService import QuestService
quest_service = QuestService()

router = Router()

def get_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти", web_app=WebAppInfo(url='https://t.me/test_thiiiis_shit_bot'))
    return builder.as_markup()

""" кнопки: предметы, квесты """
main_builder = InlineKeyboardBuilder()

main_builder.row(
    InlineKeyboardButton(text="Предметы", callback_data="items"),
    InlineKeyboardButton(text="Квесты", callback_data="quests")
)

@router.message(Command("Find"))
async def find_items(message: Message):
    await message.answer("Что вам нужно?", reply_markup=Tarkov_Market_bot.Keyboards.keyboards.main_kb)

@router.message(CommandStart())
async def on_start(message: Message):
    username = message.from_user.first_name or message.from_user.username
    await message.answer(f"Привет, {username}! Как я могу помочь вам?",
                         reply_markup=get_kb())

@router.callback_query()
async def show_items_categories(query: CallbackQuery):
    if query.data == "items":
        await query.message.edit_reply_markup(reply_markup=Tarkov_Market_bot.Keyboards.keyboards.item_kb)

@router.callback_query()
async def go_back(query: CallbackQuery):
    if query.data == "back":
        await query.message.edit_reply_markup(reply_markup=Tarkov_Market_bot.Keyboards.keyboards.main_kb())

@router.message(Command("help"))
async def wait_help(message: Message):
    await message.answer('не ну вот так как-то')

"""Реализайция поиска через сообщения"""
bot = Bot(token=TOKEN_BOT)
@router.message()
async def get_message(message: Message):
    search_query = message.text
    items = _apiService.get_item_by_name(search_query)

    for item in items:
        name = item["name"]
        price = item["price"]
        avg24hPrice = item["avg24hPrice"]
        icon = item["icon"]

        await bot.send_photo(chat_id=message.chat.id, photo=icon,
                             caption=
                             f"Название: {name}\n"
                             f"Цена: {price}\n"
                             f"Средняя цена за 24 часа: {avg24hPrice}")
# bot = Bot(token=TOKEN_BOT)
# @router.message()
# async def get_message(message: Message):
#     search_query = message.text
#     items = _apiService.get_item_by_name(search_query)
#
#     for item in items:
#         info_message = "Информация о товаре:\n"
#         for key, value in item.items():
#             info_message += f"{key}: {value}\n"
#
#         await bot.send_message(chat_id=message.chat.id, text=info_message)

# New quest-related routers

@router.message(Command("Quests"))
async def list_quests(message: Message):
    trader_name = message.text.split(maxsplit=1)[-1]
    quests = quest_service.get_quests_for_trader(trader_name)
    # trader_name = message.text
    # quests = quest_service.get_quest_details(trader_name)

    if not quests:
        await message.answer("К сожалению, я не нашел квестов для этого торговца.")
        return

    response = f"Квесты для торговца {trader_name}:\n\n"
    for quest in quests:
        response += f"{quest['Название']}\n"
        response += f"Ссылка: {quest['url']}\n\n"

    await message.answer(response)


@router.message(Command("quest_detail"))
async def quest_details(message: Message):
    await message.answer('test')
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Пожалуйста, укажите имя торговца и название квеста.")
        return

    trader_name = parts[1]
    quest_name = parts[2]

    print(f"Received request for quest details: Trader Name: {trader_name}, Quest Name: {quest_name}")  # Diagnostic message
    try:
        quest_data = await quest_service.get_quest_details(trader_name, quest_name)
    except Exception as e:
        print(f"Error while fetching quest details: {e}")
        await message.answer("Произошла ошибка при получении данных о квесте.")
        return

    if not quest_data:
        await message.answer("К сожалению, я не нашел подробной информации по этому квесту.")
        return

    response = f"Подробная информация о квесте {quest_name}:\n\n"
    response += f"Требования: {quest_data.get('Требования', 'Нет данных')}\n"
    response += f"Цели квеста: {quest_data.get('Цели квеста', 'Нет данных')}\n"
    response += f"Как выполнить квест: {quest_data.get('Как выполнить квест', 'Нет данных')}\n"
    response += f"Награды за квест: {quest_data.get('Награды за квест', 'Нет данных')}\n"

    images = quest_data.get("Ссылки на изображения", [])
    for image in images:
        await bot.send_photo(chat_id=message.chat.id, photo=image)

    await message.answer(response)

