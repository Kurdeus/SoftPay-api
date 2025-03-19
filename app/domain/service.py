import base64
from datetime import timedelta, datetime
import random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.Request_MetaData import License_Period
from app.models import ProductModel
import base64
from datetime import datetime, timedelta
import random
import time
import pytz



async def time_encoding():
    time_string = datetime.now(pytz.timezone('Asia/Tehran')).time().isoformat().split(".")[0]
    convert_case = lambda s: ''.join([c.lower() if c.isupper() else c.upper() for c in s])
    params = time_string.split(":")
    data = []
    random_numbers = random.randint(1, 100)
    for item in params:
        for char in item:
            data.append(hex(int(char) * random_numbers)[2:])
    text = "-".join(data)[::-1]
    raw_text = base64.b64encode(text.encode()).decode().replace("=", "")
    base64_text = convert_case(raw_text)
    encoded = "-".join([hex(ord(c))[2:][::-1] for c in str(base64_text)])[::-1]
    final_text = "{}-{}".format(random_numbers, encoded)
    return final_text









async def time_decoding(dec_string:str):
    convert_case = lambda s: ''.join([c.lower() if c.isupper() else c.upper() for c in s])
    data = dec_string.split("-")
    random_numbers = int(data[0])
    encoded = "-".join(data[1:])[::-1].split('-')
    p = "".join([chr(int(item[::-1], 16)) for item in encoded])
    case_text = convert_case(p) + "=="
    base64_text = base64.b64decode(case_text.encode()).decode()[::-1]
    rt = "".join([str(int(item, 16)//random_numbers) for item in base64_text.split("-")])
    chunks = [rt[i:i + 2] for i in range(0, len(rt), 2)]
    original_text = ':'.join(chunk for chunk in chunks)
    time_obj = datetime.strptime(original_text, "%H:%M:%S")
    current_time = datetime.now(pytz.timezone('Asia/Tehran'))
    # Convert time_obj to a datetime object for subtraction and make it timezone-aware
    time_obj = datetime.combine(current_time.date(), time_obj.time())
    time_obj = pytz.timezone('Asia/Tehran').localize(time_obj)
    return  (current_time - time_obj).seconds




async def do_encoding(number:int):
    first_number = random.randint(3,9)
    encoded = str(first_number) + "".join([str(ord(c)) for c in str(number)])[::-1]
    response = hex(int(encoded) * first_number)[2:][::-1]
    base64_encoded = base64.b64encode(response.encode()).decode().replace("=", "")[::-1]
    return  str(first_number) + base64_encoded




async def undo_encoding(encoded_text:str):
    first_number = int(encoded_text[0])
    reversed_hex = base64.b64decode(encoded_text[1:][::-1] + "==").decode()[::-1]
    number = int(reversed_hex, 16) // first_number
    reversed_string = str(number)[1:][::-1]
    chunks = [reversed_string[i:i + 2] for i in range(0, len(reversed_string), 2)]
    original_text = ''.join(chr(int(chunk)) for chunk in chunks)
    return original_text


async def get_price(product_id:int, license_period: License_Period, db: Session):
    product = db.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if license_period.one_month == "one_month":
        return product.one_month_price
    elif license_period.three_month == "three_month":
        return product.three_month_price
    elif license_period.six_month == "six_month":
        return product.six_month_price
    else:
        raise HTTPException(status_code=404, detail="License period not found")
    


async def get_expire_date(license_period: License_Period):
    if license_period.one_month == "one_month":
        return datetime.now() + timedelta(days=30)
    elif license_period.three_month == "three_month":
        return datetime.now() + timedelta(days=90)
    elif license_period.six_month == "six_month":
        return datetime.now() + timedelta(days=180)
    else:
        return datetime.now()