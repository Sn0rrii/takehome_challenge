from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime


from app import crud, schema, database

app = FastAPI()


@app.get("/{datetime_iso}")
def get_open_restaurants(datetime_iso: str, db: Session = Depends(database.get_db)) -> List[schema.Restaurant]:
    try:
        datetime_obj = datetime.fromisoformat(datetime_iso)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid datetime format. Use ISO format.")

    return crud.get_restaurants(db, datetime_obj)
