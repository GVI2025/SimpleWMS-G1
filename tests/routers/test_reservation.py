from fastapi.testclient import TestClient
from unittest.mock import patch, ANY
from datetime import datetime, timedelta

from app.main import app
from app.schemas.reservation import ReservationCreate, ReservationUpdate
from app.models import Reservation as ReservationModel

client = TestClient(app)

# Mock reservation data
current_datetime = datetime.now()

mock_reservation_data = {
    "salle_id": "7e76e987-9691-4080-8f93-6c456ff2c285",
    "date": str(current_datetime.date()),
    "heure": str(current_datetime.time()),
    "utilisateur": "Lune",
    "id": "fdb6539a-f0a6-41c6-93a0-56083455aabe",
    "commentaire": "Salut",
}

mock_reservation_model = ReservationModel(
    salle_id="7e76e987-9691-4080-8f93-6c456ff2c285",
    date=current_datetime.date(),
    heure=current_datetime.time(),
    utilisateur="Lune",
    id="fdb6539a-f0a6-41c6-93a0-56083455aabe",
    commentaire="Salut",
)

mock_reservation_list = [
    ReservationModel(
        salle_id="7e76e987-9691-4080-8f93-6c456ff2c285",
        date=current_datetime.date(),
        heure=current_datetime.time(),
        utilisateur="Lune",
        id="fdb6539a-f0a6-41c6-93a0-56083455aabe",
        commentaire="Salut",
    ),
    ReservationModel(
        salle_id="7e76e987-9691-4080-8f93-6c456ff2c285",
        date=current_datetime.date(),
        heure=(current_datetime + timedelta(hours=1, minutes=20)).time(),
        utilisateur="Yohann",
        id="2a185871-f1f1-4cac-b29c-2f47cb8e5549",
        commentaire="Bonjour",
    )
]


class TestReservationRouter:
    @patch('app.routers.reservation.reservation_service.list_reservations')
    def test_list_reservations(self, mock_list_reservations):
        # Configure mock
        mock_list_reservations.return_value = mock_reservation_list

        # Test the endpoint
        response = client.get("/reservations/")

        # Verify response
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Verify service function was called
        mock_list_reservations.assert_called_once()

    @patch('app.routers.reservation.reservation_service.create_reservation')
    def test_create_reservation_success(self, mock_create_reservation):
        # Configure mock
        mock_create_reservation.return_value = mock_reservation_model

        # Test the endpoint
        response = client.post("/reservations/", json={
            "salle_id": mock_reservation_data["salle_id"],
            "date": mock_reservation_data["date"],
            "heure": mock_reservation_data["heure"],
            "utilisateur": mock_reservation_data["utilisateur"],
            "commentaire": mock_reservation_data["commentaire"],
        })

        # Verify response
        assert response.status_code == 201
        assert response.json()["salle_id"] == mock_reservation_data["salle_id"]
        assert response.json()["date"] == mock_reservation_data["date"]
        assert response.json()["heure"] == mock_reservation_data["heure"]
        assert response.json()["utilisateur"] == mock_reservation_data["utilisateur"]
        assert response.json()["id"] == mock_reservation_data["id"]
        assert response.json()["commentaire"] == mock_reservation_data["commentaire"]

        # Verify service function was called correctly
        mock_create_reservation.assert_called_once()

    @patch('app.routers.reservation.reservation_service.create_reservation')
    def test_create_reservation_fail(self, mock_create_reservation):
        # Configure mock
        mock_create_reservation.return_value = None

        # Test the endpoint
        response = client.post("/reservations/", json={
            "salle_id": mock_reservation_data["salle_id"],
            "date": mock_reservation_data["date"],
            "heure": mock_reservation_data["heure"],
            "utilisateur": mock_reservation_data["utilisateur"],
            "commentaire": mock_reservation_data["commentaire"],
        })

        # Verify response
        assert response.status_code == 400
        assert "Créneau déjà réservé" in response.json()["detail"]

    @patch('app.routers.reservation.reservation_service.get_reservation')
    def test_get_reservation_success(self, mock_get_reservation):
        # Configure mock
        mock_get_reservation.return_value = mock_reservation_model

        # Test the endpoint
        response = client.get(f"/reservations/{mock_reservation_data['id']}")

        # Verify response
        assert response.status_code == 200
        assert response.json()["id"] == mock_reservation_data["id"]

        # Verify service function was called correctly
        mock_get_reservation.assert_called_once_with(ANY, mock_reservation_data["id"])

    @patch('app.routers.reservation.reservation_service.get_reservation')
    def test_get_reservation_not_found(self, mock_get_reservation):
        # Configure mock
        mock_get_reservation.return_value = None

        # Test the endpoint
        response = client.get("/reservations/nonexistent")

        # Verify response
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]