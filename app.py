from typing import Optional
from fastapi import FastAPI, Form
import json, random
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
    global random_row
    random_row = select_random_word()
    msg = tm.render(random_word = random_row.rus_word_1)
    return Response(msg, media_type="text/html")

@app.get("/dictionary")
def index():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    tm = env.get_template('dictionary.html')
    all = show_all_dictionary()
    msg = tm.render(all = all, headings = headings, data = data)
    return Response(msg, media_type="text/html")

class Vocabulary(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    eng_word: Optional[str] = None
    rus_word_1: Optional[str] = None
    rus_word_2: Optional[str] = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# def create_words(new_word):
#     """Сохраняем введённое английское слово в базу"""
#     with Session(engine) as session:
#         session.add(Vocabulary(eng_word=new_word))
#         session.commit()

# @app.post("/")
# def get_new_word(input_word : str = Form(...)):
#     """Получаем POST с английским словом, сохраняем в базу,
#     отправляем ответ на frontend"""
#     create_words(new_word=input_word)
#     response = Response(
#         json.dumps({
#             "success": True,
#             "message": f"Слово {input_word} добавлено в словарь" 
#         }),
#         media_type='application/json')
#     return response

@app.post("/")
def check_trans_and_give_answer(input_word : str = Form(...)):
    """Получаем POST с английским словом, проверяем.
    Отправляем ответ верно или нет"""
    if input_word == random_row.eng_word:
        response = Response(
            json.dumps({
                "success": True,
                "message": f"Верно" 
            }),
            media_type='application/json')
        return response
    else:
        response = Response(
            json.dumps({
                "success": True,
                "message": f"Неверно" 
            }),
            media_type='application/json')
        return response

def check_trans(new_word):
    """Проверяем верный ли перевод слова"""
    with Session(engine) as session:
        word = session.exec(select(Vocabulary).where(Vocabulary.eng_word == new_word)).first()
        print(word.rus_word_1)

def show_all_dictionary():
    "Забираем все данные из базы"
    with Session(engine) as session:
        statement = select(Vocabulary.id, Vocabulary.eng_word, Vocabulary.rus_word_1)
        all = session.exec(statement).all()
        print(all)
        # for i in all:
        #     print(i)
        return all



        # mass = range(1, session.query(Vocabulary.id).count())
        # for i in mass: 
        #     mass[i] = session.exec(select(Vocabulary.eng_word).where(Vocabulary.id == i)).first()
        # all = session.exec(select(Vocabulary)).all()
        # print(all)
        # return all

def select_random_word():
    """Забираем случайный ряд из базы"""
    with Session(engine) as session:
        count = session.query(Vocabulary.id).count()
        random_word = session.get(Vocabulary, random.randint(1, count))
        return random_word

def main():
    # create_db_and_tables()
    show_all_dictionary()

if __name__ == "__main__":
    main()



headings = ("ID", "English", "Russian")
data = (
    ("1", "yes", "да"),
    ("2", "dictionary", "словарь"),
    ("3", "no", "нет")
)

