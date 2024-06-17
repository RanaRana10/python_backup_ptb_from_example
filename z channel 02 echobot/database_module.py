from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


db_location = "bot_data_store.db"
engine = create_engine(f"sqlite+pysqlite:///{db_location}", echo= False)

Base = declarative_base()

class Sticker(Base):
    __tablename__ = "sticker_store"

    id = Column(Integer, primary_key= True)
    file_id = Column(String)
    unique_id = Column(String)
    size = Column(Integer)
    user_id = Column(Integer)
    user_name = Column(String)

    def __init__(self, file_id:str, unique_id:str, user_id:int, user_name:str,size:int = 999):
        self.file_id = file_id
        self.unique_id = unique_id

        self.user_id = user_id
        self.user_name = user_name
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind= engine)
session = Session()


def add_sticker(file_id:str, unique_id:str, user_id: int = None, user_name:str = None):

    sticker_obj = Sticker(file_id= file_id, unique_id= unique_id, user_id= user_id, user_name= user_name)
    session.add(sticker_obj)
    session.commit()

def add_sticker_and_return(file_id: str, unique_id: str, user_id: int = None, user_name: str = None, size:int = 998):
    try:
        sticker_obj = Sticker(file_id=file_id, unique_id=unique_id, user_id=user_id, user_name=user_name, size= 99)
        session.add(sticker_obj)
        session.commit()

        return sticker_obj.id, sticker_obj.file_id, sticker_obj.user_id
    
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback changes if an error occurred
        return None  # Return None if insertion failed


def get_sticker_by_id(id:int = 1):
    sticker_obj = session.query(Sticker).filter(Sticker.id == id).first()
    if sticker_obj:
        return sticker_obj.file_id
    else:
        return None



if __name__ == "__main__":

    # add_document("This is Title for 1", "BQACAgUAAxkBAAJB02X_7YwVBbxHIWHJQIdx8KIlsxYEAAIOCwACrPOIVjRgtjeGLAAB-TQE")
    # add_sticker("Hello", "uni", 79, "@ok")
    print(add_sticker_and_return("hklj", "klj"))
    # print(get_sticker_by_id(98))
