from pydantic import BaseModel


class Item(BaseModel):
    ID: str
    Name: str
    Class: str