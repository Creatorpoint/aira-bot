import random
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8786463307:AAGeKOQtZSBiXzcmf_kieaI3y_yQieC05uI"
DEVELOPER = "@PREMGUPTA2M"

# -------------------------
# DATA FILES
# -------------------------

LEVEL_FILE = "levels.json"
COIN_FILE = "coins.json"

# -------------------------
# BAD WORDS
# -------------------------

bad_words = ["mc","bc","madarchod","bhosdike","chutiya"]

# -------------------------
# MEMES
# -------------------------

memes = [
"https://i.imgflip.com/1bij.jpg",
"https://i.imgflip.com/30b1gx.jpg",
"https://i.imgflip.com/26am.jpg"
]

videos = [
"https://files.catbox.moe/meme1.mp4",
"https://files.catbox.moe/meme2.mp4"
]

# -------------------------
# AI REPLIES
# -------------------------

aira_replies = [
"Aira yahin hai 😊",
"bolo na kya baat hai?",
"tum mujhe bula rahe the?",
"Aira sun rahi hai 👀",
"hehe kya baat hai senpai 😆"
]

# -------------------------
# JSON HELPERS
# -------------------------

def load(file):

    try:
        return json.load(open(file))
    except:
        return {}

def save(file,data):

    json.dump(data,open(file,"w"))

# -------------------------
# LEVEL SYSTEM
# -------------------------

def add_xp(user_id):

    data = load(LEVEL_FILE)

    if user_id not in data:
        data[user_id]={"xp":0,"level":1}

    data[user_id]["xp"]+=5

    if data[user_id]["xp"]>=50:
        data[user_id]["level"]+=1
        data[user_id]["xp"]=0

    save(LEVEL_FILE,data)

    return data[user_id]

# -------------------------
# COINS
# -------------------------

def add_coins(user_id):

    data=load(COIN_FILE)

    if user_id not in data:
        data[user_id]={"coins":0}

    data[user_id]["coins"]+=10

    save(COIN_FILE,data)

    return data[user_id]["coins"]

# -------------------------
# WELCOME
# -------------------------

async def welcome(update:Update,context:ContextTypes.DEFAULT_TYPE):

    for user in update.message.new_chat_members:

        name=user.first_name
        group=update.effective_chat.title

        msg=f"""
💖 Welcome {name}

🌸 {group} mein tumhara romantic welcome hai

Aira tumse milke khush hai 🥰
"""

        await update.message.reply_text(msg)

# -------------------------
# LOVE METER
# -------------------------

async def love(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if len(context.args)<2:
        await update.message.reply_text("Usage: /love @user1 @user2")
        return

    u1=context.args[0]
    u2=context.args[1]

    score=random.randint(1,100)

    await update.message.reply_text(
f"""
❤️ LOVE METER

{u1} ❤️ {u2}

Match: {score}%

Aira ko lagta hai tum cute couple ho 😆
"""
)

# -------------------------
# CASINO
# -------------------------

async def casino(update:Update,context:ContextTypes.DEFAULT_TYPE):

    symbols=["🍒","💎","7️⃣","🍀"]

    spin=[random.choice(symbols) for _ in range(3)]

    text=" | ".join(spin)

    if spin[0]==spin[1]==spin[2]:

        coins=add_coins(str(update.message.from_user.id))

        msg=f"""
🎰 CASINO

{text}

🎉 JACKPOT

Coins: {coins}
"""

    else:

        msg=f"""
🎰 CASINO

{text}

Better luck next time 😆
"""

    await update.message.reply_text(msg)

# -------------------------
# MARRIAGE
# -------------------------

async def marry(update:Update,context:ContextTypes.DEFAULT_TYPE):

    if len(context.args)==0:
        await update.message.reply_text("Usage: /marry @user")
        return

    user1=update.message.from_user.first_name
    user2=context.args[0]

    await update.message.reply_text(
f"""
💍 AIRA MARRIAGE SYSTEM

{user1} ❤️ {user2}

Aira ne tum dono ki shaadi approve kar di 😆
"""
)

# -------------------------
# BALANCE
# -------------------------

async def balance(update:Update,context:ContextTypes.DEFAULT_TYPE):

    data=load(COIN_FILE)

    uid=str(update.message.from_user.id)

    coins=data.get(uid,{"coins":0})["coins"]

    await update.message.reply_text(
f"💰 Tumhare coins: {coins}"
)

# -------------------------
# MAIN MESSAGE HANDLER
# -------------------------

async def message(update:Update,context:ContextTypes.DEFAULT_TYPE):

    text=update.message.text.lower()
    user=update.message.from_user
    uid=str(user.id)
    name=user.first_name

    # bad words
    for w in bad_words:
        if w in text:
            await update.message.reply_text(
"⚠️ Bad language allowed nahi hai"
)
            return

    # XP + coins
    level=add_xp(uid)
    coins=add_coins(uid)

    # developer question
    if "developer" in text or "creator" in text:

        await update.message.reply_text(
f"💖 Mujhe {DEVELOPER} ne banaya hai"
)

    # bf question
    elif "bf" in text:

        await update.message.reply_text(
f"😌 Aira ka bf sirf {DEVELOPER}"
)

    # meme
    elif "meme" in text:

        await update.message.reply_photo(random.choice(memes))

    # video meme
    elif "reel" in text or "video" in text:

        await update.message.reply_video(random.choice(videos))

    # hug sticker
    elif "hug" in text:

        await update.message.reply_sticker(
"CAACAgUAAxkBAAEC0lpkf2stickerID"
)

    # AI chat
    elif "aira" in text:

        reply=random.choice(aira_replies)

        await update.message.reply_text(
f"{name} 😊\n\n{reply}"
)

# -------------------------
# BOT START
# -------------------------

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("love",love))
app.add_handler(CommandHandler("casino",casino))
app.add_handler(CommandHandler("marry",marry))
app.add_handler(CommandHandler("balance",balance))

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS,welcome))
app.add_handler(MessageHandler(filters.TEXT,message))

import asyncio

print("Aira Ultra Bot Running...")

async def main():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

asyncio.run(main())
