import os
import telebot
from deepface import DeepFace

# توکن ربات تلگرام خود را وارد کنید
TOKEN = '7494712545:AAFXzPJpKwpbgtcRsUkUiZz4HRhxqwZHBIs'
bot = telebot.TeleBot(TOKEN)

# پوشه‌ای برای ذخیره عکس‌ها ایجاد کنید
if not os.path.exists('./uploads'):
    os.makedirs('./uploads')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! لطفاً یک عکس ارسال کنید تا تحلیل شود.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        file_path = f"./uploads/{file_info.file_id}.jpg"

        # دانلود عکس
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # تحلیل عکس
        analysis = DeepFace.analyze(file_path, actions=['age', 'gender', 'race'])
        result = (
            f"سن: {analysis[0]['age']}\n"
            f"جنسیت: {analysis[0]['gender']}\n"
            f"نژاد: {analysis[0]['dominant_race']}"
        )
        bot.reply_to(message, result)

    except Exception as e:
        bot.reply_to(message, f"خطا: {str(e)}")
    finally:
        # پاک کردن عکس پس از پردازش
        if os.path.exists(file_path):
            os.remove(file_path)

# شروع ربات
bot.polling(none_stop=True)