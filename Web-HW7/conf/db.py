import configparser
import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf.models import Base

file_condig = pathlib.Path(__file__).parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_condig)

user = config.get("DEV_DB", "USER")
password = config.get("DEV_DB", "PASSWORD")
domain = config.get("DEV_DB", "DOMAIN")
port = config.get("DEV_DB", "PORT")
db = config.get("DEV_DB", "DB_NAME")

URI = f"postgresql://{user}:{password}@{domain}:{port}/{db}"

engine = create_engine(URI, echo=True, pool_size=5, max_overflow=0)

Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
