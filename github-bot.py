import telegram, time, os, glob
from telegram.ext import *
from telegram import Update
from difflib import SequenceMatcher

TOKEN = "YOUR TOKEN HERE"
SIMILARITY_RATE = 85

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown_v2("Hey \! Moi C'estCiaoBot\. 🫡\nAjoute moi dans un groupe ou un channel et *mets\-moi administrateur*, je supprimerai les messages de scams selon" +
        " ma liste interne configurée\.\n📊 Taux de sensibilité configuré : " + str(SIMILARITY_RATE) + "%")

async def analyze_msg(update, context):
    msg = update.effective_message
    text = msg.text
    for forbidden_text in retrieve_forbidden_messages():
        if get_string_similarity(forbidden_text, text) >= SIMILARITY_RATE:
            await msg.delete()
            print("- SPAM DETECTED - message removed")
            user = msg.from_user
            if user is not None:
                print("-> User ID : " + str(user.id))
                print("-> Username : " + user.username)
                print("------------------------------")

def retrieve_forbidden_messages():
    files = glob.glob(os.path.join("forbidden-messages", "*.txt"))
    file_contents = []
    for file in files:
        with open(file, 'r', encoding="utf-8") as f:
            content = f.read()
            file_contents.append(content)
    return file_contents

def get_string_similarity(string1, string2):
    matcher = SequenceMatcher(None, string1, string2)
    similarity = matcher.ratio() * 100
    return similarity

if not os.path.exists("forbidden-messages"):
    os.makedirs("forbidden-messages")

application = Application.builder().token(TOKEN).build()
print("|----------------------------------------------|")
print("| C'estCiaoBot CONNECTED - Created by KeyKatyu |")
print("|------- https://github.com/KeyKatyu ----------|")
print("|----------------------------------------------|")
application.add_handler(CommandHandler("start", start_callback))
application.add_handler(MessageHandler(filters.TEXT, analyze_msg))
application.run_polling()