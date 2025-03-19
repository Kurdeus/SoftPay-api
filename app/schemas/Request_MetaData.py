from pydantic import BaseModel
from typing import Union, Optional, List, Any
from enum import Enum




class Gateway(Enum):
    NextPay = "NEXTPAY"


class License_Period(Enum):
    one_month = "one_month"
    three_month = "three_month"
    six_month = "six_month"



    

class BuyRequest(BaseModel):
    gateway: Gateway
    product_id: str
    system_token: str
    license_period: License_Period
    product_version : str
    


class CheckRequest(BaseModel):
    product_id: str
    system_token: str
    


class VerifyRequest(BaseModel):
    trans_id: str
    gateway: Gateway
    amount: int