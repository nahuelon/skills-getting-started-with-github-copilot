from fastapi import status


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_path = "/static/index.html"

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.url.path == expected_path


def test_get_activities_returns_activity_list(client):
    # Arrange
    expected_activities = {"Chess Club", "Programming Class"}

    # Act
    response = client.get("/activities")
    activity_names = set(response.json().keys())

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert expected_activities.issubset(activity_names)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    payload = {"email": "newstudent@mergington.edu"}
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=payload)
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Signed up {payload['email']} for {activity_name}"}
    assert payload["email"] in activities[activity_name]["participants"]


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    payload = {"email": "student@mergington.edu"}
    activity_name = "Nonexistent"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=payload)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_when_already_registered_returns_400(client):
    # Arrange
    payload = {"email": "michael@mergington.edu"}
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params=payload)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_removes_existing_student(client):
    # Arrange
    payload = {"email": "michael@mergington.edu"}
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=payload)
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Removed {payload['email']} from {activity_name}"}
    assert payload["email"] not in activities[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    payload = {"email": "unknown@mergington.edu"}
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=payload)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Student not registered for this activity"


def test_remove_participant_from_missing_activity_returns_404(client):
    # Arrange
    payload = {"email": "student@mergington.edu"}
    activity_name = "Nonexistent"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params=payload)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"
