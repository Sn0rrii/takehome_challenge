from pydantic import BaseModel


class Restaurant(BaseModel):
    name: str
    operating_hours: str

    class Config:
        orm_mode = True

