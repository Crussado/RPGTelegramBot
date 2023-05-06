import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from settings import TOKEN, RACES, CLASSES

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

NAME, CLASS, RACE, CANCEL = range(4)

# COMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    WELCOME_MSG = 'WELCOME TO THE DUNGEON ADVENTURER! to begin tell me your heroe name.'
    context.user_data['total_msgs'] = []
    await update.message.reply_text(WELCOME_MSG)

    return NAME

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HELP_MSG = 'this is a help message'
    await update.message.reply_text(HELP_MSG)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CANCEL_MSG = 'It\'s a lot for you i guess'
    await update.message.reply_text(CANCEL_MSG)

    return CANCEL

# HANDLERS

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name: str = update.message.text
    context.user_data['name'] = name

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

async def get_race(update: Update, context: ContextTypes.DEFAULT_TYPE):
    race: str = update.message.text
    context.user_data['race'] = race

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

async def get_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clas: str = update.message.text
    context.user_data['class'] = clas

    ADVENTURE_MSG: str = 'Oh you are sooo cute. I hope you can handle the adventure'

    await update.message.reply_text(
        ADVENTURE_MSG,
        reply_markup=ReplyKeyboardRemove()
    )

    return CLASS

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    UNKNOWN_MSG = 'Sorry, I didn\'t understand that command.'
    await update.message.reply_text(UNKNOWN_MSG)

# ERROR
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot')

    app = Application.builder().token(TOKEN).build()

    start = CommandHandler("start", start_command)

    conv_handler = ConversationHandler(
        entry_points=[start],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            RACE: [MessageHandler(filters.Regex(f'^({"|".join(RACES)})$'), get_race)],
            CLASS: [MessageHandler(filters.Regex(f'^({"|".join(CLASSES)})$'), get_class)],
            CANCEL: [start],
        },
        fallbacks=[CommandHandler("cancel", cancel_command)],
    )

    app.add_handler(conv_handler)

    # Commands
    # app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    # app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_unknown))

    # Errors
    app.add_error_handler(handle_error)

    print('Polling')
    app.run_polling(poll_interval=2)
