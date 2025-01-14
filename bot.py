rom telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    text=load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)


# Here we write our code :)
async def hello(update, context):
    await send_text(update, context, "*Hello Bro*")
    await send_text(update, context, "*How are you doing today?*")
    await send_text(update, context, "You replied with " + update.message.text)

    await send_photo(update, context, "avatar_main")
    await send_text_buttons(update, context, "Start the process?",
                            {"start":"Start",
                             "stop": "Stop"
})

async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "Process started")
    else:
        await send_text(update, context, "Process stoped")


app = ApplicationBuilder().token("7496096792:AAEbmJ_oMSfnMnBSjZMP62x9NdBzAu89ykY").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()