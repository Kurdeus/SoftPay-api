import logging
import os, time
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s ', 
                    level=logging.ERROR)
LOGGER = logging.getLogger(__name__)









load_dotenv('config.env')
getConfig = lambda name: os.environ[name]



DATABASE_URL = getConfig('DATABASE_URL')
NP_API_KEY = getConfig('NP_API_KEY')
MERCHANT_ID = getConfig('MERCHANT_ID')
CALLBACK_URL = getConfig('CALLBACK_URL')
START_TIME = time.time()


# Create an engine and Create a base class for ORM models
engine = create_engine(DATABASE_URL)
Base = declarative_base()
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)




def get_db_session():
    with local_session() as session:
        yield session
