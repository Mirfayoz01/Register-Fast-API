import random
import requests
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from starlette.responses import HTMLResponse
from database import Base, engine, get_db, db_conf
from models import User
from schemas import RegisterRequest, VerifyRequest, ResponseMessage
# from crud import create_user, verify_user

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

codes = {}

BOT_TOKEN = "7360891386:AAEF-0VE2YUHPRKZq0i_PGNDvNMtzix1z6I"
BOT_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse("Hi I'm Mirfayoz!")




@app.post("/register")
def register_user(req: RegisterRequest, db: Session = Depends(get_db)):
    code = "".join([str(random.randint(0, 9)) for _ in range(6)])

    user = db.query(User).filter(User.telegram_id == req.telegram_id).first()

    if user:
        user.full_name = req.full_name
        user.verification_code = code
        user.is_verified = False
    else:
        user = User(
            telegram_id=req.telegram_id,
            phone_number=req.phone_number,
            verification_code=code,
            is_verified=False
        )
        db.add(user)

    db.commit()

    payload = {
        "chat_id": req.telegram_id,
        "text": f"Salom, {req.full_name}!\nTasdiqlash kodi: {code}"
    }

    response = requests.post(BOT_API, data=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Kod yuborib bo'lmadi")

    return {"detail": "Kod yuborildi. Iltimos, tekshiruvdan o‘ting."}



# @app.get("/search_verifications/{id}")
# def verification_code(telegram_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.telegram_id == telegram_id).first()
#
#     if not user or not user.verification_code:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Foydalanuvchi yoki verify kodi notogri"
#         )
#
#     from datetime import datetime
#     if datetime.now() > user.expires_at:
#         return {
#             "verification_code": "",
#             "message": "verify kodining vaqti tugagan"
#         }
#
#     return {
#         "verification_code": user.verification_code,
#         "expires_at": user.expires_at
#     }


@app.post("/verify-code")
def verify_code(req: VerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_code == req.code).first()

    if not user:
        raise HTTPException(status_code=404, detail="Kod topilmadi.")

    user.is_verified = True
    user.verification_code = None
    user.expires_at = None
    db.commit()

    return {"detail": "Tasdiqlash muvaffaqiyatli!"}
