from typing import Optional
from fastapi import FastAPI, Form
import json
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def index():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    tm = env.get_template('index.html')
    msg = tm.render()
    return Response(msg, media_type="text/html")

class Vocabulary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    eng_word: Optional[str] = None
    rus_word_1: Optional[str] = None
    rus_word_2: Optional[str] = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True) 

def create_words(x):
    word_1 = Vocabulary(eng_word=x)
    with Session(engine) as session:
        session.add(word_1)
        session.commit()

@app.post("/")
def get_new_word(new_word : str = Form(...)):
    """Сохраняем английское слово в базу"""
    create_words(x=new_word)
    response = Response(
        json.dumps({
            "success": True,
            "message": f"Слово {new_word} добавлено в словарь" 
        }),
        media_type='application/json')
    return response

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# def select_words():
#     """Забираем данные из базы"""
#     with Session(engine) as session:
#         words = session.exec(select(Vocabulary.eng_word).where(Vocabulary.id == 8))
#         print(words)
#         for word in words:
#             print(word)

def main():
    create_db_and_tables()
    # select_words()

if __name__ == "__main__":
    main()

