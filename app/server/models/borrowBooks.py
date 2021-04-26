from typing import Optional
from pydantic import BaseModel, Field

class BorrowBookSchema(BaseModel):
    book: dict = Field(...)
    user: dict = Field(...)
    class Config:
        schema_extra = {
            "book": {
                "id": "6082b6fa48bcb9482224007e",
                "name": "The Speech",
                "author": "Mustafa Kemal Ataturk"
            },
            "user": {
                "id": "60831becfcf8d3f7a20b2d8f",
                "firstname": "John",
                "lastname": "Doe"
            }
        }

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
