import time
import json
import os

from pyrogram import Client
from pyrogram.errors import FloodWait
from conf import *

CACHE_FILE = "/data/cache.json"

# ==============================
# CLIENT
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
def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# ==============================
# SEND
# ==============================
def send(msg):
    try:
        if msg.text:
            app.send_message(DEST_CHAT, msg.text, message_thread_id=DEST_THREAD_ID)

        elif msg.photo:
            app.send_photo(DEST_CHAT, msg.photo.file_id, caption=msg.caption, message_thread_id=DEST_THREAD_ID)

        elif msg.video:
            app.send_video(DEST_CHAT, msg.video.file_id, caption=msg.caption, message_thread_id=DEST_THREAD_ID)

        elif msg.document:
            app.send_document(DEST_CHAT, msg.document.file_id, caption=msg.caption, message_thread_id=DEST_THREAD_ID)

    except FloodWait as e:
        print(f"⏳ FloodWait {e.value}s - msg {msg.id}")
        time.sleep(e.value)
        send(msg)

    except Exception as e:
        print(f"❌ Erro msg {msg.id}: {e}")

# ==============================
# MAIN
# ==============================
with app:
    print("🚀 Iniciando clonagem...")
    cache = load_cache()
    for msg in app.get_chat_history(ORIGIN_CHAT):
        if str(msg.id) in cache:
            continue
        if msg.empty or msg.service:
            continue

        send(msg)
        cache[str(msg.id)] = True
        save_cache(cache)
        print(f"✅ Clonado msg {msg.id}")
        time.sleep(DELAY)

    print("🎉 Clonagem finalizada!")
