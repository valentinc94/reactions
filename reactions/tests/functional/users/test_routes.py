from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from reactions.apps.users import constants
from reactions.domains.users import processes, schemas


class TestUserCreate:
    """
    Tests for user creation via API endpoints.

    This class contains unit tests to verify the functionality of the endpoint responsible
    for creating users. It includes tests for successful user creation and error handling,
    ensuring that valid user data is correctly processed and saved, and invalid or missing
    data is properly handled. All tests specifically focus on routes/endpoints that manage
    user creation.
    """

    def test_create_user_return_success(
        self,
        client: TestClient,
    ):
        """
        Validates that creating a user with valid data returns 201.
        """

        user_data = schemas.UserCreate(
            username="valentinc94",
            role=constants.Role.EXTERNAL,
        )

        response = client.post("/api/v1/users/", json=user_data.model_dump())

        assert (
            response.status_code == status.HTTP_201_CREATED
        ), f"Expected 201, got {response.status_code}"

        results = response.json()

        assert "code_transaction" in results
        assert "user_id" in results

        assert results["code_transaction"] == "OK"
        assert results["user_id"] is not None

    def test_create_user_should_raise_username_already_exists(
        self,
        client: TestClient,
        db_session: Session,
    ):
        """
        Validates that attempting to create a user with an existing username
        raises the expected error.
        """

        user_data = schemas.UserCreate(
            username="valentinc94",
            role=constants.Role.EXTERNAL,
        )

        processes.create_user(
            db=db_session,
            user_data=user_data,
        )

        response = client.post("/api/v1/users/", json=user_data.model_dump())

        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), f"Expected 400, got {response.status_code}"

        results = response.json()

        assert "detail" in results
        assert "code_transaction" in results["detail"]
        assert "message" in results["detail"]

        assert results["detail"]["code_transaction"] == "UNABLE_TO_CREATE_USER"
        assert (
            results["detail"]["message"]
            == f"The username '{user_data.username}' is already in use."
        )


class TestUserUpdate:
    """
    Tests for user update via API endpoints.
    """

    def test_update_user_return_success(
        self,
        client: TestClient,
        db_session: Session,
    ):
        create_data = schemas.UserCreate(
            username="valentinc94",
            role=constants.Role.EXTERNAL,
        )

        processes.create_user(
            db=db_session,
            user_data=create_data,
        )

        update_data = schemas.UserUpdate(
            username="valentinc94",
            role=constants.Role.ADMIN,
        )

        response = client.put("/api/v1/users/", json=update_data.model_dump())

        assert response.status_code == status.HTTP_200_OK

        results = response.json()

        assert "code_transaction" in results
        assert "user_id" in results

        assert results["code_transaction"] == "OK"
        assert results["user_id"] is not None

    def test_update_user_should_raise_user_does_not_exist(
        self,
        client: TestClient,
    ):
        update_data = schemas.UserUpdate(
            username="ghost_user",
            role=constants.Role.ADMIN,
        )

        response = client.put("/api/v1/users/", json=update_data.model_dump())

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        results = response.json()

        assert "detail" in results
        assert "code_transaction" in results["detail"]
        assert "message" in results["detail"]

        assert results["detail"]["code_transaction"] == "UNABLE_TO_UPDATE_USER"


class TestUserDelete:
    """
    Tests for user deletion via API endpoints.
    """

    def test_delete_user_return_success(
        self,
        client: TestClient,
        db_session: Session,
    ):
        user_data = schemas.UserCreate(
            username="valentinc94",
            role=constants.Role.EXTERNAL,
        )

        processes.create_user(
            db=db_session,
            user_data=user_data,
        )

        response = client.request(
            "DELETE",
            "/api/v1/users/",
            data={"username": "valentinc94"},
        )

        assert response.status_code == status.HTTP_200_OK

        results = response.json()

        assert results["code_transaction"] == "OK"
        assert results["message"] == "OK"

    def test_delete_user_should_raise_user_does_not_exist(
        self,
        client: TestClient,
    ):
        response = client.request(
            "DELETE",
            "/api/v1/users/",
            data={"username": "ghost_user"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        results = response.json()

        assert "detail" in results
        assert results["detail"]["code_transaction"] == "UNABLE_TO_DELETE_USER"


class TestUserRetrieve:
    """
    Tests for user retrieval via API endpoints.
    """

    def test_retrieve_users_return_success(
        self,
        client: TestClient,
        db_session: Session,
    ):
        user_data = schemas.UserCreate(
            username="valentinc94",
            role=constants.Role.EXTERNAL,
        )

        processes.create_user(
            db=db_session,
            user_data=user_data,
        )

        response = client.get("/api/v1/users/")

        assert response.status_code == status.HTTP_200_OK

        results = response.json()

        assert "code_transaction" in results
        assert "data" in results

        assert results["code_transaction"] == "OK"
        assert isinstance(results["data"], list)
        assert len(results["data"]) >= 1

    def test_retrieve_user_by_username(
        self,
        client: TestClient,
        db_session: Session,
    ):
        user_data = schemas.UserCreate(
            username="valentinc94",
            role=constants.Role.EXTERNAL,
        )

        processes.create_user(
            db=db_session,
            user_data=user_data,
        )

        response = client.get(
            "/api/v1/users/",
            params={"username": "valentinc"},
        )

        assert response.status_code == status.HTTP_200_OK

        results = response.json()

        assert results["code_transaction"] == "OK"
        assert len(results["data"]) == 0