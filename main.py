import asyncio
import json
from pyrogram import Client
from pyrogram.errors import FloodWait
from conf import *

CACHE_FILE = "/data/cache.json"

app = Client(
    "minha_sessao",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

# ==============================
# Cache
# ==============================
async def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

async def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# ==============================
# Envio de mensagens
# ==============================
async def send(msg):
    try:
        if msg.text:
            await app.send_message(
                chat_id=DEST_CHAT,
                text=msg.text
            )
            print(f"➡️ Texto enviado: {msg.id}")

        elif msg.photo:
            await app.send_photo(
                chat_id=DEST_CHAT,
                photo=msg.photo.file_id,
                caption=msg.caption
            )
            print(f"➡️ Foto enviada: {msg.id}")

        elif msg.video:
            await app.send_video(
                chat_id=DEST_CHAT,
                video=msg.video.file_id,
                caption=msg.caption
            )
            print(f"➡️ Video enviado: {msg.id}")

        elif msg.document:
            await app.send_document(
                chat_id=DEST_CHAT,
                document=msg.document.file_id,
                caption=msg.caption
            )
            print(f"➡️ Documento enviado: {msg.id}")

        elif msg.audio:
            await app.send_audio(
                chat_id=DEST_CHAT,
                audio=msg.audio.file_id,
                caption=msg.caption
            )
            print(f"➡️ Audio enviado: {msg.id}")

        elif msg.voice:
            await app.send_voice(
                chat_id=DEST_CHAT,
                voice=msg.voice.file_id,
                caption=msg.caption
            )
            print(f"➡️ Voice enviado: {msg.id}")

        elif msg.sticker:
            await app.send_sticker(
                chat_id=DEST_CHAT,
                sticker=msg.sticker.file_id
            )
            print(f"➡️ Sticker enviado: {msg.id}")

        elif msg.animation:
            await app.send_animation(
                chat_id=DEST_CHAT,
                animation=msg.animation.file_id,
                caption=msg.caption
            )
            print(f"➡️ Animation enviado: {msg.id}")

        else:
            print(f"⚠️ Tipo não suportado: {msg.id}")

    except FloodWait as e:
        print(f"⏳ FloodWait {e.value}s msg {msg.id}")
        await asyncio.sleep(e.value)
        await send(msg)
    except Exception as e:
        print(f"❌ Erro msg {msg.id}: {e}")

# ==============================
# Main
# ==============================
async def main():
    print("🚀 Iniciando clonagem geral...")
    cache = await load_cache()
    total, sent = 0, 0

    async for msg in app.get_chat_history(ORIGIN_CHAT):
        total += 1
        if str(msg.id) in cache or msg.empty or msg.service:
            continue

        await send(msg)
        cache[str(msg.id)] = True
        await save_cache(cache)
        sent += 1
        await asyncio.sleep(DELAY)

    print(f"🎉 Clonagem finalizada! Total: {total}, Enviadas: {sent}")

async def run():
    async with app:
        await main()

if __name__ == "__main__":
    asyncio.run(run())
