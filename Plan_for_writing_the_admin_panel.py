import products
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from crud_functions import initiate_db, get_all_products, populate_products

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

def create_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    buttons = [
        types.KeyboardButton("Рассчитать"),
        types.KeyboardButton("Информация"),
        types.KeyboardButton("Купить")
    ]
    kb.add(*buttons)
    return kb

def create_inline_keyboard():
    kb = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("Рассчитать норму калорий", callback_data='calories'),
        InlineKeyboardButton("Формулы расчёта", callback_data='formulas'),
    ]
    kb.add(*buttons)
    return kb

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью. Нажми "Рассчитать", чтобы начать.',
                         reply_markup=create_keyboard())

@dp.message_handler(lambda message: message.text == "Рассчитать")
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию:', reply_markup=create_inline_keyboard())


@dp.message_handler(lambda message: message.text == "Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products()

    if not products:
        await message.answer("Нет доступных продуктов.")
        return

    for product in products:
        title, description, price, image_url = product
        caption = f'Название: {title}\nОписание: {description}\nЦена: {price} руб.'


        kb = InlineKeyboardMarkup()
        buy_button = InlineKeyboardButton("Купить",
                                          callback_data=f'buy_{title}')
        kb.add(buy_button)

        try:
            await message.answer_photo(photo=image_url, caption=caption, reply_markup=kb)
        except Exception as e:
            await message.answer(f"Ошибка при отправке фото для продукта {title}: {e}")


@dp.callback_query_handler(lambda call: call.data.startswith('buy_'))
async def handle_product_purchase(call: types.CallbackQuery):
    product_name = call.data.split('_', 1)[1]
    await call.message.answer(f"Вы выбрали продукт: {product_name}. Вы успешно приобрели его!")
    await call.answer()
@dp.callback_query_handler(lambda call: call.data.startswith('buy_'))
async def handle_product_purchase(call: types.CallbackQuery):
    product_name = call.data.split('_', 1)[1]
    await call.message.answer(f"Вы выбрали продукт: {product_name}. Вы успешно приобрели его!")
    await call.answer()

@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer("Формула Миффлина-Сан Жеора:\n"
                              "Для мужчин: BMR = 10 * вес + 6.25 * рост - 5 * возраст + 5\n"
                              "Для женщин: BMR = 10 * вес + 6.25 * рост - 5 * возраст - 161")
    await call.answer()

@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма калорий: {calories} ккал в день.')
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

if __name__ == '__main__':
    initiate_db()
    populate_products()
    executor.start_polling(dp, skip_updates=True)