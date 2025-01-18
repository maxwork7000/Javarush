from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    dialog.mode= "main"
    text=load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update, context,{
        "start": "bot main menu",
        "profile": "Tinder profile generation",
        "opener": "message for dating",
        "message": "correspondence on your behalf",
        "date": "correspondence with the celebrities",
        "gpt": "Ask a question to GPT chat",

    })

async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await  chatgpt.send_question(prompt,text)
    await  send_text(update, context, answer)


async def date(update, context):
        dialog.mode = "date"
        text = load_message("date")
        await send_photo(update, context, "date")
        await send_text_buttons(update, context, text, {
            "date_grande": "Ariana Grande",
            "date_robbie": "Margo Robbi",
            "date_zendaya":"Zendeya",
            "date_gosling": "Rayan Gosling",
            "date_hardy": "Tom Hardy"


        })


async def date_dialog(update,context):
    pass


async def date_button(update,context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update,context, query)
    await send_text(update, context, "Good choice! Invite girl or a nice guy to date with only a few messages")


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        await send_text(update, context, "*Hi and thank you for coming")
        await send_text(update, context, "*We will help you today!*")
        await send_text(update, context, "You replied with " + update.message.text)

        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Start the process?",
                            {"start":"Start",
                             "stop": "Stop"
        })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context, "Process Started")
    else:
        await send_text(update, context, "Process Stoped")


dialog = Dialog()
dialog.mode = None


chatgpt=ChatGptService("gpt:A03NYofv3ubgIx6f1SXnPAKmBZ0E9dS9Qcn2T2Zi1nOgo_QvJ0z8W5cWFvJFkblB3TavDiNT25x1--mRNrTISss9Vj3Q6lCoImv5cXw51H8RE70DG7rsRaf4bEE4")

app = ApplicationBuilder().token("7496096792:AAEbmJ_oMSfnMnBSjZMP62x9NdBzAu89ykY").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
