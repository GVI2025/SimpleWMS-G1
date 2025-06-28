from fastapi.testclient import TestClient
from unittest.mock import patch, ANY
from datetime import datetime

from app.main import app
from app.schemas.salle import SalleCreate, SalleUpdate
from app.models import Salle as SalleModel

client = TestClient(app)

# Mock salle data
mock_salle_data = {
    "nom": "Salle1",
    "capacite": 5,
    "localisation": "IG2I",
    "id": "7e76e987-9691-4080-8f93-6c456ff2c285",
    "disponible": True
}

mock_salle_model = SalleModel(
    id="7e76e987-9691-4080-8f93-6c456ff2c285",
    nom="Salle1",
    capacite=5,
    localisation="IG2I",
    disponible=True,
)

mock_salle_update_data = {
    "nom": "Salle3",
    "capacite": 6,
    "localisation": "IG2I",
    "id": "7e76e987-9691-4080-8f93-6c456ff2c285",
    "disponible": True,
}

mock_salle_update = SalleModel(
    id="7e76e987-9691-4080-8f93-6c456ff2c285",
    nom="Salle3",
    capacite=6,
    localisation="IG2I",
    disponible=True,
)

mock_salle_list = [
    SalleModel(
        id="7e76e987-9691-4080-8f93-6c456ff2c285",
        nom="Salle1",
        capacite=5,
        localisation="IG2I",
        disponible=True,
    ),
    SalleModel(
        id="b2a1b0b1-aacc-4b26-a70a-ae17ce4f61d6",
        nom="Salle2",
        capacite=10,
        localisation="IG2I",
        disponible=False,
    )
]

mock_salle_list_filter = [
    SalleModel(
        id="7e76e987-9691-4080-8f93-6c456ff2c285",
        nom="Salle1",
        capacite=5,
        localisation="IG2I",
        disponible=True,
    )
]


class TestSalleRouter:
    @patch('app.routers.salle.salle_service.list_salles')
    def test_list_salles(self, mock_list_salles):
        # Configure mock
        mock_list_salles.return_value = mock_salle_list

        # Test the endpoint
        response = client.get("/salles/")

        # Verify response
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Verify service function was called
        mock_list_salles.assert_called_once()
    
    @patch('app.routers.salle.salle_service.list_salles')
    def test_list_salles(self, mock_list_salles):
        # Configure mock
        mock_list_salles.return_value = mock_salle_list_filter

        # Test the endpoint
        response = client.get("/salles?disponible=True")

        # Verify response
        assert response.status_code == 200
        assert len(response.json()) == 1

        # Verify service function was called
        mock_list_salles.assert_called_once()

    @patch('app.routers.salle.salle_service.create_salle')
    def test_create_salle_success(self, mock_create_salle):
        # Configure mock
        mock_create_salle.return_value = mock_salle_model

        # Test the endpoint
        response = client.post("/salles/", json={
            "nom": mock_salle_data["nom"],
            "capacite": mock_salle_data["capacite"],
            "localisation": mock_salle_data["localisation"],
            "disponible": mock_salle_data["disponible"],
        })

        # Verify response
        assert response.status_code == 201
        assert response.json()["nom"] == mock_salle_data["nom"]
        assert response.json()["capacite"] == mock_salle_data["capacite"]
        assert response.json()["localisation"] == mock_salle_data["localisation"]
        assert response.json()["id"] == mock_salle_data["id"]

        # Verify service function was called correctly
        mock_create_salle.assert_called_once()

    @patch('app.routers.salle.salle_service.get_salle')
    def test_get_salle_success(self, mock_get_salle):
        # Configure mock
        mock_get_salle.return_value = mock_salle_model

        # Test the endpoint
        response = client.get(f"/salles/{mock_salle_data['id']}")

        # Verify response
        assert response.status_code == 200
        assert response.json()["id"] == mock_salle_data["id"]

        # Verify service function was called correctly
        mock_get_salle.assert_called_once_with(ANY, mock_salle_data["id"])

    @patch('app.routers.salle.salle_service.get_salle')
    def test_get_salle_not_found(self, mock_get_salle):
        # Configure mock
        mock_get_salle.return_value = None

        # Test the endpoint
        response = client.get("/salles/nonexistent")

        # Verify response
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @patch('app.routers.salle.salle_service.update_salle')
    def test_update_salle_success(self, mock_update_salle):
        # Configure mock
        mock_update_salle.return_value = mock_salle_update

        # Test the endpoint
        response = client.put(
            f"/salles/{mock_salle_data['id']}",
            json={
                "nom": mock_salle_update_data["nom"],
                "capacite": mock_salle_update_data["capacite"],
                "localisation": mock_salle_update_data["localisation"],
                "disponible": mock_salle_update_data["disponible"],
            }
        )

        # Verify response
        assert response.status_code == 200
        assert response.json()["nom"] == mock_salle_update_data["nom"]
        assert response.json()["capacite"] == mock_salle_update_data["capacite"]
        assert response.json()["localisation"] == mock_salle_update_data["localisation"]

        # Verify service function was called correctly
        mock_update_salle.assert_called_once()

    @patch('app.routers.salle.salle_service.update_salle')
    def test_update_salle_not_found(self, mock_update_salle):
        # Configure mock
        mock_update_salle.return_value = None

        # Test the endpoint
        response = client.put(
            "/salles/nonexistent",
            json={
                "nom": mock_salle_update_data["nom"],
                "capacite": mock_salle_update_data["capacite"],
                "localisation": mock_salle_update_data["localisation"],
                "disponible": mock_salle_update_data["disponible"],
            }
        )

        # Verify response
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    @patch('app.routers.salle.salle_service.delete_salle')
    def test_delete_salle_success(self, mock_delete_salle):
        # Configure mock
        mock_delete_salle.return_value = mock_salle_model

        # Test the endpoint
        response = client.delete(f"/salles/{mock_salle_data['id']}")

        # Verify response
        assert response.status_code == 200
        assert response.json()["id"] == mock_salle_data["id"]

        # Verify service function was called correctly
        mock_delete_salle.assert_called_once_with(ANY, mock_salle_data["id"])

    @patch('app.routers.salle.salle_service.delete_salle')
    def test_delete_salle_not_found(self, mock_delete_salle):
        # Configure mock
        mock_delete_salle.return_value = None

        # Test the endpoint
        response = client.delete("/salles/nonexistent")

        # Verify response
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]