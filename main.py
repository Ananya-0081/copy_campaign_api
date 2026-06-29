from datetime import datetime
from os import name
from random import randint
from fastapi import FastAPI, HTTPException, Request
from typing import Any

app = FastAPI(root_path="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

data=[
    {
        "campaign_id": 1, 
        "name": "ABC", 
        "due_date":datetime.now(),
        "created_date": datetime.now()
     } ,
    {
        "campaign_id": 2, 
        "name": "XYZ", 
        "due_date":datetime.now(), 
        "created_date": datetime.now()
    }
]

#campaign id,name,due date,created date
@app.get("/campaigns")
async def read_campaigns():
    return {"campaigns": data}

@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign["campaign_id"] == id:
            return {"campaign": campaign}
    return HTTPException(status_code=404)

@app.post("/campaigns",status_code=201)
async def create_campaign(body:dict[str,Any]):

    new :Any  ={
        "campaign_id": randint(100, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_date": datetime.now()
    }
    data.append(new)
    return {"campaign": new}

@app.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    for campaign in data:
        if campaign["campaign_id"] == id:

            updated:Any = {
                "campaign_id": campaign["campaign_id"],
                "name": body.get("name", campaign["name"]),
                "due_date": body.get("due_date", campaign["due_date"]),
                "created_date": body.get("created_date", campaign["created_date"])
            }
            data[data.index(campaign)] = updated;
            return {"campaign": updated}
    return HTTPException(status_code=404) 

@app.delete("/campaigns/{id}")
async def delete_campaign(id: int):
    for campaign in data:
        if campaign["campaign_id"] == id:
            data.remove(campaign)
            return {"message": "Campaign deleted successfully"}
    return HTTPException(status_code=404)

