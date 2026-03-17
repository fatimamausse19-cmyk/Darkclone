import os
import time
import json
import pyrogram
from pyrogram import Client, StringSession
from pyrogram.errors import FloodWait

# ==============================
# CONFIG (Railway ENV)
# ==============================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]

ORIGIN_CHAT = int(os.environ["ORIGIN_CHAT"])
DEST_CHAT = int(os.environ["DEST_CHAT"])
DEST_THREAD_ID = int(os.environ["DEST_THREAD_ID"])

DELAY = float(os.environ.get("DELAY", 1.0))

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
# SEND MESSAGE
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

        elif msg.audio:
            app.send_audio(
                DEST_CHAT,
                msg.audio.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.voice:
            app.send_voice(
                DEST_CHAT,
                msg.voice.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.animation:
            app.send_animation(
                DEST_CHAT,
                msg.animation.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.sticker:
            app.send_sticker(
                DEST_CHAT,
                msg.sticker.file_id,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.video_note:
            app.send_video_note(
                DEST_CHAT,
                msg.video_note.file_id,
                message_thread_id=DEST_THREAD_ID
            )

        elif msg.poll and msg.poll.type == "regular":
            app.send_poll(
                DEST_CHAT,
                question=msg.poll.question,
                options=[opt.text for opt in msg.poll.options],
                is_anonymous=msg.poll.is_anonymous,
                allows_multiple_answers=msg.poll.allows_multiple_answers,
                message_thread_id=DEST_THREAD_ID
            )

    except FloodWait as e:
        print(f"⏳ FloodWait {e.value}s")
        time.sleep(e.value)
        send(msg)

    except Exception as e:
        print(f"❌ Erro na msg {msg.id}: {e}")

# ==============================
# MAIN
# ==============================
with app:
    print("🚀 Iniciando clonagem...")

    posted = load_cache()

    for msg in app.get_chat_history(ORIGIN_CHAT):

        if str(msg.id) in posted:
            continue

        if msg.empty or msg.service or msg.dice or msg.location:
            continue

        send(msg)

        posted[str(msg.id)] = True
        save_cache(posted)

        print(f"✅ Clonado: {msg.id}")

        time.sleep(DELAY)

    print("🎉 Clonagem finalizada!")
