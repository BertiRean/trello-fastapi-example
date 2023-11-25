from ast import Gt
import random
from typing import Annotated, List
from typing_extensions import Literal
from pydantic import BaseModel, Field, constr
from enum import Enum, IntEnum
import string


def get_random_word():
    MAX_BUG_NAME_LENGTH = 8
    return "".join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(MAX_BUG_NAME_LENGTH)
    )


class TrelloTaskEnum(str, Enum):
    issue = "issue"
    bug = "bug"
    task = "task"


class TrelloTask(BaseModel):
    task_type: TrelloTaskEnum
    title: str = ""
    description: str = ""
    category: str = ""
    model_config = {
        "json_schema_extra": {
            "example": {
                "category": "Test",
                "task_type": "issue",
                "title": "Can I use auth modules",
                "description": "I can't login with Safari in my Macbook",
            }
        }
    }


class IssueTask(BaseModel):
    task_type: TrelloTaskEnum = Field(default=TrelloTaskEnum.issue, frozen=True)
    description: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)


class BugTask(BaseModel):
    task_type: TrelloTaskEnum = Field(default=TrelloTaskEnum.bug, frozen=True)
    description: str = Field(..., min_length=1)
    title: str = Field(
        default=f"bug-{get_random_word()}-{random.randint(1, 1000)}", frozen=True
    )


class Task(BaseModel):
    task_type: TrelloTaskEnum = Field(default=TrelloTaskEnum.task, frozen=True)
    title: str = Field(..., min_length=1)
    category: Literal["Test", "Maintenance", "Research"]
