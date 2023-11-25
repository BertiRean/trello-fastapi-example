import os
from pydantic import ValidationError
import requests
from dotenv import load_dotenv
from fastapi import Body, FastAPI, status, HTTPException
from app.helpers.trello_api_helpers import (
    get_board_labels,
    get_lists_in_board,
    get_members_id_of_board,
)
from app.models.trello import BugTask, IssueTask, Task, TrelloTask, TrelloTaskEnum
import random

load_dotenv()


TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.environ.get("TRELLO_BOARD_ID")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def create_issue(payload: IssueTask):
    print(payload)
    lists_from_board = get_lists_in_board(TRELLO_BOARD_ID)
    if "To Do" not in lists_from_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="To Do List not founded in board",
        )
    print("Exception not throwed")
    url = "https://api.trello.com/1/cards"
    query = {
        "idList": lists_from_board["To Do"],
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "name": payload.title,
        "desc": payload.description,
    }
    response = requests.post(url=url, params=query)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


def create_task(payload: Task):
    lists_from_board = get_lists_in_board(TRELLO_BOARD_ID)
    if "Tasks" not in lists_from_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task List not founded in board",
        )

    labels = get_board_labels(TRELLO_BOARD_ID)
    tag_label = payload.category

    if tag_label not in labels:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{tag_label} Label don't exist in Trello Board",
        )

    url = "https://api.trello.com/1/cards"
    query = {
        "idList": lists_from_board["Tasks"],
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "name": payload.title,
        "idLabels": [labels[tag_label]],
    }
    response = requests.post(url=url, params=query)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


def create_bug(payload: BugTask):
    lists_from_board = get_lists_in_board(TRELLO_BOARD_ID)

    if "Bugs" not in lists_from_board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task List not founded in board",
        )

    labels = get_board_labels(TRELLO_BOARD_ID)
    tag_label = "Bug"
    if tag_label not in labels:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bug Label has been not created",
        )

    url = "https://api.trello.com/1/cards"
    query = {
        "idList": lists_from_board["Bugs"],
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "name": payload.title,
        "desc": payload.description,
        "idLabels": [labels[tag_label]],
        "idMembers": random.choice(get_members_id_of_board(TRELLO_BOARD_ID)),
    }
    response = requests.post(url=url, params=query)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


@app.post(
    "/",
    response_description="Create a Trello Task based in the type",
    status_code=status.HTTP_201_CREATED,
)
def handle_task_trello(payload: TrelloTask = Body(...)):
    if payload.task_type == TrelloTaskEnum.issue:
        try:
            issue = IssueTask(title=payload.title, description=payload.description)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error.errors()[0],
            )
        return create_issue(issue)
    elif payload.task_type == TrelloTaskEnum.bug:
        try:
            bug = BugTask(description=payload.description)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error.errors()[0],
            )
        return create_bug(bug)
    elif payload.task_type == TrelloTaskEnum.task:
        try:
            task_payload = Task(
                title=payload.title,
                category=payload.category,
            )
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error.errors()[0],
            )
        return create_task(task_payload)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            description=f"Task Type {payload.task_type} of TrelloTask not handled",
        )


@app.get("/boards")
def get_account_boards():
    url = "https://api.trello.com/1/members/me/boards"
    query = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    response = requests.get(url=url, params=query)
    if response.status_code == status.HTTP_200_OK:
        boards = {}
        for item in response.json():
            boards[item["name"]] = item["id"]
        return boards
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
