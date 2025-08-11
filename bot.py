import os
import tempfile
from aiogram import Bot, Dispatcher, executor, types
from pytube import YouTube

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not found. Please set BOT_TOKEN in your environment variables.")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

MAX_FILESIZE = 50 * 1024 * 1024  # 50 MB

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Hi! Send me a YouTube link and I'll download the video for you.")

@dp.message_handler()
async def handle_message(message: types.Message):
    url = message.text.strip()
    if not ("youtube.com" in url or "youtu.be" in url):
        await message.answer("Please send a valid YouTube link.")
        return

    status = await message.answer("Downloading video, please wait...")

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not stream:
            await status.edit_text("No suitable stream found for download.")
            return

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp_path = tmp.name
        stream.download(output_path=os.path.dirname(tmp_path), filename=os.path.basename(tmp_path))

        if os.path.getsize(tmp_path) > MAX_FILESIZE:
            await status.edit_text("File is too large for Telegram (over 50 MB).")
            return

        await message.answer_video(open(tmp_path, "rb"), caption=yt.title)
        await status.delete()
        os.remove(tmp_path)

    except Exception as e:
        await status.edit_text(f"Error: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
