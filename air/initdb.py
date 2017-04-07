#from app import db
#db.create_all()
from models import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("postgresql+psycopg2://leo:password@localhost:5432/flask_air")
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
metadata = MetaData(bind=engine)
