import asyncio
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from google import genai
from google.genai import types

# ==========================================
# ==========================================
# 1. 設定區 (直接填入你的金鑰)
# ==========================================
TG_TOKEN = '8535513130:AAGeA8UiuvX_BYKMsDUCcUzHz8I9XVTmFjI'
GEMINI_API_KEY = 'AIzaSyAlQJrbBQO4GyxUawQPvKC6N721jhsSuVU'

# 初始化 Gemini 2.5 客戶端
client = genai.Client(api_key=GEMINI_API_KEY, http_options={'api_version': 'v1'})
MODEL_ID = 'gemini-2.5-flash'

# 安全設定：全部設為 BLOCK_NONE
safety_settings = [
    types.SafetySetting(
        category='HARM_CATEGORY_HATE_SPEECH',
        threshold='BLOCK_NONE'
    ),
    types.SafetySetting(
        category='HARM_CATEGORY_DANGEROUS_CONTENT',
        threshold='BLOCK_NONE'
    ),
    types.SafetySetting(
        category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
        threshold='BLOCK_NONE'
    ),
    types.SafetySetting(
        category='HARM_CATEGORY_HARASSMENT',
        threshold='BLOCK_NONE'
    )
]

# 對話記憶儲存
user_sessions = {}

# ==========================================
# 2. 指令處理區 (對應你的 Menu)
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = []
    await update.message.reply_text(
        "🚀 *Gemini 2.5 終極助手已啟動！*\n\n"
        "你可以對我做這些事：\n"
        "• 💬 *聊天*：直接輸入文字\n"
        "• 📸 *看圖*：傳送照片並附上問題\n"
        "• 🎤 *聽歌*：傳送語音訊息給我\n"
        "• 🧹 *重置*：點擊 /reset 清空記憶",
        parse_mode=constants.ParseMode.MARKDOWN
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 *使用說明書*\n\n"
        "1. *連續對話*：我會記得最近 10 則訊息。\n"
        "2. *圖片辨識*：傳送照片後，可以問我『這是什麼？』或『翻譯裡面的文字』。\n"
        "3. *語音辨識*：你可以直接錄音傳給我，我會聽懂內容並回答。\n"
        "4. *清空記憶*：輸入 /reset 即可開啟全新的話題。"
    )
    await update.message.reply_text(help_text, parse_mode=constants.ParseMode.MARKDOWN)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = []
    await update.message.reply_text("🧹 *對話記憶已清空。*")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"⚡ *系統狀態*\n\n模型：`{MODEL_ID}`\n狀態：運作正常 ✅", parse_mode=constants.ParseMode.MARKDOWN)

# ==========================================
# 3. 媒體與文字處理區
# ==========================================

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    image_data = await photo_file.download_as_bytearray()
    prompt = update.message.caption if update.message.caption else "描述這張圖片"
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt, {'mime_type': 'image/jpeg', 'data': bytes(image_data)}],
            config=types.GenerateContentConfig(safety_settings=safety_settings)
        )
        await update.message.reply_text(f"📸 *分析結果*：\n\n{response.text}", parse_mode=constants.ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ 圖片處理失敗：{e}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        voice_file = await update.message.voice.get_file()
        voice_data = await voice_file.download_as_bytearray()
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=["聽這段語音並回覆", {'mime_type': 'audio/ogg', 'data': bytes(voice_data)}],
            config=types.GenerateContentConfig(safety_settings=safety_settings)
        )
        await update.message.reply_text(f"🎧 *語音辨識回覆*：\n\n{response.text}", parse_mode=constants.ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"❌ 語音分析失敗：{e}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_sessions: user_sessions[user_id] = []
    user_sessions[user_id].append({"role": "user", "parts": [{"text": update.message.text}]})
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        response = client.models.generate_content(
            model=MODEL_ID, 
            contents=user_sessions[user_id],
            config=types.GenerateContentConfig(safety_settings=safety_settings)
        )
        user_sessions[user_id].append({"role": "model", "parts": [{"text": response.text}]})
        if len(user_sessions[user_id]) > 10: user_sessions[user_id] = user_sessions[user_id][-10:]
        await update.message.reply_text(response.text, parse_mode=constants.ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"😵 錯誤：{str(e)}")

# ==========================================
# 4. 啟動區
# ==========================================
if __name__ == '__main__':
    app = ApplicationBuilder().token(TG_TOKEN).build()
    
    # 註冊選單對應的指令
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    
    # 註冊媒體與文字處理
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    
    print(f"🚀 機器人啟動成功！模型：{MODEL_ID}")
    app.run_polling()