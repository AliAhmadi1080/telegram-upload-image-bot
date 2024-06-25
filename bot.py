from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
import logging
import configs

logging.basicConfig(filename=configs.LOG_FILE_NAME, filemode='w',\
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        num = 2

        try:
            num = int(context.args[-1])
            name = '+'.join(context.args[:-1])
        except:
            name = '+'.join(context.args)
        
        url = "https://www.google.com/search?hl=en&q=%s&safe=off&udm=2" %(name)
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html.parser').find_all('img')
        photo = str(soup[num]['src'])
        logging.info(photo)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

    else:
        await update.message.reply_text('Please provide a name after the /find command.')



app = ApplicationBuilder().token(configs.API_TOKEN).build()

app.add_handler(CommandHandler("find", find))

app.run_polling()
