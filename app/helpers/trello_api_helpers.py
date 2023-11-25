from dotenv import load_dotenv
import requests
import os
import random
import string

from fastapi import status, HTTPException

load_dotenv()

TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.environ.get("TRELLO_BOARD_ID")


def get_lists_in_board(boardId: str):
    url = f"https://api.trello.com/1/boards/{boardId}/lists"
    headers = {"Accept": "application/json"}
    query = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }

    cards = {}
    response = requests.get(url=url, params=query, headers=headers)
    if response.status_code == status.HTTP_200_OK:
        for it in response.json():
            cards.update({it["name"]: it["id"]})

    return cards


def get_members_id_of_board(boardId: str):
    url = f"https://api.trello.com/1/boards/{boardId}/members"
    query = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    response = requests.get(url=url, params=query)

    if response.status_code == status.HTTP_200_OK:
        return [x["id"] for x in response.json()]
    else:
        return []


def get_board_labels(boardId: str):
    url = f"https://api.trello.com/1/boards/{boardId}/labels"
    query = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
    }
    response = requests.get(url=url, params=query)

    labels = {}
    for it in response.json():
        labels[it["name"]] = it["id"]

    return labels
