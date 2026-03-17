import os
import time
import json
from pyrogram import Client
from pyrogram.errors import FloodWait

# ==============================
# Configuração via Variáveis de Ambiente
# ==============================
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

# ID do chat de origem e destino
ORIGIN_CHAT = int(os.environ["ORIGIN_CHAT"])
DEST_CHAT = int(os.environ["DEST_CHAT"])

# ID do tópico de destino (mensagens vão para esse tópico)
DEST_THREAD_ID = int(os.environ["DEST_THREAD_ID"])

# Delay entre mensagens em segundos (ajuste se der FloodWait)
DELAY = float(os.environ.get("DELAY", 1.0))

# Caminho do cache no Railway (persistente)
CACHE_FILE = "/data/cache.json"

# ==============================
# Inicializa Pyrogram com conta normal
# ==============================
app = Client("user", api_id=API_ID, api_hash=API_HASH)

# ==============================
# Funções de Cache
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
# Função para enviar mensagem
# ==============================
def send_message(msg):
    try:
        if msg.text:
            app.send_message(
                chat_id=DEST_CHAT,
                text=msg.text,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.photo:
            app.send_photo(
                chat_id=DEST_CHAT,
                photo=msg.photo.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.video:
            app.send_video(
                chat_id=DEST_CHAT,
                video=msg.video.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.document:
            app.send_document(
                chat_id=DEST_CHAT,
                document=msg.document.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.sticker:
            app.send_sticker(
                chat_id=DEST_CHAT,
                sticker=msg.sticker.file_id,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.animation:
            app.send_animation(
                chat_id=DEST_CHAT,
                animation=msg.animation.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.audio:
            app.send_audio(
                chat_id=DEST_CHAT,
                audio=msg.audio.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.voice:
            app.send_voice(
                chat_id=DEST_CHAT,
                voice=msg.voice.file_id,
                caption=msg.caption,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.video_note:
            app.send_video_note(
                chat_id=DEST_CHAT,
                video_note=msg.video_note.file_id,
                message_thread_id=DEST_THREAD_ID
            )
        elif msg.poll and msg.poll.type == "regular":
            app.send_poll(
                chat_id=DEST_CHAT,
                question=msg.poll.question,
                options=[opt.text for opt in msg.poll.options],
                is_anonymous=msg.poll.is_anonymous,
                allows_multiple_answers=msg.poll.allows_multiple_answers,
                message_thread_id=DEST_THREAD_ID
            )
    except FloodWait as e:
        print(f"FloodWait {e.value}s")
        time.sleep(e.value)
        send_message(msg)
    except Exception as e:
        print(f"Erro ao enviar {msg.id}: {e}")

# ==============================
# Main: Clonar chat
# ==============================
with app:
    posted = load_cache()

    print(f"Iniciando clonagem de {ORIGIN_CHAT} para {DEST_CHAT}, tópico {DEST_THREAD_ID}")
    
    for msg in app.get_chat_history(ORIGIN_CHAT):
        if str(msg.id) in posted:
            continue
        if msg.empty or msg.service or msg.dice or msg.location:
            continue

        send_message(msg)
        posted[str(msg.id)] = True
        save_cache(posted)

        print(f"Clonado: {msg.id}")
        time.sleep(DELAY)

    print("Clonagem finalizada com sucesso!")
