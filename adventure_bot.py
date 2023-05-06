import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from settings import TOKEN, RACES

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

NAME, CLASS, RAZE, BIO = range(4)

# COMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    WELCOME_MSG = 'WELCOME TO THE DUNGEON ADVENTURER! to begin tell me your heroe name.'
    context.user_data['total_msgs'] = []
    await update.message.reply_text(WELCOME_MSG)

    return NAME

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HELP_MSG = 'this is a help message'
    await update.message.reply_text(HELP_MSG)


# HANDLERS

def handle_response(text: str) -> str:
    menssages.append(text)
    if 'hello' in text:
        return 'Oh, hello my best friend!'
    return 'Do you want a fight?'

async def races(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name: str = update.message.text
    context.user_data['name'] = name

    RACES_MSG: str = 'Nice name! Now you have to choice your race'
    reply_keyboard: list[list[str]] = [RACES]
 

    await update.message.reply_text(
        RACES_MSG,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Select')
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    
    context.user_data['total_msgs'] = [text] + context.user_data['total_msgs']
    print(context.user_data)
    print(f'User {update.message.chat.id} type: "{text}"')

    response = handle_response(text)
    await update.message.reply_text(str(context.user_data.get('total_msgs', None)))
    # await update.message.reply_text(str([context.user_data[k] for k in context.user_data]))

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    UNKNOWN_MSG = 'Sorry, I didn\'t understand that command.'
    await update.message.reply_text(UNKNOWN_MSG)

# ERROR
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot')

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, races)],
            GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_handler(MessageHandler(filters.COMMAND, handle_unknown))

    # Errors
    app.add_error_handler(handle_error)

    print('Polling')
    app.run_polling(poll_interval=2)
