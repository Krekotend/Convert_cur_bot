import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from service import test_in_dig, conversion

router: Router = Router()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def cmd_start(message: Message):
    logger.info(f"User {message.from_user.username} started the bot")
    await message.answer(text=f'Приветствую вас {message.from_user.username}\!\n'
                              'Я бот котороый конвертирует валюту\.\n'
                              'Запишите *сумму\, валюту и валюту конвертации* и _отправте_\n'
                              'Пример \: *100 USD to EUR*\n'
                              'Подсказки и другие функции можно посмотреть набрав /help или в меню \n',
                         parse_mode='MarkdownV2')


@router.message(Command(commands=['help']))
async def cmd_help(message: Message):
    await message.answer(text='Что бы конвертировать валюты нужно\:\n'
                              'Запишите *сумму\, валюту и валюту конвертации* и _отправте_\n'
                              'Пример \: *100 USD to EUR* \n'
                              'или воспользоваться командой /convert \n '
                              'Пример \: */convert 100 USD to EUR* \n'
                              'список команд: /convert \- выполняет конвертацию ,\n'
                              '/contacts \- выводит контакты,\n'
                              '||/dice \- бросок кубика||',
                         parse_mode='MarkdownV2')


@router.message(Command(commands=['convert']))
async def cmd_convert(message: Message):
    logger.info(f"User {message.from_user.username} used converter")
    t_msg = message.text.replace('/convert', '')
    if not t_msg:
        await message.answer(text='Пожалуйста, укажите данные для конвертации.')
        return
    if test_in_dig(t_msg):
        resp_text = conversion(t_msg)
        await message.answer(text=f'{resp_text}')
    else:
        await message.answer(text='Некорректные данные')

@router.message(Command(commands=['dice']))
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji="🎲")


@router.message(F.text.lower().in_({'hi', 'hello', 'привет', 'здравствуй', 'здравствуйте'}))
async def process_hello(message: Message):
    await message.answer('Приветствую вас!')


@router.message(F.text.lower().in_({'bye', 'goodbye', 'до свидания', 'пока', 'прощай'}))
async def process_bye(message: Message):
    await message.answer('До скорых встреч!')


@router.message(Command(commands=['contacts']))
async def show_contacts(message: Message):
    await message.answer(text='*_I will be glad to accept suggestions or wishes_*\n'
                              '||In the subject of the email\, indicate Tg_Convert||\n'
                              '||Tg:\@Krekotend, email:Krekotend\@gmail\.com||',
                         parse_mode='MarkdownV2')


def main_filter(message: Message) -> bool:
    return test_in_dig(message.text)


@router.message(main_filter)
async def show_conversion(message: Message):
    logger.info(f"User {message.from_user.username} used converter")
    resp_text = conversion(message.text)
    await message.answer(text=f'{resp_text}')


@router.message()
async def other(message: Message):
    await message.reply(text='Не смог понять что вы написали ,'
                             'пожалуйста напипишите команду которую я пойму '
                             ' /help спиок команд ')
