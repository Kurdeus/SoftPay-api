from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.domain.service import do_encoding, get_price, get_expire_date, time_encoding
from app.irgateways import NextPayClient
from app.schemas.Request_MetaData import BuyRequest, CheckRequest, VerifyRequest
from app import get_db_session, CALLBACK_URL
from app.models import NextPayItemModel

router = APIRouter(tags=["Pay Products"])

@router.post("/api/buy", description="buy product and get url")
async def buy_product(data: BuyRequest, db: Annotated[Session, Depends(get_db_session)]) -> dict:
    if data.gateway == "NEXTPAY":
        client = NextPayClient()
        item = NextPayItemModel()
        db.add(item)
        db.commit()
        db.refresh(item)
        amount = await get_price(data.product_id, data.license_period, db)
        order_id = await do_encoding(item.id)
        expire_date = await get_expire_date(data.license_period)
        response = await client.create_url(
            amount=amount, 
            order_id=order_id, 
            callback_url=CALLBACK_URL, 
            currency="IRR",
        )
        item.order_id = order_id
        item.trans_id = response.trans_id
        item.currency = "IRR"
        item.amount = amount
        item.callback_url = CALLBACK_URL
        item.systm_token = data.system_token
        item.product_version = data.product_version
        item.product_id = data.product_id
        item.expire_date = expire_date
        item.status = "pending"
        db.commit()
        return response
    else:
        raise HTTPException(status_code=400, detail="Gateway not found")

@router.post("/api/check", description="check product")
async def check_product(data: CheckRequest, db: Annotated[Session, Depends(get_db_session)]) -> dict:
    query = db.query(NextPayItemModel).filter(NextPayItemModel.systm_token == data.system_token)
    query = query.filter(NextPayItemModel.product_id == data.product_id)
    query = query.filter(NextPayItemModel.status == "paid")
    query = query.filter(NextPayItemModel.expire_date > datetime.now())
    item = query.first()
    if item is None:
        raise HTTPException(status_code=400, detail="not found")
    else:
        time_diff = await time_encoding()
        return {
            "extra-hash": time_diff
        }

@router.post("/api/verify", description="verify payment")
async def post_verify_product(data: VerifyRequest, db: Annotated[Session, Depends(get_db_session)]) -> dict:
    if data.gateway == "NEXTPAY":
        query = db.query(NextPayItemModel).filter(NextPayItemModel.trans_id == data.trans_id)
        item = query.first()
        if item is None:
            raise HTTPException(status_code=400, detail="item not found")
        client = NextPayClient()
        response = await client.verify(trans_id=data.trans_id, amount=data.amount, currency="IRR")
        if response.code != 0:
            raise HTTPException(status_code=400, detail="payment failed.")
        item.status = "paid"
        item.card_holder = response.card_holder
        item.customer_phone = response.customer_phone
        item.shaparak_ref_id = response.shaparak_ref_id
        item.custom = str(response.custom)
        item.created_at = response.created_at
        db.commit()
        
        time_diff = await time_encoding()
        return {
            "extra-hash": time_diff
        }
    else:
        raise HTTPException(status_code=400, detail="Gateway not found")
    


@router.get("/api/verify/{amount}/{gateway}/{trans_id}/", description="verify payment")
async def get_verify_product(amount:int, gateway:str, trans_id:str, db: Annotated[Session, Depends(get_db_session)]) -> dict:
    if gateway == "NEXTPAY":
        query = db.query(NextPayItemModel).filter(NextPayItemModel.trans_id == trans_id)
        item = query.first()
        if item is None:
            raise HTTPException(status_code=400, detail="item not found")
        client = NextPayClient()
        response = await client.verify(trans_id=trans_id, amount=amount, currency="IRR")
        if response.code != 0:
            raise HTTPException(status_code=400, detail="payment failed.")
        item.status = "paid"
        item.card_holder = response.card_holder
        item.customer_phone = response.customer_phone
        item.shaparak_ref_id = response.shaparak_ref_id
        item.custom = str(response.custom)
        item.created_at = response.created_at
        db.commit()
        
        time_diff = await time_encoding()
        return {
            "extra-hash": time_diff
        }
    else:
        raise HTTPException(status_code=400, detail="Gateway not found")
    