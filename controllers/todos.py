from typing import Annotated

from fastapi import APIRouter, Depends

import models
# ainoastaan tämä import pitää vaihtaa, jos haluat vaihtaa datalähdettä

# ota tämä pois kommenteista (tätä varten pitää tietenkin olla tietokanta)
#from services.sqlalchemy_todos import TodosService


# kommentoi tämä ja kato mitä tapahtuu
from services.json_placeholder_todos import TodosService

router = APIRouter()


# get_service on vain funktio joka palauttaa kulloinkin käytössä olevan servicen
# jos siis tiedot pitääkin hakea apista / mongodb:stä tai jostakin muusta lähteestä, johon ei voi käyttää
# sqlalchemya, riittää, että teet uuden servicen esim (mongo_todos.py)
def get_service(db: models.Db):

    return TodosService(db)


TodoService = Annotated[TodosService, Depends(get_service)]


@router.get('/api/v1/todos_lists_bad')
async def get_todo_list_bad(db: models.Db):
    # Tämä on huonosti tehty
    # vaikka tässä on kyllä sqlalchemy käytössä, joka toimii useilla relaatiotietokannoilla vaihtamalla vain
    # tietokannan yhteyden sopivaksi, tämä toteutus ei kuitenkaan toimi suoraan, jos pitää vaihtaa
    # mongodb relaatiokannan tilalle, tai jos käyttäjät pitää rekisteröidä johonkin pilvipalveluun REST-apin kautta
    todo_lists = db.query(models.TodoList).all()
    return {'todo_lists': todo_lists}


@router.get('/api/v1/todo_lists_better')
async def get_todo_lists_better(service: TodoService):
    # nyt, kun tässä on mukana yksi layer lisää (tämä service), jossa tietokantakysely on, controllerin koodia
    # ei tarvitse muokata, jos datalähde vaihtuu, riittää, että tehdään uusi sevice
    todo_lists = service.get_all()
    return {'todo_lists': todo_lists}
