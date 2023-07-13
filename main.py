from fastapi import FastAPI, Body, Depends
import  schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI()

fakeDatabase = {
    1:{'task': 'Clean car'},
    2:{'task': 'Write blog'},
    3:{'task': 'Start stream'},
}

@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.get("/{id}")
def getItemById(id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

@app.post("/")
def addItem(item: schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task=item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.put("/{id}")
def updateItem(id: int, item: schemas.Item):
    fakeDatabase[id]['task'] = {'task': item.task}
    return fakeDatabase[id]

@app.delete("/{id}")
def deleteItem(id: int):
    del fakeDatabase[id]
    return fakeDatabase



# @app.post("/")
# def addItem(body = Body()):
#     newId = len(fakeDatabase.keys()) + 1
#     fakeDatabase[newId] = {'task': body['task']}
#     return fakeDatabase[newId]