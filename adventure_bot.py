import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from dotenv import load_dotenv
from functools import wraps
import os
import openai

from settings import RACES, CLASSES
from game import StateGame
from serializer import serializer_info, serializer_enemy, serializer_battle_result

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
load_dotenv('.env')
openai.api_key = os.getenv('API_KEY_OPENAI')

NAME, CLASS, RACE, CANCEL, MENU, BATTLE, RESPONSE = range(7)
MENU_BUTTONS = ['Info character', 'Find enemy', 'Pay for lvl']
BATTLE_BUTTONS = ['Fight', 'Escape']

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator

send_typing_action = send_action(constants.ChatAction.TYPING)

# COMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    WELCOME_MSG = 'WELCOME TO THE DUNGEON ADVENTURER! to begin tell me your heroe name.'
    context.user_data['total_msgs'] = []
    await update.message.reply_text(WELCOME_MSG)

    return NAME

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HELP_MSG = 'This is a help message'
    await update.message.reply_text(HELP_MSG)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    CANCEL_MSG = 'It\'s a lot for you i guess'
    await update.message.reply_text(CANCEL_MSG)

    return CANCEL

# HANDLERS

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    MENU_MSG = 'What do you want to do?'
    reply_keyboard: list[list[str]] = [[button] for button in MENU_BUTTONS]

    await update.message.reply_text(
        MENU_MSG,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder='Select',
            is_persistent=True
        )
    )

    return RESPONSE

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    PAY_MSG: str = 'Not implemented yet'

    await update.message.reply_text(
        PAY_MSG,
        parse_mode='MarkdownV2',
        reply_markup=ReplyKeyboardRemove(),
    )

    return await menu(update, context)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    info_msg: str = serializer_info(context.user_data.get('game').get_info_heroe())

    await update.message.reply_text(
        info_msg,
        parse_mode='MarkdownV2',
        reply_markup=ReplyKeyboardRemove(),
    )

    return await menu(update, context)

@send_typing_action
async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    enemy: dict = context.user_data.get('game').generate_battle()
    enemy_msg = serializer_enemy(enemy)
    reply_keyboard: list[list[str]] = [[button] for button in BATTLE_BUTTONS]

    await update.message.reply_text(
        enemy_msg,
        parse_mode='MarkdownV2',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder='Select',
            is_persistent=True
        )
    )

    return BATTLE

async def battle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option: str = update.message.text
    game: StateGame = context.user_data.get('game')

    # Fight
    if option == BATTLE_BUTTONS[0]:
        data = game.fight_battle()
        battle_msg = serializer_battle_result(data)

        await update.message.reply_text(
            battle_msg,
            parse_mode='MarkdownV2',
            reply_markup=ReplyKeyboardRemove()
        )
    # Escape
    elif option == BATTLE_BUTTONS[1]:
        game.pass_battle()

        ESCAPE_MSG = 'Chicken, chip chip chip'
        await update.message.reply_text(
            ESCAPE_MSG,
            parse_mode='MarkdownV2',
            reply_markup=ReplyKeyboardRemove()
        )

    return await menu(update, context)

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name: str = update.message.text
    context.user_data['name']: str = name

    RACES_MSG: str = 'Nice name! Now you have to choice your race'
    reply_keyboard: list[list[str]] = [[race] for race in RACES]
 
    await update.message.reply_text(
        RACES_MSG,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            input_field_placeholder='Select',
            is_persistent=True,
            one_time_keyboard=True
        )
    )

    return RACE

async def get_race(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    race: str = update.message.text
    context.user_data['race']: str = race

    CLASSES_MSG: str = 'Oh i see, well, i think the only thing missing is your class'
    reply_keyboard: list[list[str]] = [[clas] for clas in CLASSES]
 
    await update.message.reply_text(
        CLASSES_MSG,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder='Select',
            is_persistent=True
        )
    )

    return CLASS

async def get_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    clas: str = update.message.text
    context.user_data['class']: str = clas
    context.user_data['game']: StateGame = StateGame(
        context.user_data['name'],
        context.user_data['class'],
        context.user_data['race'],
    )

    ADVENTURE_MSG: str = 'Oh you are sooo cute. I hope you can handle the adventure'

    await update.message.reply_text(ADVENTURE_MSG, reply_markup=ReplyKeyboardRemove())

    return await menu(update, context)

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    UNKNOWN_MSG: str = 'Sorry, i didn\'t understand that command.'
    await update.message.reply_text(UNKNOWN_MSG)

# ERROR
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot')

    app: Application = Application.builder().token(os.getenv('TOKEN_BOT')).build()

    start: CommandHandler = CommandHandler("start", start_command)

    conv_handler: ConversationHandler = ConversationHandler(
        entry_points=[start],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            RACE: [MessageHandler(filters.Regex(f'^({"|".join(RACES)})$'), get_race)],
            CLASS: [MessageHandler(filters.Regex(f'^({"|".join(CLASSES)})$'), get_class)],
            MENU: [MessageHandler(filters.Regex(f'^({"|".join(MENU_BUTTONS)})$'), menu)],
            RESPONSE: [
                MessageHandler(filters.Regex(MENU_BUTTONS[0]), info),
                MessageHandler(filters.Regex(MENU_BUTTONS[1]), find),
                MessageHandler(filters.Regex(MENU_BUTTONS[2]), pay),
            ],
            BATTLE: [MessageHandler(filters.Regex(f'^({"|".join(BATTLE_BUTTONS)})$'), battle)],
            CANCEL: [start],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    app.add_handler(conv_handler)

    # Commands
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    # app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_unknown))

    # Errors
    app.add_error_handler(handle_error)

    print('Polling')
    app.run_polling(poll_interval=2)
