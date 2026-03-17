import os
import time
import json
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.session import StringSession

# ==============================
# CONFIG
# ==============================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]

ORIGIN_CHAT = int(os.environ["ORIGIN_CHAT"])
DEST_CHAT = int(os.environ["DEST_CHAT"])
DEST_THREAD_ID = int(os.environ["DEST_THREAD_ID"])

DELAY = float(os.environ.get("DELAY", 1))

CACHE_FILE = "/data/cache.json"

# ==============================
# CLIENT
# ==============================
app = Client(
    StringSession(STRING_SESSION),
    api_id=API_ID,
    api_hash=API_HASH
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
            app.send_message(
                DEST_CHAT,
                msg.text,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.photo:
            app.send_photo(
                DEST_CHAT,
                msg.photo.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.video:
            app.send_video(
                DEST_CHAT,
                msg.video.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.document:
            app.send_document(
                DEST_CHAT,
                msg.document.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

    except FloodWait as e:
        print(f"FloodWait {e.value}s")
        time.sleep(e.value)
        send(msg)

    except Exception as e:
        print("Erro:", e)

# ==============================
# MAIN
# ==============================
with app:
    posted = load_cache()

    print("🚀 Iniciando clonagem...")

    for msg in app.get_chat_history(ORIGIN_CHAT):

        if str(msg.id) in posted:
            continue

        if msg.empty or msg.service:
            continue

        send(msg)

        posted[str(msg.id)] = True
        save_cache(posted)

        print(f"Clonado: {msg.id}")
        time.sleep(DELAY)

    print("✅ Finalizado")
