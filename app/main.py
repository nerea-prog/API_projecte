from typing import Optional

from fastapi import HTTPException, Depends
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine, update
from sqlmodel import SQLModel, Session, select, delete
from models.Usuari import Usuari, UsuariRequest, UsuariResponse, UsuariResponsePartial
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/usuari", response_model=dict, tags=["CREATE"])
def afegir_usuari(usuari: UsuariRequest, db: Session = Depends(get_db)):
    nou_usuari = Usuari.model_validate(usuari)
    db.add(nou_usuari)
    db.commit()
    db.refresh(nou_usuari)
    return {"msg": "Usuari afegit correctament"}

@app.get("/usuari/{pk}", response_model=UsuariResponse, tags=["GETS"])
def obtenir_usuari(pk: int, db: Session = Depends(get_db)):
    consulta = select(Usuari).where(Usuari.PK == pk)
    result = db.exec(consulta).first()
    if not result:
        raise HTTPException(status_code=404, detail = "Usuari no trobat")
    return UsuariResponse.model_validate(result)

@app.get("/usuaris", response_model=dict, tags=["GETS"])
def llista_usuaris(db: Session = Depends(get_db)):
    consulta = select(Usuari)
    return db.exec(consulta).all()

@app.put("/usuari/{pk}", response_model=dict, tags=["UPDATE"])
def actualitzar_usuari(pk: int, usuari: UsuariRequest, db: Session = Depends(get_db)):
    consulta = update(Usuari).where(Usuari.PK == pk).values(usuari.model_dump())
    db.exec(consulta)
    db.commit()
    return{"msg": "Usuari actualitzat correctament"}

@app.patch("/usuari/{pk}", response_model=dict, tags=["UPDATE"])
def actualitzacio_parcial_usuari(
    pk: int,
    apellido1: Optional[str] = None,
    apellido2: Optional[str] = None,
    correo: Optional[str] = None,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    camps_actualitzacio = {}
    if apellido1 is not None:
        camps_actualitzacio["apellido1"] = apellido1
    if apellido2 is not None:
        camps_actualitzacio["apellido2"] = apellido2
    if correo is not None:
        camps_actualitzacio["correo"] = correo
    if activo is not None:
        camps_actualitzacio["activo"] = activo
    if not camps_actualitzacio:
        raise HTTPException(status_code=400, detail="No hi han camps per actualitzar")
    consulta = update(Usuari).where(Usuari.PK == pk).values(camps_actualitzacio)
    db.exec(consulta)
    db.commit()
    return {"msg": "Usuari actualitzat correctament"}

@app.delete("/usuari/{pk}", response_model=dict, tags=["DELETE"])
def eliminar_usuari (pk: int, db: Session = Depends(get_db)):
    consulta = delete(Usuari).where(Usuari.PK == pk)
    db.exec(consulta)
    db.commit()
    return {"msg": "Usuari eliminat correctament"}

