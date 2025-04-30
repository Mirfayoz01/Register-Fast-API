from datetime import datetime, timedelta
from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Nullable, func, BigInteger
# from config import VERIFICATION_CODE_EXPIRY_MINUTES

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    phone_number = Column(String, index=True)
    verification_code = Column(String)
    expires_at = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
