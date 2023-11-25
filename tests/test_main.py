from fastapi.testclient import TestClient
from fastapi import status
from pydantic import ValidationError

from app.main import app
from app.models.trello import IssueTask

client = TestClient(app)


def test_create_bug():
    response = client.post(
        url="/",
        json={
            "description": "I can't login with Safari in my Macbook",
            "task_type": "bug",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_issue():
    response = client.post(
        url="/",
        json={
            "description": "I can't use Edge with the App",
            "task_type": "issue",
            "title": "Edge browser incompatible",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_task():
    response = client.post(
        url="/",
        json={
            "description": "Migrate Database store to AWS RDS",
            "task_type": "task",
            "title": "Database Migration AWS",
            "category": "Research",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_issue_need_description():
    response = client.post(
        url="/",
        json={"task_type": "issue", "title": "Migration fail"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_bug_need_description():
    response = client.post(
        url="/",
        json={
            "task_type": "bug",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_task_without_category():
    response = client.post(
        url="/",
        json={
            "task_type": "requests",
            "title": "Migration fail",
            "description": "Need migrate to Amazon RDS with MySQL 9",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_task_without_title():
    response = client.post(
        url="/",
        json={
            "task_type": "requests",
            "category": "Test",
            "description": "Need migrate to Amazon RDS with MySQL 9",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
