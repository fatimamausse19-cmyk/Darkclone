import os

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
STRING_SESSION = os.environ["STRING_SESSION"]

ORIGIN_CHAT = int(os.environ["ORIGIN_CHAT"])  # Canal ou grupo de origem
DEST_CHAT = int(os.environ["DEST_CHAT"])      # Canal ou grupo de destino

DELAY = float(os.environ.get("DELAY", 1))  # Delay entre envios em segundos
