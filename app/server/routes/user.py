from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database.user import (
    retrieve_user,
    retrieve_users,
    add_user,
    update_user,
    delete_user
)

from app.server.models.user import (
    UserSchema,
    UpdateUserModel,
    ResponseModel,
    ErrorResponseModel
)

router = APIRouter()
@router.get("/", response_description="Users retrieved")
async def get_users():
    users = retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully.")
    return ResponseModel(users, "Empty list returned")

@router.post("/add", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = add_user(user)
    return ResponseModel(new_user, "User added successfully.")

@router.get("/detail/{id}", response_description="User data retrieved")
async def get_user_data(id):
    user = retrieve_user(id)
    if user:
        return ResponseModel(user, "User data retrieved successfully.")
    return ErrorResponseModel("An error occured.", 404, "User doesn't exist.")

@router.put("/update/{id}")
async def update_user_data(id, req: UpdateUserModel = Body(...)):
    req = { k: v for k, v in req.dict().items() if v is not None }
    updated_user = update_user(id, req)
    if updated_user:
        return ResponseModel("User with ID:{} name update is successful.".format(id), "User updated.")
    return ErrorResponseModel("An error occured.", 404, "There was an error.")

@router.delete("/delete/{id}", response_description="User data deleted from database")
async def delete_user_data(id: str):
    deleted_user = delete_user(id)
    if deleted_user:
        return ResponseModel("User with ID:{} removed.".format(id), "User deleted successfully.")
    return ErrorResponseModel("An error occured.", 404, "User with ID:{0} doesn't exist.".format(id))

