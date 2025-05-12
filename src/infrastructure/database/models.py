import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from urllib.parse import urlparse

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    url = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Float)
    currency = Column(String)
    full_price = Column(Float)
    on_sale = Column(String)
    has_member_price = Column(String)
    member_price = Column(Float)
    check_date = Column(String)
    main_image_url = Column(String)


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True)
    product_url = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)
    product_name = Column(String)