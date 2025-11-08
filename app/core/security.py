import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("JWT_SECRET")
ALGO = os.getenv("JWT_ALGORITHM")

def create_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGO)
    return token
