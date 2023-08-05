# -*- encoding: utf-8 -*-
from fastapi import FastAPI, Depends, Path, HTTPException
import models
from fastapi.middleware.cors import CORSMiddleware
import handle_db
import datetime

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path="/")
async def FastAPI():
    return { "message" : "Hello World" }

## select user list
@app.get(path="/api/users")
async def get_list_user():
    result = handle_db.select_all_user()
    return {
        "status": "OK",
        "data": result
    }

## create user
@app.post(path="/api/users")
async def post_user(user_name: str, user_mail: str):
    result = handle_db.create_user(user_name, user_mail)
    if result == 1:
        raise HTTPException(status_code=404, detail="Query Error!!")
    return {
        "status": "OK",
        "data": result
    }

## select user
@app.get(path="/api/users/{user_id}")
async def get_user(user_id: str):
    result = handle_db.select_user(user_id)
    if result == 1:
        raise HTTPException(status_code=404, detail="Query Error!!")
    return {
        "status": "OK",
        "data": result
    }

## update user 
@app.put(path="/api/users/{user_id}")
async def put_user(user_id: str, user_name: str, user_mail: str, user_status: str):
    result = handle_db.update_user(user_id, user_name, user_mail, user_status)
    if result == 1:
        raise HTTPException(status_code=404, detail="Query Error!!")
    return {
        "status": "OK",
        "data": result
    }

## delete user 
@app.delete(path="/api/users/{user_id}")
async def delete_user(user_id: str):
    result = handle_db.delete_user(user_id)
    if result == 1:
        raise HTTPException(status_code=404, detail="Query Error!!")
    return {
        "status": "OK",
        "data": result
    }
