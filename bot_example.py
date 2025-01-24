import logging
from telegram.ext import CallbackQueryHandler, CommandHandler
from telegram import  ReplyKeyboardRemove, Update
from telegram import Update
from telegram.ext import Application
import calendar_picker
import hours_picker
import string_helper
import messages

# Go to botfather and create a bot and copy the token and paste it here in token
TOKEN = "7306348916:AAGeSLw30ANIds9O_aDq-ac7fF2gcvxuvKY" # token of the bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update, context):
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=messages.start_message.format(update.message.from_user.first_name),
        parse_mode="HTML")

# A simple command to display the calender
async def calendar_handler(update, context):
    await update.message.reply_text(text=messages.calendar_message,
                    reply_markup=calendar_picker.create_calendar())
    
async def time_handler(update, context):
    await update.message.reply_text(text=messages.calendar_message,
        reply_markup=hours_picker.create_hours_picker())
    
async def inline_handler(update, context):
    query = update.callback_query
    (kind, _, _, _, _) = string_helper.separate_callback_data(query.data)
    if kind == messages.CALENDAR_CALLBACK:
        await inline_calendar_handler(update, context)
    elif kind == messages.TIME_CALLBACK:
        await inline_time_handler(update, context)

async def inline_calendar_handler(update, context):
    selected,date = await calendar_picker.process_calendar_selection(update, context)
    if selected:
        await context.bot.send_message(chat_id=update.callback_query.from_user.id,
                        text=messages.calendar_response_message % (date.strftime("%d/%m/%Y")),
                        reply_markup=ReplyKeyboardRemove())
        
async def inline_time_handler(update, context):
    selected, hours = await hours_picker.process_hours_selection(update, context)
    if selected:
        await context.bot.send_message(chat_id=update.callback_query.from_user.id,
                        text=messages.calendar_response_message % (hours),
                        reply_markup=ReplyKeyboardRemove())

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start",start))
    application.add_handler(CommandHandler("calendar",calendar_handler))
    application.add_handler(CommandHandler("time", time_handler))
    application.add_handler(CallbackQueryHandler(inline_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

