from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


db_location = "cache_docs.db"
engine = create_engine(f"sqlite+pysqlite:///{db_location}", echo= False)

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents_inline'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    file_id = Column(String)

    def __init__(self, title:str, file_id:str):
        self.title = title
        self.file_id = file_id


class PhotoInline(Base):
    __tablename__ = 'photo_inline'

    id = Column(Integer, primary_key=True)
    photo_name = Column(String)
    photo_file_id = Column(String)

    def __init__(self, photo_name:str, photo_file_id:str):
        self.photo_name = photo_name
        self.photo_file_id = photo_file_id






Base.metadata.create_all(engine)
Session = sessionmaker(bind= engine)
session = Session()


def add_document(title:str, file_id:str):
    doc_obj = Document(title= title, file_id= file_id)
    session.add(doc_obj)
    session.commit()

def get_documents():
    documents = session.query(Document).all()
    for document in documents:
        ...
        # print(f"ID: {document.id}, Title: {document.title}, File ID: {document.file_id}")
    return documents


def get_document_by_id(document_id):
    document = session.query(Document).filter(Document.id == document_id).first()
    if document:
        return document.id, document.title, document.file_id
    else:
        return None
    
def add_document_no_commit(title: str, file_id: str):
    doc_obj = Document(title=title, file_id=file_id)
    return doc_obj



def add_photo(photo_name:str, photo_file_id:str) -> int:
    '''This will add the data in photo table and return the id of the row'''
    photo_obj = PhotoInline(photo_name=photo_name, photo_file_id=photo_file_id)
    session.add(photo_obj)
    session.commit()
    return photo_obj.id

def get_photo_by_id(photo_id):
    photo = session.query(PhotoInline).filter(PhotoInline.id == photo_id).first()
    if photo:
        return photo.id, photo.photo_name, photo.photo_file_id
    else:
        return None

def get_all_photo():
    documents = session.query(PhotoInline).all()
    return documents








if __name__ == "__main__":

    add_document("This is Title for 1", "BQACAgUAAxkBAAJB02X_7YwVBbxHIWHJQIdx8KIlsxYEAAIOCwACrPOIVjRgtjeGLAAB-TQE")

    # print(add_photo("This is Name of Photo", "AgACAgUAAxkBAAJMJ2YBTLM8y_JRq7AAATrG9LxB5-DqHQACVrwxGy38-Veb03XT_w86KQEAAwIAA3cAAzQE"))
    # print(get_document_by_id(5))
    # print(get_document_by_id("5"))






# def add_document_list(title, file_id):
#     if not title:
#         title = "Default Title"
#     new_document = Document(title=title, file_id=file_id)
#     session.add(new_document)
#     session.commit()


# file_info = [
#     ("", "BQACAgUAAxkBAAJB02X_7YwVBbxHIWHJQIdx8KIlsxYEAAIOCwACrPOIVjRgtjeGLAAB-TQE"),
#     ("Tit for 2", "BQACAgUAAxkBAAJB0mX_7Yz43ODL0qYY03sBjOx1Ggb7AAINCwACrPOIVsd5it0osCluNAQ"),
#     ("", "BQACAgUAAxkBAAJB0WX_7YwXJV8PJT4_O7mPxOS3LrB3AAIMCwACrPOIVsBR9fpl86oiNAQ"),
#     ("Title this is movie", "BQACAgEAAxkBAAJB4WX_8uzka6rUJD4wrne4fLLVDkGfAAKKAwACOpiARfKkNxrrREz8NAQ"),
#     ("thumbnail image file with 3", "BQACAgUAAxkBAAJB3WX_8Q_-5imNlMZdnGkUcCJwoJjiAALdDgACExT5V5U1gwYsHDyCNAQ"),
# ]

# for title, file_id in file_info:
#     add_document_list(title, file_id)






