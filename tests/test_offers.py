from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_existing_offer() -> None:
    response = client.get("/offers/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Python Developer"


def test_not_found_offer() -> None:
    response = client.get("/offers/99")

    assert response.status_code == 404
    assert response.json()["detail"] == "Offer not found"


def test_create_offer() -> None:
    response = client.post(
        "/offers",
        json={
            "title": "Data Analyst",
            "description": "Work",
            "company": "ABC Enterprises",
            "work_mode": "onsite",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 4


def test_create_then_list() -> None:
    response = client.post(
        "/offers",
        json={
            "title": "Data Analyst",
            "description": "Work",
            "company": "ABC Enterprises",
            "work_mode": "onsite",
        },
    )
    assert response.status_code == 201
    response = client.get("/offers")

    assert len(response.json()) == 4


def test_delete_offer_then_search() -> None:
    response = client.delete("/offers/1")
    assert response.status_code == 204
    response = client.get("/offers/1")
    assert response.status_code == 404


def test_delete_nonexistent_offer() -> None:
    response = client.delete("/offers/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Offer not found"


def test_create_invalid_work_mode() -> None:
    response = client.post(
        "/offers",
        json={
            "title": "Data Analyst",
            "description": "Work",
            "company": "ABC Enterprises",
            "work_mode": "onsitehybrid",
        },
    )

    assert response.status_code == 422
