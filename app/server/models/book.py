from typing import Optional
from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    name: str = Field(...)
    author: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Crime and Punishment",
                "author": "Dostoyevski"
            }
        }

class UpdateBookModel(BaseModel):
    name: Optional[str]
    author: Optional[str]
    status: Optional[bool]

    class Config:
        schema_extra = {
            "example":{
                "name": "Crime and Punishment",
                "author": "Fyodor Mihailoviç Dostoyevski"
            }
        }

def ResponseModel(data, message):
    return {
        "data":[data],
        "code":200,
        "message":message
    }

def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }