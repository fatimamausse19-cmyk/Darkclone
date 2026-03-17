import time
import json
import os

from pyrogram import Client
from pyrogram.errors import FloodWait

# Importa as tuas variáveis do ficheiro conf.py
from conf import *

CACHE_FILE = "/data/cache.json"

# ==============================
# CLIENT (CORRIGIDO)
# ==============================
app = Client(
    "minha_sessao",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION  # O parâmetro correto é este
)

# ==============================
# SEND (CORRIGIDO PARA ASYNC)
# ==============================
async def send_msg(msg): # Mudei o nome para não conflitar com bibliotecas nativas
    try:
        # No Pyrogram moderno, usamos await antes de enviar
        if msg.text:
            await app.send_message(
                DEST_CHAT,
                msg.text,
                message_thread_id=DEST_THREAD_ID
            )
        # ... repita o 'await' para app.send_photo, send_video, etc.
        elif msg.photo:
            await app.send_photo(
                DEST_CHAT,
                msg.photo.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
        # Adicione o 'await' nos outros (video, document) igual acima

    except FloodWait as e:
        print(f"⏳ FloodWait {e.value}s")
        time.sleep(e.value)
        await send_msg(msg) # await aqui também

    except Exception as e:
        print(f"❌ Erro {msg.id}: {e}")

# ==============================
# MAIN (CORRIGIDO PARA ASYNC)
# ==============================
async def main():
    async with app:
        print("🚀 Iniciando...")
        cache = load_cache()

        # O iterador de histórico também é assíncrono
        async for msg in app.get_chat_history(ORIGIN_CHAT):
            if str(msg.id) in cache:
                continue
            if msg.empty or msg.service:
                continue

            await send_msg(msg)

            cache[str(msg.id)] = True
            save_cache(cache)
            print(f"✅ {msg.id}")
            time.sleep(DELAY)

        print("🎉 Finalizado")

# Executa o loop principal
app.run(main())
