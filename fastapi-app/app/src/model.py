from pydantic import BaseModel


class Item(BaseModel):
    URL: str
    Word: str