import os

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]

ORIGIN_CHAT = int(os.environ["ORIGIN_CHAT"])
DEST_CHAT = int(os.environ["DEST_CHAT"])
DEST_THREAD_ID = int(os.environ["DEST_THREAD_ID"])

DELAY = float(os.environ.get("DELAY", 1))
