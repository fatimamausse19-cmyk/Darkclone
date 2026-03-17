import asyncio
import json
import os
from pyrogram import Client
from pyrogram.errors import FloodWait
from conf import *

CACHE_FILE = "/data/cache.json"


# ==============================
# CLIENTE
# ==============================
app = Client(
    "minha_sessao",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
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
# ENVIO ASYNC COM DEBUG
# ==============================
async def send(msg):
    try:
        if msg.text:
            await app.send_message(
                DEST_CHAT,
                msg.text,
                message_thread_id=DEST_THREAD_ID
            )
            print(f"➡️ Texto enviado: msg {msg.id}")

        elif msg.photo:
            await app.send_photo(
                DEST_CHAT,
                msg.photo.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
            print(f"➡️ Foto enviada: msg {msg.id}")

        elif msg.video:
            await app.send_video(
                DEST_CHAT,
                msg.video.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
            print(f"➡️ Video enviado: msg {msg.id}")

        elif msg.document:
            await app.send_document(
                DEST_CHAT,
                msg.document.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
            print(f"➡️ Documento enviado: msg {msg.id}")

        else:
            print(f"⚠️ Tipo não suportado, msg {msg.id}")

    except FloodWait as e:
        print(f"⏳ FloodWait {e.value}s - msg {msg.id}")
        await asyncio.sleep(e.value)
        await send(msg)

    except Exception as e:
        print(f"❌ Erro msg {msg.id}: {e}")


# ==============================
# DEBUG: MOSTRAR MENSAGENS
# ==============================
async def main():
    print("🚀 Iniciando clonagem async (debug)...")
    cache = await load_cache()

    count_total = 0
    count_sent = 0
    async for msg in app.get_chat_history(ORIGIN_CHAT):
        count_total += 1
        print(f"🔹 Encontrada msg {msg.id} tipo: {type(msg)}")

        if str(msg.id) in cache:
            print(f"⏭️ Pulando msg {msg.id} (já no cache)")
            continue

        if msg.empty or msg.service:
            print(f"⏭️ Pulando msg {msg.id} (vazia ou serviço)")
            continue

        await send(msg)
        cache[str(msg.id)] = True
        await save_cache(cache)
        count_sent += 1
        await asyncio.sleep(DELAY)

    print(f"🎉 Clonagem finalizada! Total mensagens: {count_total}, enviadas: {count_sent}")


# ==============================
# EXECUÇÃO
# ==============================
async def run():
    async with app:
        await main()


if __name__ == "__main__":
    asyncio.run(run())
