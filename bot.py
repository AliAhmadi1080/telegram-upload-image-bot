from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
import logging
import configs

def upscale(image_url:str):
    url = "https://api.picsart.io/tools/1.0/upscale"
    payload = {"upscale_factor": "x8",
            "image_url": image_url}
    headers = {
        "accept": "application/json",
        "x-picsart-api-key": configs.AI_IMAGE_UPSCALER
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()[
        'data']['url']
    return response

logging.basicConfig(filename=configs.LOG_FILE_NAME, filemode='w', level='INFO',
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) > 0:
        num = 2

        try:
            num = int(context.args[-1])
            name = '+'.join(context.args[:-1])
        except:
            name = '+'.join(context.args)

        url = "https://www.google.com/search?hl=en&q=%s&safe=off&udm=2" % (
            name)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser').find_all('img')
        photo = str(soup[num]['src'])
        photo = upscale(photo)
        logging.info(photo)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

    else:
        await update.message.reply_text('Please provide a name after the /find command.')


app = ApplicationBuilder().token(configs.API_TOKEN).build()

app.add_handler(CommandHandler("find", find))

app.run_polling()
