from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from ...states import Registration
from ...keyboards.registration import share_phone_keyboard

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("\U0001F44B Привет! Поделись номером", reply_markup=share_phone_keyboard)
    await state.set_state(Registration.AwaitingPhone)

@router.message(Registration.AwaitingPhone)
async def handle_contact(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Нужно поделиться контактом")
        return
    # Here we would save the user to database
    await message.answer("Готово, ты в системе!", reply_markup=None)
    await state.clear()
