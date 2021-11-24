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

@app.post("/")
def get_new_word(new_word : str = Form(...)):
    response = Response(
        json.dumps({
            "success": True,
            "message": f"There are 100 words in dictionary" 
        }),
        media_type='application/json')
    return response

class Vocabulary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    eng_word: str
    rus_word_1: str
    rus_word_2: Optional[str] = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True) 
# echo shoudn't be used in the production

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_words():
    """Записываем данные в базу"""
    word_1 = Vocabulary(eng_word="you", rus_word_1="ты")
    word_2 = Vocabulary(eng_word="we", rus_word_1="мы")
    word_3 = Vocabulary(eng_word="call", rus_word_1="звонить", rus_word_2='позвонить')

    with Session(engine) as session:
        session.add(word_1)
        session.add(word_2)
        session.add(word_3)

        session.commit()

def select_words():
    """Забираем данные из базы"""
    with Session(engine) as session:
        words = session.exec(select(Vocabulary)).all()
        return words


def main():
    create_db_and_tables()
    create_words()
    select_words()

"""The main purpose of the __name__ == "__main__" is to have some code that 
is executed when your file is called with: python app.py, but is not called 
when another file imports it"""
if __name__ == "__main__":
    main()

