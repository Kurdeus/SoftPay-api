from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from app import Base


class ProductModel(Base):
    __tablename__ = 'product_table'
    id = Column(Integer, primary_key=True)
    product_id = Column(String, nullable=True)
    product_name = Column(String, nullable=True)
    product_description = Column(String, nullable=True)
    product_version = Column(String, nullable=True)
    one_month_price = Column(Integer, nullable=True)
    three_month_price = Column(Integer, nullable=True)
    six_month_price = Column(Integer, nullable=True)
    
    



