import logging
from aiogram import Bot, Dispatcher, executor, types
import yt_dlp
import os

API_TOKEN = os.getenv("API_TOKEN")  # التوكن من Environment Variables

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '/tmp/video.%(ext)s',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

@dp.message_handler()
async def send_video(message: types.Message):
    url = message.text.strip()
    if url.startswith("http"):
        await message.reply("⏳ جاري التحميل...")
        try:
            video_file = download_video(url)
            await message.reply_video(open(video_file, 'rb'))
        except Exception as e:
            await message.reply(f"❌ حدث خطأ: {e}")
    else:
        await message.reply("أرسل رابط فيديو صحيح.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
