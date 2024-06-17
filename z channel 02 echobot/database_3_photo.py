from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import update
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime



db_location = "bot_data_store_2.db"
engine = create_engine(f"sqlite+pysqlite:///{db_location}", echo= False)

Base = declarative_base()


class Photo(Base):
    __tablename__ = "photos_store"

    id_ = Column(Integer, primary_key= True)
    file_unique_id_ = Column(String)
    file_id_ = Column(String)
    file_size_ = Column(Integer)

    user_id_ = Column(Integer)
    user_name_ = Column(String)
    time_of_saved_ = Column(String)
    column_1_ = Column(String)
    column_2_ = Column(String)

    def __init__(self, file_unique_id_:str, file_id_:str, file_size_:int, user_id_:int, user_name_:str, time_of_saved_:str, column_1_:str, column_2_:str):
        self.file_unique_id_ = file_unique_id_
        self.file_id_ = file_id_
        self.file_size_ = file_size_
        self.user_id_ = user_id_
        self.user_name_ = user_name_
        self.time_of_saved_ = time_of_saved_
        self.column_1_ = column_1_
        self.column_2_ = column_2_

    def __repr__(self):
        f"This is the Table of photo store"



Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()


def add_photo_and_return_id(
                            file_unique_id_:str = None, 
                            file_id_:str = None, 
                            file_size_:int = None, 
                            user_id_:str = None, 
                            user_name_:str = None, 
                            time_of_saved_:str = None, 
                            column_1_:str = None, 
                            column_2_:str = None
                            ):
    '''This take some rows value and after insert this returns the id_ value or None if not successful'''
    try:
        photo_obj = Photo(
            file_unique_id_= file_unique_id_,
            file_id_= file_id_,
            file_size_= file_size_,
            user_id_= user_id_,
            user_name_= user_name_,
            time_of_saved_= time_of_saved_,
            column_1_= column_1_,
            column_2_= column_2_
        )
        session.add(photo_obj)
        session.commit()
        return photo_obj.id_
    
    except Exception as e:
        print(f"This error occured\n{e}")
        session.rollback() 
        return None 



def get_photo_by_id_1(id_: int = 1):
    '''This use to search around the database to find the information regarding the given id_
     column'''
    photo_obj = session.query(Photo).filter(Photo.id_ == id_).first()
    if photo_obj:
        return photo_obj.file_id_, photo_obj.file_unique_id_



def get_photo_by_id(id_: int = 1) :
    '''This function searches the database to find the information regarding the given id_ column\nThis returns a dictionary'''
    photo_obj = session.query(Photo).filter(Photo.id_ == id_).first()
    if photo_obj:
        photo_info = {
            "file_id_": photo_obj.file_id_,
            "file_unique_id_": photo_obj.file_unique_id_,
            "file_size_": photo_obj.file_size_,
            "user_id_": photo_obj.user_id_,
            "user_name_": photo_obj.user_name_,
            "time_of_saved_": photo_obj.time_of_saved_,
            "column_1_": photo_obj.column_1_,
            "column_2_": photo_obj.column_2_
        }
        return photo_info
    else:
        return None

def update_photo_user_id_1(old_user_id: int, new_user_id: int):
    try:
        stmt = (
            update(Photo)
            .where(Photo.user_id_ == old_user_id)
            .values(user_id_=new_user_id)
        )
        
        session.execute(stmt)
        session.commit()
        
        print(f"User ID {old_user_id} updated to {new_user_id} successfully.")
    except Exception as e:
        print(f"An error occurred while updating user ID: {e}")
        session.rollback()


def update_photo_user_id_2(old_user_id: int, new_user_id: int):
    try:
        check_stmt = session.query(Photo).filter(Photo.user_id_ == old_user_id).first()
        if check_stmt is None:
            print(f"No rows found with user ID {old_user_id}. No update performed.")
            return
        stmt = (
            update(Photo)
            .where(Photo.user_id_ == old_user_id)
            .values(user_id_=new_user_id)
        )
        
        session.execute(stmt)
        session.commit()
        
        print(f"User ID {old_user_id} updated to {new_user_id} successfully.")
    except Exception as e:
        print(f"An error occurred while updating user ID: {e}")
        session.rollback()





def update_photo_user_id_3(old_user_id: int, new_user_id: int):
    try:
        check_stmt = session.query(Photo).filter(Photo.user_id_ == old_user_id).first()
        if check_stmt is None:
            print(f"No rows found with user ID {old_user_id}. No update performed.")
            return
        
        new_column_1_value = int(check_stmt.column_1_) + 1 if check_stmt.column_1_ is not None else 1
        
        new_column_2_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        stmt = (
            update(Photo)
            .where(Photo.user_id_ == old_user_id)
            .values(user_id_=new_user_id, column_1_=new_column_1_value, column_2_=new_column_2_value)
        )
        
        session.execute(stmt)
        session.commit()
        
        print(f"User ID {old_user_id} updated to {new_user_id} successfully.")
    except Exception as e:
        print(f"An error occurred while updating user ID: {e}")
        session.rollback()




def update_photo_user_id(old_user_id: int, new_user_id: int):
    try:
        check_stmt = session.query(Photo).filter(Photo.user_id_ == old_user_id).first()
        if check_stmt is None:
            print(f"No rows found with user ID {old_user_id}. No update performed.")
            return None
        
        # Increment column_1_ if it's not None, otherwise set it to 1
        new_column_1_value = int(check_stmt.column_1_ )+ 1 if check_stmt.column_1_ is not None else 1
        
        # Get the current timestamp for column_2_
        new_column_2_value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        stmt = (
            update(Photo)
            .where(Photo.user_id_ == old_user_id)
            .values(user_id_=new_user_id, column_1_=str(new_column_1_value), column_2_=new_column_2_value)
            .returning(Photo.id_)  # Add returning clause to get the updated id_
        )
        
        result = session.execute(stmt)
        updated_ids = [row[0] for row in result.fetchall()]  # Get all updated id_ values

        session.commit()
        
        if updated_ids:
            print(f"User ID {old_user_id} updated to {new_user_id} successfully.")
            return updated_ids
        else:
            print("Failed to get updated IDs. Update may have failed.")
            return None

    except Exception as e:
        print(f"An error occurred while updating user ID: {e}")
        session.rollback()
        return None








if __name__ == "__main__":

    # new_photo_id = add_photo_and_return_id(
    #     file_unique_id_="unique123",
    #     file_id_="file456",
    #     file_size_=999,
    #     user_id_=1234,
    #     user_name_="user123",
    #     time_of_saved_="2024-03-28",
    #     column_1_="Extra Column 1",
    #     column_2_="Extra Column 2"
    # )
    # print("New Photo ID:", new_photo_id)


    # photo_info_dict = get_photo_by_id(5)
    # if photo_info_dict:
    #     print(photo_info_dict["file_id_"], photo_info_dict["file_size_"])
    # else:
    #     print("Not Found")

    # update_photo_user_id(123, 456)
    print(update_photo_user_id(5668981409,1895194333))

