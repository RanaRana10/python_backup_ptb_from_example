from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

db_location = "bot_data_store_2.db"
engine = create_engine(f"sqlite+pysqlite:///{db_location}", echo= False)

Base = declarative_base()


class Sticker(Base):
    __tablename__ = "sticker_store"

    id_ = Column(Integer, primary_key= True)
    file_unique_id_ = Column(String)
    file_id_ = Column(String)
    set_name_ = Column(String)

    user_id_ = Column(Integer)
    user_name_ = Column(String)
    time_of_saved_ = Column(String)
    column_1_ = Column(String)
    column_2_ = Column(String)

    def __init__(self, file_unique_id_:str, file_id_:str, set_name_:str, user_id_:int, user_name_:str, time_of_saved_:str, column_1_:str, column_2_:str):
        self.file_unique_id_ = file_unique_id_
        self.file_id_ = file_id_
        self.set_name_ = set_name_
        self.user_id_ = user_id_
        self.user_name_ = user_name_
        self.time_of_saved_ = time_of_saved_
        self.column_1_ = column_1_
        self.column_2_ = column_2_

    def __repr__(self):
        f"This is the Table of sticker store"



Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()


def add_sticker_and_return_id(
                            file_unique_id_:str = None, 
                            file_id_:str = None, 
                            set_name_:str = None, 
                            user_id_:str = None, 
                            user_name_:str = None, 
                            time_of_saved_:str = None, 
                            column_1_:str = None, 
                            column_2_:str = None
                            ):
    try:
        sticker_obj = Sticker(
            file_unique_id_= file_unique_id_,
            file_id_= file_id_,
            set_name_= set_name_,
            user_id_= user_id_,
            user_name_= user_name_,
            time_of_saved_= time_of_saved_,
            column_1_= column_1_,
            column_2_= column_2_
        )
        session.add(sticker_obj)
        session.commit()
        return sticker_obj.id_
    
    except Exception as e:
        print(f"This error occured\n{e}")
        session.rollback() 
        return None 



def get_sticker_by_id_1(id_: int = 1):
    '''This use to search around the database to find the information regarding the given id_
     column'''
    sticker_obj = session.query(Sticker).filter(Sticker.id_ == id_).first()
    if sticker_obj:
        return sticker_obj.file_id_, sticker_obj.file_unique_id_



def get_sticker_by_id(id_: int = 1) :
    '''This function searches the database to find the information regarding the given id_ column\nThis returns a dictionary'''
    sticker_obj = session.query(Sticker).filter(Sticker.id_ == id_).first()
    if sticker_obj:
        sticker_info = {
            "file_id_": sticker_obj.file_id_,
            "file_unique_id_": sticker_obj.file_unique_id_,
            "set_name_": sticker_obj.set_name_,
            "user_id_": sticker_obj.user_id_,
            "user_name_": sticker_obj.user_name_,
            "time_of_saved_": sticker_obj.time_of_saved_,
            "column_1_": sticker_obj.column_1_,
            "column_2_": sticker_obj.column_2_
        }
        return sticker_info
    else:
        return None






if __name__ == "__main__":

    new_sticker_id = add_sticker_and_return_id(
        file_unique_id_="unique123",
        file_id_="file456",
        set_name_="MyStickerSet",
        user_id_=123,
        user_name_="user123",
        time_of_saved_="2024-03-28",
        column_1_="Extra Column 1",
        column_2_="Extra Column 2"
    )
    print("New Sticker ID:", new_sticker_id)


    sticker_info_dict = get_sticker_by_id(5)
    if sticker_info_dict:
        print(sticker_info_dict["file_id_"], sticker_info_dict["set_name_"])

