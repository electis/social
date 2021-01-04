import typing
import random

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import Field


class PhraseInput(BaseModel):
    """Phrase model"""
    author: str = "Anonymous"
    text: str = Field(..., title="Text", description="Text of phrase", max_length=200)


class PhraseOutput(PhraseInput):
    id: typing.Optional[int] = None


class Database:
    """
    Our **fake** database.
    """

    def __init__(self):
        self._items: typing.Dict[int, PhraseOutput] = {}  # id: model

    def get_random(self) -> int:
        # Получение случайной фразы
        return random.choice(list(self._items.keys()))

    def get(self, id: int) -> typing.Optional[PhraseOutput]:
        # Получение фразы по ID
        return self._items.get(id)

    def add(self, phrase: PhraseInput) -> PhraseOutput:
        # Добавление фразы

        id = len(self._items) + 1
        phrase_out = PhraseOutput(id=id, **phrase.dict())
        self._items[phrase_out.id] = phrase_out
        return phrase_out

    def delete(self, id: int) -> typing.Union[typing.NoReturn, None]:
        # Удаление фразы

        if id in self._items:
            del self._items[id]
            return
        else:
            raise ValueError("Phrase doesn't exist")

app = FastAPI(title="Random phrase")
db = Database()


@app.get(
    "/get",
    response_description="Random phrase",
    description="Get random phrase from database",
    response_model=PhraseOutput,
)
async def get():
    try:
        phrase = db.get(db.get_random())
    except IndexError:
        raise HTTPException(404, "Phrase list is empty")
    return phrase

@app.post(
    "/add",
    response_description="Added phrase with *id* parameter",
    response_model=PhraseOutput,
)
async def add(phrase: PhraseInput):
    phrase_out = db.add(phrase)
    return phrase_out

@app.delete("/delete", response_description="Result of deleting")
async def delete(id: int):
    try:
        db.delete(id)
    except ValueError as e:
        raise HTTPException(404, str(e))

if __name__ == "__main__":
    # http://q.c.electis.ru:8000/docs
    uvicorn.run(app, host="0.0.0.0", port=8000)
