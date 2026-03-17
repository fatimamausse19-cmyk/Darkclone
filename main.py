import asyncio
import json
import os
from pyrogram import Client, StringSession
from pyrogram.errors import FloodWait
from conf import *

CACHE_FILE = "/data/cache.json"

# ==============================
# CLIENT ASYNC
# ==============================
app = Client(
    StringSession(STRING_SESSION),
    api_id=API_ID,
    api_hash=API_HASH
)

# ==============================
# CACHE
# ==============================
async def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

async def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# ==============================
# ENVIO DE MENSAGEM (async)
# ==============================
async def send(msg):
    try:
        if msg.text:
            await app.send_message(
                DEST_CHAT,
                msg.text,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.photo:
            await app.send_photo(
                DEST_CHAT,
                msg.photo.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.video:
            await app.send_video(
                DEST_CHAT,
                msg.video.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.document:
            await app.send_document(
                DEST_CHAT,
                msg.document.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

    except FloodWait as e:
        print(f"⏳ FloodWait {e.value}s - msg {msg.id}")
        await asyncio.sleep(e.value)
        await send(msg)

    except Exception as e:
        print(f"❌ Erro msg {msg.id}: {e}")

# ==============================
# MAIN LOOP ASYNC
# ==============================
async def main():
    print("🚀 Iniciando clonagem async...")

    cache = await load_cache()

    async for msg in app.get_chat_history(ORIGIN_CHAT):
        if str(msg.id) in cache:
            continue
        if msg.empty or msg.service:
            continue

        await send(msg)
        cache[str(msg.id)] = True
        await save_cache(cache)
        print(f"✅ Clonado msg {msg.id}")
        await asyncio.sleep(DELAY)

    print("🎉 Clonagem finalizada!")

# ==============================
# RUN
# ==============================
async def run():
    async with app:
        await main()

if __name__ == "__main__":
    asyncio.run(run())
