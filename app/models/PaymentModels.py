from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from app import Base


class PaymentItemModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    systm_token = Column(String, nullable=True)
    status = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow)
    expire_date = Column(DateTime, nullable=True)
    product_id = Column(Integer, nullable=True)
    product_version = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    currency = Column(String, nullable=True)
    callback_url = Column(String, nullable=True)
    
    




class NextPayItemModel(PaymentItemModel):
    __tablename__ = 'nextpay_history_table'
    order_id = Column(String, nullable=True)
    trans_id = Column(String, nullable=True)
    card_holder = Column(String, nullable=True)
    customer_phone = Column(Integer, nullable=True)
    shaparak_ref_id = Column(String, nullable=True)
    custom = Column(String, nullable=True)
    created_at = Column(String, nullable=True)