import json
import json
import urllib.parse

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_initial():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # sanity check for a known activity
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_remove_participant():
    activity = "Programming Class"
    email = "unittest@example.com"

    # ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # sign up
    signup_url = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    resp = client.post(signup_url)
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # verify participant present
    get_resp = client.get("/activities")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert email in data[activity]["participants"]

    # remove participant
    remove_url = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    rem = client.delete(remove_url)
    assert rem.status_code == 200
    assert "Removed" in rem.json().get("message", "")

    # verify participant removed
    final = client.get("/activities").json()
    assert email not in final[activity]["participants"]